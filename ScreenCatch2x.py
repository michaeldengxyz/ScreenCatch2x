#Pyhton 3.x
# -*- coding: UTF-8 -*-

import time 
import traceback
import re
import os,sys

from tkinter import *
from tkinter import messagebox,ttk,filedialog
import tkinter.tix as Tix
import tkinter.font as tkFont

import win32api
import win32con
import win32gui
import win32ui

from io import BytesIO
import win32clipboard

from PIL import ImageGrab,Image,ImageTk,ImageFont,ImageDraw
import base64
#import pykeyboard
#from pykeyboard import PyKeyboard
from screeninfo import get_monitors

import threading
import imageio
import wx
import numpy
from pygifsicle import gifsicle
from pynput.mouse import Listener

WindX  = {}
WindXX = {}
WindX['self_folder'] = re.sub(r'\\','/',os.path.abspath(os.path.dirname(__file__)))
print("\nroot:",WindX['self_folder'])  
sys.path.append(WindX['self_folder'])       

def usedTime(stime,t=0):
    if not t:
        t = time.time() - stime

    tt={'h':'00','m':'00','s':'00'}
    
    if t > 3600:
        h = int(t/3600)
        tt['h'] = "{:0>2d}".format(h)
        t = t - h*3600
       
    if t > 60:
        m = int(t/60)
        tt['m'] = "{:0>2d}".format(m)
        t = t - m*60

    if t > 0:
        tt['s'] = "{:0>6.3f}".format(t)

    return tt['h'] + ':' + tt['m'] + ':' + tt['s'] 

def XYminMax(mm,xy):
    try:
        if not mm.__contains__('xmin'):
            mm['xmin'] = xy[0]
        if not mm.__contains__('ymin'):
            mm['ymin'] = xy[1]
        if not mm.__contains__('xmax'):     
            mm['xmax'] = xy[0]
        if not mm.__contains__('ymax'):
            mm['ymax'] = xy[1]
        
        while len(xy) >0:
             x = xy.pop(0)
             y = xy.pop(0)
             
             if(x > mm['xmax']):
                 mm['xmax'] = x
    
             if(x < mm['xmin']):
                 mm['xmin'] = x
        
             if(y > mm['ymax']):
                 mm['ymax'] = y
    
             if(y < mm['ymin']):
                 mm['ymin'] = y  
    except:        
        print("XYminMax error:\n" + traceback.format_exc()) 

def HideConsole():
    try:
        myfile = re.sub(r'.*(\\|\/)','',sys.argv[0])
        print("\nfile: ",myfile,"\n")
        if re.match(r'.*\.py$',myfile,re.I):
            return
            
        whnd = win32gui.FindWindowEx(0,0,'ConsoleWindowClass',None)
        title  = win32gui.GetWindowText(whnd)
        print(whnd,title)
        if title.endswith(myfile) or re.match(r'.*'+ title +'',myfile,re.I):
            win32gui.ShowWindow(whnd, win32con.SW_HIDE)
    except:
        error = traceback.format_exc()
        print(error)

def GetMonitors():
    displays = {}
    displays['Monitor'] = {}
    displays['all'] = []
    mm={}

    print("\nDispaly Monitor:")
    i = 0
    for m in get_monitors(): 
        #m   Monitor(x=0, y=0, width=2560, height=1440, width_mm=700, height_mm=390, name='\\\\.\\DISPLAY1')            
        i +=1
        displays['Monitor'][str(i)] = [m.width,m.height,m.x,m.y]  #width, height, x0, y0
        print("..",i,displays['Monitor'][str(i)]) 
        XYminMax(mm,[m.x,m.y, m.x + m.width, m.y + m.height])
    
    if i > 0:
        displays['Monitor']['FullScreen'] = [
            mm['xmax'] - mm['xmin'],
            mm['ymax'] - mm['ymin'],
            mm['xmin'],
            mm['ymin']
        ]
        print("..",'FullScreen',displays['Monitor']['FullScreen'])

        displays['FullScreenSize'] = (
            mm['xmax'] - mm['xmin'],
            mm['ymax'] - mm['ymin'],
            mm['xmin'],
            mm['ymin']
        )    
        print("..",'FullScreenSize',displays['FullScreenSize'])

    for x in sorted(displays['Monitor'].keys()):
        displays['all'].append("["+str(x)+"] " + str(displays['Monitor'][x][0]) + ',' + str(displays['Monitor'][x][1]) + ',' + str(displays['Monitor'][x][2]) + ',' + str(displays['Monitor'][x][3]))

    return displays

def GetPara(IsCustomized=0):
    WindX['PicFormatStr'] = WindXX['b_PicFormat'].get()

    WindX['Save2Folder'] = re.sub(r'\\','/',WindXX['Save2Folder'].get())
    if not WindX['Save2Folder']:
        WindX['Save2Folder'] = WindX['self_folder'] 
    else:
        WindX['Save2FolderStr'] = WindX['Save2Folder']

    WindX['Prefix'] = re.sub(r'\s+','',WindXX['Prefix'].get())
    if not WindX['Prefix']:
        WindX['Prefix'] = 'ScreenCatch'
    else:
        WindX['PrefixStr'] = WindX['Prefix']
    
    WindX['main'].title("Screen Catch: " + WindX['Prefix'])

    WindX['ImageOrder']  = int(re.sub(r'\s+','',WindXX['ImageOrder'].get()))
    if not WindX['ImageOrder']:
        WindX['ImageOrder'] = 1
        WindX['e_ImageOrder'].delete(0,END)
        WindX['e_ImageOrder'].insert(0,str(WindX['ImageOrder']))
    else:
        WindX['ImageOrderStr'] = WindX['ImageOrder']

    WindX['CatchPointStr'] = WindX['b_CatchPoint'].current()  
    WindX['CatchPoint']  = []   
    carea = WindXX['b_CatchPoint'].get()
    if IsCustomized and WindX['newRect']:
        carea = WindX['newRect']

    if re.match(r'.*\,0\,0$',carea):
        WindX['CatchPrimary'] = 1
    else:
        WindX['CatchPrimary'] = 0
        WindX['CatchPoint']  = re.split(r',',re.sub(r'\[.*\]\s+','',carea))
        if not (WindX['CatchPoint'] and len(WindX['CatchPoint'])==4):
            WindX['CatchPoint'] = ('1920','1080','0','0')

    #print(WindX)    

def PicCatchEdit():
    PicCatch(0,1)

def PicCatch(IsCustomized=0,isEdit=0):
    GetPara(IsCustomized)
    os.chdir(WindX['Save2Folder'])
     
    try:
        DelayCheck()
        StatusShow(1,auto_hide=1)

        err = None
        im  = None
        ShowMainWindow(0)
        if not WindX['CatchPrimary']:  
            im,err = ScreenShotXY(
                width=int(WindX['CatchPoint'][0]),
                height=int(WindX['CatchPoint'][1]),
                xSrc=int(WindX['CatchPoint'][2]),
                ySrc=int(WindX['CatchPoint'][3]))
        else:
            #bbox = ()
            im = ImageGrab.grab()
        ShowMainWindow(1)

        if im:  
            WindX['e_ImageCateched'].config(text="")
            WindX['main'].update()

            if isEdit:                
                m = re.sub(r'^.*\[|\].*$','',WindXX['b_CatchPoint'].get()) 
                print("WindX['Displays']['Monitor']["+str(m)+"]=",WindX['Displays']['Monitor'][m])
                TopCanvas([WindX['Displays']['Monitor'][m][0],WindX['Displays']['Monitor'][m][1]],                           
                          [WindX['Displays']['Monitor'][m][2],WindX['Displays']['Monitor'][m][3]],im,'edit')
            else:  
                PicSave(im,err)

        elif err:
            WindX['e_ImageCateched'].config(text=err,fg='red')    
    except:
        error = traceback.format_exc()
        print(error)

def PicSaveFile(PicFormatStr="PNG",xstr=""):
    #new image file name
    if WindX['ImageOrderLast'] == WindX['ImageOrder']:
            WindX['ImageOrderLastSub'] +=1                
    else:
        WindX['ImageOrderLastSub'] = 1
        WindX['ImageOrderLast']    = WindX['ImageOrder']
    
    subfix = "-" + "{:0>2d}".format(WindX['ImageOrderLastSub']) + xstr  
    picFile = WindX['Prefix'] + ".S" + "{:0>2d}".format(WindX['ImageOrder']) + subfix + '.' + PicFormatStr

    #delete existing image file                
    filep = WindX['Save2Folder']+"/"+ picFile

    if os.path.exists(filep):
        result = messagebox.askyesno("Warning!!!","The file is existing!!\nDo you want to overwrite it?\n\n    "+ filep)
        if result:
            os.remove(filep)
        else:
            saveasfilename = filedialog.asksaveasfilename(
                filetypes= [('image files', PicFormatStr), ('All files', '*')], 
                defaultextension= PicFormatStr,
                initialdir= WindX['Save2Folder'],
                title= "Save As",
                initialfile = os.path.basename(filep)
                )
            if not saveasfilename:
                return None
            filep = saveasfilename

    return filep

def PicSave(im=None,err=None):
    if not im:
        return

    filep = PicSaveFile(WindX['PicFormatStr'])
    if not filep:
        return

    #Save image to file
    if WindX['CatchPrimary']:
        print ("Image: size : %s, mode: %s" % (im.size, im.mode))  
    im.save(filep) 
    if WindX['CatchPrimary']:              
        print("Saved Primary screen to file:", filep,"\n")
    else:
        print ("Saved to:",filep,"\n")

    #verify image file
    if os.path.exists(filep):
        WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep),fg='#009900')
    else:
        if err:
            WindX['e_ImageCateched'].config(text=err,fg='red')
        else:    
            WindX['e_ImageCateched'].config(text="Failed to save image!",fg='red')
        WindX['ImageOrderLastSub'] -=1
    
    #delete Toplevel when it's catched and edited.
    if WindX['Toplevel']:
        print('close: Toplevel=',WindX['Toplevel'])
        WindX['Toplevel'].destroy()
        WindX['Toplevel'] = None

def PicSaveToClipboard(im=None,p=None):
    if not im:
        return
    
    try:
        win32clipboard.OpenClipboard() #打开剪贴板
        win32clipboard.EmptyClipboard()  #先清空剪贴板

        output=BytesIO()
        if p=='base64':
            im.save(output, format='JPEG')
            byte_data = output.getvalue()
            base64_str = "data:image/jpeg;base64," + re.sub(r'^b\'|\'+$','',str(base64.b64encode(byte_data)))
            #print(base64_str)
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, base64_str)  #将base64编码放入剪贴板
            WindX['e_ImageCateched'].config(text="Copied image to Clipboard as base64 HTML5 format!",fg='green')
        else:            
            im.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)  #将图片放入剪贴板
            WindX['e_ImageCateched'].config(text="Copied image to Clipboard!",fg='green')

        win32clipboard.CloseClipboard()
    except:
        print(traceback.format_exc()) 

def NextPicOrder(x=1):
    WindX['e_ImageCateched'].config(text="") 
    WindX['ImageOrderLastSub'] = 0

    xc = re.sub('.*[^\d]+','',WindXX['ImageOrder'].get())
    if not xc:
        WindX['ImageOrder']  = x
    else:
        WindX['ImageOrder']  = int(xc) + x
    
    if WindX['ImageOrder'] < 0:
        WindX['ImageOrder'] = 0

    WindX['e_ImageOrder'].delete(0,END)
    WindX['e_ImageOrder'].insert(0,str(WindX['ImageOrder']))

def PreviousPicOrder():
    NextPicOrder(-1)

def WindExit():              
    WindX['main'].destroy()  
    os._exit(0)
    #sys.exit(0)  # This will cause the window error: Python has stopped working ...
def DelayCheck():
    WindX['DelayStr'] = re.sub(r'.*[^0-9]+','',WindXX['e_Delay'].get())
    if WindX['DelayStr'] and int(WindX['DelayStr']) > 0:
        tt = int(WindX['DelayStr'])*10
        while tt > 0:
            WindX['e_ImageCateched'].config(text= "{:>02d}".format(tt) + " to catch screen!")
            WindX['main'].update()
            time.sleep(0.1)
            tt = tt - 1        

def GIF_File_Optimize(filep):
    try:
        gifsicle(
            sources=[filep], # or a single_file.gif
            destination= filep + ".o.gif", # or just omit it and will use the first source provided.
            optimize=True, # Whetever to add the optimize flag of not
            colors=256, # Number of colors t use
            options=["--verbose"] # Options to use.
        )
    except:
        print(traceback.format_exc())

def GIF_Make(sizes=[0, 0], xys=[0, 0], checkOnly=False):

    if WindX['GIF_recording'] and len(WindX['GIF_Frames']): #save GIF, reset
        WindX['GIF_recording'] = False
        time.sleep(2/int(WindX['GIF_FPS_Str']))
        nn = len(WindX['GIF_Frames'])

        filep = PicSaveFile("gif","." + str(nn))
        if not filep:
            filep = PicSaveFile("gif")

        if filep:
            try:
                WindX['e_ImageCateched'].config(text="saving: " + os.path.basename(filep) + " ... ...",fg='#009900')
                WindX['main'].update()

                images = []
                n = 0 
                font_end = None 
                font_type = None    
                try:
                    font_end = ImageFont.truetype(font='C:/Windows/Fonts/Arial.ttf',size=80) 
                    font_type = ImageFont.truetype(font='C:/Windows/Fonts/Arial.ttf',size=20) 
                except:
                    print(traceback.format_exc())

                for imp in WindX['GIF_Frames']:
                    n +=1
                    draw = ImageDraw.Draw(imp[0])
                    draw.text((0,0), re.sub(r'^00\:',"",imp[1]) + " #" + str(n) + "/" + str(nn), fill = (255, 0 ,0), font=font_type)
                    if n == nn-1 or n == nn:
                        isize = imp[0].size
                        x = int(isize[0]/2 - 100)
                        if x < 10:
                            x = 10
                        draw.text((x,int(isize[1]/2 - 80)), '--- END --- ',  fill = (255, 0 ,0), font=font_end)
                    elif n==1 or n==2:
                        isize = imp[0].size
                        x = int(isize[0]/2 - 100)
                        if x < 10:
                            x = 10
                        draw.text((x,int(isize[1]/2 - 80)), '--- START --- ', fill = (255, 0 ,0), font=font_end)

                    if len(imp[2]):
                        dx = 10                     
                        for p in imp[2]:
                            xy = [p[0]-dx, p[1]-dx, p[0]+dx, p[1]+dx]
                            xy0 = [p[0]-1, p[1]-1, p[0]+1, p[1]+1]
                            draw.ellipse(xy0,fill=None,outline='red',width=1)
                            draw.arc(xy,0,90,   fill='red',     width=4)
                            draw.arc(xy,90,180, fill='#FFA500', width=4)
                            draw.arc(xy,180,270,fill='blue',    width=4)
                            draw.arc(xy,270,360,fill='green',   width=4)

                            dx = dx*2
                            xy1 = [p[0]-dx, p[1]-dx, p[0]+dx, p[1]+dx]
                            draw.ellipse(xy1,fill=None, outline='red',width=1)


                    if len(imp[3]):
                        dx = 1                    
                        for p in imp[3]:
                            xy = [p[0]-dx, p[1]-dx, p[0]+dx, p[1]+dx]
                            draw.ellipse(xy,fill=None,outline='red',width=1)        

                    img = imp[0].convert("RGB")   # 通过convert将RGBA格式转化为RGB格式，以便后续处理 
                    #print("img.size=",img.size)
                    img = numpy.array(img)        # im还不是数组格式，通过此方法将img转化为数组
                    images.append(img) 

                imageio.mimsave(filep, images, 'GIF', duration=2/int(WindX['GIF_FPS_Str']))

                #verify image file
                if os.path.exists(filep):
                    print("optimize: ", filep)
                    WindX['e_ImageCateched'].config(text="optimizing: " + os.path.basename(filep) + " ... ...",fg='#009900')
                    WindX['main'].update()                    
                    GIF_File_Optimize(filep)

                    if os.path.exists(filep + ".o.gif"):
                        os.unlink(filep)
                        WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep + ".o.gif"),fg='#009900')
                    else:
                        WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep),fg='#009900')                    
                else:
                    WindX['e_ImageCateched'].config(text="Failed to save image!",fg='red')
                    WindX['ImageOrderLastSub'] -=1
            except:
                print(traceback.format_exc())

        WindX['GIF_Frames'] = []        
        DisplayRecordArea(sizes, xys, color_index=0, isClosed=True)
        WindX['e_snip_gif'].config(fg='red')
        StatusHide_Delay()
        return 1

    if checkOnly:
        return 0

    if not sizes[0]:
        print("GIF_Make_GO: sizes is invalid!", sizes)
        return

    GetPara()
    WindX['GIF_Frames'] = []
    WindX['GIF_recording'] = True

    p = threading.Thread(target=GIF_Make_GO, args=[sizes, xys])
    p.start()

def GIF_Make_GO(sizes=[0, 0], xys=[0, 0]):
    if not sizes[0]:
        print("GIF_Make_GO: sizes is invalid!", sizes)
        return

    WindX['GIF_FPS_Str'] = re.sub(r'.*[^0-9]+','',WindXX['e_GIF_FPS'].get())
    if not WindX['GIF_FPS_Str']:
        WindX['GIF_FPS_Str'] = 5
    WindX['e_GIF_FPS'].delete(0,END)
    WindX['e_GIF_FPS'].insert(0,str(WindX['GIF_FPS_Str']))

    stime = time.time()
    penColors = ["red","blue","green"]
    color_index = 0
    n = 0
    fps = int(WindX['GIF_FPS_Str'])
    tfps = 1 / 1/fps

    WindX['mouse_click_points'] = []
    WindX['mouse_move_points']  = []

    lastMPS = []
    while WindX['GIF_recording']:
        if n==0 or n%fps==0:
            DisplayRecordArea(sizes, xys, color_index)
            WindX['e_snip_gif'].config(fg= penColors[color_index])        
            WindX['e_ImageCateched'].config(text="making GIF " + usedTime(stime) + " (" + str(len(WindX['GIF_Frames'])) + "), click [GIF] to stop", fg=penColors[color_index])
            WindX['main'].update()
            lastMPS = []

        im,err = ScreenShotXY(
            width =int(sizes[0]),
            height=int(sizes[1]),
            xSrc  =int(xys[0]),
            ySrc  =int(xys[1])
        )
        if isinstance(im, Image.Image):
            mps = []
            if len(WindX['mouse_click_points']):
                for p in WindX['mouse_click_points']:
                    if (p[0] >= xys[0] and p[0] <= xys[0] + sizes[0]) and (p[1] >= xys[1] and p[1] <= xys[1] + sizes[1]):
                        mps.append([p[0] - xys[0], p[1] - xys[1]])
                        lastMPS.append([p[0] - xys[0], p[1] - xys[1]])
            
            elif len(lastMPS):
                pos = win32api.GetCursorPos()
                dx = 2               
                for p in lastMPS:
                    if (pos[0] >= p[0] - dx and pos[0] <= p[0] + dx) and (pos[1] >= p[1] - dx and pos[1] <= p[1] + dx):
                        mps.append(p)

            mps_move = []
            if len(WindX['mouse_move_points']):
                for p in WindX['mouse_move_points']:
                    if (p[0] >= xys[0] and p[0] <= xys[0] + sizes[0]) and (p[1] >= xys[1] and p[1] <= xys[1] + sizes[1]):
                        mps_move.append([p[0] - xys[0], p[1] - xys[1]])

            WindX['GIF_Frames'].append([im, usedTime(stime), mps, mps_move])   
        
        WindX['mouse_click_points'] = []
        WindX['mouse_move_points']  = []

        color_index +=1
        if color_index > 2:
            color_index = 0    
        time.sleep(tfps)
        n +=1

def DisplayRecordArea(sizes, xys, color_index=0, isClosed=False):
    try:
        try:
            if WindX['wx_screen']:
                WindX['wx_screen'].Destroy()
                WindX['wx_screen'] = None
            if WindX['wx_app']:
                WindX['wx_app'].Destroy()
                WindX['wx_app'] = None
        except:
            pass

        if isClosed:
            return

        penColors = ["red","blue","green"]

        penColors = ["red","blue","green"]

        x1 = xys[0] - 2 
        y1 = xys[1] - 2
        x2 = xys[0] + sizes[0] + 2
        y2 = xys[1] + sizes[1] + 2

        try:
            WindX['wx_app'] = wx.App(False)
            s = wx.ScreenDC()
            s.Clear()
            s.Pen = wx.Pen(penColors[color_index],2,wx.LONG_DASH)
            s.DrawLine(x1, y1, x2, y1)
            s.DrawLine(x2, y1, x2, y2)
            s.DrawLine(x2, y2, x1, y2)
            s.DrawLine(x1, y2, x1, y1)                
            #s.Refresh()  #AttributeError: 'ScreenDC' object has no attribute 'Refresh'
            WindX['wx_screen'] = s
        except:
            print(traceback.format_exc())
    except:
        print(traceback.format_exc())

def SetWindow(todo=None): 
    if todo == "snip_gif":
        if GIF_Make(checkOnly=True):
            StatusShow(1)
            return

    DelayCheck()
    WindX['e_ImageCateched'].config(text="")        
    WindX['main'].update()
       
    try:        
        StatusShow(1, auto_hide=1)
        ShowMainWindow(0)   
        im,err = ScreenShotXY(width =int(WindX['Displays']['FullScreenSize'][0]),
                            height=int(WindX['Displays']['FullScreenSize'][1]),
                            xSrc  =int(WindX['Displays']['FullScreenSize'][2]),
                            ySrc  =int(WindX['Displays']['FullScreenSize'][3]))
        ShowMainWindow(1)
        if isinstance(im, Image.Image):
            print ("Full Screen: size : %s, mode: %s" % (im.size, im.mode),"\n")                       
            TopCanvas(
                [WindX['Displays']['FullScreenSize'][0], 
                WindX['Displays']['FullScreenSize'][1]],
                [int(WindX['Displays']['FullScreenSize'][2]), 
                int(WindX['Displays']['FullScreenSize'][3])],
                im,
                todo
            )                    
        else:
            print("Failed to get screenshot!")
            WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')

    except:
        print(traceback.format_exc())

def ScreenShotXY(width=0,height=0,xSrc=None,ySrc=None):
    im_PIL = None  
    err = None
    try:
        if width == 0: 
            width = WindX['Displays']['FullScreenSize'][0]
        if height== 0:
            height= WindX['Displays']['FullScreenSize'][1]

        if xSrc == None:
            xSrc = WindX['Displays']['FullScreenSize'][2]
        if ySrc == None:
            ySrc = WindX['Displays']['FullScreenSize'][3]
        
        hWnd = 0
        hWndDC = win32gui.GetWindowDC(hWnd)   #0 - desktop
        #创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        #创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()
        #创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        #为bitmap开辟存储空间
        #print(width,height,xSrc,ySrc,';',hWndDC,';',mfcDC) #-1920 1080 1920 1080 ; 889263399 ; object 'PyCDC' - assoc is 000001F1B3EC5998, vi=<None>
        saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
        #将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)
        #保存bitmap到内存设备描述表
        saveDC.BitBlt((0,0), (width,height), mfcDC, (xSrc, ySrc), win32con.SRCCOPY)  
        #BOOLBitBlt((int x,int y),(int nWidth,int nHeight),CDC*pSrcDC,(int xSrc,int ySrc),DWORDdwRop);
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        ###生成图像
        im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
        #print(im_PIL)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hWnd,hWndDC)
    except:
        err = traceback.format_exc()
        print(traceback.format_exc())
    '''
    if isinstance(im_PIL, Image.Image):
        print ("Image size: %s, mode: %s" % (im_PIL.size, im_PIL.mode))                    
    else:
        print("Failed to get screenshot!")
    '''
    return im_PIL,err

class cButton:
    def __init__(self,obj,text='',cmd=None,rs=[],ts=[]):
        self.canvas = obj.canvas
        self.rect_outlineColor = rs[5]
        self.button_bg  = self.canvas.create_rectangle(rs[0],rs[1],rs[2],rs[3],fill=rs[4],outline=rs[5],width=rs[6])
        self.canvas.tag_bind(self.button_bg, "<Button-1>", cmd)
        self.canvas.tag_bind(self.button_bg, "<Motion>", self.cMotion)
        self.canvas.tag_bind(self.button_bg, "<Leave>", self.cLeave)
        obj.buttons.append(self.button_bg)

        if text:
            self.button_txt = self.canvas.create_text(ts[0],ts[1],text=text,fill=ts[2],font=ts[3])             
            self.canvas.tag_bind(self.button_txt,"<Button-1>", cmd)
            self.canvas.tag_bind(self.button_txt, "<Motion>", self.cMotion)
            self.canvas.tag_bind(self.button_txt, "<Leave>", self.cLeave)
            obj.buttons.append(self.button_txt)


    def cMotion(self,event):
        self.canvas.itemconfig(self.button_bg,outline='red')

    def cLeave(self,event):
        self.canvas.itemconfig(self.button_bg,outline=self.rect_outlineColor)

class TopCanvas:
    def __init__(self,sizes,xys,im,todo=None,titleOn=False):
        self.is_mousedown = 0
        self.is_draw_rectangle = 0
        self.rectangle = None
        self.Items = []
        self.buttons = []
        self.mouse_xs = 0
        self.mouse_ys = 0
        self.mouse_xe = 0
        self.mouse_ye = 0
        self.xys = xys
        self.sizes = sizes
        self.todo = todo
        self.titleOn = titleOn
        self.tip = None
        self.outline_color = 'red'
        self.im = im
        self.topTempText = None
        self.tmp_addedtexts = []
        self.topTempTextMousePoints = []
        self.canvas_height_offset = 0

        if titleOn:
            self.canvas_height_offset = 41

        WindX['newRect'] = ""

        if WindX['Toplevel']:
            print('close: Toplevel=',WindX['Toplevel'])
            WindX['Toplevel'].destroy()

        if self.todo == 'snip' or self.todo == 'snip_edit' or self.todo == 'snip_gif':
            self.top = Toplevel(cursor='tcross')
        else:
            self.top = Toplevel()

        WindX['Toplevel'] = self.top
        #print('new: Toplevel=',WindX['Toplevel']) 
        print('\nnew toplevel size, x,y:',sizes, xys)
        self.top.wm_attributes('-topmost',1) 
        if not titleOn:
            self.top.overrideredirect(1)
            self.top.geometry(str(sizes[0]) + 'x' + str(sizes[1]) + '+' + str(xys[0]) + '+' + str(xys[1]))
        else:
            self.top.geometry('+' + str(xys[0]) + '+' + str(xys[1]))            

        self.canvas=Canvas(self.top,
                    width=sizes[0],
                    height=sizes[1] + self.canvas_height_offset,
                    bg="white",
                    relief=FLAT,
                    bd = 0,
                    )
        self.canvas.configure(highlightthickness = 0)
        self.canvas.pack()        
        self.canvas.bind("<ButtonRelease-1>",self.MouseUp)
        self.canvas.bind("<Button-1>",self.MouseDown)
        self.canvas.bind("<B1-Motion>",self.MouseMove)
        
        self.im_width = sizes[0] - xys[0]
        self.im_height= sizes[1] - xys[1]
        self.im_x0 = xys[0]
        self.im_y0 = xys[1]
        if im:
            #print("canvas.create_image:",((sizes[0] - xys[0])/2,(sizes[1] - xys[1])/2,im.size),', sizes=',sizes,', xys=',xys)
            imk = ImageTk.PhotoImage(im)             
            #self.canvas.create_image((sizes[0] - xys[0])/2,(sizes[1] - xys[1])/2,image = imk) 
            self.canvas.create_image(int(sizes[0]/2),int(sizes[1]/2 + self.canvas_height_offset),image = imk)

        #cButton(self,'',self.TDBX,  [0, 0, 480, 40,'#FEFEFE',"#FEFEFE",1],[30, 30,'red',("Arial",20,"bold")])
        cButton(self,'X',self.Close,[0, 0, 40, 40,'#E0E0E0',"#E0E0E0" ,1],[20, 20,'red',("Arial",20,"bold")])

        self.is_draw_rectangle = 1
        self.is_draw_addText = 0
        self.is_draw_line = 0
        self.drawn_line = None
        self.text_box = None

        print("self.todo=", self.todo)
        if self.todo == 'snip' or self.todo == 'snip_edit':
            self.tip = None
            '''
            self.tip = self.canvas.create_text(
                            200,
                            200,
                            text='Please use mouse to draw a rectangle to catch image!',
                            fill='red',
                            anchor=W,
                            justify=LEFT,
                            font=("Arial",20,"bold")
                            )
            '''            
        elif self.todo == 'edit':      
            cButton(self,'',self.OutLineColor1,[41, 0, 61, 20,'red',"red",1])
            cButton(self,'',self.OutLineColor2,[61, 0, 81, 20,'green',"green",1])
            cButton(self,'',self.OutLineColor3,[41, 20, 61, 40,'black',"black",1])
            cButton(self,'',self.OutLineColor4,[61, 20, 81, 40,'yellow',"yellow",1])

            cb = cButton(self,'Rect',self.AddRectangle,[82, 0, 162, 40,'#00CC99',"#E0E0E0",1],[122, 20,'blue',("Arial",20,"normal")])
            self.button_rect_bg  = cb.button_bg

            cb = cButton(self,'Line',self.AddLine,  [163, 0, 243, 40,'#E0E0E0',"#E0E0E0",1],[203, 20,'blue',("Arial",20,"normal")])
            self.button_addLine_bg  = cb.button_bg

            cb = cButton(self,'Text',self.AddText,  [244, 0, 324, 40,'#E0E0E0',"#E0E0E0",1],[284, 20,'blue',("Arial",20,"normal")])
            self.button_addText_bg  = cb.button_bg

            cb = cButton(self,'Undo',self.Undo,     [325, 0, 405, 40,'#E0E0E0',"#E0E0E0",1],[365, 20,'gray',("Arial",20,"normal")])
            self.button_delLast_txt = cb.button_txt 

            cButton(self,'Save',self.Save,          [406, 0, 486, 40,'#E0E0E0',"#E0E0E0",1],[446, 20,'blue',("Arial",20,"normal")])

            cButton(self,'Copy',  self.Copy2Clipboard,[487, 0, 567, 40,'#E0E0E0',"#E0E0E0",1],[527, 20,'blue',("Arial",20,"normal")])

            cButton(self,'Base64',self.Copy2ClipboardBase64,[568, 0, 648, 40,'#E0E0E0',"#E0E0E0",1],[608, 20,'blue',("Arial",15,"normal")])

        self.top.mainloop()

    def TDBX(self,event):
        return 0

    def Copy2ClipboardBase64(self,event):
        self.Copy2Clipboard(event,p='base64')

    def Copy2Clipboard(self,event,p=''):        
        try:             
            HWND = self.canvas.winfo_id()
            rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
            ShowMainWindow(0)
            im,err = ScreenShotXY(
                width =int(rect[2] - rect[0]),
                height=int(rect[3] - rect[1] - self.canvas_height_offset),
                xSrc  =int(rect[0]),
                ySrc  =int(rect[1] + self.canvas_height_offset)
            )
            ShowMainWindow(1)
            if isinstance(im, Image.Image):                    
                PicSaveToClipboard(im=im,p=p)
            else:
                print("Failed to get screenshot!")
                WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')               
        except:
            print(traceback.format_exc())                                       

    def Save(self,event):
        if self.todo == 'edit':
            for b in self.buttons:
                self.canvas.delete(b)
            self.top.update()  
            #print("\nsave edited image ...\n")   
            if self.titleOn:                 
                try:                     
                    HWND = self.canvas.winfo_id()
                    rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
                    ShowMainWindow(0)
                    im,err = ScreenShotXY(
                        width =int(rect[2] - rect[0]),
                        height=int(rect[3] - rect[1] - self.canvas_height_offset),
                        xSrc  =int(rect[0]),
                        ySrc  =int(rect[1] + self.canvas_height_offset)
                    )
                    ShowMainWindow(1)
                    if isinstance(im, Image.Image):                    
                        GetPara(0)
                        imCopy = im.copy()
                        PicSave(im=im)
                        PicSaveToClipboard(im=imCopy)      
                    else:
                        print("Failed to get screenshot!")
                        WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')
                       
                except:
                    print(traceback.format_exc()) 
                                              
            else:
                PicCatch()
            self.Close(event)
        else:
            self.Close(event)

    def OutLineColor1(self,event):
        self.outline_color = 'red'

    def OutLineColor2(self,event):
        self.outline_color = 'green'

    def OutLineColor3(self,event):
        self.outline_color = 'black'

    def OutLineColor4(self,event):
        self.outline_color = 'yellow'

    def Undo(self,event):
        if len(self.Items):
            self.canvas.delete(self.Items.pop())
        elif self.rectangle:
            self.canvas.delete(self.rectangle)
            self.rectangle = None

    def AddRectangle(self,event):
        if self.is_draw_rectangle:
            self.is_draw_rectangle = 0
        else:
            self.is_draw_rectangle = 1            
        self.is_draw_addText = 0
        self.is_draw_line = 0  
        self.ButtonBG()

    def AddText(self,event):
        if self.is_draw_addText:
            self.is_draw_addText = 0            
        else:
            self.is_draw_addText = 1
        self.is_draw_rectangle = 0
        self.is_draw_line = 0  
        self.ButtonBG()    

    def AddLine(self,event):
        if self.is_draw_line:
            self.is_draw_line = 0            
        else:
            self.is_draw_line = 1
        self.is_draw_rectangle = 0
        self.is_draw_addText = 0
        self.ButtonBG()  

    def ButtonBG(self):
        if self.is_draw_rectangle:
            self.canvas.itemconfig(self.button_rect_bg,fill='#00CC99')
        else:
            self.canvas.itemconfig(self.button_rect_bg,fill='#E0E0E0')

        if self.is_draw_addText:
            self.canvas.itemconfig(self.button_addText_bg,fill='#00CC99')
        else:
            self.canvas.itemconfig(self.button_addText_bg,fill='#E0E0E0')

        if self.is_draw_line:
            self.canvas.itemconfig(self.button_addLine_bg,fill='#00CC99')
        else:
            self.canvas.itemconfig(self.button_addLine_bg,fill='#E0E0E0')

    def TextInputView(self,event):
        if self.topTempText:
            inputText = re.sub(r'\n+$','',self.topTempTextWedget.get("0.0", "end"))
            if len(self.tmp_addedtexts):
                for xt in self.tmp_addedtexts:
                    self.canvas.delete(xt)
            self.tmp_addedtexts = []

            if len(inputText):
                if self.is_draw_addText and self.rectangle:
                    lines = re.split(r'\n', inputText)
                    lineH = int(abs(self.topTempTextMousePoints[3] - self.topTempTextMousePoints[1] - 3*(len(lines) + 1)) / len(lines))             
                    fsize = int(lineH / 1.33)  #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
                    if fsize > 1:
                        y = self.topTempTextMousePoints[1] + lineH/2 + 3
                        for line in lines:  
                            if y < 50 + lineH/2 + 3:
                                y = 50 + lineH/2 + 3                      
                            textbox = self.canvas.create_text(
                                        self.topTempTextMousePoints[0] + 3,
                                        y,
                                        font = ('Arial', fsize, 'normal'),
                                        text = line,
                                        fill= self.outline_color,
                                        anchor = W,
                                        justify = LEFT)
                            self.tmp_addedtexts.append(textbox)
                            y += lineH + 3
                    self.top.update()

    def MouseUp(self,event):
        if self.text_box:
            self.canvas.delete(self.text_box)
            self.text_box = None

        self.is_mousedown = 0   
        self.mouse_xe = event.x
        self.mouse_ye = event.y 
        if self.mouse_ye <= 50:
            if self.rectangle:
                self.canvas.delete(self.rectangle)
            self.rectangle = None
            return

        if self.todo == 'snip' or self.todo == 'snip_edit' or self.todo == "snip_gif":
            self.Close(event,1)
        elif self.todo == 'edit':
            if self.is_draw_rectangle and self.rectangle:
                self.Items.append(self.rectangle)
                self.rectangle = None

            elif self.is_draw_addText and self.rectangle:                
                tw = abs(self.mouse_xs - self.mouse_xe)
                th = abs(self.mouse_ys - self.mouse_ye)
                if tw > 5 and th > 5:
                    if self.topTempText:
                        self.topTempText.destroy()

                    mm = {}
                    XYminMax(mm,[self.mouse_xs, self.mouse_ys, self.mouse_xe, self.mouse_ye])
                    self.topTempTextMousePoints = [mm['xmin'], mm['ymin'], mm['xmax'], mm['ymax']]

                    HWND = self.canvas.winfo_id()
                    rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b

                    x = rect[0] + mm['xmin'] + 1
                    y = rect[1] + mm['ymin'] + 1 + th
                    if y + th*2 > rect[3]:
                        y = rect[1] + mm['ymin'] - th*2 - 1

                    self.topTempText = Toplevel()
                    self.topTempText.wm_attributes('-topmost',1) 
                    self.topTempText.overrideredirect(1)
                    self.topTempText.geometry(str(tw) + 'x' + str(th*2) + '+' + str(x) + '+' + str(y))
                    fontStyle = tkFont.Font(family='Arial', size=15)
                    self.topTempTextWedget = Text(self.topTempText, padx=5, pady=5, font=fontStyle, fg=self.outline_color)
                    self.topTempTextWedget.pack(side=TOP, fill=BOTH)
                    self.topTempTextWedget.focus()
                    self.topTempTextWedget.bind('<KeyRelease>',self.TextInputView)
                                        

            elif self.is_draw_line and self.rectangle and self.drawn_line:
                self.canvas.delete(self.rectangle)
                self.Items.append(self.drawn_line)
                self.drawn_line = None
                self.rectangle  = None

            if len(self.Items):
                self.canvas.itemconfig(self.button_delLast_txt,fill='blue')
            else:
                self.canvas.itemconfig(self.button_delLast_txt,fill='gray')

            if len(self.tmp_addedtexts):
                for xt in self.tmp_addedtexts:
                    self.canvas.delete(xt)
            self.tmp_addedtexts = []

        self.mouse_xs = 0
        self.mouse_ys = 0
        self.mouse_xe = 0
        self.mouse_ye = 0

    def MouseDown(self,event):
        self.is_mousedown = 1
        self.mouse_xs = event.x
        self.mouse_ys = event.y
        if self.topTempText:
            inputText = re.sub(r'\n+$','',self.topTempTextWedget.get("0.0", "end"))
            self.topTempText.destroy()
            self.topTempText = None
            if len(inputText):
                if self.is_draw_addText and self.rectangle:
                    lines = re.split(r'\n', inputText)  
                    lineH = int(abs(self.topTempTextMousePoints[3] - self.topTempTextMousePoints[1] - 3*(len(lines) + 1)) / len(lines))             
                    fsize = int(lineH / 1.33)  #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
                    if fsize > 1:
                        y = self.topTempTextMousePoints[1] + lineH/2 + 3
                        for line in lines:  
                            if y < 50 + lineH/2 + 3:
                                y = 50 + lineH/2 + 3                      
                            textbox = self.canvas.create_text(
                                        self.topTempTextMousePoints[0] + 3,
                                        y,
                                        font = ('Arial', fsize, 'normal'),
                                        text = line,
                                        fill= self.outline_color,
                                        anchor = W,
                                        justify = LEFT)
                            self.Items.append(textbox)
                            #self.canvas.tag_bind(textbox, "<Motion>",         self.Text_MouseMove)
                            #self.canvas.tag_bind(textbox, "<Leave>",          self.Text_MouseOut)
                            #self.canvas.tag_bind(textbox, "<ButtonRelease-1>",self.Text_MouseUp)
                            #self.canvas.tag_bind(textbox, "<Button-1>",       self.Text_MouseDown)

                            y += lineH + 3
                    self.top.update()
                    time.sleep(0.3)
            self.canvas.delete(self.rectangle)
            self.rectangle = None

        self.topTempTextMousePoints = []

    def MouseMove(self,event):
        if self.tip:
            self.canvas.delete(self.tip)
            self.tip = None
        if self.is_mousedown:
            if self.is_draw_rectangle or self.todo == 'snip' or self.is_draw_addText or self.is_draw_line:
                if self.rectangle:
                    self.canvas.delete(self.rectangle)
                
                iwidth = 2
                idash = ()
                if self.is_draw_addText or self.is_draw_line or self.todo == 'snip' or self.todo == 'snip_edit':
                    iwidth = 1
                    idash = (4,4)
                self.rectangle = self.canvas.create_rectangle(
                                    self.mouse_xs,
                                    self.mouse_ys,
                                    event.x,
                                    event.y,
                                    outline = self.outline_color,
                                    width= iwidth,
                                    dash= idash
                                    )
                
                if self.is_draw_line:
                    if self.drawn_line:
                        self.canvas.delete(self.drawn_line)
                    self.drawn_line = self.canvas.create_line(
                                    self.mouse_xs,
                                    self.mouse_ys,
                                    event.x,
                                    event.y,
                                    fill = self.outline_color,
                                    width= 2,
                                    )
                if self.text_box:
                    self.canvas.delete(self.text_box)
                    self.text_box = None
                self.text_box = self.canvas.create_text(
                    event.x + 5,
                    self.mouse_ys + 8,
                    font = ('Arial', 10, 'normal'),
                    text = str(abs(event.x - self.mouse_xs)) + "x" + str(abs(event.y - self.mouse_ys)),
                    fill = self.outline_color,
                    anchor = W,
                    justify = LEFT)
                self.top.update()

    def Close(self,event,IsMouseUp=0):
        if self.text_box:
            self.canvas.delete(self.text_box)
            self.text_box = None
        if self.topTempText:
            self.topTempText.destroy()
            self.topTempText = None

        if (self.todo == 'snip' or self.todo == 'snip_edit' or self.todo == "snip_gif") and IsMouseUp:
            x1 = self.mouse_xs #+ self.xys[0]
            x2 = self.mouse_xe #+ self.xys[0]
            y1 = self.mouse_ys #+ self.xys[1]
            y2 = self.mouse_ye #+ self.xys[1]
            
            if x1 > x2:
                x1 = self.mouse_xe
                x2 = self.mouse_xs
            if y1 > y2:
                y1 = self.mouse_ye
                y2 = self.mouse_ys

            ww = x2 - x1
            hh = y2 - y1
            if ww > 10 and hh > 10:
                try:  
                    im = self.im.crop((x1,y1,x2,y2))              
                    
                    if self.todo == 'snip_edit':
                        x0 = self.xys[0] + x1
                        y0 = self.xys[1] + y1
                        self.top.destroy()
                        print(im)                        
                        if isinstance(im, Image.Image):                  
                            TopCanvas(
                                sizes= [ww, hh],
                                xys  = [x0, y0],
                                im   = im,
                                todo = 'edit',
                                titleOn = True
                            )
                        else:
                            print("Failed to get screenshot!")
                            WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')
                    
                    elif self.todo == "snip_gif":
                        x0 = self.xys[0] + x1
                        y0 = self.xys[1] + y1

                        GIF_Make(sizes= [ww, hh],
                                xys  = [x0, y0]
                            )
                        self.top.destroy()
                    else:
                        self.top.destroy()
                        GetPara(0)
                        PicSave(im=im)                  
                except:
                    print(traceback.format_exc()) 
        else:
            self.top.destroy()

    def Text_MouseDown(self,event):
        print(self,event)
        return 0
    def Text_MouseUp  (self,event):
        return 0
    def Text_MouseMove(self,event):  
        print(self, event) 
        return 0
    def Text_MouseOut (self,event):
        print(self,event)
        return 0

def SetFolder():
    fpath = filedialog.askdirectory(initialdir = WindX['self_folder'])
    if fpath:
        print(fpath)
        fps = re.split(r'/',re.sub(r'\\','/',fpath))
        WindX['e_Save2Folder'].delete(0,END)
        WindX['e_Save2Folder'].insert(0,fpath)
        WindX['e_Prefix'].delete(0,END)
        WindX['e_Prefix'].insert(0,fps[-1])
        WindX['main'].title("Screen Catch: " + fps[-1])

def ShowHideBasic():
    if WindX['ShowHideBasic'] == 1:
        WindX['ShowHideBasic'] = 0
        WindX['Frame1'].grid_remove()
        WindX['e_HideBase'].config(text="∨")
        WinAnchor()
        WindX['main'].overrideredirect(1)
        StatusShow(0)
    else:
        WindX['ShowHideBasic'] = 1
        WindX['Frame1'].grid()
        WindX['e_HideBase'].config(text="∧")
        WindX['main'].overrideredirect(0)
        StatusShow(1)

def WinAnchor():
    gs = re.split(r'x|\+', WindX['main'].geometry()) #506x152+-1418+224
    WindX['main'].geometry('+'+ str(gs[2]) +'+0')

def StatusShow(display=1,auto_hide=0):
    if display:
        WindX['e_ImageCateched'].grid()
        if auto_hide:
            t1 = threading.Timer(1, StatusHide_Delay)
            t1.start() 
    else:
        WindX['e_ImageCateched'].grid_remove()

def StatusHide_Delay():
    time.sleep(30)
    StatusShow(0)

def ShowMainWindow(toShow):
    if toShow:
        print("--------- show root window ---------")
        #WindX['main'].geometry('+'+ str(WindX['LastGeometry'][2]) +'+' + str(WindX['LastGeometry'][3]))
        WindX['main'].update()
        WindX['main'].deiconify()
    else:
        print("--------- hide root window ---------")
        #WindX['LastGeometry'] = re.split(r'x|\+', WindX['main'].geometry()) #506x152+-1418+224
        #WindX['main'].geometry('+'+ str(WindX['LastGeometry'][2]) +'+-' + str(WindX['LastGeometry'][1]))
        WindX['main'].withdraw()
        time.sleep(0.5)

def GUI(IsInit=None):
    if IsInit:
        WindX['Displays'] = GetMonitors()

    WindX['main'] = Tix.Tk()
    WindX['main'].title("Screen Catch")
    WindX['main'].geometry('+' + str(WindX['mainPX']) + '+' + str(WindX['mainPY']))
    WindX['main'].wm_attributes('-topmost',1) 
    WindX['main'].protocol("WM_DELETE_WINDOW", WindExit)

    balstatus = Label(WindX['main'], justify=CENTER, relief=FLAT,pady=3,padx=3, bg='yellow',wraplength = 50)
    #balstatus.grid(row=4,column=0,sticky=E+W+S+N,pady=0,padx=0)
    WindX['winBalloon'] = Tix.Balloon(WindX['main'], statusbar = balstatus)

    Lfg = 'gray'    
    WindX['Frame1'] = Frame(WindX['main'])
    WindX['Frame1'].grid(row=0,column=0,sticky=W,pady=5,padx=5)
    WindX['Frame2'] = Frame(WindX['main'])
    WindX['Frame2'].grid(row=1,column=0,sticky=W,pady=0,padx=0)

    if WindX['Frame1']:
        row = 0 
        Label(WindX['Frame1'], text='Image Format', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['b_PicFormat'] = StringVar()
        b = ttk.Combobox(WindX['Frame1'], textvariable=WindXX['b_PicFormat'], justify=CENTER,state="readonly",width=5)
        b.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        b['values'] = ('jpg','png')
        if WindX['PicFormatStr'] == 'jpg':
            b.current(0)
        else:
            b.current(1)

        Label(WindX['Frame1'], text='Prefix', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=3,sticky=W)
        WindXX['Prefix'] = StringVar()
        e=Entry(WindX['Frame1'], justify=LEFT, relief=FLAT, textvariable= WindXX['Prefix'],width=20)
        e.grid(row=row,column=4,sticky=E,padx=3)
        WindX['e_Prefix'] = e
        if WindX['PrefixStr']:
            e.insert(0,WindX['PrefixStr'])

        #b=iButton(WindX['Frame1'],row,5,WindExit,'x','red','#F0F0F0',msg='Close')

        row +=1
        Label(WindX['Frame1'], text='Save To Folder', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['Save2Folder'] = StringVar()
        e=Entry(WindX['Frame1'], justify=LEFT, relief=FLAT, textvariable= WindXX['Save2Folder'])
        e.grid(row=row,column=2,sticky=E+W,padx=3,columnspan=3)
        WindX['e_Save2Folder'] = e
        if WindX['Save2FolderStr']:
            e.insert(0,WindX['Save2FolderStr'])
        elif WindX['self_folder']:
            e.insert(0,WindX['self_folder'])

        b=iButton(WindX['Frame1'],row,5,SetFolder,'...',None,'#F0F0F0',msg='Select folder') 

        row +=1
        Label(WindX['Frame1'], text='Catch Window', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)

        WindXX['b_CatchPoint'] = StringVar()
        b = ttk.Combobox(WindX['Frame1'], textvariable=WindXX['b_CatchPoint'], justify=LEFT,state="readonly")
        b.grid(row=row,column=2,sticky=E+W,pady=0,padx=5,columnspan=3) 
        b['values'] = WindX['Displays']['all']        
        
        WindX['b_CatchPoint'] = b
        if WindX['CatchPointStr']:
            b.current(WindX['CatchPointStr'])    
        else:
            b.current(0)

        row +=1
        Label(WindX['Frame1'], text='Catch Delay', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['e_Delay'] = StringVar()
        e=Entry(WindX['Frame1'], justify=CENTER, relief=FLAT, textvariable= WindXX['e_Delay'],width=4)
        WindX['e_Delay'] = e
        if WindX['DelayStr']:
            e.insert(0,WindX['DelayStr'])
        else:
            e.insert(0,'0')
        e.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        Label(WindX['Frame1'], text='seconds', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=3,sticky=W)    
    
        row +=1
        Label(WindX['Frame1'], text='GIF FPS', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['e_GIF_FPS'] = StringVar()
        e=Entry(WindX['Frame1'], justify=CENTER, relief=FLAT, textvariable= WindXX['e_GIF_FPS'],width=4)
        WindX['e_GIF_FPS'] = e
        if WindX['GIF_FPS_Str']:
            e.insert(0,WindX['GIF_FPS_Str'])
        else:
            e.insert(0,'0')
        e.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        Label(WindX['Frame1'], text='frames per seconds', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=3,sticky=W) 

    if WindX['Frame2']:
        row =0
        Label(WindX['Frame2'], text='Step#', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=0,sticky=W)
        WindXX['ImageOrder'] = StringVar()
        e=Entry(WindX['Frame2'], justify=CENTER, relief=FLAT, textvariable= WindXX['ImageOrder'],width=4)
        e.grid(row=row,column=1,sticky=E+W+N+S,padx=0)
        WindX['e_ImageOrder'] = e
        if WindX['ImageOrderStr']:
            e.insert(0,WindX['ImageOrderStr'])
        else:
            e.insert(0,'1')

        b=iButton(WindX['Frame2'],row,2,PreviousPicOrder,'<',msg='Step -1') 
        iSeparator(WindX['Frame2'],row,3)
        b=iButton(WindX['Frame2'],row,4,NextPicOrder,'>',msg='Step +1')
        iSeparator(WindX['Frame2'],row,5)

        b=iButton(WindX['Frame2'],row,6,ShowHideBasic,'∧',msg='Show / Hide')
        WindX['e_HideBase'] = b.b
        iSeparator(WindX['Frame2'],row,7)
  
        b=iButton(WindX['Frame2'],row,8,PicCatch,'Win','red',msg='[Win]: Catch the window which is selected in the field [Catch Window]')
        iSeparator(WindX['Frame2'],row,9)
        b=iButton(WindX['Frame2'],row,10,PicCatchEdit,'W+E','red',msg='[W+E]: Catch the whole widhow and edit')
        iSeparator(WindX['Frame2'],row,11)
        b=iButton(WindX['Frame2'],row,12,lambda:SetWindow("snip"),'Snip','red',msg='[Snip]: Snip window then save')

        iSeparator(WindX['Frame2'],row,13)
        b=iButton(WindX['Frame2'],row,14,lambda:SetWindow("snip_edit"),'S+E','red',msg='[S+E]: Snip window and edit image')

        iSeparator(WindX['Frame2'],row,15)
        b=iButton(WindX['Frame2'],row,16,lambda:SetWindow("snip_gif"),'GIF','red',msg='[GIF]: Snip window and make GIF')
        WindX['e_snip_gif'] = b.b

        row +=1
        e = Label(WindX['Frame2'], text='', justify=LEFT, fg='#009900',relief=FLAT,pady=3,padx=3)
        e.grid(row=row,column=0,sticky=E+W+N+S,pady=0,padx=0,columnspan=20)
        WindX['e_ImageCateched'] = e

    if IsInit:
        HideConsole()

    mainloop()

class iSeparator:
    def __init__(self,frm,row=0,col=0,txt='|',fg='#FFFFFF',bg='#E0E0E0',p=[CENTER,FLAT,0,0]):
        self.label = Label(frm, 
                            text=txt, 
                            justify=p[0], 
                            relief=p[1],
                            pady=p[2],
                            padx=p[3],
                            fg=fg,
                            bg=bg
                            )
        self.label.grid(
                    row=row,
                    column=col,
                    sticky=E+W+N+S,
                    pady=0,
                    padx=0,
                        )

class iButton:
    def __init__(self,frm,row=0,col=0,cmd=None,txt='?',fg='blue',bg='#E0E0E0',
                    colspan=1,msg=None,
                    p=[LEFT,FLAT,3,1,'#FFFF66','#FFFF99',5,E+W+N+S,0,0]):

        self.b = Button( frm, 
                    text=txt, 
                    fg=fg,
                    bg=bg,
                    justify=p[0], 
                    relief=p[1],
                    padx=p[2],
                    pady=p[3],                    
                    activebackground=p[4],
                    highlightbackground=p[5],
                    width=p[6],
                    command=cmd
                    )
        self.b.grid( row=row,
                column=col,
                sticky=p[7],
                pady=p[8],
                padx=p[9],
                columnspan=colspan
                )
        self.b.bind('<Motion>',self.iMotion)
        self.b.bind('<Leave>',self.iLeave)
        self.bg = bg

        if msg:                
            self.message = msg
            WindX['winBalloon'].bind_widget(self.b, balloonmsg= msg)
        else:
            self.message = ""

    def iMotion(self,event):
        self.b.config(bg = '#FFFFF0')
        #if self.message:
        #    WindX['e_ImageCateched'].config(text=self.message) 

    def iLeave(self,event):
        self.b.config(bg = self.bg)

def MouseOnClick(x, y, button, pressed):
    #print(button,'{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    if re.match(r'.*left',str(button),re.I) and (not pressed):
        WindX['mouse_click_points'].append([x,y])

def MouseOnMove(x, y):
    WindX['mouse_move_points'].append([x,y])

def MouseListener():
    with Listener(on_click=MouseOnClick, on_move=MouseOnMove) as listener: #(on_move=on_move, on_click=on_click, on_scroll=on_scroll) 
        listener.join()

def main():   
    WindX['Toplevel'] = None  
    WindX['BoxTopLevel'] = None    
    WindX['ImageOrderLastSub'] = 1
    WindX['ImageOrderLast'] =  0  
    WindX['Save2FolderStr'] = ""
    WindX['PrefixStr']      = "ScreenCatch"
    WindX['ImageOrderStr']  = ""
    WindX['CatchPointStr']  = 0
    WindX['PicFormatStr']   = 'png'
    WindX['mainPX'] = 0
    WindX['mainPY'] = 0 
    WindX['ShowHideBasic'] = 1
    WindX['CatchPrimary'] = 1
    WindX['newRect'] = ""
    WindX['DelayStr'] = '0'
    WindX['wx_screen'] = None
    WindX['wx_app'] = None
    WindX['mouse_click_points'] = []
    WindX['mouse_move_points'] = []
    WindX['GIF_Frames'] = []
    WindX['GIF_recording'] = False
    WindX['GIF_FPS_Str'] = 5
    WindX['LastGeometry'] = []

    t1 = threading.Timer(1,MouseListener)
    t1.start() 
    GUI(1)

if __name__ == "__main__":      
    main()


