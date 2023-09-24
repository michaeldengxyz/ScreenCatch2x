#Pyhton 3.x
# -*- coding: UTF-8 -*-
#rev.13.0.0.0
#change: close the current toplevel window only after Save the image.
#Pyinstaller -F ScreenCatch13x.py

"""
pip install pywin32
pip install screeninfo
pip install pynput
pip install imageio
pip install pygifsicle
pip install PythonMagick-0.9.19-cp310-cp310-win_amd64.whl  #cd C:/Users/dengm/OneDrive/Program/Normalcd 
pip install moviepy

#https://blog.csdn.net/luanyongli/article/details/81385284
pip install pytesseract 

#https://github.com/paddlepaddle/paddleocr
#https://github.com/PaddlePaddle/PaddleOCR/blob/develop/doc/doc_ch/installation.md
pip install paddlepaddle
pip install Shapely-1.8.2-cp310-cp310-win_amd64.whl  #cd C:/Users/dengm/OneDrive/Program/Normalcd 
pip install paddleocr
"""

import time
WindX  = {}
WindX['load_times'] = []
WindX['load_times'].append([time.time(), 'app start and load basic modules ...'])

#from hashlib import shake_128 
import traceback
import re
import os,sys
import glob

from mypyUtilsUI import UI_ClassSnapshotMaskFullscreen

from tkinter import *
from tkinter import messagebox,ttk,filedialog
import tkinter.tix as Tix
import tkinter.font as tkFont
import tkinter.colorchooser as icolorchooser

import win32api
import win32con
import win32gui
import win32ui

from io import BytesIO
import win32clipboard

WindX['load_times'].append([time.time(), 'app load modules: PIL module, ...'])
from PIL import ImageGrab,Image,ImageTk,ImageFont,ImageDraw
import base64
#import pykeyboard
#from pykeyboard import PyKeyboard
from screeninfo import get_monitors

import json
import threading
import imageio     #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ imageio
import numpy
from pygifsicle import gifsicle   #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pygifsicle
from pynput.mouse import Listener
from pynput import keyboard as keyboardX
import math

WindX['load_times'].append([time.time(), 'app load modules: paddleocr, pytesseract, ...'])
from paddleocr import PaddleOCR, draw_ocr  #will use more time to import this module
import pytesseract                         #will use more time to import this module
#from collections import Counter 
import random
import shutil
import pandas
import PythonMagick ##pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ PythonMagick
#https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonmagick


WindX['load_times'].append([time.time(), 'app load modules: moviepy ...'])
from moviepy.editor import concatenate_videoclips, ImageClip

WindX['load_times'].append([time.time(), 'app load modules - end.'])

WindXX = {}
WindX['self_folder'] = re.sub(r'\\','/',os.path.abspath(os.path.dirname(__file__)))
print("\nroot:",WindX['self_folder'])  
sys.path.append(WindX['self_folder'])       

WindX['Toplevels'] = []  
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
WindX['mouse_click_points'] = []
WindX['mouse_move_points'] = []
WindX['GIF_Frames'] = []
WindX['GIF_recording'] = False
WindX['GIF_recording_pause'] = False
WindX['GIF_recording_pause_time_start'] = 0
WindX['GIF_recording_pause_time_sec'] = 0
WindX['GIF_FPS_Str'] = 5
WindX['LastGeometry'] = []
WindX['toplevel_lines'] = []
WindX['toplevel_lines_label'] = None
WindX['display_scale'] = []
WindX['e_progressbar_on'] = 1

WindX['canny_controls_para'] = {}


WindX['DrawRectangleOnScreen'] = 0
WindX['DrawRectangleOnScreen_is2fill'] = False
WindX['DrawRectangleOnScreen_fillRect'] = []
WindX['toplevel_Rect'] = {}
WindX['mouse_left_pressed_on_screen'] = []

WindX['ShowHideMoreButtons'] = False
WindX['top_level_masks'] = []
WindX['GUI_Hide_YES']  = False
WindX['motion_on_frame2_last_time'] = 0
WindX['ShowHideBasic2_thread_timers'] = []
WindX['GUI_Hide_countdown_t'] = 0
WindX['WinCustomAdd_Class'] = None
WindX['TopCustomWind_frame_id'] = 'TopCustomWind_123456'
WindX['win_display_scale'] = 1.25

print('TESSDATA_PREFIX',os.getenv('TESSDATA_PREFIX'))

def usedTime(stime,t=0):
    if not t:
        t = time.time() - stime

    tt={'h':'00','m':'00','s':'00'}
    
    if t >= 3600:
        h = int(t/3600)
        tt['h'] = "{:0>2d}".format(h)
        t = t - h*3600
       
    if t >= 60:
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
        WindX['display_scale'].append([m.x, m.x + m.width, m.y, 1])

        if m.x == 0:
            WindX['mainPX'] = int(m.width / 2)
    
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
            if len(WindX['CatchPoint']):
                ToplevelRect(sizes=[int(WindX['CatchPoint'][0]), int(WindX['CatchPoint'][1])], xys=[int(WindX['CatchPoint'][2]), int(WindX['CatchPoint'][3])], icolor='colorful', idx='win_catch_123456')
            WindX['main'].update()

            if isEdit:     
                m = re.sub(r'^.*\[|\].*$','',WindXX['b_CatchPoint'].get())           
                sizes = []
                xys   = []
                if WindX['Displays']['Monitor'].__contains__(m):                    
                    sizes = [WindX['Displays']['Monitor'][m][0],WindX['Displays']['Monitor'][m][1]]
                    xys   = [WindX['Displays']['Monitor'][m][2],WindX['Displays']['Monitor'][m][3]]
                else:
                    sizes = [int(WindX['CatchPoint'][0]), int(WindX['CatchPoint'][1])]
                    xys   = [int(WindX['CatchPoint'][2]), int(WindX['CatchPoint'][3])]
                print("Window ["+str(m)+"]=", sizes, xys)

                TopCanvas(sizes,  #sizes [width, height]                         
                          xys,    #xys   [x0, y0]
                          im,
                          'edit',
                          iswindow=True,
                          isWinEdit=True
                        )
            else:  
                PicSave(im,err)

            t1 = threading.Timer(1, ToplevelRectHide, args=['win_catch_123456'])
            t1.start()
            #ToplevelRectHide(idx='win_catch_123456')
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

def PicSave(im=None,err=None,close_edit_win=True):
    if not im:
        return

    filep = PicSaveFile(WindX['PicFormatStr'])
    if not filep:
        return

    #Save image to file
    if WindX['CatchPrimary']:
        print ("Image: size : %s, mode: %s" % (im.size, im.mode))  
    
    if str(WindX['PicFormatStr']).upper() == 'ICO':
        tmp_file = filep + '.png'
        width = im.size[0]
        if width > im.size[1]:
            width = im.size[1]
        imc = im.crop([0, 0, width, width])
        imc.save(tmp_file)
        img = PythonMagick.Image(tmp_file)

        s = re.sub(r'[^0-9]+','', WindXX['e_ICO_Size'].get())
        if int(s) > 0:
            s = int(s)
            if int(s) > 255:
                s = 255
        else:
            s = 64
        if s > width:
            s =  width
        
        s = str(s) + 'x' + str(s)
        img.sample(s)
        filep = re.sub(r'\.ico$','',filep,re.I) + '.' + s + '.ico'
        img.write(filep)
        os.unlink(tmp_file)
    else:    
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
    if close_edit_win:
        Close_TopLevels()

def TextStringToClipboard(text=''):
    if not text:
        return
    
    try:
        win32clipboard.OpenClipboard()   #打开剪贴�?
        win32clipboard.EmptyClipboard()  #先清空剪贴板

        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)  #将text放入剪贴�?
        WindX['e_ImageCateched'].config(text="Text in Clipboard now!",fg='green')
        win32clipboard.CloseClipboard()
        StatusShow(1, auto_hide=1)
        return True
    except:
        print(traceback.format_exc())
        return False

def PicSaveToClipboard(im=None,p=None, self=None):
    if not im:
        return ""
    
    try:
        win32clipboard.OpenClipboard() #打开剪贴�?
        win32clipboard.EmptyClipboard()  #先清空剪贴板

        output=BytesIO()
        msg = ""
        if p=='base64':
            im.save(output, format='JPEG')
            byte_data = output.getvalue()
            base64_str = "data:image/jpeg;base64," + re.sub(r'^b\'|\'+$','',str(base64.b64encode(byte_data)))
            #print(base64_str)
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, base64_str)  #将base64编码放入剪贴�?
            msg = "Copied image to Clipboard as base64 HTML5 format!"
        else:            
            im.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]            
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)  #将图片放入剪贴板
            msg = "Copied image to Clipboard!"
        output.close()        
        win32clipboard.CloseClipboard()

        if self:
            self.message_show(msg= msg, bg= 'green', fg='white')
        else:
            WindX['e_ImageCateched'].config(text=msg,fg='green')
            StatusShow(1, auto_hide=1)
        return True
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

def Close_TopLevels():
    if len(WindX['Toplevels']):
        for tl in WindX['Toplevels']:
            print('close: Toplevel=',tl)
            tl.destroy()
        WindX['Toplevels'] = []

def WindExit():   
    Close_TopLevels()
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

def DrawMouseShapeArrow(x0=0, y0=0, draw=None):
    ab = 12 
    a0 = 60/180*3.1415926
    a1 = 80/180*3.1415926
    a2 = 40/180*3.1415926              

    xy = [
        x0, y0, 
        x0 + ab * math.cos(a1), y0 + ab * math.sin(a1), 
        x0 + ab * math.cos(a2), y0 + ab * math.sin(a2), 
        x0, y0
    ]

    AE = ab * math.cos(a2)
    AF = AE / math.cos(a0)
    EF = math.sqrt(AF*AF - AE*AE)
    xy2 =[
        x0, y0,
        x0 + AE, y0 + EF
    ]       
    draw.line(xy2, fill ="#909090", width = 2)
    draw.polygon(xy,fill='white',outline='#909090')  

def TextSize_Get(text,font_family,font_size):
    (x,y) = (5,5)
    pttopx = lambda x:int(x * 3 // 4)
    font_size= pttopx(font_size)
    font = tkFont.Font(family=font_family, size=font_size)
    w= font.measure(text)
    h= font.metrics("linespace")
    #print ("Font Family is %s, Font Size is %d pt" % (font_family,font_size))
    #print ("Text Width is %s px, height is %s px" % (w,h))
    return w,h

def IsTrue(obj):
    #Print2Log('', type(obj),obj)
    if(type(obj) == numpy.ndarray and obj.any()):
        return True
    elif(type(obj) == tuple and len(obj)):
        return True
    elif(type(obj) == list and len(obj)):
        return True
    elif(type(obj) == dict and len(obj.keys())):
        return True
    elif obj:
        return True    
    else: 
        return False

def Save2File(data,filepath, format='bytes'):    
    print("\t.... Save to file:",filepath)
    try:
        if os.path.exists(filepath):       
            os.unlink(filepath) 

        if format == 'bytes':    
            with open(filepath,'wb+') as f:   
                f.write(data)
        else:
            with open(filepath,'w+',encoding="utf-8") as f:  
            #important to have encoding="utf-8", to prevent Window opens the file as encoding="gbk" or else encoding then cause error.
                f.write(str(data))            
    except:
        print(sys._getframe().f_lineno, traceback.format_exc())   

def del_file(path):
    try:
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)    
        shutil.rmtree(path)                     
    except:
        pass 

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

def GIF_Add_Frame(itext,isize,fontType,fontSize,num=3, img=[]):
    images = []
    colors = []
    w, h = TextSize_Get(itext, 'Arial', fontSize)

    for i in range(num):
        colors.append((int(255 - 255/num*i), int(255 - 255/num*i), int(255 - 255/num*i)))

    for i in range(num):
        new_draw = None
        newImage = None
        if IsTrue(img):
            newImage = img
            new_draw = ImageDraw.Draw(img)
        else:
            newImage = Image.new('RGB',isize,color=(0,0,0))
            new_draw = ImageDraw.Draw(newImage)

        text = itext
        x = int(isize[0]/2 - w/2)
        if x < 10:
            x = 10
        new_draw.text((x,int(isize[1]/2 - h/2)), text, fill =colors[i], font=fontType)
        newImage = numpy.array(newImage)        # im还不是数组格式，通过此方法将img转化为数�?
        images.append(newImage)
    
    return images
    
def GIF_Make(sizes=[0, 0], xys=[0, 0], checkOnly=False):
    WindX['e_progressbar']['value'] = 0
    WindX['e_progressbar'].grid()
    StatusShow(1)
    Close_TopLevels()
    if WindX['GIF_recording'] and len(WindX['GIF_Frames']): #save GIF, reset
        WindX['GIF_recording'] = False
        DisplayRecordArea(sizes, xys, color_index=0, isClosed=True)

        tl = Toplevel()
        tl.title("Save As")
        tl.configure(bg='yellow')
        tl.wm_attributes('-topmost',1) 
        frm = Frame(tl, background='yellow')
        frm.grid(row=1,column=0,sticky=W,pady=5,padx=5)

        Label(frm, text="Catched images - total " + str(len(WindX['GIF_Frames'])) + " frames", bg='yellow',
                justify=LEFT, anchor='w', relief=FLAT,pady=3,padx=3).grid(row=0,column=1,sticky=W,columnspan=10,pady=3,padx=3)

        iButton(frm,1,1,lambda:GIF_Make2File("GIF", tl),'Save as GIF','blue',msg='Save as a GIF file',p=[LEFT,FLAT,5,5,'#FFFF66','#FFFF99',10,E+W+N+S,1,1])
        iButton(frm,1,2,lambda:GIF_Make2File("Video", tl),'Save as Video','blue',msg='Save as a video file',p=[LEFT,FLAT,5,5,'#FFFF66','#FFFF99',10,E+W+N+S,1,1])
        iButton(frm,1,3,lambda:GIF_Make2File("Cancel", tl),'Cancel','blue',msg='Not save to file',p=[LEFT,FLAT,5,5,'#FFFF66','#FFFF99',10,E+W+N+S,1,1])

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

def GIF_Make2File(todo="", tl=None):
    tl.destroy()

    if todo=="GIF" or todo == "Video":        
        StatusShow(1)
        time.sleep(2/int(WindX['GIF_FPS_Str']))
        nn = len(WindX['GIF_Frames'])
        if nn:
            #save images to a tmp folder                
            total_sec = WindX['GIF_Frames'][nn-1][4] - WindX['GIF_Frames'][0][4] - WindX['GIF_recording_pause_time_sec']
            fps1 = int(10 / (total_sec/nn))/10
            print("\nreal fps=", fps1, ", set fps=",int(WindX['GIF_FPS_Str']), ", pause time (sec)",int(WindX['GIF_recording_pause_time_sec']))
            n = 0
            strTime = str(time.time())
            gif_tmp_folder = WindX['Save2Folder'] + "/ScreenCatch/tmp" + strTime
            CreateFolder(gif_tmp_folder)
            WindX['e_ImageCateched'].config(text="saving images ("+str(nn)+") to /ScreenCatch/tmp" + strTime,fg='#009900')
            WindX['main'].update()
            gif_info={
                'slides':[],
                'recording_pause': WindX['GIF_recording_pause_time_sec']
            }
            for imp in WindX['GIF_Frames']:
                n +=1
                try:
                    outfile = gif_tmp_folder + '/gif_slide_{:>04d}'.format(n) +'.PNG'
                    imp[0].save(outfile)
                    gif_info['slides'].append([
                        n,
                        imp[1],
                        imp[2],
                        imp[3],
                        imp[4]
                    ])
                except:
                    print(traceback.format_exc())
            Save2File(json.dumps(gif_info), gif_tmp_folder + '/gif_info.json', 'string')

            #Processing images for gif file
            iformat = "gif"
            if todo == "Video": 
                iformat = "avi"

            filep = PicSaveFile(iformat,"." + str(nn))
            if not filep:
                filep = PicSaveFile(iformat)

            if filep:
                try:
                    StatusShow(1)
                    print("processing images ("+str(nn)+") for "+iformat+" file ... ...")
                    WindX['e_ImageCateched'].config(text="processing images ("+str(nn)+") for "+iformat+" file ... ...",fg='#009900')
                    WindX['main'].update()

                    images = []
                    n = 0 
                    font_end = None 
                    font_type = None    
                    try:
                        font_end  = ImageFont.truetype(font='C:/Windows/Fonts/Arial.ttf',size=80) 
                        font_type = ImageFont.truetype(font='C:/Windows/Fonts/Arial.ttf',size=12)
                    except:
                        print(traceback.format_exc())

                    last_imp = None
                    for imp in WindX['GIF_Frames']:
                        n +=1
                        last_imp = imp
                        WindX['e_progressbar']['value'] = int(n/nn*100)
                        WindX['main'].update()

                        #draw = ImageDraw.Draw(imp[0])
                        isize = imp[0].size

                        imc = imp[0].crop((0,0,isize[0],20))
                        bgColorX = Image_getBGColor(numpy.array((imc.copy()).convert("RGB")))
                        bgColor   = (bgColorX[0], bgColorX[1], bgColorX[2])
                        foreColor = (255-bgColor[0], 255 - bgColor[1], 255 - bgColor[2])
                        #doneColor = (int((bgColor[0] + foreColor[0])/2) % 255, int((bgColor[1] + foreColor[1])/2) % 255, int((bgColor[2] + foreColor[2])/2) % 255)
                        doneWidth = int(isize[0] * n/nn)
                        #draw.rectangle((0,0,isize[0],15), fill  = bgColor)
                        #draw.rectangle((0,0,doneWidth,15), fill = doneColor)

                        bg_img = (imp[0].copy()).convert('RGBA')  #change to 'RGBA' format
                        transp1 = Image.new('RGBA', isize, (0,0,0,0))  # create a new image, blank and transparent as Alpha=0
                        draw1 = ImageDraw.Draw(transp1, "RGBA")  #draw the blank and transparent image 
                        draw1.rectangle((0,0,isize[0],15), fill=(bgColorX[0], bgColorX[1], bgColorX[2], int(255*0.5)))
                        bg_img.paste(Image.alpha_composite(bg_img, transp1)) #combine the images                           

                        transp2 = Image.new('RGBA', isize, (0,0,0,0))
                        draw2 = ImageDraw.Draw(transp2, "RGBA")
                        draw2.rectangle((0,0,doneWidth,15), fill=(0,255,0,int(255*0.7)))
                        bg_img.paste(Image.alpha_composite(bg_img, transp2))
                        
                        imp[0] = bg_img
                        draw = ImageDraw.Draw(imp[0])
                        draw.text((1,0), time.strftime("%Y-%m-%d %H:%M:%S %z",time.localtime(imp[4])) + "  " + re.sub(r'^00\:',"",imp[1]) + " / " + re.sub(r'^00\:',"",WindX['GIF_Frames'][nn-1][1]) + " #" + str(n) + "/" + str(nn), 
                                        fill = foreColor, font=font_type)                                            
                        draw.rectangle((0,0,isize[0]-1,isize[1]-1), fill=None, outline=(224,224,224,int(255*0.8)))
                        #imp[0].show()
                        '''
                        if n==1:                            
                            for j in range(3):
                                newImages = GIF_Add_Frame('START ' + str(3 - j), isize, font_end, 80, 3, imp[0])
                                images.extend(newImages)
                        '''

                        if len(imp[2]): #mouse-click point
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
                                DrawMouseShapeArrow(x0=p[0], y0=p[1], draw=draw)

                        if len(imp[3]): #mouse-move traces
                            dx = 1            
                            for p in imp[3]:
                                #xy = [p[0]-dx, p[1]-dx, p[0]+dx, p[1]+dx]
                                #draw.ellipse(xy,fill=None,outline='red',width=1)
                                DrawMouseShapeArrow(x0=p[0], y0=p[1], draw=draw) 

                        img = imp[0].convert("RGB")   # 通过convert将RGBA格式转化为RGB格式，以便后续处�?
                        #print("img.size=",img.size)
                        img = numpy.array(img)        # im还不是数组格式，通过此方法将img转化为数�?
                        images.append(img) 

                    for j in range(3):
                        newImages = GIF_Add_Frame('END', isize, font_end, 80, 3, last_imp[0])
                        images.extend(newImages)

                    WindX['e_ImageCateched'].config(text="saving: " + os.path.basename(filep) + " ... ...",fg='#009900')
                    WindX['main'].update()
                    StatusShow(1)

                    if todo=="GIF":
                        imageio.mimsave(filep, images, 'GIF', duration= 2/fps1) #2/int(WindX['GIF_FPS_Str'])
                        #verify image file
                        if os.path.exists(filep):
                            print("optimize: ", filep)
                            WindX['e_ImageCateched'].config(text="optimizing: " + os.path.basename(filep) + " ... ...",fg='#009900')
                            WindX['main'].update()                    
                            GIF_File_Optimize(filep)

                            if os.path.exists(filep + ".o.gif"):
                                os.unlink(filep)
                                WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep + ".o.gif"),fg='#009900')
                                del_file(gif_tmp_folder)
                            else:
                                WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep),fg='#009900')                    
                        else:
                            WindX['e_ImageCateched'].config(text="Failed to save!",fg='red')
                            WindX['ImageOrderLastSub'] -=1

                    elif todo == "Video":
                        image_clips = []
                        for i in range(len(images)):
                            image_clips.append(ImageClip(images[i], duration= 2/fps1))

                        video = concatenate_videoclips(image_clips) 
                        video.write_videofile(filep, codec="png", fps=fps1*2, threads=4, audio=False)
                        video.close()
                        """
                        "mpeg4 .avi (1608x794 ~0.12MB/second)",
                        "mpeg4 .mp4 (1608x794 ~0.12MB/second)", 
                        #"libvorbis .ogv",
                        "libvpx .webm (1608x794 ~0.025MB/second)",   
                        "png .avi (perfect quality, midium size, 1608x794~2MB/second)",
                        "rawvideo .avi (high quality huge size, 1608x794~130MB/second)"
                        """
                        if os.path.exists(filep):
                            WindX['e_ImageCateched'].config(text= "Saved: " + os.path.basename(filep),fg='#009900') 
                            del_file(gif_tmp_folder)
                        else:
                            WindX['e_ImageCateched'].config(text="Failed to save!",fg='red')
                            WindX['ImageOrderLastSub'] -=1
                except:
                    print(traceback.format_exc())

    else:
        StatusShow(1)
        WindX['e_ImageCateched'].config(text="Not save the GIF!",fg='#009900')
        WindX['main'].update()

    WindX['GIF_Frames'] = []       
    WindX['e_snip_gif'].config(fg='red')
    #StatusHide_Delay()
    t1 = threading.Timer(1, StatusHide_Delay)
    t1.start()
    return 1

def GIF_Make_GO(sizes=[0, 0], xys=[0, 0]):
    WindX['GIF_recording_pause_time_start'] = 0
    WindX['GIF_recording_pause_time_sec'] = 0

    if not sizes[0]:
        print("GIF_Make_GO: sizes is invalid!", sizes)
        return

    WindX['GIF_FPS_Str'] = re.sub(r'.*[^0-9]+','',WindXX['e_GIF_FPS'].get())
    if not WindX['GIF_FPS_Str']:
        WindX['GIF_FPS_Str'] = 5
    WindX['e_GIF_FPS'].delete(0,END)
    WindX['e_GIF_FPS'].insert(0,str(WindX['GIF_FPS_Str']))

    stime = time.time()
    penColors = GetColors(istart=16711680, n=100) #["red","blue","green"]
    color_index = 0
    n = 0
    fps = int(WindX['GIF_FPS_Str'])
    tfps = 1 / 1/fps

    WindX['mouse_click_points'] = []
    WindX['mouse_move_points']  = []

    lastMPS = []
    lastusedtime = ''
    DisplayRecordArea(sizes, xys, color_index=0, isClosed=True)
    while WindX['GIF_recording']:
        if WindX['GIF_recording_pause']:
            while WindX['GIF_recording_pause']:
                try:
                    WindX['e_ImageCateched'].config(text="Pause ... @ " + lastusedtime + " (" + str(len(WindX['GIF_Frames'])) + "), click [GIF] to stop", fg=penColors[color_index])
                    WindX['toplevel_lines_label'].config(text="Pause ... @ " + lastusedtime + " (" + str(len(WindX['GIF_Frames'])) + ")", fg=penColors[color_index])
                    WindX['toplevel_button_pause'].config(fg=penColors[color_index])
                    WindX['main'].update()
                except:
                    pass
                
                time.sleep(tfps)
                color_index +=1
                if color_index > len(penColors)-1:
                    color_index = 0  
        
        if n==0 or n%fps==0:
            DisplayRecordArea(sizes, xys, color_index)
            try:
                WindX['e_snip_gif'].config(fg= penColors[color_index])  
                lastusedtime = usedTime(stime)     
                WindX['e_ImageCateched'].config(text="recording GIF " + usedTime(stime) + " (" + str(len(WindX['GIF_Frames'])) + "), click [GIF] to stop", fg=penColors[color_index])
                WindX['toplevel_lines_label'].config(text="recording GIF " + usedTime(stime) + " (" + str(len(WindX['GIF_Frames'])) + ")", fg=penColors[color_index])
                for tl in WindX['toplevel_lines']:
                    tl[1].config(bg=penColors[color_index])
            except:
                pass

            WindX['toplevel_progressbar']['value'] += fps
            if WindX['toplevel_progressbar']['value'] > 100:
                WindX['toplevel_progressbar']['value'] = 0

            WindX['e_progressbar']['value'] += fps
            if WindX['e_progressbar']['value'] > 100:
                WindX['e_progressbar']['value'] = 0

            WindX['main'].update()
            lastMPS = []
            StatusShow(1)

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

            WindX['GIF_Frames'].append([im, usedTime(stime), mps, mps_move, time.time()])   
        
        WindX['mouse_click_points'] = []
        WindX['mouse_move_points']  = []

        color_index +=1
        if color_index > len(penColors)-1:
            color_index = 0    
        time.sleep(tfps)
        n +=1

def GIF_Make_Pause():
    if WindX['GIF_recording_pause']:
        WindX['GIF_recording_pause'] = False
        WindX['toplevel_button_pause'].config(fg='red', text='Pause')
        if WindX['GIF_recording_pause_time_start']:
            WindX['GIF_recording_pause_time_sec'] += time.time() - WindX['GIF_recording_pause_time_start']
        WindX['GIF_recording_pause_time_start'] = 0
    else:
        WindX['GIF_recording_pause'] = True
        WindX['toplevel_button_pause'].config(fg='red', text='Continue')
        WindX['GIF_recording_pause_time_start'] = time.time()

def GIF_Make_Stop():
    WindX['GIF_recording_pause'] = False
    SetWindow("snip_gif")
    if WindX['GIF_recording_pause_time_start']:
        WindX['GIF_recording_pause_time_sec'] += time.time() - WindX['GIF_recording_pause_time_start']
    WindX['GIF_recording_pause_time_start'] = 0

def ToplevelLine(x,y,width,height,color,notAppend=False):
    tl = Toplevel()
    tl.wm_attributes('-topmost',1) 
    canvas = Canvas(tl,
            width = width,
            height= height,
            bg= color,
            relief=FLAT,
            bd = 0,
            )
    canvas.configure(highlightthickness = 0)
    canvas.pack()

    tl.geometry('+'+ str(x) +'+' + str(y))
    tl.overrideredirect(1)

    if notAppend:
        return [tl,canvas]
    else:
        WindX['toplevel_lines'].append([tl,canvas])

def DisplayRecordArea(sizes, xys, color_index=0, isClosed=False):
    try:
        if isClosed:
            if len(WindX['toplevel_lines']):
                for tl in WindX['toplevel_lines']:
                    try:
                        tl[0].destroy()
                    except:
                        pass
            WindX['toplevel_lines'] = []
            WindX['toplevel_lines_label'] = None
            return

        penColors = ["red","blue","green"]

        if len(WindX['toplevel_lines']):
            for tl in WindX['toplevel_lines']:
                try:
                    tl[1].configure(bg = penColors[color_index])
                except:
                    pass

            return

        x1 = xys[0] - 1 
        y1 = xys[1] - 1
        x2 = xys[0] + sizes[0] + 1
        y2 = xys[1] + sizes[1] + 1

        try:
            ToplevelLine(x1,y1,sizes[0]+2,1,penColors[color_index])
            ToplevelLine(x1,y2,sizes[0]+2,1,penColors[color_index])

            ToplevelLine(x1,y1,1,sizes[1]+2,penColors[color_index])
            ToplevelLine(x2,y1,1,sizes[1]+2,penColors[color_index])

            tl = Toplevel()
            tl.wm_attributes('-topmost',1) 
            frm = Frame(tl)
            frm.grid(row=1,column=0,sticky=W,pady=0,padx=0)

            iButton(frm,0,1,GIF_Make_Stop,'Stop','red',msg='Stop to record GIF',p=[LEFT,FLAT,3,3,'#FFFF66','#FFFF99',10,E+W+N+S,1,1])
            b = iButton(frm,0,2,GIF_Make_Pause,'Pause','red',msg='Pause and wait',p=[LEFT,FLAT,3,3,'#FFFF66','#FFFF99',10,E+W+N+S,1,1])
            WindX['toplevel_button_pause'] = b.b 

            label = Label(frm, text='', justify=LEFT, relief=FLAT,pady=3, padx=3, fg='green')
            label.grid(row=0, column=3, sticky=W+N+S,pady=1,padx=1)            

            e = ttk.Progressbar(frm, orient=HORIZONTAL, length=300, mode='indeterminate',value=0,maximum=100)
            e.grid(row=0,column=4,sticky=E+W+N+S,pady=0,padx=0)
            WindX['toplevel_progressbar'] = e
            WindX['toplevel_progressbar']['value'] = 0            

            tl.geometry('+'+ str(x1) +'+' + str(y2))
            tl.overrideredirect(1)

            WindX['toplevel_lines'].append([tl,frm])
            WindX['toplevel_lines_label'] = label

        except:
            print(traceback.format_exc())
    except:
        print(traceback.format_exc())


WindX['ClassSnapshotMaskFullscreen'] = None
def SetWindowCallbackAtEndSnapshotMask(todo=None):
    try:
        if WindX['ClassSnapshotMaskFullscreen']:
            print("\n",todo, WindX['ClassSnapshotMaskFullscreen'].mouse_selected_box)
            box = WindX['ClassSnapshotMaskFullscreen'].mouse_selected_box
            dx  = abs(box[2] - box[0])
            dy  = abs(box[3] - box[1])
            if dx and dy:
                SetWindow(todo=todo, box=box)
        WindX['ClassSnapshotMaskFullscreen'] = None
    except:
        print(traceback.format_exc())

def SetWindow(todo=None, action_tag='', box=[]): 
    if todo == "snip_gif":
        if GIF_Make(checkOnly=True):            
            return

    DelayCheck()
    WindX['e_ImageCateched'].config(text="")        
    WindX['main'].update()
       
    try:
        if todo == 'snip_edit':
            if not len(box):
                print("\nSnapshotMaskFullscreen ...")  
                WindX['ClassSnapshotMaskFullscreen'] = UI_ClassSnapshotMaskFullscreen(CallbackAtEnd=lambda:SetWindowCallbackAtEndSnapshotMask('snip_edit'))
            else:
                StatusShow(1, auto_hide=1)
                ShowMainWindow(0)   
                dx  = int(abs(box[2] - box[0]))
                dy  = int(abs(box[3] - box[1]))
                im,err = ScreenShotXY(width =dx,
                                      height=dy,
                                      xSrc  =box[0],
                                      ySrc  =box[1])
                ShowMainWindow(1)
                if isinstance(im, Image.Image):
                    print ("Snapshot: size : %s, mode: %s" % (im.size, im.mode),"\n", box)                       
                    TopCanvas(
                        [dx, dy],
                        [box[0], box[1]],
                        im,
                        todo = 'edit',
                        titleOn = True
                    )                    
                else:
                    print("Failed to get screenshot!")
                    WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')
        else:
            if todo == "snip_edit2":
                todo = 'snip_edit'

            StatusShow(1, auto_hide=1)
            ShowMainWindow(0)   
            im,err = ScreenShotXY(width =int(WindX['Displays']['FullScreenSize'][0]),
                                height=int(WindX['Displays']['FullScreenSize'][1]),
                                xSrc  =int(WindX['Displays']['FullScreenSize'][2]),
                                ySrc  =int(WindX['Displays']['FullScreenSize'][3]))
            ShowMainWindow(1)
            if isinstance(im, Image.Image):
                print ("Full Screen: size : %s, mode: %s" % (im.size, im.mode),"\n", WindX['Displays'])                       
                TopCanvas(
                    [WindX['Displays']['FullScreenSize'][0], 
                    WindX['Displays']['FullScreenSize'][1]],
                    [int(WindX['Displays']['FullScreenSize'][2]), 
                    int(WindX['Displays']['FullScreenSize'][3])],
                    im,
                    todo,
                    iswindow=True,
                    is_snip=True,
                    action_tag= action_tag
                )                    
            else:
                print("Failed to get screenshot!")
                WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')

    except:
        print(traceback.format_exc())
 
def CreateFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        if not os.path.exists(folder):
            print(sys._getframe().f_lineno, "Can not create the folder:\n\t" + folder)
            return False
    return True
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
        #创建设备描述�?
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        #创建内存设备描述�?
        saveDC = mfcDC.CreateCompatibleDC()
        #创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        #为bitmap开辟存储空�?
        #print(width,height,xSrc,ySrc,';',hWndDC,';',mfcDC) #-1920 1080 1920 1080 ; 889263399 ; object 'PyCDC' - assoc is 000001F1B3EC5998, vi=<None>
        saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
        #将截图保存到saveBitMap�?
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

def isRectanglesInterSection(boxa, boxb, display=False, displayOnScreen=False):
    isInteract = True
    try:
        min_x = max(boxa[0], boxb[0])
        min_y = max(boxa[1], boxb[1])
        max_x = min(boxa[2], boxb[2])
        max_y = min(boxa[3], boxb[3])

        if min_x >= max_x or min_y >= max_y:
            isInteract = False
        if display:
            print('', "\n---- Is interacted: ", isInteract, boxa, boxb)
    except:
        pass

    #'''
    if displayOnScreen:
        minx = min(boxa[0], boxb[0])
        miny = min(boxa[1], boxb[1])
        maxx = max(boxa[2], boxb[2])
        maxy = max(boxa[3], boxb[3])

        tl = Toplevel()
        canvas=Canvas(tl,
            width = maxx - minx  + 100,
            height= maxy - miny  + 100,
            bg="white",
            relief=FLAT,
            bd = 0,
            )
        canvas.pack(side=TOP, fill=BOTH, expand=1)

        rect = canvas.create_rectangle(
            boxa[0] - minx + 20,
            boxa[1] - miny + 20,
            boxa[2] - minx + 20,
            boxa[3] - miny + 20,
            outline = 'red',
            width= 1
            )

        rect2 = canvas.create_rectangle(
            boxb[0] - minx + 20,
            boxb[1] - miny + 20,
            boxb[2] - minx + 20,
            boxb[3] - miny + 20,
            outline = 'blue',
            width= 1,
        )      

        canvas.create_text(
            10,
            10,
            font = ('Arial', 10, 'normal'),
            text = str(isInteract),
            fill = 'black',
            anchor = W,
            justify = LEFT) 
    #'''
    return isInteract

def Image_IsBlank(im_arr, wherfrom):
    #check if the image is blank
    try:
        a1 = im_arr[0][0]  #get the first point color
        aa = numpy.ones((im_arr.shape[0], im_arr.shape[1], 3), dtype=numpy.int16)  #create an image array
        aa[:,:,[0]] = a1[0]      #fill up the new image array with the first point color                 
        aa[:,:,[1]] = a1[1]                       
        aa[:,:,[2]] = a1[2]     
        return (im_arr == aa).all()  #compare the image arrays
    except:
        print('\033[0;31;40m-!!-\033[0m',end="")  #31 - red color
        #print("\nImage_IsBlank, from=",wherfrom)
        #print(traceback.format_exc())
        return False

def Image_IsOneLine(arr, minNonZero=5, getNonzeroIndex=False):
    icount = False
    result = {
        'unique': None,
        'inverse': None,
        'counts' : None,
        'nonzero':None
    }    
    try:
        unique,inverse,counts=numpy.unique(arr,axis=0,return_inverse=True,return_counts=True)
        result= [unique,inverse,counts]
        result = {
            'unique': unique,
            'inverse': inverse,
            'counts' : counts,
            'nonzero':None
        }
        
        if getNonzeroIndex or len(counts) <= 5:
            #print("\tY:", y, ", unique=", unique.tolist(),', counts=',counts,', inverse=', inverse)
            #How many times the values change in the series of [inverse]?
            a = numpy.array(inverse[1:len(inverse)])
            b = numpy.array(inverse[0:len(inverse)-1])                        
            nz_indexs = numpy.nonzero(a - b)
            
            #print("\tY: nz_indexs=",nz_indexs)

            #print("\tY:", y, ", unique=", unique.tolist(),', counts=',counts, ", nz_indexs=",nz_indexs, type(nz_indexs), len(nz_indexs[0]))
            
            zn = 0
            if type(nz_indexs) == tuple:
                zn = len(nz_indexs[0])             
                result['nonzero'] = nz_indexs[0]
                #print("type(result['nonzero'])=", type(result['nonzero']))
            else:
                zn = len(nz_indexs)
                result['nonzero'] = nz_indexs

            if zn <= minNonZero:                        
                icount = True
    except:
        print(traceback.format_exc())

    return icount, result

def Image_getBGColor(im_arr_temp):
    #get background color of the image
    
    im_arr_temp_1 = im_arr_temp.reshape(-1,3)
    #print("\nim_arr_temp.reshape(-1,3)=",im_arr_temp_1.shape,im_arr_temp_1)
    unique,counts=numpy.unique(im_arr_temp_1, axis=0,return_counts=True)
    bgColor = list(unique[numpy.argmax(counts)])
    #print("unique=",unique)
    #print("counts=",counts)
    #print("background color=",bgColor,"\n")        
    #im_arr_temp[:,:,0], im_arr_temp[:,:,1], im_arr_temp[:,:,2] = bgColor
    #im_arr_temp = Image.fromarray(im_arr_temp)
    #im_arr_temp.show()    
    return bgColor

import cv2
def Image_FindContours(img, dx=1, dy=1, is2mergeBoxs=False):
    try:
        o_frame = cv2.cvtColor(numpy.array(img.copy()), cv2.COLOR_RGB2BGR)
        o_frame2= cv2.cvtColor(numpy.array(img.copy()), cv2.COLOR_RGB2BGR)

        frame = cv2.cvtColor(numpy.array(img.copy()), cv2.COLOR_RGB2GRAY)
        gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        can_frame= cv2.Canny(gs_frame, 5, 200)
        #cv2.imshow("can_frame", can_frame)
        countours, hierarchy = cv2.findContours(can_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        boxs= []
        for cnt in countours:
            area = cv2.contourArea(cnt)
            if area > 0:
                #cv2.drawContours(o_frame, cnt, -1, (255,0,0),3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                #objCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)                
                box = [x-dx, y-dy, x+w + dx, y+h+dy]
                if box[0] < 0:
                    box[0] = 0
                if box[1] < 0:
                    box[1] = 0
                #print(box)

                isNotGet = True                
                if is2mergeBoxs and len(boxs):                    
                    for i in range(len(boxs)):
                        if isRectanglesInterSection(boxs[i], box):                            
                            isNotGet = False
                            min_x = min(boxs[i][0], boxs[i][2], box[0], box[2])
                            min_y = min(boxs[i][1], boxs[i][3], box[1], box[3])
                            max_x = max(boxs[i][0], boxs[i][2], box[0], box[2])
                            max_y = max(boxs[i][1], boxs[i][3], box[1], box[3])
                            boxs[i] = [min_x, min_y, max_x, max_y]
                            #print(".... merged:", box)
                if isNotGet:
                    boxs.append(box) 

        #for b in boxs:
        #    cv2.rectangle(o_frame, (b[0], b[1]), (b[2], b[3]), (0,255,0), 1)
        #cv2.imshow("Contours before merge",o_frame)
        #print(boxs)

        if is2mergeBoxs:
            #merge intersection boxs              
            for xx in range(3):
                boxs_new = []  
                box_merged = {}          
                for i in range(len(boxs)):
                    if box_merged.__contains__(i):
                        print(".... merged:", i)
                        continue
                    
                    for j in range(i+1, len(boxs)):
                        if box_merged.__contains__(j):
                            continue

                        box = boxs[j]
                        if isRectanglesInterSection(boxs[i], box):                            
                            box_merged[j] = 1
                            min_x = min(boxs[i][0], boxs[i][2], box[0], box[2])
                            min_y = min(boxs[i][1], boxs[i][3], box[1], box[3])
                            max_x = max(boxs[i][0], boxs[i][2], box[0], box[2])
                            max_y = max(boxs[i][1], boxs[i][3], box[1], box[3])
                            boxs[i] = [min_x, min_y, max_x, max_y]

                    boxs_new.append(boxs[i])
                boxs = boxs_new.copy()
          
        for b in boxs:
            cv2.rectangle(o_frame2, (b[0], b[1]), (b[2], b[3]), (0,255,0), 1)

        im_arr_temp1 = Image.fromarray(cv2.cvtColor(o_frame2, cv2.COLOR_BGR2RGB))
        im_arr_temp1.show()
        #cv2.imshow("Contours after merge",o_frame2)
        #cv2.waitKey(0)

        return boxs
    except:
        print(traceback.format_exc())

def Image_FindContours_colorObject(img):
    #refer to https://blog.csdn.net/See_Star/article/details/103044722?spm=1001.2101.3001.6650.6&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-6.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-6.pc_relevant_antiscanv2&utm_relevant_index=13
    ball_color = 'green' #如果只是想识别绿色，那这一段就显得多余了。但是如果你想识别红色或是蓝色，可以直接将ball_color = 'green'改成ball_color = 'red'或是ball_color = 'blue'
    color_dist ={
                'red'  :{'Lower':numpy.array([0,60,60]   ), 'Upper':numpy.array([6,  255,255])},
                'blue' :{'Lower':numpy.array([100,80,461]), 'Upper':numpy.array([124,255,255])},
                'green':{'Lower':numpy.array([35,43,35]  ), 'Upper':numpy.array([90,255,255] )}
                }

    try:
        frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
        gs_frame = cv2.GaussianBlur(frame, (5, 5), 0) #将原图像进行模糊处理，方便颜色的提取, frame需要高斯模糊的图像, (5, 5)高斯矩阵的长与宽都是5, 0标准差是0
        cv2.imshow("gs_frame",gs_frame)

        hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV) #刚刚高斯模糊后的图像的颜色模式从BGR转换为HSV
        cv2.imshow("hsv",hsv)

        erode_hsv = cv2.erode(hsv, None, iterations=2) #就是将图像变瘦，用于去除噪声点。hsv原图像, iterations=2腐蚀的宽度
        cv2.imshow("erode_hsv",erode_hsv)

        inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper']) #将绿色以外的其他部分去除掉，并将图像转化为二值化图像
        cv2.imshow("inRange_hsv",inRange_hsv)

        cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #使用该函数找出方框外边界，并存储在cnts中
        if IsTrue(cnts):
            c = max(cnts, key=cv2.contourArea) #在边界中找出面积最大的区域
            rect = cv2.minAreaRect(c) #绘制出该区域的最小外接矩形
            box = cv2.boxPoints(rect) #记录该矩形四个点的位置坐标
            cv2.drawContours(frame, [numpy.int0(box)], -1, (0, 255, 255), 2) #在原图像上将分析出的矩形边界绘制出来
        cv2.imshow("Contour",frame)
        cv2.waitKey(0)
    except:
        print(traceback.format_exc())


def Image_cleanUp(img, stime = time.time()): 
    '''
    A = numpy.array((img.copy()).convert("L"))
    print(A)
    B = A[1:A.shape[0],1:A.shape[1]]
    C = A[0:A.shape[0] - 1,0:A.shape[1] - 1]
    
    df = pandas.DataFrame(A)
    print(df)
    print(df.nunique(), "\n")

    dfT = df.T
    print(dfT)
    print(dfT.nunique(), "\n")

    D = B - C
    print(D, "\n")
    dfD = pandas.DataFrame(D)
    print(dfD.astype(bool).sum(axis=1), "\n")
    return []
    '''
    
    #get background color of the image
    bgColor = Image_getBGColor(numpy.array((img.copy()).convert("RGB")))
    Lcolor = int(bgColor[0] * 299/1000 + bgColor[1] * 587/1000 + bgColor[2] * 114/1000)
    print("background color=",bgColor, Lcolor,"\n") 
    #bgColor = Lcolor

    #statistic color of the image
    im_arr_temp1 = numpy.array((img.copy()).convert("RGB"))
    print("im_arr_temp1 (height, width, channels)=",im_arr_temp1.shape)
    #im_arr_temp1[int(im_arr_temp1.shape[0]/2),:] = [0,0,0]
    #im_arr_temp1[:,int(im_arr_temp1.shape[1]/2)] = [0,0,0]
    print(sys._getframe().f_lineno, ".... Image Clean to get background color, used time", usedTime(stime))
    #return

    #clean in frist round: erase the line whose width/height is not least than value of [step] 
    clean_fillColor = bgColor
    cleanBox = []
    step  = 10
    for shape_i in [0,1,1]:
        for row in range(im_arr_temp1.shape[shape_i]):
            arr = []
            try:
                if shape_i == 0:
                    arr = im_arr_temp1[row]
                else:
                    arr = im_arr_temp1[:,row]
            except:
                print("im_arr_temp1[?], row=", row,"\n")
                print(traceback.format_exc())   
            
            IsOneLine, result = Image_IsOneLine(arr, minNonZero=0, getNonzeroIndex=True)

            if IsOneLine:
                #one color in one line, no text, can be erased
                if shape_i == 0:
                    im_arr_temp1[row,:] = clean_fillColor
                    cleanBox.append(['row', row, 0, im_arr_temp1.shape[1]])
                else:
                    im_arr_temp1[:, row] = clean_fillColor
                    cleanBox.append(['col', row, 0, im_arr_temp1.shape[0]])
                continue

            start_i = 0
            next_i  = 1
            try:
                nz_indexs = result['nonzero']
                inverse   = result['inverse']

                nz_indexs_copy = nz_indexs.copy()
                if nz_indexs_copy[0] !=0:
                    nz_indexs_copy = [0] + nz_indexs_copy
                if nz_indexs_copy[len(nz_indexs_copy) - 1] != len(inverse) - 2:
                    nz_indexs_copy = nz_indexs_copy + [len(inverse)]

                index1 = nz_indexs_copy[start_i]
                index2 = nz_indexs_copy[next_i]

                #print(nz_indexs)
                #print(nz_indexs_copy)  
                # erase the line whose width/height is not least than value of [step]              
                while True:        
                    if index2 - index1 + 1 >= step:
                        ss = index1
                        ee = index2 + 1                            

                        if ss > 0:
                            ss = index1 + 2
                        if ee < len(inverse) - 2:
                            ee = index2 - 1                       

                        if shape_i == 0:
                            im_arr_temp1[row, ss: ee] = clean_fillColor
                            cleanBox.append(['row',row, ss, ee])
                        else:
                            im_arr_temp1[ss:ee, row] = clean_fillColor
                            cleanBox.append(['col',row, ss, ee])

                    start_i += 1
                    next_i  += 1

                    if start_i >= len(nz_indexs_copy) - 1 or next_i >= len(nz_indexs_copy):
                        break

                    index1 = nz_indexs_copy[start_i]
                    index2 = nz_indexs_copy[next_i]
            except:
                print("\nresult.inverse=", result['inverse'],"\n")
                print("result.nonzero=",   result['nonzero'],"\n")
                print(traceback.format_exc())

    im_arr_temp1 = Image.fromarray(im_arr_temp1)
    #im_arr_temp1.show()
    print(sys._getframe().f_lineno, ".... Image Clean in first round, used time", usedTime(stime))

    do_again = False
    if do_again:
        #clean up again, repeat those in the first round, but ignore where is in the countours boxes.
        boxs = []
        #boxs = Image_FindContours(img.copy())

        if len(boxs):
            im_arr_temp1 = numpy.array(img.copy())
            print("im_arr_temp1 again (height, width, channels)=",im_arr_temp1.shape)
            xboxs = {}
            hasxx = 0
            for i in range(len(cleanBox)):
                s = cleanBox[i]
                id= s[0] + '-' + str(s[1]) + '-' + str(s[2]) + '-' + str(s[3])

                if not xboxs.__contains__(id):
                    xboxs[id] = []
                
                    xbox = []
                    for boxa in boxs:
                        isInterSection = False
                        if s[0] == 'row':  #row Y is constant              
                            if (s[1] >= boxa[1] and s[1] <= boxa[3]) and (not (s[3] < boxa[0] or s[2] > boxa[2])):
                                isInterSection = True

                        else: #col X is constant
                            if (s[1] >= boxa[0] and s[1] <= boxa[2]) and (not (s[3] < boxa[1] or s[2] > boxa[3])):
                                isInterSection = True
                    
                        if isInterSection:
                            if len(xbox):
                                min_x = min(xbox[0], xbox[2], boxa[0], boxa[2])
                                min_y = min(xbox[1], xbox[3], boxa[1], boxa[3])
                                max_x = max(xbox[0], xbox[2], boxa[0], boxa[2])
                                max_y = max(xbox[1], xbox[3], boxa[1], boxa[3])
                                xbox = [min_x, min_y, max_x, max_y]
                            else:
                                xbox = boxa
                            hasxx += 1

                    if len(xbox):
                        if s[0] == 'row':  #row Y is constant  
                            if s[2] >= xbox[0] and s[2] <= xbox[2] and s[3] >= xbox[2]:
                                xboxs[id].append([s[1], xbox[2], s[3]])
                            elif s[2] <= xbox[0] and s[3] >= xbox[2]:
                                xboxs[id].append([s[1], s[2], xbox[0]])
                                xboxs[id].append([s[1], xbox[2], s[3]])
                            elif s[2] <= xbox[0] and s[3] <= xbox[2] and s[3] >= xbox[0]:
                                xboxs[id].append([s[1], xbox[2], xbox[0]])
                            
                        else: #col X is constant
                            if s[2] >= xbox[1] and s[2] <= xbox[3] and s[3] >= xbox[3]:
                                xboxs[id].append([s[1], xbox[3], s[3]])
                            elif s[2] <= xbox[1] and s[3] >= xbox[3]:
                                xboxs[id].append([s[1], s[2], xbox[1]])
                                xboxs[id].append([s[1], xbox[3], s[3]])
                            elif s[2] <= xbox[1] and s[3] <= xbox[3] and s[3] >= xbox[1]:
                                xboxs[id].append([s[1], xbox[3], xbox[1]])
                    else:
                        xboxs[id].append([s[1], s[2], s[3]])

                for xs in xboxs[id]:
                    if s[0] == 'row':  #row Y is constant  
                        im_arr_temp1[xs[0], xs[1]: xs[2]] = clean_fillColor
                    else: #col X is constant            
                        im_arr_temp1[xs[1]: xs[2], xs[0]] = clean_fillColor

            print("\n.... hasxx=",hasxx)
            im_arr_temp1 = Image.fromarray(im_arr_temp1)
            print(sys._getframe().f_lineno, ".... Image Clean in second round, used time", usedTime(stime))

    #im_arr_temp1.show()
    #boxs = Image_FindContours(im_arr_temp1)

    boxs = Image_OCR_Result_Crop_Pre(
        numpy.array((im_arr_temp1.copy()).convert("RGB")), 
        im_arr_temp1.size, 
        im_RGB_raw= numpy.array((img.copy()).convert("RGB"))
        )
    print(sys._getframe().f_lineno, ".... Image Clean - crop image, used time", usedTime(stime))
    return boxs

def Image_OCR_Result_Crop_Y(im_RGB, isize, step_x=50, step_y=15, x0=0, y0=0):
    cropframes = []
    i = 0
    if isize[0] > step_x or isize[1] > step_y:
        y1 = y0
        y2 = y0
        last_y2 = y0          

        while last_y2 < y0  + isize[1]:
            i += 1

            y1 = last_y2
            if y1 >= y0 + isize[1]:
                break
            
            if i > 1:
                y2 = y1 + step_y
                if y2 > y0  + isize[1]:
                    y2 = y0 + isize[1]

            y_blank_count = 0
            y_blank_last_y2 = 0
            #print('--------- 1 y2:', y2, isize)
            while True:
                if y2 > y0 + isize[1]:                    
                    break

                #'''
                #check by line, use less time!!!
                try:
                    IsOneLine, result = Image_IsOneLine(im_RGB[y2,x0:isize[0]], minNonZero=5)
                    if IsOneLine and y2 - y1 > 5:
                        if y2 - y_blank_last_y2 == 1:
                            y_blank_count += 1
                            if y_blank_count >= 2:
                                y_blank_count = 0
                                y_blank_last_y2 = y2
                                break
                        else:
                            y_blank_count = 0
                        y_blank_last_y2 = y2
                except:
                    pass
                    #print("\nim_RGB[y2,x0:isize[0]]=im_RGB[", y2, x0, isize[0],"]\n")
                    #print(traceback.format_exc())
                y2 +=1

            #print('\n--------- '+ str(i) + '/' + str(ny) +' y1, y2, ibox, rgb:', y1, y2, ibox, rgb)

            if y2 > y0 + isize[1]:
                y2 = y0 + isize[1]
            elif abs(y0 + isize[1] - y2) <= 10:
                y2 = y0 + isize[1]

            last_y2 = y2
            Image_OCR_Result_Crop_Frame(ibox= [x0, y2, x0 + isize[0], y2], i=i)
            cropframes.append(y2)

            if y2 == y1:
                break
    
        if y2 < y0 + isize[1]:
            box=[x0, y2, x0 + isize[0], y0 + isize[1]]
            Image_OCR_Result_Crop_Frame(ibox=[x0, y0 + isize[1], x0 + isize[0], y0 + isize[1]], i=i)
            cropframes.append(y0 + isize[1])

    else:
        box = [x0, y0, x0 + isize[0], y0 + isize[1]]
        Image_OCR_Result_Crop_Frame(ibox=[x0, y0 + isize[1], x0 + isize[0], y0 + isize[1]], i=i)
        cropframes.append(y0 + isize[1])

    return cropframes

def Image_OCR_Result_Crop_X(im_RGB, isize, step_x=50, step_y=15, x0=0, y0=0, im_RGB_raw=None, cropframes= []):
    #print('\nImage_OCR_Result_Crop_X (x0, y0, isize, cropframes):', x0, y0, isize, cropframes, im_RGB.shape, im_RGB_raw.shape)
    
    i = 0
    #if isize[0] > step_x or isize[1] > step_y:
    if isize[0] and isize[1]:
        nx = int(isize[0] / step_x) + 1   #total blocks in X axis
        x1 = x0
        y1 = y0
        y2 = y0 + isize[1]
     
        last_x2 = x0
        for j in range(nx):   
            i += 1

            x1 = last_x2
            if x1 >= x0 + isize[0]:
                break

            x2 = x1 + step_x
            x_blank_count = 0
            x_blank_last_x2 = 0
            #print('--------- #1 x2:', x2, isize)
            icounts = []
            while True:
                icount = 0

                if x2 >= x0 + isize[0]:
                    break
                
                #'''
                #check by line, use less time!!!
                try:
                    unique,counts=numpy.unique(im_RGB[y1:y2+1,x2], axis=0,return_counts=True)
                    icount = len(counts) - 1

                    #if icount == -1:
                    #    print("\t::",x2, y1, y2+1,  im_RGB[y1:y2+1,x2])
                except:
                    pass
                    #print("\tX:unique,counts=numpy.unique(im_RGB",im_RGB.shape, "[",y1,":",y2+1,",",x2,"], axis=0, return_counts=True)")
                    icount = 1
                #'''
                icounts.append(str(icount))
                if icount == 0 and x2 - x1 > 5:
                    if x2 - x_blank_last_x2 == 1:
                        x_blank_count += 1
                        if x_blank_count > 5:
                            x_blank_count = 0
                            x_blank_last_x2 = x2
                            break
                    else:
                        x_blank_count = 0
                    x_blank_last_x2 = x2

                x2 +=1

            #print('--------- #2 x2:', x2, ".".join(icounts))

            if x2 > x0 + isize[0]:
                x2 = x0 + isize[0]  
            elif abs(x2 - (x0 + isize[0])) <= 10:
                x2 = x0 + isize[0]  

            if x1 == x2:
                break     
                
            last_x2 = x2  

            x_blank = []
            GoCheckXagain = True
            if GoCheckXagain:
                x1_final = x1
                x_all_icounts = {}
                for xx in range(x1,x2):
                    icount = 1
                    try:
                        unique,counts=numpy.unique(im_RGB_raw[y1:y2+1,xx], axis=0,return_counts=True)
                        if len(counts) == 1:
                            icount = 0
                        #print(unique)
                    except:
                        pass
                        #print("\tXX:unique,counts=numpy.unique(im_RGB",im_RGB.shape, "[",y1,":",y2+1,",",xx,"], axis=0, return_counts=True)")                 
                    
                    if icount == 0:
                        x_blank.append(xx)
                    elif x1_final == x1:
                        if xx - x1 >=2:
                            x1_final = xx - 2
                        else:
                            x1_final = xx - 1
                    x_all_icounts[xx] = icount

            if len(x_blank):
                xx1 = x1_final
                for xii in range(len(x_blank)):
                    xx = x_blank[xii]
                    if xx <= x1_final:
                        continue             

                    if xx - xx1 >=10:
                        canGo = 0
                        toBreak = 0

                        for ddd in range(1, 3):
                            if toBreak:
                                break
                            if x_all_icounts.__contains__(xx-ddd):
                                if x_all_icounts[xx-ddd] == 1:
                                    toBreak = 1

                            if x_all_icounts.__contains__(xx+ddd):
                                if x_all_icounts[xx+ddd] == 1:
                                    toBreak = 1

                        if canGo or toBreak == 0:
                            canGo2 = 0
                            for xxx in range(xx1,xx+1):
                                if x_all_icounts.__contains__(xxx):
                                    canGo2 += x_all_icounts[xxx]
                            if canGo2:
                                #box=[xx1,y1,xx,y2], 
                                #Image_OCR_Result_Crop_Frame(ibox=[xx, y1, xx, y2], i=i)
                                #cropframes.append(xx)
                                Image_OCR_Result_Crop_X_Check(cropframes, xx, [xx, y1, xx, y2], i, step_x)
                                #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(xx1,y1,xx,y2), ibox) 
                                #cropframes.append([xx1,y1,xx,y2])
                            xx1 = xx
                
                if xx1 < x2:
                    #box=[xx1,y1,x2,y2]
                    #Image_OCR_Result_Crop_Frame(ibox=[x2, y1, x2, y2], i=i)
                    #cropframes.append(x2)
                    Image_OCR_Result_Crop_X_Check(cropframes, x2, [x2, y1, x2, y2], i, step_x)
                    #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(xx1,y1,x2,y2), ibox) 
                    #cropframes.append([xx1,y1,x2,y2])
            else:
                #box=[x1,y1,x2,y2]
                #Image_OCR_Result_Crop_Frame(ibox=[x2, y1, x2, y2], i=i)
                #cropframes.append(x2)
                Image_OCR_Result_Crop_X_Check(cropframes, x2, [x2, y1, x2, y2], i, step_x)
                #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(x1,y1,x2,y2), ibox) 
                #cropframes.append([x1,y1,x2,y2])
    else:
        #box = [x0, y0, x0 + isize[0], y0 + isize[1]]
        #Image_OCR_Result_Crop_Frame(ibox= [x0 + isize[0], y0, x0 + isize[0], y0 + isize[1]] , i=i)
        #cropframes.append(x0 + isize[0])
        Image_OCR_Result_Crop_X_Check(cropframes, x0 + isize[0], [x0 + isize[0], y0, x0 + isize[0], y0 + isize[1]], i, step_x)

    return sorted(cropframes)

def Image_OCR_Result_Crop_X_Check(cropframes, x, ibox, i, step_x):
    e = False
    for xx in cropframes:
        if abs(xx - x) < step_x:
            e = True
            break
    if not e:
        cropframes.append(x)
        #print("\tXbox=", ibox)
        Image_OCR_Result_Crop_Frame(ibox= ibox , i=i)

def Image_OCR_Result_Crop_Frame(ibox=[], i=0, lcolor='red', is2go=True):
    if WindX['win_ocr_PaddleOCR_self'] and is2go:
        Image_OCR_Result_AddFrame(
            WindX['win_ocr_PaddleOCR_self'],
            [ibox[0] + 1,
             ibox[1] + 1 + WindX['win_ocr_PaddleOCR_self'].canvas_height_offset,
             ibox[2] - 1,
             ibox[3] - 1 + WindX['win_ocr_PaddleOCR_self'].canvas_height_offset
            ],
            tipstr='Crop Area #' + str(i), 
            lcolor= lcolor
        )

def Image_OCR_Result_Crop_Pre(im_RGB, isize, step_x=50, step_y=15, x0=0, y0=0, im_RGB_raw=None, layer=1, box0=[]):
    cropframes = []

    if layer > 1:
        x0 = box0[0]
        y0 = box0[1]
    
    cropframesY = Image_OCR_Result_Crop_Y(im_RGB, isize, step_x=50, step_y=15, x0=x0, y0=y0)
    #cropframesX = Image_OCR_Result_Crop_X(im_RGB, isize, step_x=50, step_y=15, x0=x0, y0=y0, im_RGB_raw=im_RGB_raw)
    #print("\ncropframesX=", cropframesX)
    print(  "cropframesY=", cropframesY, "\n")
    
    for ny in range(len(cropframesY)):
        #print("cropframesX", len(cropframesX))
        x1 = x0
        cropframesX = []
        isizeXX = [isize[0], cropframesY[ny] - y0]
        #im_arr_temp1 = Image.fromarray(im_RGB2)
        #im_arr_temp1.show()
        cropframesX = Image_OCR_Result_Crop_X(im_RGB, isizeXX, step_x=50, step_y=15, x0=x0, y0=y0, im_RGB_raw=im_RGB_raw, cropframes=cropframesX)
        print("{:0>3d} X={} blocks".format(ny+1, len(cropframesX) +1))

        for nx in range(len(cropframesX)):
            cropframes.append([[x1, y0, cropframesX[nx], cropframesY[ny]], ny+1, nx+1])
            x1 = cropframesX[nx]
        y0 = cropframesY[ny]

        #if len(cropframesX) < int(isize[0]/step_x):
        #    isizeX = [isize[0], isize[1] - y0]
        #    cropframesX = Image_OCR_Result_Crop_X(im_RGB, isizeX, step_x=50, step_y=15, x0=x0, y0=y0, im_RGB_raw=im_RGB_raw, cropframes=cropframesX)
    
    #return []

    cropframesX = []
    for cf in cropframes:        
        box = cf[0]
        im_RGB2 = im_RGB[box[1]:box[3]+1 , box[0]:box[2]+1]
        
        isBlank = Image_IsBlank(im_RGB2, 'Crop_pre') #check if the image is blank
        if not isBlank:
            Image_OCR_Result_Crop_Frame(ibox=cf[0], i=str(cf[1]) + str(cf[2]), lcolor='blue',  is2go=True)
            
            isize = [box[2] - box[0] + 1, box[3] - box[1] + 1]
            im_RGB_raw2 = im_RGB_raw[box[1]:box[3]+1 , box[0]:box[2]+1]

            cfx = Image_OCR_Result_Crop(im_RGB2, isize, step_x=step_x, step_y=step_y, x0=0, y0=0, im_RGB_raw=im_RGB_raw2, layer=1, box0=box)
            if len(cfx):            
                cfxx = []
                for b in cfx:
                    box2 = [b[0] + box[0], b[1] + box[1], b[2] + box[0], b[3] + box[1]]
                    if box2[0] < 0:
                        box2[0] = 0
                    if box2[1] < 0:
                        box2[1] = 0
                    cfxx.append(box2)
                    #Image_OCR_Result_Crop_Frame(ibox=box2, i=0, lcolor='green',  is2go=True)

                cropframesX.append([cfxx, box, cf[1], cf[2]])   #[[boxes, box, ny, nx], [...]]

    return cropframesX

def Image_OCR_Result_Crop(im_RGB, isize, step_x=50, step_y=15, x0=0, y0=0, im_RGB_raw=None, layer=1, box0=[]):
    #print("\n//// Image_OCR_Result_Crop layer=", layer, isize)

    """
    if layer == 1:
        cropframesX = Image_OCR_Result_Crop_X(im_RGB, isize, step_x=50, step_y=15, x0=x0, y0=y0, im_RGB_raw=im_RGB_raw)
        cropframesY = Image_OCR_Result_Crop_Y(im_RGB, isize, step_x=50, step_y=15, x0=x0, y0=y0)

        print("\ncropframesX=", cropframesX)
        print(  "cropframesY=", cropframesY, "\n")
    #else:
    #    cropframesX = Image_OCR_Result_Crop_X(im_RGB, isize, step_x=50, step_y=15, x0=box0[0], y0=box0[1], im_RGB_raw=im_RGB_raw)
    #return
    """

    cropframes = []
    if isize[0] > step_x or isize[1] > step_y:
        nx = int(isize[0] / step_x) + 1   #total blocks in X axis
        ny = int(isize[1] / step_y) + 1   #total blocks in Y axis
        x1 = x0
        y1 = y0
        y2 = y0
        last_y2 = y0
        ibox = [x0, y0, x0 + isize[0],y0 + isize[1]]   #box of the whole image              

        i = 0
        while last_y2 < y0  + isize[1]:
            i += 1

            y1 = last_y2
            if y1 >= y0 + isize[1]:
                break
            
            if i > 1:
                y2 = y1 + step_y
                if y2 > y0  + isize[1]:
                    y2 = y0 + isize[1]

            y_blank_count = 0
            y_blank_last_y2 = 0
            #print('--------- 1 y2:', y2, isize)
            while True:
                icount = 0

                if y2 > y0 + isize[1]:                    
                    break

                try:
                    #check by line, use less time!!!
                    IsOneLine, result = Image_IsOneLine(im_RGB[y2,x0:isize[0]], minNonZero=5)
                    if IsOneLine and y2 - y1 > 5:
                        if y2 - y_blank_last_y2 == 1:
                            y_blank_count += 1
                            if y_blank_count >= 2:
                                y_blank_count = 0
                                y_blank_last_y2 = y2
                                break
                        else:
                            y_blank_count = 0
                        y_blank_last_y2 = y2
                except:
                    pass
                    #print("im_RGB[y2,x0:isize[0]]=im_RGB[", y2, x0, isize[0],"]\n")
                    #print(traceback.format_exc())    
                y2 +=1

            #print('\n--------- '+ str(i) + '/' + str(ny) +' y1, y2, ibox, rgb:', y1, y2, ibox, rgb)

            if y2 > y0 + isize[1]:
                y2 = y0 + isize[1]
            elif abs(y0 + isize[1] - y2) <= 10:
                y2 = y0 + isize[1]

            last_y2 = y2

            if y2 == y1:
                break

            last_x2 = x0
            for j in range(nx):                            
                x1 = last_x2
                if x1 >= x0 + isize[0]:
                    break

                x2 = x1 + step_x
                x_blank_count = 0
                x_blank_last_x2 = 0
                #print('--------- 1 x2:', x2, isize)
                while True:
                    icount = 0

                    if x2 >= x0 + isize[0]:
                        break
                    
                    #'''
                    #check by line, use less time!!!
                    try:
                        unique,counts=numpy.unique(im_RGB[y1:y2+1,x2], axis=0,return_counts=True)
                        icount = len(counts) - 1
                    except:
                        pass
                        #print("\tX:unique,counts=numpy.unique(im_RGB",im_RGB.shape, "[",y1,":",y2+1,",",x2,"], axis=0, return_counts=True)")
                        icount = 1
                    #'''

                    if icount == 0 and x2 - x1 > 5:
                        if x2 - x_blank_last_x2 == 1:
                            x_blank_count += 1
                            if x_blank_count > 5:
                                x_blank_count = 0
                                x_blank_last_x2 = x2
                                break
                        else:
                            x_blank_count = 0
                        x_blank_last_x2 = x2

                    x2 +=1

                #print('--------- 2 x2:', x2, ibox, rgb)

                if x2 > x0 + isize[0]:
                    x2 = x0 + isize[0]  
                elif abs(x2 - (x0 + isize[0])) <= 10:
                    x2 = x0 + isize[0]  

                if x1 == x2:
                    break     
                    
                last_x2 = x2   

                x_blank = []
                GoCheckXagain = True
                if GoCheckXagain:
                    x1_final = x1
                    x_all_icounts = {}
                    for xx in range(x1,x2):
                        icount = 1
                        try:
                            unique,counts=numpy.unique(im_RGB_raw[y1:y2+1,xx], axis=0,return_counts=True)
                            if len(counts) == 1:
                                icount = 0
                            #print(unique)
                        except:
                            pass
                            #print("\tXX:unique,counts=numpy.unique(im_RGB",im_RGB.shape, "[",y1,":",y2+1,",",xx,"], axis=0, return_counts=True)")                 
                        
                        if icount == 0:
                            x_blank.append(xx)
                        elif x1_final == x1:
                            if xx - x1 >=2:
                                x1_final = xx - 2
                            else:
                                x1_final = xx - 1
                        x_all_icounts[xx] = icount

                if len(x_blank):
                    xx1 = x1_final
                    for xii in range(len(x_blank)):
                        xx = x_blank[xii]
                        if xx <= x1_final:
                            continue             

                        if xx - xx1 >=10:
                            canGo = 0
                            toBreak = 0

                            for ddd in range(1, 3):
                                if toBreak:
                                    break
                                if x_all_icounts.__contains__(xx-ddd):
                                    if x_all_icounts[xx-ddd] == 1:
                                        toBreak = 1

                                if x_all_icounts.__contains__(xx+ddd):
                                    if x_all_icounts[xx+ddd] == 1:
                                        toBreak = 1

                            if canGo or toBreak == 0:
                                canGo2 = 0
                                for xxx in range(xx1,xx+1):
                                    if x_all_icounts.__contains__(xxx):
                                        canGo2 += x_all_icounts[xxx]
                                if canGo2:
                                    Image_OCR_Result_Crop2(
                                        im_RGB, step_x=step_x, step_y=step_y, 
                                        box=[xx1,y1,xx,y2], 
                                        im_RGB_raw=im_RGB_raw, 
                                        cropframes=cropframes,
                                        layer = layer
                                    )
                                    #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(xx1,y1,xx,y2), ibox) 
                                    #cropframes.append([xx1,y1,xx,y2])
                                xx1 = xx
                    
                    if xx1 < x2:
                        Image_OCR_Result_Crop2(
                            im_RGB, step_x=step_x, step_y=step_y, 
                            box=[xx1,y1,x2,y2], 
                            im_RGB_raw=im_RGB_raw, 
                            cropframes=cropframes,
                            layer = layer
                        )
                        #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(xx1,y1,x2,y2), ibox) 
                        #cropframes.append([xx1,y1,x2,y2])
                else:
                    Image_OCR_Result_Crop2(
                        im_RGB, step_x=step_x, step_y=step_y, 
                        box=[x1,y1,x2,y2], 
                        im_RGB_raw=im_RGB_raw, 
                        cropframes=cropframes,
                        layer = layer
                    )
                    #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(x1,y1,x2,y2), ibox) 
                    #cropframes.append([x1,y1,x2,y2])
    
        if y2 < y0 + isize[1]:
            Image_OCR_Result_Crop2(
                im_RGB, step_x=step_x, step_y=step_y, 
                box=[x0, y2, x0 + isize[0], y0 + isize[1]], 
                im_RGB_raw=im_RGB_raw, 
                cropframes=cropframes,
                layer = layer
            )
            #print("&", end="")
            #print('crop (x1,y1,x2,y2) [0,0,width,height]:',(x1,y1,x2,y2), ibox) 
            #cropframes.append([x0, y2, x0 + isize[0], y0 + isize[1]])

    else:
        Image_OCR_Result_Crop2(
            im_RGB, step_x=step_x, step_y=step_y, 
            box=[x0, y0, x0 + isize[0], y0 + isize[1]], 
            im_RGB_raw=im_RGB_raw, 
            cropframes=cropframes,
            layer = 100
        )
        #cropframes.append([x0, y0, x0 + isize[0], y0 + isize[1]])

    if layer < 2:
        print("")
    return cropframes

WindX['win_ocr_crop_layers'] = {
    1: 0,
    2: 0
}
def Image_OCR_Result_Crop2(im_RGB, step_x=50, step_y=50, box=[], im_RGB_raw=None, cropframes=[], layer=2):
    if box[2] - box[0] < 10 or box[3] - box[1] < 10:
        return
    
    if not WindX['win_ocr_crop_layers'].__contains__(layer):
        WindX['win_ocr_crop_layers'][layer] = 0
    WindX['win_ocr_crop_layers'][layer] +=1

    if layer < 2 and (box[3] - box[1])/step_y > 3:
        isize = [box[2] - box[0] + 1, box[3] - box[1] + 1]
        im_RGB2     = im_RGB[box[1]:box[3]+1 , box[0]:box[2]+1]
        im_RGB_raw2 = im_RGB_raw[box[1]:box[3]+1 , box[0]:box[2]+1]
        cropframesX = Image_OCR_Result_Crop(im_RGB2, isize, step_x=step_x, step_y=step_y, im_RGB_raw=im_RGB_raw2, layer=2, box0=box)
        for b in cropframesX:
            box2 = [b[0] + box[0], b[1] + box[1], b[2] + box[0], b[3] + box[1]]
            if box2[0] < 0:
                box2[0] = 0
            if box2[1] < 0:
                box2[1] = 0

            isBlank = Image_IsBlank(im_RGB[box2[1]:box2[3], box2[0]:box2[2]], 'Crop2 B') #check if the image is blank
            if not isBlank:
                print("%" + str(layer)+ '.' + str(len(cropframes)+1), end=" ")
                #print('crop2 (x1,y1,x2,y2):', box2) 
                cropframes.append(box2)
    else:
        boxes = []
        nn = 5
        #crop the image in width if its width is too large which will result in bad text recognization
        if (box[2] - box[0])/step_x > nn:
            for i in range(int((box[2] - box[0])/step_x)):
                b0 = box[0] + step_x*nn*i
                b2 = box[0] + step_x*nn*(i + 1)
                if b2 > box[2]:
                    b2 = box[2]
                boxes.append([b0, box[1], b2, box[3]])

                if b2 == box[2]:
                    break
        else:
            boxes.append(box)

        for ibox in boxes:
            if ibox[0] < 0:
                ibox[0] = 0
            if ibox[1] < 0:
                ibox[1] = 0
            isBlank = Image_IsBlank(im_RGB[ibox[1]:ibox[3], ibox[0]:ibox[2]], 'Crop2 A') #check if the image is blank
            if not isBlank:
                print("#"+ str(layer) +'.'+ str(len(cropframes)+1), end=" ")
                #print('crop1 (x1,y1,x2,y2):', box)
                cropframes.append(ibox)

WindX['win_ocr_PaddleOCR'] = None
WindX['win_ocr_PaddleOCR_self'] = None
def Image_OCR_Result(im_PIL,isDisplay=True,Tolang='eng',isFind=False,izoom=1,ToUse_PaddleOCR=0,self=None):
    results = {
        'image_to_boxes':None,
        'image_to_data':None,
        'image_to_string': [],
        'image_zoom_rate': izoom
    }

    WindX['win_ocr_PaddleOCR_self'] = self

    try:       
        if im_PIL:
            stime = time.time()
            print("\n-------- Image_OCR_Result - Start " + usedTime(stime) + " --------")

            if self:                
                self.canvas_progress_bar(1,100)

            isize = im_PIL.size
            if izoom != 1 and (not ToUse_PaddleOCR):
                sizes = im_PIL.size
                im_PIL = im_PIL.resize((int(sizes[0]*izoom), int(sizes[1]*izoom)),Image.ANTIALIAS)

            output=BytesIO()
            im_PIL.save(output, format='PNG')
            ##byte_data = output.getvalue()
            im = Image.open(output)
            #im = im_PIL
            
            #results['image_to_boxes'] = pytesseract.image_to_boxes(im)

            #Image_FindContours(im.copy())
            #cropframes = Image_cleanUp(im.copy())
            #return

            #tmp_folder = WindX['self_folder'] + "/ScreenCatch/tmp_orc_" + str(stime)
            #CreateFolder(tmp_folder)

            cropframes = []
            if ToUse_PaddleOCR:
                results['image_zoom_rate'] = 1
                isize = im.size
                step_x=100
                step_y=300
                #im_RGB = numpy.array(((im.copy()).convert('1')).convert("RGB"))                
                #im_RGB = numpy.array(((im.copy()).convert('L')).convert("RGB"))   
                             
                #im_RGB = numpy.array((im.copy()).convert("RGB"))
                #cropframes = Image_OCR_Result_Crop(im_RGB, isize, step_x=step_x, step_y=step_y, x0=0, y0=0)

                if self:
                    self.canvas_progress_bar(5,100)

                cropframes = Image_cleanUp(im.copy(), stime)   #[[boxes, box, ny, nx], [...]]
                if not len(cropframes):
                    cropframes.append([[0,0,isize[0],isize[1]], [0, 0, isize[0],isize[1]], 1, 1])
                #return
                print("\nwin_ocr_crop_layers=",WindX['win_ocr_crop_layers'],"\n")

                imssX = []
                for cfs in cropframes:  #cfs: [boxes, box, ny, nx]
                    for cf in cfs[0]:
                        imssX.append([cf[0],cf[1],im.crop(cf), cf, cfs[2], cfs[3]])  #[x0, y0, im_crop, box, ny, nx]
                
                print("\nPaddleOCR image size:", isize , 'x '+str(int(results['image_zoom_rate']*100)/100)+' -->', im.size, '-->',str(len(imssX)) + 'X', ", used time " + usedTime(stime) + "\n")

                if not WindX['win_ocr_PaddleOCR']:
                    try:
                        # need to run only once to download and load model into memory, try to use GPU at first
                        # paddleocr whl包会自动下载ppocr轻量级模型作为默认模型，可以根据�?节自定义模型进行自定义更换�?
                        WindX['win_ocr_PaddleOCR'] = PaddleOCR(use_angle_cls=True, lang="ch",det_max_side_len=2000,show_log=False, use_gpu=True, cls=True) 
                        """
                        #Use server mode, and will take more time
                        WindX['win_ocr_PaddleOCR'] = PaddleOCR(
                            use_angle_cls=True, 
                            lang="ch",
                            det_max_side_len=2000,
                            show_log=False, 
                            use_gpu=True,
                            det_model_dir='I:/Program Files/Python385/Lib/site-packages/paddleocr/inference/ch_ppocr_server_v2.0_det_infer',
                            rec_model_dir='I:/Program Files/Python385/Lib/site-packages/paddleocr/inference/ch_ppocr_server_v2.0_rec_infer',
                            rec_char_dict_path='I:/Program Files/Python385/Lib/site-packages/paddleocr/doc/fonts/chinese_cht.ttf',
                            cls_model_dir = 'I:/Program Files/Python385/Lib/site-packages/paddleocr/inference/ch_ppocr_mobile_v2.0_cls_infer',
                            max_text_length=256
                        )
                        """
                    except:
                        print(traceback.format_exc())
                        WindX['win_ocr_PaddleOCR'] = PaddleOCR(use_angle_cls=True, lang="ch",det_max_side_len=2000,show_log=False, use_gpu=False, cls=True) #not use GPU, if error
                    # need to run only once to download and load model into memory

                if self:
                    self.canvas_progress_bar(30,100)
                    self.ocr_result_len_imssX = len(imssX)
                    self.ocr_result_i_done = 0
                try:
                    results['image_data_paddle'] = []
                    i = 0
                    print("")
                    threads = []
                    Go_This_Way_No_Threads = True #False - the multiple threads will kill the app!!!

                    for im in imssX: 
                        i+=1
                        
                        if Go_This_Way_No_Threads:
                            Image_OCR_Result_Go(self, i, im, isize, izoom, results)
                        else:
                            threads.append(threading.Thread(target=Image_OCR_Result_Go, args=[self, i, im, isize, izoom, results]))

                    if not Go_This_Way_No_Threads: #the multiple threads will kill the app!!!
                        for t in threads:
                            t.start()
                        for t in threads:
                            t.join()

                    print("")    
                    #print(results,"\n\n")
                except:
                    print(sys._getframe().f_lineno, "\nTry PaddleOCR and get error:\n" + traceback.format_exc())
            else:
                print("\nTesseractOCR image size:", isize , 'x '+str(int(results['image_zoom_rate']*100)/100)+' -->', im.size, "\n")
                if self:
                    self.canvas_progress_bar(30,100)

                if isFind:
                    results['image_to_data']  = pytesseract.image_to_data(im, output_type=pytesseract.Output.DICT,lang=Tolang,config='--dpi 300')
                else:
                    rets = re.split(r'\n+',pytesseract.image_to_string(im,lang=Tolang,config='--dpi 300'))            
                    for ret in rets:
                        ret1 = re.sub(r'^\s+|\s+$','',ret)
                        if ret1:
                            results['image_to_string'].append(ret)

                    if len(results['image_to_string']):
                        #
                        if isDisplay:
                            print("\n".join(results['image_to_string']))
                            print(results['image_to_boxes'])
                            #Message("\n".join(results['image_to_string']), 'yellow', 'red')

            print("\n-------- Image_OCR_Result - End, used time " + usedTime(stime) + " --------")
            output.close()
    except:
        print(traceback.format_exc())

    if self:
        self.canvas_progress_bar(100,100)
    return results

def Image_OCR_Result_Go(self, i, im, isize, izoom, results):
    #return
    ny = im[4]
    nx = im[5]

    isBlank = Image_IsBlank(numpy.array(im[2].copy()), 'Result') #check if the image is blank
    if not isBlank:    
        print('\033[0;32;40m*'+str(i)+'\033[0m',end=" ")  #32 - green color, print *                        
        #print("*", end="")
        #print("-- block (width,height):", im[2].size, ', is blank=', isBlank) 
        #image box: left,top and right, bottom
        x1 = im[3][0]+1
        y1 = im[3][1]+1
        x2 = im[3][2]-1
        y2 = im[3][3]-1
        if x2 >= isize[0] - 2:
            x2 = isize[0] - 2
        if y2 >= isize[1] - 2:
            y2 = isize[1] - 2

        display_frame_in_time = True
        if display_frame_in_time and self and self.ocr_method_to_use_baidu.get():
            xx = sorted([x1, x2])
            yy = sorted([y1, y2])                                
            ibox = [int(xx[0]), int(yy[0] + self.canvas_height_offset), int(xx.pop()), int(yy.pop() + self.canvas_height_offset)]
            
            Image_OCR_Result_AddFrame(self, ibox, tipstr='Crop Area #' + str(i) + ', isBlank=' + str(isBlank), lcolor='#FF66FF')
            '''
            lcolor = '#FF66FF'
            cb = cButton(self,'',None,
                [ibox[0] - 1, ibox[1] - 1, ibox[2] + 1, ibox[3] + 1,'', lcolor,1],
                [], tip= 'Crop Area #' + str(i) + ', isBlank=' + str(isBlank))

            self.Items.append(cb.button_bg)
            if cb.button_txt_frame_num:
                self.Items.append(cb.button_txt_frame_num)
            self.top.update()
            '''
        else:
            results['image_data_paddle'].append(
                [
                    [[x1, y1], [x2, y1], [x2, y2], [x1, y2]],
                    ['Crop Area #' + str(i) + ', isBlank=' + str(isBlank)],
                    'NOT-TEXT'
                ]
            )

        #image OCR
        try:
            imgx = im[2].copy()  ##[x0, y0, im_crop, box, ny, nx]
            if izoom != 1:
                sizes = imgx.size
                imgx  = imgx.resize((int(sizes[0]*izoom), int(sizes[1]*izoom)),Image.ANTIALIAS)

            #add edge to the image
            dxy = 15 #edge height or width
            bgColor = Image_getBGColor(numpy.array(imgx))
            im_arr  = numpy.array(imgx.convert("RGB"))
            imshape = im_arr.shape
            im_arrX = numpy.zeros((imshape[0] + dxy*2, imshape[1] + dxy*2,3), numpy.uint8)
            im_arrX[:] = bgColor #[255,0,0]
            #print(im_arrX)
            im_arrX[dxy:dxy+imshape[0],dxy:dxy+imshape[1]] = im_arr
            #im_arr_temp1 = Image.fromarray(im_arrX)
            #im_arr_temp1.show()
            #im_arr_temp1.save(tmp_folder + '/X' + str(izoom) + ' ' + str(i) + '.png')
            
            #rint(im_arr.shape,im_arr)  #.shape(height, width, color-channels)
            data_paddle = WindX['win_ocr_PaddleOCR'].ocr(im_arrX) 
            parsedLines = []
            for line in data_paddle:
                if not len(line):
                    continue
                
                '''      
                print('line=', line)          
                #结果是一个list，每个item包含了文本框，文字和识别置信�?
                ##### paddleocr version<2.6.1.2 #####
                #case-1
                line = [   
                    [[24.0, 36.0], [304.0, 34.0], [304.0, 72.0], [24.0, 74.0]], 
                    ['纯臻营养护发�?, 0.964739]
                ]

                ##### paddleocr version=2.6.1.2 #####
                #case-2
                line= [
                    [
                        [[29.0, 52.0], [292.0, 52.0], [292.0, 79.0], [29.0, 79.0]], 
                        ('Bo,Qingzhu,Wenjian', 0.9083628058433533)
                    ]
                ]

                #case-3
                line= [
                    [
                        [[18.0, 31.0], [383.0, 29.0], [383.0, 64.0], [19.0, 67.0]], 
                        ('ohan Zoom Image: 2', 0.9425995349884033)
                    ], 
                    [
                        [[15.0, 97.0], [516.0, 97.0], [516.0, 129.0], [15.0, 129.0]], 
                        ('vaSankar Yepuri; Saibaba Kon', 0.9415278434753418)
                    ]
                ]
                '''
                try:
                    if len(line) == 1: #case-2
                        line = line[0]

                    if len(line) < 2:
                        print('\tinvlad line:', line)
                        continue
                    elif len(line) == 2 and len(line[0]) == 4 and len(line[1]) == 2 and type(line[1][0]) == str and (type(line[1][1]) == float or type(line[1][1]) == int): #case-1                   
                        line[1] = list(line[1])
                        parsedLines.append(line)
                    else: 
                        line0 = line[0]  #case-3
                        if len(line0) == 2 and len(line0[0]) == 4 and len(line0[1]) == 2 and type(line0[1][0]) == str and (type(line0[1][1]) == float or type(line0[1][1]) == int): #case-1   
                            for linex in line:
                                linex[1] = list(linex[1])
                                parsedLines.append(linex)
                except:
                    print('line=', line)
                    print(sys._getframe().f_lineno, "Try to parse line of PaddleOCR result and get error:\n" + traceback.format_exc())

            for line in parsedLines:
                '''                
                #结果是一个list，每个item包含了文本框，文字和识别置信�?
                line = [   
                    [[24.0, 36.0], [304.0, 34.0], [304.0, 72.0], [24.0, 74.0]], 
                    ['纯臻营养护发�?, 0.964739]
                ]
                '''
                try:                                    
                    line[0][0] = [(line[0][0][0] - dxy)/izoom + im[0], (line[0][0][1] - dxy)/izoom + im[1]]
                    line[0][1] = [(line[0][1][0] - dxy)/izoom + im[0], (line[0][1][1] - dxy)/izoom + im[1]]
                    line[0][2] = [(line[0][2][0] - dxy)/izoom + im[0], (line[0][2][1] - dxy)/izoom + im[1]]
                    line[0][3] = [(line[0][3][0] - dxy)/izoom + im[0], (line[0][3][1] - dxy)/izoom + im[1]]
                    line[0].append(ny)
                    line[0].append(nx)

                    results['image_data_paddle'].append(line)                        
                    if line[1][0]:
                        results['image_to_string'].append(line[1][0])

                        if self and self.ocr_method_to_use_baidu_val:
                                xx = sorted(list(set([line[0][0][0], line[0][1][0], line[0][2][0], line[0][3][0]])))
                                yy = sorted(list(set([line[0][0][1], line[0][1][1], line[0][2][1], line[0][3][1]])))                                
                                ibox = [int(xx[0]), int(yy[0] + self.canvas_height_offset), int(xx.pop()), int(yy.pop() + self.canvas_height_offset)]
                                
                                Image_OCR_Result_AddFrame(self, ibox, tipstr=line[1][0], lcolor="green")
                                '''
                                lcolor = "green"                            
                                cb = cButton(self,'',None,
                                    [ibox[0] - 1, ibox[1] - 1, ibox[2] + 1, ibox[3] + 1,'', lcolor,1],
                                    [], tip= str(line[1][0]))
                                self.Items.append(cb.button_bg)
                                if cb.button_txt_frame_num:
                                    self.Items.append(cb.button_txt_frame_num)
                                '''
                except:
                    print('line=', line)
                    print('line[0][0][0]=', line[0][0][0],', dxy=', dxy,', izoom=', izoom,', im[0]=', im[0],', line[0][0][1]=', line[0][0][1],', im[1]=', im[1]) 
                    print(sys._getframe().f_lineno, "Try to process line of PaddleOCR result and get error:\n" + traceback.format_exc())

        except:
            print(sys._getframe().f_lineno, "Try PaddleOCR and get error:\n" + traceback.format_exc())

    if self:
        self.ocr_result_i_done += 1
        self.canvas_progress_bar(int(30 + 69*self.ocr_result_i_done/self.ocr_result_len_imssX),100)    

def Image_OCR_Result_AddFrame(self, ibox, tipstr="", lcolor="green"):
    box = [ibox[0] - 1, ibox[1] - 1, ibox[2] + 1, ibox[3] + 1]
    if box[0] == box[2] or box[1] == box[3]: #line
        line_index = self.canvas.create_line(
                        box[0],
                        box[1],
                        box[2],
                        box[3],
                        fill = lcolor,
                        width= 1,
                    )
        self.Items.append(line_index)
    else: #rectangle
        cb = cButton(self,'',None,
            [ibox[0] - 1, ibox[1] - 1, ibox[2] + 1, ibox[3] + 1,'', lcolor, 1],
            [], tip= str(tipstr))
        self.Items.append(cb.button_bg)
        if cb.button_txt_frame_num:
            self.Items.append(cb.button_txt_frame_num)
        self.top.update()

def Image_OCR_ParseText_for_PaddleOCR(results,izoom):
    rett = []
    ttbox= []
    try:
        xx = []
        yy = []
        if len(results['image_data_paddle']):
            boxs = {}
            boxsNyXs = []
            lengths = []
            alignX = {}           
            for i in range(0, len(results['image_data_paddle'])):
                line = results['image_data_paddle'][i]
                if len(line) > 2 and line[2] == 'NOT-TEXT':
                    continue
                
                xx = sorted(list(set([line[0][0][0], line[0][1][0], line[0][2][0], line[0][3][0]])))
                yy = sorted(list(set([line[0][0][1], line[0][1][1], line[0][2][1], line[0][3][1]])))                                
                ibox = [xx[0], yy[0], xx.pop(), yy.pop()]

                xs = int(ibox[0] / izoom)
                ys = int(ibox[1] / izoom)
                xe = int(ibox[2] / izoom)
                ye = int(ibox[3] / izoom)
                rtext = line[1][0]
                if len(rtext):
                    lengths.append((xe - xs) / len(rtext))

                ny = line[0][4]
                nx = line[0][5]

                xx.extend([xs,xe])
                yy.extend([ys,ye])

                cy = int((ys + ye)/2)
                #Print2Log('', cy, xs, rtext)
                ibcy = cy
                if boxs.__contains__(ny):
                    for bcy in boxs[ny].keys():
                        if abs(bcy - cy) <= 5:
                            ibcy = bcy  #just get all into one line

                if not boxs.__contains__(ny):
                    boxs[ny] = {}                
                if not boxs[ny].__contains__(ibcy):
                    boxs[ny][ibcy] = []
                boxs[ny][ibcy].append([[xs, ys, xe, ye], rtext, 0])

                boxsNyXs.append(xs)

                leftXS = xs
                for lxs in alignX.keys():
                    if abs(leftXS - lxs) <= 5:
                        leftXS = lxs
                        break
                if not alignX.__contains__(leftXS):
                    alignX[leftXS] = []
                
                alignX[leftXS].append([ny, ibcy, [xs, ys, xe, ye], rtext])

            """
            for ny in sorted(boxs.keys()):
                for ibcy in sorted(boxs[ny].keys()):
                    ss = []
                    for nx in sorted(boxs[ny][ibcy].keys()):
                        for item in sorted(boxs[ny][ibcy][nx], key=lambda x:x[0][0]):
                            ss.append(item[1])

                    print(">>", ny, ibcy, " | ".join(ss))
            """
            xlen = 7
            #if len(lengths):
            #    xlen = int(sum(lengths)/len(lengths)/2)
            print("\n\tOne space length (pixel):", xlen)

            #'''
            go_format_column = False
            if go_format_column:
                nk = 0
                for lxs in sorted(alignX.keys()):
                    if len(alignX[lxs]) > 1:
                        nk +=1 
                        print("")
                        xmax_len = 0
                        affected = []
                        is2go = True
                        match_items = 0
                        
                        for s in sorted(alignX[lxs], key=lambda x:x[1]):
                            if not is2go:
                                break
                            last_xe = 0
                            ny = s[0]
                            ibcy = s [1]
                            for item in sorted(boxs[ny][ibcy], key=lambda x:x[0][0]):
                                if item[0] == s[2] and item[1] == s[3]:
                                    match_items += 1
                                    print("\t\t", item[0][0] - last_xe, item[1])
                                    if item[0][0] - last_xe < 50:
                                        is2go = False
                                    break
                                
                                last_xe = item[0][2]
                        
                        if is2go and match_items:
                            for s in sorted(alignX[lxs], key=lambda x:x[1]):
                                print("\t#" + str(nk), lxs, s)

                                last_xe = 0
                                nx_texts= []
                                ny = s[0]
                                ibcy = s [1]
                                affected.append([ny, ibcy])
                                
                                leftItems = []
                                xxx = []
                                yyy = []
                                for item in sorted(boxs[ny][ibcy], key=lambda x:x[0][0]):
                                    if len(leftItems) or (item[0] == s[2] and item[1] == s[3]):
                                        leftItems.append(item)
                                    else:
                                        if not item[2]:
                                            gap_x = item[0][0] - last_xe - 2
                                            if gap_x < 0:
                                                gap_x = 0
                                            nx_texts.append("*" * int(gap_x/xlen) + item[1])
                                        else:
                                            nx_texts.append(item[1])

                                        last_xe = item[0][2]

                                        xxx.append(item[0][0])
                                        xxx.append(item[0][2])
                                        yyy.append(item[0][1])
                                        yyy.append(item[0][3])

                                if len(nx_texts):
                                    xxx = sorted(xxx)
                                    yyy = sorted(yyy)
                                    preText = "".join(nx_texts)
                                    if len(preText) > xmax_len:
                                        xmax_len = len(preText)

                                    boxs[ny][ibcy] = []
                                    boxs[ny][ibcy].append([[xxx[0], yyy[0], xxx.pop(), yyy.pop()], preText, 1])
                                    boxs[ny][ibcy].extend(leftItems)
                                else:
                                    item0 = boxs[ny][ibcy][0]
                                    boxs[ny][ibcy] = []
                                    boxs[ny][ibcy].append([item0[0], '', 1])
                                    boxs[ny][ibcy].extend(leftItems)

                            if xmax_len and len(affected):
                                fmat = "{:_<"+str(xmax_len)+"}"
                                print("\t\t#" + str(nk) + " format=", fmat)
                                for ss in sorted(affected, key=lambda x:x[0]):                           
                                    boxs[ss[0]][ss[1]][0][1] = fmat.format(boxs[ss[0]][ss[1]][0][1])
                                    print("\t\t", ss[0], ss[1], ":") 
                                    for itx in boxs[ss[0]][ss[1]]:
                                        print("\t\t  :", itx[1])
                                print("")
            #'''

            xs_min = min(boxsNyXs)
            last_ny = sorted(boxs.keys())[0]
            for ny in sorted(boxs.keys()):                
                if ny - last_ny > 1:
                    rett.append('')

                for ibcy in sorted(boxs[ny].keys()):
                    xs_min0 = xs_min
                    last_xe = 0
                    nx_texts = []

                    for item in sorted(boxs[ny][ibcy], key=lambda x:x[0][0]):
                        gap_x = item[0][0] - last_xe - 2 - xs_min0
                        if gap_x < 0:
                            gap_x = 0
                        nx_texts.append(" " * int(gap_x/xlen) + item[1])
                        last_xe = item[0][2]
                        xs_min0 = 0

                    #rett.append("{:0>3d}".format(ny) + ": " + "".join(nx_texts))
                    rett.append("".join(nx_texts))

                last_ny = ny     
                
        if len(xx) and len(yy):
            ttbox= [min(xx), min(yy), max(xx), max(yy)]
    except:
        print(sys._getframe().f_lineno, traceback.format_exc())

    return [rett, ttbox]

def Image_OCR_ParseText_for_PaddleOCR2(results,izoom):
    rett = []
    ttbox= []
    try:
        xx = []
        yy = []
        if len(results['image_data_paddle']):
            boxs = {}
            for i in range(0, len(results['image_data_paddle'])):
                line = results['image_data_paddle'][i]
                if len(line) > 2 and line[2] == 'NOT-TEXT':
                    continue
                
                xx = sorted(list(set([line[0][0][0], line[0][1][0], line[0][2][0], line[0][3][0]])))
                yy = sorted(list(set([line[0][0][1], line[0][1][1], line[0][2][1], line[0][3][1]])))                                
                ibox = [xx[0], yy[0], xx.pop(), yy.pop()]

                xs = int(ibox[0] / izoom)
                ys = int(ibox[1] / izoom)
                xe = int(ibox[2]  / izoom)
                ye = int(ibox[3] / izoom)
                rtext = line[1][0]

                xx.extend([xs,xe])
                yy.extend([ys,ye])

                cy = int((ys + ye)/2)
                #Print2Log('', cy, xs, rtext)
                ibcy = cy
                for bcy in boxs.keys():
                    if abs(bcy - cy) <=5:
                        ibcy = bcy  #just get all into one line
                        '''
                        if xe < boxs[bcy]['box'][0]:
                            if xe >= boxs[bcy]['box'][0] - 15:
                                ibcy = bcy
                                break
                        elif xs > boxs[bcy]['box'][2]:
                            if xs <= boxs[bcy]['box'][2] + 15:
                                ibcy = bcy
                                break
                        '''

                if not boxs.__contains__(ibcy):
                    boxs[ibcy] = {}
                    boxs[ibcy]['text'] = {}
                    boxs[ibcy]['xs']   = []
                    boxs[ibcy]['box']   = [1000000,1000000,-1000000,-1000000]
                
                x = 'x' + str(xs)
                if not boxs[ibcy]['text'].__contains__(x):
                    boxs[ibcy]['text'][x] = []

                boxs[ibcy]['xs'].append(xs)
                boxs[ibcy]['text'][x].append(rtext)

                if xs < boxs[ibcy]['box'][0]:
                    boxs[ibcy]['box'][0] = xs 
                if xe > boxs[ibcy]['box'][2]:
                    boxs[ibcy]['box'][2] = xe 

                if ys < boxs[ibcy]['box'][1]:
                    boxs[ibcy]['box'][1] = ys 
                if ye > boxs[ibcy]['box'][3]:
                    boxs[ibcy]['box'][3] = ye

            ibcys = sorted(boxs.keys())
            for i in range(0,len(ibcys)):
                ibcy = ibcys[i]
                rtexts = []
                xss = sorted(list(set(boxs[ibcy]['xs'])))
                #Print2Log('', xss)
                for xs in xss:
                    x = 'x' + str(xs)
                    for t in boxs[ibcy]['text'][x]:
                        rtexts.append(t)

                #Print2Log('', "ParseText: ", ' '.join(rtexts))
                rett.append(' '.join(rtexts))

        if len(xx) and len(yy):
            ttbox= [min(xx), min(yy), max(xx), max(yy)]
    except:
        print(sys._getframe().f_lineno, traceback.format_exc())

    return [rett, ttbox]

class cButton:
    def __init__(self,obj,text='',cmd=None,rs=[],ts=[], tip='', ikey=None):
        self.tip = tip
        self.obj = obj
        self.canvas = obj.canvas
        self.rect_outlineColor = rs[5]
        self.button_bg  = self.canvas.create_rectangle(rs[0],rs[1],rs[2],rs[3],fill=rs[4],outline=rs[5],width=rs[6])
        self.canvas.tag_bind(self.button_bg, "<Button-1>", cmd)
        self.canvas.tag_bind(self.button_bg, "<Motion>", self.cMotion)
        self.canvas.tag_bind(self.button_bg, "<Leave>", self.cLeave)
        obj.buttons.append(self.button_bg)
        self.button_txt_frame_num = None

        if ikey:
            self.obj.active_buttons_bg[ikey] = self.button_bg

        if text:
            text1 = text[0:1]
            self.button_txt = self.canvas.create_text(ts[0],ts[1],text=text1,fill=ts[2],font=ts[3])             
            self.canvas.tag_bind(self.button_txt,"<Button-1>", cmd)
            self.canvas.tag_bind(self.button_txt, "<Motion>", self.cMotion)
            self.canvas.tag_bind(self.button_txt, "<Leave>", self.cLeave)
            obj.buttons.append(self.button_txt)

            if len(text) > 1:
                #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
                fsize = int(8/WindX['win_display_scale'])
                self.button_txt2 = self.canvas.create_text(ts[0],int(ts[1] + (ts[3][1] + fsize)*1.333/2 + 2),text=text[1:],fill=ts[2],font=("Arial",fsize))             
                self.canvas.tag_bind(self.button_txt2,"<Button-1>", cmd)
                self.canvas.tag_bind(self.button_txt2, "<Motion>", self.cMotion)
                self.canvas.tag_bind(self.button_txt2, "<Leave>", self.cLeave)
                obj.buttons.append(self.button_txt2)

        if re.match(r'^Crop\s+Area\s+\#', tip, re.I):
            i = re.sub(r'^Crop\s+Area\s+\#',"", tip, re.I)
            i = re.sub(r'\s*\,\s+isBlank\=.*$',"", i, re.I)
            if len(i):
                fsize = 6
                self.button_txt_frame_num = self.canvas.create_text(int(rs[0] + fsize*1.333/2 + len(str(i))), int(rs[1] + fsize*1.333/2 + 1),text=str(i),fill='blue',font=("Arial",fsize)) 
                obj.buttons.append(self.button_txt_frame_num)

    def cMotion(self,event):
        self.canvas.itemconfig(self.button_bg,outline='red')
        if self.tip:
            self.obj.top.title(self.tip)

    def cLeave(self,event):
        self.canvas.itemconfig(self.button_bg,outline=self.rect_outlineColor)
        self.obj.top.title("Screen Catch - Viewer")


class TopCanvas:
    def __init__(self,sizes,xys,im,todo=None,titleOn=False,iswindow=False,is_snip=False,isWinEdit=False, action_tag=''):
        self.action_tag = action_tag
        self.is_mousedown = 0
        self.rectangle = None
        self.Items = []
        self.buttons = []
        self.mouse_xs = 0
        self.mouse_ys = 0
        self.mouse_xe = 0
        self.mouse_ye = 0
        self.xys   = xys
        self.sizes = sizes
        self.todo = todo
        self.titleOn = titleOn
        self.tip = None
        self.outline_color = 'red'
        self.im = im.copy()
        self.im_array = []
        self.topTempText = None
        self.tmp_addedtexts = []
        self.topTempTextMousePoints = []
        self.canvas_height_offset = 0
        self.topInputTextFontSize = 15
        self.insert_image_do = 0
        self.insert_img = []
        self.imkks = []
        self.ocr_lang_top = None
        self.ocr_lang_sels= ['eng','chi_sim']
        self.ocr_method_to_use_baidu_val = 0
        self.transparent_background_go = False
        self.KeepSelectColor_go = False

        self.iswindow = iswindow
        self.is_snip = is_snip
        self.mask_images = []
        self.canva_mask_images = []
        self.canvas_image_tmp = None

        self.canny_controls = {}
        self.canny_controls_default = {}
        self.im_mouse_last_point_color = []

        self.main_button_width = 40
        if titleOn:
            self.canvas_height_offset = self.main_button_width + 2

        WindX['newRect'] = ""
        WindX['canny_controls_para']['last_key_value'] = []
        WindX['top_level_masks'] = []

        if self.todo == 'snip' or self.todo == 'snip_edit' or self.todo == 'snip_gif':
            self.top = Toplevel(cursor='tcross')
        else:
            self.top = Toplevel()
        self.top.title("Screen Catch - Viewer")

        WindX['Toplevels'].append(self.top)

        print('\nnew toplevel size, x,y:',sizes, xys)
        self.top.wm_attributes('-topmost',1) 
        
        wind_width = sizes[0]
        if self.todo == 'edit' and wind_width < 12* (self.main_button_width + 2):   
            wind_width = 13* (self.main_button_width + 2)
            
        self.padxy_canv = 5
        if iswindow:
            self.padxy_canv = 0

        if not titleOn:
            self.top.overrideredirect(1)                
            self.top.geometry(str(wind_width) + 'x' + str(sizes[1]) + '+' + str(xys[0]) + '+' + str(xys[1]))
        else:
            #self.top.geometry('+' + str(xys[0]) + '+' + str(xys[1]))   
            self.top.geometry(str(wind_width + self.padxy_canv*2) + 'x' + str(sizes[1] + self.canvas_height_offset + self.padxy_canv*2) + '+' + str(xys[0]) + '+' + str(xys[1]))         
        
        self.top.bind("<Key>",self.KeyPress)
        #if iswindow and is_snip:
        #    self.top.wm_attributes('-alpha',0.75)
        self.canvas_bg_color = 'white'     
        self.canvas=Canvas(self.top,
                    width=wind_width,
                    height=sizes[1] + self.canvas_height_offset,
                    bg= self.canvas_bg_color,
                    relief=FLAT,
                    bd = 0,
                    )

        self.canvas.configure(highlightthickness = 0)
        self.canvas.place(x=self.padxy_canv,y=self.padxy_canv)        
        self.canvas.bind("<ButtonRelease-1>",self.MouseUp)
        self.canvas.bind("<Button-1>",self.MouseDown)
        #self.canvas.bind("<B1-Motion>",self.MouseMove)
        self.canvas.bind("<Motion>",self.MouseMove)
        self.canvas.bind("<Leave>",self.MouseLeave)
        self.progress_bar = None
        self.last_progress_percentage = 0
        
        self.im_width = sizes[0] - xys[0]
        self.im_height= sizes[1] - xys[1]
        self.im_x0 = xys[0]
        self.im_y0 = xys[1]

        self.toplevel_message = None
        self.fill_color = "yellow"

        if im:
            if WindXX['e_AddTimeStamp'].get():
                im = self.AutoAddTimeStamp(im)        

            #print("canvas.create_image:",((sizes[0] - xys[0])/2,(sizes[1] - xys[1])/2,im.size),', sizes=',sizes,', xys=',xys)
            imk = ImageTk.PhotoImage(im)             
            #self.canvas.create_image((sizes[0] - xys[0])/2,(sizes[1] - xys[1])/2,image = imk) 
            self.canvas_image = self.canvas.create_image(int(sizes[0]/2),int(sizes[1]/2 + self.canvas_height_offset),image = imk)

            if self.iswindow and self.is_snip:
                self.canvas_mask_rectangle(int(sizes[0]/2),int(sizes[1]/2 + self.canvas_height_offset), self.im_width, self.im_height, fill='black', alpha=0.6)

        #cButton(self,'',self.TDBX,  [0, 0, 480, 40,'#FEFEFE',"#FEFEFE",1],[30, 30,'red',("Arial",20,"bold")])
        scale = re.sub(r'\D+', '', WindXX['e_WinDisplayScale'].get())
        if not scale:
            scale = 100
        
        scale = int(scale)
        if scale > 250:
            scale = 250
        elif scale < 80:
            scale = 80
        WindXX['e_WinDisplayScale'].set(scale)
        WindX['win_display_scale'] = scale / 100

        fsize = int(20/WindX['win_display_scale'])
        ftop = int(fsize*1.33 /2 + 2)
        if isWinEdit or self.todo == 'edit':
            cButton(self,'XClose',self.Close,
                    [0, 0, self.main_button_width, self.main_button_width,'#E0E0E0',"#E0E0E0" ,1],
                    [int(self.main_button_width/2), ftop,'red',("Arial",fsize,"bold")], 
                    tip='Close this window'
                )

        self.active_buttons={
            'sel_color': 0,
            'sel_color2': 0,
            'draw_rectangle': 1,
            'draw_text': 0,
            'draw_line': 0,
            'undo':0,
            'save':0,
            'copy':0,
            'base64':0,
            'insert':0,
            'ocr':0,
            'snip_edit':0,
            'transparent':0,
            'keep_sel_color': 0,
            'canny':0,
            'fill_color':0,
            'delete_all':0,
            'mosaic':0,
            'time_stamp':0
        }
        self.active_buttons_bg = {}
        self.plug_buttons_yes = {
            'fill_color': False,
            'mosaic': False,
            'time_stamp': False
        }
        self.to_draw_items = {
            'draw_text': False,
            'draw_rectangle': True,
            'draw_line': False,
            'time_stamp': False
        }

        self.drawn_line_index = None
        self.text_box_index = None

        print("self.todo=", self.todo)

        if self.todo == 'edit' or self.todo == 'snip_edit':
            self.im_array = numpy.array(im.copy())
            print("self.im_array.shape=", self.im_array.shape)  #height width channels
        
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
            #cButton(self,'',self.OutLineColor1,[41, 0, 61, 20,'red',"red",1], tip='Select red color')
            #cButton(self,'',self.OutLineColor2,[61, 0, 81, 20,'green',"green",1], tip='Select green color')
            #cButton(self,'',self.OutLineColor3,[41, 20, 61, 40,'black',"black",1], tip='Select black color')
            #cButton(self,'',self.OutLineColor4,[61, 20, 81, 40,'yellow',"yellow",1], tip='Select yellow color')
            
            TESSDATA_PREFIX = os.getenv('TESSDATA_PREFIX')
            if not TESSDATA_PREFIX:
                TESSDATA_PREFIX = 1   #make sure app diaplsy ORC button

            self.active_buttons_para={ 
                #[Is to show, Text, Tip, command, font color]
                'sel_color': [1,'CColor', 'Select outline color', self.SelectColorForOutline, 'blue'],
                'sel_color2': [1,'BBColor', 'Select background color', self.SelectColorForBackground, 'blue'],
                'save': [1,'SSave', 'Save', self.Save, 'blue'],
                'copy': [1,'CCopy', 'Copy to clipboard', self.Copy2Clipboard, 'blue'],
                'base64': [1,'BBase64', 'Copy to clipboard with HTML base64 format', self.Copy2ClipboardBase64, 'blue'],

                'draw_rectangle': [1,'RRect', 'Draw rectangle', self.AddRectangle, 'blue'],
                'draw_line': [1,'LLine', 'Draw line', self.AddLine, 'blue'],
                'draw_text': [1,'TText', 'Set text', self.AddText, 'blue'],
                'undo': [1,'UUndo', 'Undo', self.Undo, 'gray'],
                'delete_all': [1, 'DDelete', 'Delete all and clean the canvas', self.CanvasClean, 'blue'],
                
                'insert': [1,'IInsert', 'Insert image from clipboard', self.InsertImage, 'blue'],
                'ocr': [TESSDATA_PREFIX,'OOCR', 'Optical Character Recognition (OCR)', self.ImageOCR, 'blue'],
                #'snip_edit': [1, 'ES+E', 'Snip window and edit image', self.SnipEdit, 'blue'],
                'transparent': [1, 'TTrans.', 'Transparent image background', self.Transparent, 'blue'],
                'keep_sel_color': [1, 'KKeep', 'Keep the selected color only', self.ImageKeepSelectColor, 'blue'],
                
                'canny': [1, 'CCanny.', 'Canny image for its contours', self.ImageCanny, 'blue'],
                'fill_color': [1, 'FFill', 'Fill color for rectangle', self.FillColor, 'blue'],                
                'mosaic': [1, 'MMosaic', 'add mosaic', self.AddMosaic, 'blue'],
                'time_stamp': [1, 'TTime', 'add time stamp', self.AddTimeStamp, 'blue']
            }
            px = 41
            for b in self.active_buttons_para:
                if self.active_buttons_para[b][0]:
                    ibg = "#E0E0E0"
                    if self.active_buttons[b]:
                        ibg = '#00CC99'
                    cb = cButton(
                            self,
                            self.active_buttons_para[b][1], #Text
                            self.active_buttons_para[b][3], #command
                            [px, 0, px+ self.main_button_width, self.main_button_width,ibg,"#E0E0E0",1],
                            [px + int(self.main_button_width/2), ftop, self.active_buttons_para[b][4], ("Arial",fsize,"normal")], 
                            tip = self.active_buttons_para[b][2], 
                            ikey= b
                        )                
                    if b == 'undo':
                        self.button_delLast_txt = cb.button_txt 
                    px += 41

            try:
                self.canvas.itemconfig(self.active_buttons_bg['sel_color'],fill=self.outline_color)
                self.canvas.itemconfig(self.active_buttons_bg['sel_color2'],fill= self.fill_color)
            except:
                pass

        if titleOn and im:
            t1 = threading.Timer(0.1, self.SetBackground)
            t1.start()

        self.top.mainloop()

    def TDBX(self,event):
        return 0

    def SelectColorForOutline(self,event):
        self.ButtonActivate('sel_color')
        
        sel_color = icolorchooser.askcolor()
        print("\nselected color", sel_color, "\n")
        self.outline_color = sel_color[1]
        self.canvas.itemconfig(self.active_buttons_bg['sel_color'],fill=self.outline_color)

    def SelectColorForBackground(self,event):
        self.ButtonActivate('sel_color2')
        
        sel_color = icolorchooser.askcolor()
        print("\nselected color", sel_color, "\n")
        self.fill_color = sel_color[1]
        self.canvas.itemconfig(self.active_buttons_bg['sel_color2'],fill= self.fill_color)

    def CanvasClean(self,event):
        while len(self.Items):
            self.Undo()

    def AutoAddTimeStamp(self, im):
        try:
            font_type = None    
            try:
                font_type = ImageFont.truetype(font='C:/Windows/Fonts/Arial.ttf',size=10)
            except:
                print(traceback.format_exc())

            timestamp = time.strftime("-*- %Y-%b-%d %H:%M:%S %z -*-",time.localtime(time.time()))
            ts_w = len(timestamp)*10

            isize = im.size
            x0 = 1
            y0 = 1
            foreColor = []

            height = 15
            boxes = [
                (0,0,isize[0],height),
                (0,0,int(isize[0]/2),height),
                (int(isize[0]/2),0,isize[0],height),
                (0,isize[1] - height, isize[0], isize[1]),
                (0,isize[1] - height, int(isize[0]/2), isize[1]),
                (int(isize[0]/2), isize[1] - height, isize[0], isize[1])
            ]
            selbox = []
            for b in boxes:
                imc = im.crop(b)
                if Image_IsBlank(numpy.array(imc.copy()), 'add-time-stamp'):
                    x0 = b[0]
                    y0 = b[1]
                    selbox = b
                    break
            if not len(selbox):
                selbox = boxes[0]

            imc = im.crop(selbox)
            bgColorX = Image_getBGColor(numpy.array((imc.copy()).convert("RGB")))
            
            for i in range(3):
                x = bgColorX[i] + 70
                if x > 255:
                    x = bgColorX[i] - 70
                if x < 0:
                    x = 0
                foreColor.append(x)

            print('AutoAddTimeStamp foreColor=',tuple(foreColor), ', from ', bgColorX, ", box=", selbox, ", text-len=", len(timestamp))
            draw = ImageDraw.Draw(im)
            draw.text((x0,y0), timestamp, fill = tuple(foreColor), font=font_type)    
        except:
            print(traceback.format_exc())

        return im   
            
    def plug_buttons_check(self, bnow):        
        self.ButtonActivate(bnow)
        if self.plug_buttons_yes[bnow]:
            self.plug_buttons_yes[bnow] = False
        else:
            for b in self.plug_buttons_yes.keys():
                if b == bnow:
                    self.plug_buttons_yes[b] = True
                else:
                    self.plug_buttons_yes[b] = False

        for b in self.plug_buttons_yes.keys():
            if self.active_buttons_bg.__contains__(b):
                if self.plug_buttons_yes[b]:
                    self.canvas.itemconfig(self.active_buttons_bg[b],fill='#00CC99')
                else:
                    self.canvas.itemconfig(self.active_buttons_bg[b],fill='#E0E0E0')

    def AddTimeStamp(self, event):
        self.plug_buttons_check('time_stamp')

    def AddMosaic(self, event):
        self.plug_buttons_check('mosaic')

    def FillColor(self,event):
        self.plug_buttons_check('fill_color')

    def KeyPress(self, event):
        #char = event.char
        #print('key char:{}'.format(char))
        key_code = event.keycode
        #print('key code:{}'.format(key_code))
        if key_code == 27: #Esc
            self.top.destroy()

    def message_show(self,msg="", bg='#FFFF66', fg='red', stayOn=3):
        self.message_hide()
        self.toplevel_message = Label(self.top, text=msg, bg=bg, fg=fg, padx=5, pady=5)
        self.toplevel_message.place(x=self.padxy_canv,y=self.padxy_canv + self.canvas_height_offset)
        self.top.update()
        t1 = threading.Timer(stayOn, self.message_hide)
        t1.start()
        
    def message_hide(self):
        if self.toplevel_message:
            self.toplevel_message.destroy()
            self.toplevel_message = None

    def canvas_progress_bar(self,n,nn):
        if n == 1:
            self.last_progress_percentage = 0
            if self.progress_bar:            
                self.canvas.delete(self.progress_bar)

        pc = int(n / nn * 1000)/10
        if pc != self.last_progress_percentage:
            self.last_progress_percentage = pc
            x2 = int(self.im.size[0]*n / nn)
            if self.progress_bar:
                self.canvas.coords(self.progress_bar,(0,self.canvas_height_offset,x2,self.padxy_canv+self.canvas_height_offset))
            else:
                self.progress_bar = self.canvas.create_rectangle(0,self.canvas_height_offset,x2,self.padxy_canv+self.canvas_height_offset,fill='red',width=0)
            self.top.update()

        if n==nn and n > 1 and self.progress_bar:
            self.canvas.delete(self.progress_bar)  
            self.progress_bar = None  

    def SetBackground(self):            
        try:     
            self.canvas_bg_color = 'white'       
            imx = self.im.crop([0,0,self.im.size[0],10])
            bgColorX  = Image_getBGColor(numpy.array((imx).convert("RGB")))
            icbg = ColorRGB_to_Hex([255-bgColorX[0], 255-bgColorX[1], 255-bgColorX[2]])
            self.top.configure(background= icbg)
            self.canvas.configure(bg = icbg)
            self.canvas_bg_color = icbg
            #self.canvas.create_rectangle(0,0,self.im_width,self.canvas_height_offset,fill=icbg,width=0)
        except:
            print(traceback.format_exc())

    def ImageKeepSelectColor(self, event=None):        
        self.ButtonActivate('keep_sel_color')
        print("Keep Select Color!!")
        messagebox.showinfo("Tip","After the cursor shape is changed\n\nplese click on a point to keep the color on the image")
        t1 = threading.Timer(1, self.ImageKeepSelectColorPre)
        t1.start()
        
    def ImageKeepSelectColorPre(self):
        self.KeepSelectColor_go = True
        self.is_mousedown = 0
        self.top.configure(cursor='target')
    
    def ImageKeepSelectColorGo(self,event):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
        dxy = 0
        dwh = 1
        im,err = ScreenShotXY(
            width = dwh,
            height= dwh,
            xSrc  = int(rect[0] + event.x - dxy),
            ySrc  = int(rect[1] + event.y - dxy + self.canvas_height_offset)
        )
        if isinstance(im, Image.Image) or IsTrue(self.im_mouse_last_point_color):
            selcolor = []

            if IsTrue(self.im_mouse_last_point_color):
                selcolor = self.im_mouse_last_point_color.tolist()
                selcolor.append(255)
            else:
                #bgColorX  = Image_getBGColor(numpy.array(im))
                #print("\nselected to keep color: bgColorX=", bgColorX, ColorRGB_to_Hex(str(bgColorX[0]) + ',' + str(bgColorX[1]) + ',' + str(bgColorX[2])))
                im = im.convert("RGBA")
                clist = numpy.array(im).tolist()
                print("clist=", clist)
                #clist= [
                # [[187, 142, 88, 255], [197, 152, 99, 255], [208, 163, 109, 255]], 
                # [[180, 137, 83, 255], [197, 153, 99, 255], [210, 166, 113, 255]], 
                # [[180, 136, 83, 255], [196, 153, 99, 255], [207, 164, 111, 255]]
                # ]
                #image size 3x3 
                #one pint: clist= [[[30, 30, 30, 255]]]
                selcolor = clist[0][0]

            d = 60
            print("\nselected to keep color:",selcolor, ColorRGB_to_Hex(str(selcolor[0]) + ',' + str(selcolor[1]) + ',' + str(selcolor[2])), ", RGB tolerance=",d)
            img = self.GetThisImage()
            if isinstance(img, Image.Image):
                img = img.convert("RGBA")
                pixdata = img.load()
                n = 0
                nn = img.size[1]*img.size[0]
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        n+=1
                        self.canvas_progress_bar(n,nn)
                        if (abs(pixdata[x, y][0] - selcolor[0]) <= d and abs(pixdata[x, y][1] - selcolor[1]) <= d and abs(pixdata[x, y][2] - selcolor[2]) <= d):
                            pixdata[x, y] = (selcolor[0], selcolor[1], selcolor[2], selcolor[3])
                        else:
                            pixdata[x, y] = (255 - selcolor[0], 255 - selcolor[1], 255 - selcolor[2], pixdata[x, y][3])
            
            output=BytesIO()
            #img.show()
            img.save(output, format='PNG')
            img = Image.open(output)
            img = img.copy()
            self.imk_tmp = ImageTk.PhotoImage(img)    
            self.canvas.itemconfig(self.canvas_image, image=self.imk_tmp)
            PicSaveToClipboard(im=img, self=self)
            #GetPara()
            #PicSave(im=img,close_edit_win=False) 
            self.im_array = numpy.array(img.copy())

            output.close()
        self.ButtonActivate('')        

    def ImageCanny(self,event=None):
        self.ButtonActivate('canny')
        self.ImageCannyUI()
        self.ImageCanny_ParaChange()

    def ImageCanny_ParaChange(self, event=None):        
        self.ImageCannyUI_ScaleValue(None,printX=True)

        keyvalue = [] 
        for s in self.canny_controls.keys():
            if re.match(r'^scale\_', s, re.I):
                keyvalue.append(WindX['canny_controls_para'][s])
        if WindX['canny_controls_para'].__contains__('last_key_value') and len(WindX['canny_controls_para']['last_key_value']):
            if WindX['canny_controls_para']['last_key_value'] == keyvalue:
                return
        WindX['canny_controls_para']['last_key_value'] = keyvalue

        self.canva_mask_images.append(ImageTk.PhotoImage(self.im.copy()))           
        ximage = self.canvas.create_image(int(self.im.size[0]/2),int(self.im.size[1]/2 + self.canvas_height_offset),image = self.canva_mask_images[-1])
        self.Items.append(ximage)
        self.top.update()

        self.ImageCannyUI_Enabled(False)
        p = threading.Thread(target=self.ImageCannyRun)
        p.start()

    def ImageCannyUI_Enabled(self,is_enabled=True):
        for s in self.canny_controls.keys():
            if is_enabled:
                self.canny_controls[s].configure(state='normal')
            else:
                self.canny_controls[s].configure(state='disabled')

    def ImageCannyUI_Destory(self,event=None):
        for s in self.canny_controls.keys():
            if self.canny_controls[s]:
                if re.match(r'^scale\_', s, re.I):
                    WindX['canny_controls_para'][s] = self.canny_controls[s].get()
                self.canny_controls[s].destroy()
            self.canny_controls[s] = None

    def ImageCannyUI_ScaleValue(self,event=None,printX=False):        
        for s in self.canny_controls.keys():
            if re.match(r'^scale\_', s, re.I):
                WindX['canny_controls_para'][s] = self.canny_controls[s].get()
                if s == 'scale_gaussianBlur_ksize' or s == 'scale_aperture_size':
                    if WindX['canny_controls_para'][s] % 2 == 0:
                        WindX['canny_controls_para'][s] = WindX['canny_controls_para'][s] + 1
                        self.canny_controls[s].set(WindX['canny_controls_para'][s])  

                self.canny_controls['label_' + s].config(text= self.canny_controls_default[s][2] + ": " + str(WindX['canny_controls_para'][s]))
                if printX:
                    print("Canny "+str(s)+"=", WindX['canny_controls_para'][s])

    def ImageCannyUI(self,event=None):         
        self.canny_controls_default = {
            #[row, col, name, from, to, default-value,]
            'scale_gaussianBlur_ksize':[0,1,'GaussianBlur Ksize',1,25,3],
            'scale_threshold1':[0,2,'Threshold1', 1, 200, 5], 
            'scale_threshold2':[0,3,'Threshold2', 1, 500, 80],
            'scale_aperture_size': [0,4,'Aperture Size', 3, 7, 3]            
        }
        n = len(self.canny_controls_default.keys())
        iwidth = int((self.im.size[0] - self.padxy_canv*(n*2-1))/(n + 0.2))

        for s in self.canny_controls_default.keys():
            self.canny_controls[s] = Scale(
                self.top, 
                label = '',
                from_= self.canny_controls_default[s][3],
                to   = self.canny_controls_default[s][4],
                troughcolor= 'green',
                borderwidth=1,
                bg = '#A0A0A0',
                fg = 'white',
                orient='horizontal',
                length= iwidth,    
                width = 6,
                sliderrelief="flat",
                showvalue=False,
                name = s,
                command=self.ImageCannyUI_ScaleValue
                )

            if not (WindX['canny_controls_para'].__contains__(s) and WindX['canny_controls_para'][s]):
                WindX['canny_controls_para'][s] = self.canny_controls_default[s][5]     
            self.canny_controls[s].set(WindX['canny_controls_para'][s])

            self.canny_controls[s].place(
                x= self.padxy_canv * self.canny_controls_default[s][1]*2 + iwidth * (self.canny_controls_default[s][1] - 1), 
                y= self.main_button_width * (self.canny_controls_default[s][0] + 1) + self.padxy_canv * (self.canny_controls_default[s][0] + 2) + int(10*1.33) + 7
            )
            self.canny_controls[s].bind("<ButtonRelease-1>", self.ImageCanny_ParaChange)

            self.canny_controls['label_' + s] = Label(
                    self.top,
                    text= self.canny_controls_default[s][2] + ": " + str(WindX['canny_controls_para'][s]),
                    font= ('Arial',8),
                    fg= 'green',
                    width = 20,
                    anchor = W,
                    justify = LEFT
                )
            self.canny_controls['label_' + s].place(
                x= self.padxy_canv * self.canny_controls_default[s][1]*2 + iwidth * (self.canny_controls_default[s][1] - 1),
                y= self.main_button_width * (self.canny_controls_default[s][0] + 1) + self.padxy_canv * (self.canny_controls_default[s][0] + 2) + 1
            )

    def ImageCannyRun(self,event=None):   
        for b in self.to_draw_items.keys():
            self.to_draw_items[b] = False
            if self.plug_buttons_yes.__contains__(b):
                self.plug_buttons_yes[b] = False

        frame = cv2.cvtColor(numpy.array(self.im.copy()), cv2.COLOR_RGB2GRAY)
        gs_frame = cv2.GaussianBlur(frame, (WindX['canny_controls_para']['scale_gaussianBlur_ksize'], WindX['canny_controls_para']['scale_gaussianBlur_ksize']), 0)
        can_frame= cv2.Canny(gs_frame, 
                        WindX['canny_controls_para']['scale_threshold1'], 
                        WindX['canny_controls_para']['scale_threshold2'],
                        apertureSize = WindX['canny_controls_para']['scale_aperture_size']
                    )
        im_canny = Image.fromarray(cv2.cvtColor(can_frame, cv2.COLOR_BGR2RGB))
        #im_canny.show()

        bgColorX  = Image_getBGColor(numpy.array((im_canny.copy()).convert("RGB")))
        bgColorA  = [bgColorX[0], bgColorX[1], bgColorX[2], 255]
        bgColorB  = [bgColorX[0], bgColorX[1], bgColorX[2], 0]
        print("bgColorA=",bgColorA)
        im_canny_A = numpy.array(im_canny.convert('RGBA'))
        print("im_canny_A=", im_canny_A.shape)
        #'''
        nn = im_canny_A.shape[0]*im_canny_A.shape[1]
        n = 0
        for y in range(im_canny_A.shape[0]):
            for x in range(im_canny_A.shape[1]):
                #print(im_canny_A[y,x])
                n+=1
                self.canvas_progress_bar(n,nn)

                if (im_canny_A[y,x] == bgColorA).all():
                    im_canny_A[y,x][3] = 0 #int(255*0.5)

        #'''
        #result = (im_canny_A[:] == bgColorA).all()
        #print(result)
        #im_canny_A[(im_canny_A == bgColorA).all()] = bgColorB
        im_cannyT = Image.fromarray(im_canny_A)

        bg_img = (self.im.copy()).convert('RGBA')  #change to 'RGBA' format
        bg_img.paste(Image.alpha_composite(bg_img, im_cannyT)) #combine the images 
        #bg_img.show()  
        self.canva_mask_images.append(ImageTk.PhotoImage(bg_img))           
        self.canvas_canny_image = self.canvas.create_image(int(self.im.size[0]/2),int(self.im.size[1]/2 + self.canvas_height_offset),image = self.canva_mask_images[-1])
        self.Items.append(self.canvas_canny_image)

        
        if len(self.Items):
            self.canvas.itemconfig(self.button_delLast_txt,fill='blue')
        else:
            self.canvas.itemconfig(self.button_delLast_txt,fill='gray')
                    
        #self.ButtonActivate('')
        print("Canny - done!\n")
        self.ImageCannyUI_Enabled()    

    def canvas_mask_rectangle(self, x1, y1, width, height, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = WindX['main'].winfo_rgb(fill) + (alpha,)
            #print("fill=",fill)
            image = Image.new('RGBA', (width, height), fill)
            self.canva_mask_images.append(ImageTk.PhotoImage(image))
            self.mask_images.append(self.canvas.create_image(x1, y1, image=self.canva_mask_images[-1]))

            WindX['top_level_masks'].append(self.top)

    def canvas_show_buttons(self, istate='normal'):
        for b in self.buttons:
            self.canvas.itemconfigure(b, state=istate)
        self.top.update()

    def Transparent(self,event):
        self.ButtonActivate('transparent')
        print("Transparent image background")
        messagebox.showinfo("Tip","After the cursor shape is changed\n\nplese click on a background point to transparent image background")
        t1 = threading.Timer(1, self.TransparentPre)
        t1.start()
        
    def TransparentPre(self):
        self.transparent_background_go = True
        self.is_mousedown = 0
        self.top.configure(cursor='target')
    
    def TransparentGo(self,event):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
        im,err = ScreenShotXY(
            width = 1,
            height= 1,
            xSrc  = int(rect[0] + event.x),
            ySrc  = int(rect[1] + event.y + self.canvas_height_offset)
        )
        if isinstance(im, Image.Image):
            im = im.convert("RGBA")
            bgcolor = (numpy.array(im).tolist())[0][0]
            print("\nselected background color:",bgcolor)

            img = self.GetThisImage()
            if isinstance(img, Image.Image):
                img = img.convert("RGBA")
                pixdata = img.load()
                n = 0
                nn = img.size[1]*img.size[0]
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        n+=1
                        self.canvas_progress_bar(n,nn)
                        if pixdata[x, y][0] == bgcolor[0] and pixdata[x, y][1] == bgcolor[1] and pixdata[x, y][2] == bgcolor[2] and pixdata[x, y][3] == bgcolor[3]:
                            pixdata[x, y] = (255, 255, 255, 0)
            
            output=BytesIO()
            #img.show()
            img.save(output, format='PNG')
            img = Image.open(output)
            img = img.copy()
            self.imk_tmp = ImageTk.PhotoImage(img)    
            self.canvas.itemconfig(self.canvas_image, image=self.imk_tmp)
            PicSaveToClipboard(im=img, self=self)
            GetPara()
            PicSave(im=img,close_edit_win=False) 
            self.im_array = numpy.array(img.copy())

            output.close()
        self.ButtonActivate('')

    def SnipEdit(self, event):
        self.top.destroy()
        WindX['main'].update()
        time.sleep(0.5)
        SetWindow("snip_edit")

    def ImageOCR(self, event):
        self.ButtonActivate('ocr')

        self.ocr_lang_sel='eng'                
        self.ocr_lang_chbBV = {}
        self.ocr_lang_chbCB = {}
        self.ocr_lang_names = pytesseractLanguages()
        while len(self.Items):
            self.Undo()

        if self.ocr_lang_top:
            self.ocr_lang_top.destroy()

        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b

        tl = Toplevel()
        tl.wm_attributes('-topmost',1)
        tl.title('OCR Options')
        #tl.configure(background='#E0E0E0')
        tl.geometry('+' + str(rect[0]) + '+' + str(rect[1] + self.canvas_height_offset))  
        self.ocr_lang_top = tl
        self.ocr_lang_frm1 = None

        b= iButton(tl,0,0,self.ImageOCR_LangOK,'Go OCR','blue',colspan=5,p=[CENTER,FLAT,5,5,'#FFFF66','#FFFF99',50,N+S+E+W,0,0])
        
        self.ocr_method_to_use_baidu = BooleanVar()
        cb = Checkbutton(tl, text='Use BaiDu PaddleOCR', bg='#E2E2E5', variable=self.ocr_method_to_use_baidu, justify=LEFT, anchor="w", relief=FLAT,pady=3,padx=3)
        cb.grid(row=1,column=0,sticky=E+W+S+N, pady=1,padx=0)
        self.ocr_method_to_use_baidu.set(1)
        cb.bind('<ButtonRelease>',self.ImageOCR_Method_Change)

        lbl1 = Label(tl, text='Zoom Image:', justify=RIGHT, relief=FLAT,pady=3,padx=3, bg='#E2E2E5',anchor='e')
        lbl1.grid(row=1,column=1,sticky=E+W+S+N, pady=1,padx=1) #,rowspan=2
        self.ocr_zoom_image = StringVar()
        e=Entry(tl, justify=LEFT, relief=FLAT, textvariable= self.ocr_zoom_image, width=5)
        e.grid(row=1,column=2,sticky=E+W+S+N,pady=1,padx=1,columnspan=3)  #,rowspan=2
        e.insert(0,2)

        if os.getenv('TESSDATA_PREFIX') and os.environ['TESSDATA_PREFIX'] and os.path.exists(os.environ['TESSDATA_PREFIX']):
            frm1 = Frame(tl,bg='#E0E0E0')
            frm1.grid(row=3,column=0,sticky=E+W,padx=0,pady=0,columnspan=5)

            self.ocr_method_to_use_TESSDATA = BooleanVar()
            cb = Checkbutton(frm1, text='Use TESSDATA OCR (please select 1 ~ 4 languages)', bg='#E2E2E5', variable=self.ocr_method_to_use_TESSDATA, justify=LEFT, anchor="w", relief=FLAT,pady=3,padx=3)
            cb.grid(row=0,column=0,sticky=E+W+S+N, pady=1,padx=0)
            self.ocr_method_to_use_TESSDATA.set(0)
            cb.bind('<ButtonRelease>',self.ImageOCR_Method_Change2)

            self.ocr_lang_frm1 = Frame(tl,bg='#E0E0E0')
            self.ocr_lang_frm1.grid(row=4,column=0,sticky=E+W,padx=0,pady=0,columnspan=5)

            frm1 = ScrollableFrame(self.ocr_lang_frm1,'#E2E2E5')
            frm1.grid(row=1,column=0,sticky=E+W+S+N,pady=0,padx=0)
            frm1.canvas.configure(width=580, height=350)

            icol = 0
            irow = 0
            os.chdir(os.environ['TESSDATA_PREFIX'])
            for f in sorted(glob.glob("*.traineddata")):                
                fname = (re.sub(r'\.traineddata$','',f)).lower()
                #print(fname, f)
                fnameX = fname
                if self.ocr_lang_names.__contains__(fname):
                    fnameX = self.ocr_lang_names[fname]
                else:
                    self.ocr_lang_names[fname] = fname

                icol += 1    
                self.ocr_lang_chbBV[fname] = BooleanVar()
                cb = Checkbutton(frm1.scrollable_frame, text=fnameX, variable=self.ocr_lang_chbBV[fname], justify=LEFT, anchor="w", relief=FLAT,pady=3,padx=3)
                cb.grid(row=irow,column=icol,sticky=E+W+S+N)
                self.ocr_lang_chbCB[fname] = cb
                cb.bind('<Button>',self.ImageOCR_LangSelect)
                cb.bind('<Leave>' ,self.ImageOCR_LangSelect)

                if fname in self.ocr_lang_sels:
                    cb.select()
                    cb.config(bg='green')
                if icol > 2:
                    icol = 0
                    irow +=1

            self.ocr_lang_frm1.grid_remove()

    def ImageOCR_Method_Change(self, event):        
        if not self.ocr_method_to_use_baidu.get():
            self.ocr_lang_frm1.grid_remove()
            self.ocr_method_to_use_TESSDATA.set(0)
        else:
            self.ocr_lang_frm1.grid()
            self.ocr_method_to_use_TESSDATA.set(1)

    def ImageOCR_Method_Change2(self, event):        
        if not self.ocr_method_to_use_TESSDATA.get():
            self.ocr_method_to_use_baidu.set(0)
            self.ocr_lang_frm1.grid()
        else:
            self.ocr_lang_frm1.grid()
            self.ocr_lang_frm1.grid_remove()
            self.ocr_method_to_use_baidu.set(1)

    def ImageOCR_LangSelect(self,event=None):
        sel = []
        for fn in self.ocr_lang_chbBV:
            if self.ocr_lang_chbBV[fn].get():
                if len(sel) < 4:
                    sel.append(fn)
                    self.ocr_lang_chbCB[fn].config(bg='green')
                else:
                    self.ocr_lang_chbBV[fn].set(0)
                    self.ocr_lang_chbCB[fn].config(bg='#EFEFEF')
            else:
                self.ocr_lang_chbCB[fn].config(bg='#EFEFEF')
        if len(sel):
            self.ocr_lang_sel= '+'.join(sel)            
        else:
            self.ocr_lang_sel='eng'
        self.ocr_lang_sels = sel

    def ImageOCR_LangOK(self):
        self.ImageOCR_LangSelect()
        self.ocr_lang_top.destroy()

        self.top.wm_attributes('-topmost',1)
        self.top.update()
        t1 = threading.Timer(0.2, self.ImageOCR_Go)
        t1.start()

    def ImageOCR_Go(self):
        stime = time.time()
        sels = []
        for fn in self.ocr_lang_sels:
            sels.append(self.ocr_lang_names[fn])

        self.top.title("OCR to language ["+ ", ".join(sels) +"], (to_use_baidu="+str(self.ocr_method_to_use_baidu.get())+") ... ...") 
        try:
            im = self.GetThisImage()
            if isinstance(im, Image.Image):
                z = re.sub(r'[^0-9\.]+','',self.ocr_zoom_image.get())
                if not z:
                    z = 2.5
                izoom= float(z)
                self.ocr_method_to_use_baidu_val = self.ocr_method_to_use_baidu.get()
                #imc = im.copy()                    
                results = Image_OCR_Result(im.copy(),isDisplay=True,Tolang=self.ocr_lang_sel,isFind=True,izoom=izoom, ToUse_PaddleOCR=self.ocr_method_to_use_baidu_val, self=self)
                
                if self.ocr_method_to_use_baidu_val:
                    izoom = 1 #always set back to 1, as the zoom rate is correct in Image_OCR_Result when ToUse_PaddleOCR is ture
                    results['image_zoom_rate'] = 1

                if IsTrue(results["image_to_data"]) and results["image_to_data"].__contains__("text") and len(results["image_to_data"]["text"]):
                    ss = []
                    sid = []
                    for i in range(0, len(results["image_to_data"]["text"])):
                        tmp_level = results["image_to_data"]["level"][i]
                        if(tmp_level == 5):
                            ret1 = re.sub(r'^\s+|\s+$','',results["image_to_data"]["text"][i])
                            if ret1:
                                ss.append(results["image_to_data"]["text"][i])
                                sid.append(i)

                    boxs = {}
                    for i in range(0,len(sid)):
                        xs = int(results["image_to_data"]["left"][sid[i]] / izoom)
                        ys = int(results["image_to_data"]["top"][sid[i]]  / izoom  + self.canvas_height_offset)
                        xe = int(xs + results["image_to_data"]["width"][sid[i]]  / izoom)
                        ye = int(ys + results["image_to_data"]["height"][sid[i]] / izoom)
                        rtext = results["image_to_data"]["text"][sid[i]]
                        #cb = cButton(self,'',None,[xs, ys, xe, ye,'',"red",1],[], tip= rtext)
                        #self.Items.append(cb.button_bg)

                        cy = int((ys + ye)/2)
                        #print(cy, xs, rtext)
                        ibcy = cy
                        for bcy in boxs.keys():
                            if abs(bcy - cy) <=5:
                                if xe < boxs[bcy]['box'][0]:
                                    if xe >= boxs[bcy]['box'][0] - 15:
                                        ibcy = bcy
                                        break
                                elif xs > boxs[bcy]['box'][2]:
                                    if xs <= boxs[bcy]['box'][2] + 15:
                                        ibcy = bcy
                                        break

                        if not boxs.__contains__(ibcy):
                            boxs[ibcy] = {}
                            boxs[ibcy]['text'] = {}
                            boxs[ibcy]['xs']   = []
                            boxs[ibcy]['box']   = [1000000,1000000,-1000000,-1000000]
                        
                        x = 'x' + str(xs)
                        if not boxs[ibcy]['text'].__contains__(x):
                            boxs[ibcy]['text'][x] = []

                        boxs[ibcy]['xs'].append(xs)
                        boxs[ibcy]['text'][x].append(rtext)

                        if xs < boxs[ibcy]['box'][0]:
                            boxs[ibcy]['box'][0] = xs 
                        if xe > boxs[ibcy]['box'][2]:
                            boxs[ibcy]['box'][2] = xe 

                        if ys < boxs[ibcy]['box'][1]:
                            boxs[ibcy]['box'][1] = ys 
                        if ye > boxs[ibcy]['box'][3]:
                            boxs[ibcy]['box'][3] = ye

                    ibcy_del = {}
                    ibcys = sorted(boxs.keys())
                    '''
                    for i in range(0,len(ibcys)):
                        if ibcy_del.__contains__(ibcys[i]):
                            continue

                        ib = boxs[ibcys[i]]['box']
                        for j in range(i+1,len(ibcys)):
                            if ibcy_del.__contains__(ibcys[j]):
                                continue

                            jb = boxs[ibcys[j]]['box']
                            if self.BoxsContains(ib,jb):
                                print('#1 ib=',ib,i,', jb=', jb,j, ', ib contains jb')

                                boxs[ibcys[i]]['xs'] = boxs[ibcys[i]]['xs'] + boxs[ibcys[j]]['xs']
                                for x in boxs[ibcys[j]]['text']:
                                    if boxs[ibcys[i]]['text'].__contains__(x):
                                        boxs[ibcys[i]]['text'][x] += boxs[ibcys[j]]['text'][x]
                                    else:
                                        boxs[ibcys[i]]['text'][x] = boxs[ibcys[j]]['text'][x]
                                ibcy_del[ibcys[j]] = 1

                            elif self.BoxsContains(jb,ib):
                                print('#2 ib=',ib,i,', jb=', jb,j, ', jb contains ib')
                                boxs[ibcys[j]]['xs'] = boxs[ibcys[i]]['xs'] + boxs[ibcys[j]]['xs']
                                for x in boxs[ibcys[i]]['text']:
                                    if boxs[ibcys[j]]['text'].__contains__(x):
                                        boxs[ibcys[j]]['text'][x] += boxs[ibcys[i]]['text'][x]
                                    else:
                                        boxs[ibcys[j]]['text'][x] = boxs[ibcys[i]]['text'][x]
                                ibcy_del[ibcys[i]] = 1
                    '''
                    #print("ibcys:", ibcys)
                    #print("ibcy_del:", ibcy_del.keys())
                    rett = []
                    for i in range(0,len(ibcys)):
                        ibcy = ibcys[i]
                        if ibcy_del.__contains__(ibcy):
                            continue

                        rtexts = []
                        xss = sorted(list(set(boxs[ibcy]['xs'])))
                        #print(xss)
                        for xs in xss:
                            x = 'x' + str(xs)
                            for t in boxs[ibcy]['text'][x]:
                                rtexts.append(t)

                        rett.append(' '*int(abs(xss[0]/12)) + ' '.join(rtexts))
                        cb = cButton(self,'',None,
                            [boxs[ibcy]['box'][0] - 1, boxs[ibcy]['box'][1] - 1, boxs[ibcy]['box'][2] + 1, boxs[ibcy]['box'][3] + 1,'',"green",1],
                            [], tip= ' '.join(rtexts))
                        self.Items.append(cb.button_bg)
                        if cb.button_txt_frame_num:
                            self.Items.append(cb.button_txt_frame_num)
                    
                    if len(rett):
                        TextStringToClipboard(text= "\n".join(rett))
                        print("\nImage OCR\n--------------------------------------------")
                        print("\n".join(rett))
                        print("--------------------------------------------\n")  
                        self.canvas.itemconfig(self.button_delLast_txt,fill='blue')
                        messagebox.showwarning(title='Warning', message="OCR result is copied to Clipboard now!")
                elif len(results['image_to_string']):
                    for line in results['image_data_paddle']:
                        '''
                        Print2Log('', line)
                        #结果是一个list，每个item包含了文本框，文字和识别置信�?
                        [   
                            [[24.0, 36.0], [304.0, 34.0], [304.0, 72.0], [24.0, 74.0]], 
                            ['纯臻营养护发�?, 0.964739]
                        ]
                        '''
                        izoom = results['image_zoom_rate']
                        if line[1][0] and not self.ocr_method_to_use_baidu_val:
                            xx = sorted(list(set([line[0][0][0], line[0][1][0], line[0][2][0], line[0][3][0]])))
                            yy = sorted(list(set([line[0][0][1], line[0][1][1], line[0][2][1], line[0][3][1]])))                                
                            ibox = [int(xx[0]/izoom), int(yy[0]/izoom + self.canvas_height_offset), int(xx.pop()/izoom), int(yy.pop()/izoom + self.canvas_height_offset)]
                            
                            lcolor = "green"
                            if re.match(r'^Crop\s+Area\s+\#', str(line[1][0]), re.I):
                                lcolor = '#FF66FF'
                            
                            cb = cButton(self,'',None,
                                [ibox[0] - 1, ibox[1] - 1, ibox[2] + 1, ibox[3] + 1,'', lcolor,1],
                                [], tip= str(line[1][0]))
                            self.Items.append(cb.button_bg)
                            if cb.button_txt_frame_num:
                                self.Items.append(cb.button_txt_frame_num)

                    parse = Image_OCR_ParseText_for_PaddleOCR(results,izoom)
                    TextStringToClipboard(text= "\n".join(parse[0]))

                    #print("\n\n","\n".join(parse[0]), "\n", parse[1],"\n\n")
                    print("\nImage OCR\n--------------------------------------------")
                    print("\n".join(parse[0]))
                    print("--------------------------------------------\n")  
                    self.canvas.itemconfig(self.button_delLast_txt,fill='blue')
                    print("\nused time " + usedTime(stime))
                    messagebox.showwarning(title='Warning', message="OCR result is copied to Clipboard now!")
                else:
                    messagebox.showwarning(title='OCR Warning', message= "Try OCR but no text found!!")
        except:
            print("Try OCR to the language ["+ ", ".join(sels) +"],\nand get error:\n" + traceback.format_exc())
            messagebox.showwarning(title='OCR Warning', message= "Try OCR to the language\n-- "+ "\n-- ".join(sels) +"\nthen get the error:\n\n" + traceback.format_exc())

        self.top.title("Screen Catch - Viewer")
        print("\n-------- ImageOCR_Go - End, total used time " + usedTime(stime) + " --------")
        self.ButtonActivate('')

    def BoxsContains(self, ib=[0,0,0,0], jb=[0,0,0,0]):  #[left top right bottom]
        if ib[0] <= jb[0] and ib[2] >= jb[2] and ib[1] <= jb[1] and ib[3] >= jb[3]:            
            return True
        else:
            return False

    def InsertImage(self, event):        
        #check if there's image data in clicpboard 
        for b in self.to_draw_items.keys():
            self.to_draw_items[b] = False
            if self.plug_buttons_yes.__contains__(b):
                self.plug_buttons_yes[b] = False

        self.insert_image_do = 0   
        self.insert_img = []
        try:
            win32clipboard.OpenClipboard() #打开剪贴�?
            #
            #im.convert("RGB").save(output, "BMP")
            #data = output.getvalue()[14:]
            #output.close()
            data = win32clipboard.GetClipboardData(win32con.CF_DIB)
            if data:
                cf= BytesIO(data)  
                cim = Image.open(cf)  
                self.insert_img = numpy.array(cim)
                self.insert_image_do = 1
                cf.close()
                self.ButtonActivate('insert')
                self.top.configure(cursor='tcross')
            else:
                messagebox.showwarning(title='Warning', message='No image in the clicpboard!')
                self.ButtonActivate('')
            
            win32clipboard.CloseClipboard()
        except:            
            win32clipboard.CloseClipboard()
            messagebox.showwarning(title='Warning', message='No image in the clicpboard!')
            print(traceback.format_exc())
            self.ButtonActivate('')

    def Copy2ClipboardBase64(self,event):        
        self.Copy2Clipboard(event,p='base64')

    def Copy2Clipboard(self,event,p=''):    
        if p == 'base64':
            self.ButtonActivate('base64')
        else:
            self.ButtonActivate('copy')
            
        try:   
            self.canvas_show_buttons('hidden')
            im = self.GetThisImage()

            if isinstance(im, Image.Image):                    
                PicSaveToClipboard(im=im, p=p, self=self)
            else:
                print("Failed to get screenshot!")
                WindX['e_ImageCateched'].config(text="Failed to get screenshot!",fg='red')               
        except:
            print(traceback.format_exc()) 

        self.canvas_show_buttons('normal')

    def GetThisImage(self):
        self.top.wm_attributes('-topmost',1)
        self.top.update()

        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
        #ShowMainWindow(0)
        im,err = ScreenShotXY(
            width = self.sizes[0], #int(rect[2] - rect[0]),
            height=int(rect[3] - rect[1] - self.canvas_height_offset),
            xSrc  =int(rect[0]),
            ySrc  =int(rect[1] + self.canvas_height_offset)
        )
        #ShowMainWindow(1)
        return im

    def Save(self,event):
        self.ButtonActivate('save')

        if self.todo == 'edit':
            for b in self.buttons:
                self.canvas.delete(b)
            self.top.update()  
            #print("\nsave edited image ...\n")   
            if self.titleOn:                 
                try:                     
                    im = self.GetThisImage()
                    if isinstance(im, Image.Image):                    
                        GetPara(0)
                        imCopy = im.copy()
                        PicSaveToClipboard(im=imCopy)
                        PicSave(im=im, close_edit_win=False)                           
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

    def Undo(self,event=None):
        self.ButtonActivate('undo')
        if len(self.Items):
            self.canvas.delete(self.Items.pop())
        elif self.rectangle:
            self.canvas.delete(self.rectangle)
            self.rectangle = None
        self.ButtonActivate('')

    def AddRectangle(self,event):
        self.ButtonActivate('draw_rectangle')

    def AddText(self,event):
        self.ButtonActivate('draw_text')

    def AddLine(self,event):
        self.ButtonActivate('draw_line')

    def ButtonActivate(self, bttn):
        self.ImageCannyUI_Destory()
        self.top.configure(cursor='arrow')

        for b in self.to_draw_items.keys():
            if b == bttn:
                self.to_draw_items[b] = True
            else:
                self.to_draw_items[b] = False
                if self.plug_buttons_yes.__contains__(b):
                    self.plug_buttons_yes[b] = False

        for b in self.active_buttons:
            if (self.plug_buttons_yes.__contains__(b) and self.plug_buttons_yes[b]) or b == 'sel_color' or b == 'sel_color2':
                continue
    
            if b == bttn:
                self.active_buttons[b] = 1
            else:
                self.active_buttons[b] = 0

            if self.active_buttons_bg.__contains__(b):
                if self.active_buttons[b]:
                    self.canvas.itemconfig(self.active_buttons_bg[b],fill='#00CC99')
                    if b == 'insert':
                        self.top.configure(cursor='tcross')
                else:
                    self.canvas.itemconfig(self.active_buttons_bg[b],fill='#E0E0E0')

        self.top.update()

    def TextInputView(self,event):
        if self.topTempText:
            if event.keycode == 17:
                self.topInputTextCtrlPress = 0

            inputText = re.sub(r'\n+$','',self.topTempTextWedget.get("0.0", "end"))
            if len(self.tmp_addedtexts):
                for xt in self.tmp_addedtexts:
                    self.canvas.delete(xt)
            self.tmp_addedtexts = []

            if len(inputText):
                if self.to_draw_items['draw_text'] and self.rectangle:
                    lines = re.split(r'\n', inputText)
                    lineH = int(self.topInputTextFontSize*1.33 + 3) #int(abs(self.topTempTextMousePoints[3] - self.topTempTextMousePoints[1] - 3*(len(lines) + 1)) / len(lines))             
                    fsize = self.topInputTextFontSize #int(lineH / 1.33)  #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
                    
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

                            rect = win32gui.GetWindowRect(self.topTempTextOnBottom_xyz[2])  #left top right bottom   l, t, r, b
                            if self.topTempTextOnBottom and (rect[1] + y + lineH/2 + 3 > self.topTempTextOnBottom_xyz[1]):
                                self.topTempTextOnBottom_xyz[1] = int(rect[1] + y + lineH/2 + 3)
                                self.topTempText.geometry('+' + str(self.topTempTextOnBottom_xyz[0]) + '+' + str(self.topTempTextOnBottom_xyz[1]))
                                
                            y += lineH + 3
                    self.top.update()

    def TextInputViewKeyPress(self,event):        
        if event.keycode == 17:
            self.topInputTextCtrlPress = 1
        elif self.topInputTextCtrlPress and event.keycode==38:
            self.topInputTextFontSize +=1
        elif self.topInputTextCtrlPress and event.keycode==40:
            self.topInputTextFontSize -=1

        if self.topInputTextFontSize < 2:
            self.topInputTextFontSize = 2

        fontStyle = tkFont.Font(family='Arial', size= self.topInputTextFontSize)
        self.topTempTextWedget.configure(font=fontStyle)
        #print(self.topInputTextFontSize, event.keycode)

    def MouseUp(self,event):
        #print('Canvas mouse up:', event, self.todo)
        if self.transparent_background_go:
            self.transparent_background_go = False
            self.top.configure(cursor='arrow')
            self.is_mousedown = 0
            return

        if self.KeepSelectColor_go:
            self.KeepSelectColor_go = False
            self.top.configure(cursor='arrow')
            self.is_mousedown = 0
            return

        if self.text_box_index:
            self.canvas.delete(self.text_box_index)
            self.text_box_index = None

        self.is_mousedown = 0   
        self.mouse_xe = event.x
        self.mouse_ye = event.y 
        if self.mouse_ye <= self.canvas_height_offset:
            if self.rectangle:
                self.canvas.delete(self.rectangle)
            self.rectangle = None
            return

        if self.todo == 'snip' or self.todo == 'snip_edit' or self.todo == "snip_gif":
            self.Close(event,1)
        elif self.todo == 'edit':
            if self.to_draw_items['draw_rectangle'] and self.rectangle:
                self.Items.append(self.rectangle)
                self.rectangle = None

            elif self.plug_buttons_yes['time_stamp']:            
                fsize = self.topInputTextFontSize #int(lineH / 1.33)  #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
                textbox = self.canvas.create_text(
                            event.x,
                            event.y,
                            font = ('Arial', fsize, 'normal'),
                            text = time.strftime("%Y-%b-%d %H:%M:%S %z",time.localtime(time.time())),
                            fill= self.outline_color,
                            anchor = W,
                            justify = LEFT)
                self.Items.append(textbox)

            elif self.to_draw_items['draw_text'] and self.rectangle:                
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

                    self.topTempTextOnBottom = 1
                    x = rect[0] + mm['xmin'] + 1
                    y = rect[1] + mm['ymin'] + 1 + th
                    if y + th*2 > rect[3]:
                        y = rect[1] + mm['ymin'] - th - 1
                        self.topTempTextOnBottom = 0

                    self.topTempText = Toplevel()
                    self.topTempText.wm_attributes('-topmost',1) 
                    self.topTempText.overrideredirect(1)
                    self.topTempText.geometry(str(tw) + 'x' + str(th) + '+' + str(x) + '+' + str(y))
                    self.topTempTextOnBottom_xyz = [x,y,HWND]

                    self.topInputTextCtrlPress = 0
                    fontStyle = tkFont.Font(family='Arial', size=15)
                    self.topTempTextWedget = Text(self.topTempText, padx=5, pady=5, font=fontStyle, fg=self.outline_color, bd=1, highlightcolor='#D0D0D0', relief=FLAT)
                    self.topTempTextWedget.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
                    self.topTempTextWedget.focus()
                    self.topTempTextWedget.bind('<KeyRelease>',self.TextInputView)                     
                    self.topTempTextWedget.bind('<KeyPress>',self.TextInputViewKeyPress)                     
                    WindX['winBalloon'].bind_widget(self.topTempTextWedget, balloonmsg= "[Ctrl + UpArrow] keys to enlarge font size,\n[Ctrl + DownArrow] keys to reduce font size")                 

            elif self.to_draw_items['draw_line'] and self.rectangle and self.drawn_line_index:
                self.canvas.delete(self.rectangle)
                self.Items.append(self.drawn_line_index)
                self.drawn_line_index = None
                self.rectangle  = None

            elif self.insert_image_do and self.rectangle and self.insert_img.any():
                self.canvas.delete(self.rectangle)
                tw = abs(self.mouse_xs - self.mouse_xe)
                th = abs(self.mouse_ys - self.mouse_ye)
                if tw > 5 and th > 5:
                    '''
                    rect = self.canvas.create_rectangle(
                                        self.mouse_xs,
                                        self.mouse_ys,
                                        self.mouse_xe,
                                        self.mouse_ye,
                                        outline = self.outline_color,
                                        width= 2,
                                        )
                    self.Items.append(rect)
                    '''
                    img = Image.fromarray(self.insert_img.astype('uint8'))
                    size = img.size
                    r1 = tw / size[0]
                    r2 = th / size[1]
                    r = 1
                    if r1 > r2:
                        r = r2
                    else:
                        r = r1
                    if r > 1:
                        r = 1                        
                    if not (r == 1):                        
                        img = img.resize((int(size[0]*r), int(size[1]*r)))
                    #print("size:",img.size, ", format:", img.format, ', to size:', tw, th)
                    #img.show()
                    imkk = ImageTk.PhotoImage(img)             
                    iim = self.canvas.create_image(int((self.mouse_xs + self.mouse_xe)/2),int((self.mouse_ys + self.mouse_ye)/2) ,image = imkk)
                    self.imkks.append([iim,imkk])
                    self.Items.append(iim)

                self.insert_image_do = 0
                self.insert_img = []
                self.ButtonActivate('')
                #print('insert image #', iim)

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
                if self.to_draw_items['draw_text'] and self.rectangle:
                    lines = re.split(r'\n', inputText)  
                    lineH = int(self.topInputTextFontSize*1.33 + 3) #int(abs(self.topTempTextMousePoints[3] - self.topTempTextMousePoints[1] - 3*(len(lines) + 1)) / len(lines))             
                    fsize = self.topInputTextFontSize #int(lineH / 1.33)  #A point (pt) is equal to 0.352778 millimeters, 0.0138889 inches, or 1.333 pixels
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

        elif self.transparent_background_go:
            self.TransparentGo(event)
            
        elif self.KeepSelectColor_go:
            self.ImageKeepSelectColorGo(event)

        self.topTempTextMousePoints = []

    def MouseMove(self,event):
        #print(event, self.is_mousedown)
        if self.tip:
            self.canvas.delete(self.tip)
            self.tip = None

        if self.is_mousedown:
            self.canvas.configure(bg = self.canvas_bg_color)

            if self.to_draw_items['draw_rectangle'] or self.todo == 'snip' or self.to_draw_items['draw_text'] or self.to_draw_items['draw_line'] or self.insert_image_do:
                if self.rectangle:
                    self.canvas.delete(self.rectangle)
                
                iwidth = 2
                idash = ()
                if self.to_draw_items['draw_text'] or self.to_draw_items['draw_line'] or self.todo == 'snip' or self.todo == 'snip_edit':
                    iwidth = 1
                    idash = (4,4)
                
                if self.iswindow and self.is_snip:
                    if IsTrue(self.canvas_image_tmp):
                        self.canvas.delete(self.canvas_image_tmp)

                    xs = self.mouse_xs
                    xe = event.x
                    if xs > xe:
                        xs = event.x
                        xe = self.mouse_xs
                    ys = self.mouse_ys
                    ye = event.y
                    if ys > ye:
                        ys = event.y
                        ye = self.mouse_ys

                    imcrop = self.im.crop((xs, ys, xe, ye))
                    self.canvas_image_tmpimk = ImageTk.PhotoImage(imcrop)             
                    self.canvas_image_tmp = self.canvas.create_image(int((xe + xs)/2),int((ye + ys)/2 + self.canvas_height_offset), image = self.canvas_image_tmpimk)
                    #print(imcrop, self.canvas_image_tmp)
                else:
                    if self.plug_buttons_yes['fill_color'] and self.to_draw_items['draw_rectangle']:
                        self.rectangle = self.canvas.create_rectangle(
                                            self.mouse_xs,
                                            self.mouse_ys,
                                            event.x,
                                            event.y,
                                            outline = self.outline_color,
                                            fill= self.fill_color,
                                            width= iwidth,
                                            dash= idash
                                            )
                        
                    elif self.plug_buttons_yes['mosaic'] and self.to_draw_items['draw_rectangle']:
                        self.rectangle = self.canvas.create_rectangle(
                                            self.mouse_xs,
                                            self.mouse_ys,
                                            event.x,
                                            event.y,
                                            outline = '#E0E0E0',
                                            fill= '#E0E0E0',
                                            width= iwidth,
                                            dash= idash
                                            )
                    
                    else:
                        self.rectangle = self.canvas.create_rectangle(
                                            self.mouse_xs,
                                            self.mouse_ys,
                                            event.x,
                                            event.y,
                                            outline = self.outline_color,
                                            width= iwidth,
                                            dash= idash
                                            )
                
                if self.to_draw_items['draw_line']:
                    if self.drawn_line_index:
                        self.canvas.delete(self.drawn_line_index)
                    self.drawn_line_index = self.canvas.create_line(
                                    self.mouse_xs,
                                    self.mouse_ys,
                                    event.x,
                                    event.y,
                                    fill = self.outline_color,
                                    width= 2,
                                    )
                if self.text_box_index:
                    self.canvas.delete(self.text_box_index)
                    self.text_box_index = None

                self.text_box_index = self.canvas.create_text(
                    event.x + 5,
                    self.mouse_ys + 8,
                    font = ('Arial', 10, 'normal'),
                    text = str(abs(event.x - self.mouse_xs)) + "x" + str(abs(event.y - self.mouse_ys)),
                    fill = self.outline_color,
                    anchor = W,
                    justify = LEFT)

                self.top.update()

        elif (self.transparent_background_go or self.KeepSelectColor_go) and IsTrue(self.im_array) and event.x > 0 and event.y > (self.canvas_height_offset + 0):
            px = event.x - 0 - 1
            py = event.y - (self.canvas_height_offset + 0) - 1
            if px < self.im_array.shape[1] and py < self.im_array.shape[0]:     
                try:           
                    #print("self.im_array", px, py, self.im_array[py, px])                     
                    pcolor = self.im_array[py, px]
                    icbg = ColorRGB_to_Hex([pcolor[0], pcolor[1], pcolor[2]])
                    self.canvas.configure(bg = icbg)
                    self.im_mouse_last_point_color = pcolor
                except:
                    pass
        else:
            self.canvas.configure(bg = self.canvas_bg_color)

    def MouseLeave(self,event):
        self.canvas.configure(bg = self.canvas_bg_color)

    def Close(self,event,IsMouseUp=0):
        ToplevelRectHide(idx='win_catch_123456')
        
        if self.text_box_index:
            self.canvas.delete(self.text_box_index)
            self.text_box_index = None
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
                        PicSave(im=im, close_edit_win=False)                  
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

def ShowHideBasic(is_to_hide=True):
    if WindX['ShowHideBasic'] == 1:
        WindX['ShowHideBasic'] = 0
        WindX['Frame1'].grid_remove()
        WindX['e_HideBase'].config(text="⋁")
        WinAnchor()
        WindX['main'].overrideredirect(1)
        StatusShow(0)

        if is_to_hide:
            GUI_Hide_countdown_timer()
    else:
        WindX['ShowHideBasic'] = 1
        WindX['Frame1'].grid()
        WindX['e_HideBase'].config(text="⋀")
        WindX['main'].overrideredirect(0)
        StatusShow(1)

def WinTopGet(x=0):
    y = 0
    GetMonitors()
    if len(WindX['display_scale']):
        for dp in WindX['display_scale']:
            if x >= dp[0] and x <= dp[1]:
                y = dp[2]
                break
    return y

def WinAnchor():
    gs = re.split(r'x|\+', WindX['main'].geometry()) #506x152+-1418+224
    WindX['main'].geometry('+'+ str(gs[2]) +'+' + str(WinTopGet(int(gs[2]))))

def Progressbar_Show():
    while WindX['e_progressbar_on']:
        WindX['e_progressbar'].grid()
        try:
            WindX['e_progressbar']['value'] +=1
            if WindX['e_progressbar']['value'] > 100:
                WindX['e_progressbar']['value'] = 0
            WindX['main'].update()
            time.sleep(1)
        except:
            break

def StatusShow(display=1,auto_hide=0):
    if display:
        WindX['e_progressbar_on'] = 1
        WindX['Frame4'].grid()
        WindX['e_ImageCateched'].grid()        
        if auto_hide:
            t1 = threading.Timer(1, StatusHide_Delay)
            t1.start()
    else:
        WindX['e_progressbar_on'] = 0
        WindX['e_ImageCateched'].grid_remove()
        WindX['e_progressbar'].grid_remove()
        WindX['Frame4'].grid_remove()

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
        time.sleep(0.2)

def GUI_Hide_countdown(t=30):
    WindX['GUI_Hide_countdown_t'] = t
    while WindX['GUI_Hide_countdown_t'] > 0 and not WindX['GUI_Hide_YES'] and not WindX['ShowHideBasic']:
        WindX['e_HideToolbar'].config(text='⇡ ' + str(WindX['GUI_Hide_countdown_t']))
        WindX['main'].update()
        WindX['GUI_Hide_countdown_t'] -= 1
        time.sleep(1)

    if not WindX['GUI_Hide_YES']:
        if WindX['motion_on_frame2_last_time'] and time.time() - WindX['motion_on_frame2_last_time'] > 30:
            GUI_Hide()
        elif not WindX['ShowHideBasic']:
            GUI_Hide_countdown()

    WindX['e_HideToolbar'].config(text='⇡')

def GUI_Hide_countdown_timer():
    if len(WindX['ShowHideBasic2_thread_timers']):
        for t in WindX['ShowHideBasic2_thread_timers']:
            try:
                t.cancel()
            except:
                print(sys._getframe().f_lineno, traceback.format_exc())
    WindX['ShowHideBasic2_thread_timers'] = []

    t1 = threading.Timer(0.01,GUI_Hide_countdown)
    t1.start()
    WindX['ShowHideBasic2_thread_timers'].append(t1)

def GUI_Hide():
    WindX['ShowHideBasic'] =1
    WindX['GUI_Hide_YES']  = True
    ShowHideBasic(is_to_hide=False)
    WindX['Frame0'].grid()
    WindX['Frame1'].grid_remove()
    WindX['Frame2'].grid_remove()
    WindX['Frame3'].grid_remove()
    WindX['Frame4'].grid_remove()

def GUIonFrame0Motion(event=None):
    #print("GUIonFrame0Motion event=", event)
    WindX['GUI_Hide_YES']  = False
    WindX['Frame2'].grid()
    WindX['Frame0'].grid_remove()
    WindX['Frame1'].grid_remove()
    WindX['Frame3'].grid_remove()
    WindX['Frame4'].grid_remove()

    GUIonFrame2Motion()
    GUI_Hide_countdown_timer()    

def GUIonFrame2Motion(event=None):
    WindX['motion_on_frame2_last_time'] = time.time()
    WindX['GUI_Hide_countdown_t'] = 30

def GUI(IsInit=None):
    WindX['load_times'].append([time.time(), 'UI loading: ...'])

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
    WindX['Frame0'] = Frame(WindX['main'], width=120, height=3, bg='yellow')
    WindX['Frame0'].grid(row=0,column=0,sticky=W,pady=0,padx=0)
    WindX['Frame0'].bind('<Motion>', GUIonFrame0Motion)
    WindX['Frame0'].grid_remove()

    WindX['Frame1'] = Frame(WindX['main'])
    WindX['Frame1'].grid(row=1,column=0,sticky=W,pady=5,padx=5)
    WindX['Frame2'] = Frame(WindX['main'])
    WindX['Frame2'].grid(row=2,column=0,sticky=W,pady=0,padx=0)
    #WindX['Frame2'].bind('<Motion>', GUIonFrame2Motion)

    WindX['Frame3'] = Frame(WindX['main'])
    WindX['Frame3'].grid(row=3,column=0,sticky=W,pady=0,padx=0)
    WindX['Frame3'].grid_remove()

    WindX['Frame4'] = Frame(WindX['main'])
    WindX['Frame4'].grid(row=4,column=0,sticky=W,pady=0,padx=0)

    if WindX['Frame1']:
        row = 0 
        Label(WindX['Frame1'], text='Image Format', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['b_PicFormat'] = StringVar()
        b = ttk.Combobox(WindX['Frame1'], textvariable=WindXX['b_PicFormat'], justify=CENTER,state="readonly",width=5)
        b.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        b['values'] = ('jpg','png','ico')
        if WindX['PicFormatStr'] == 'jpg':
            b.current(0)
        elif WindX['PicFormatStr'] == 'png':
            b.current(1)
        else:
            b.current(2)

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

        b.bind("<Motion>", WinFrameShow)
        b.bind("<Leave>",  WinFrameHide)
        b.bind("<<ComboboxSelected>>", WinFrameShow)
                  
        b=iButton(WindX['Frame1'],row,5,WinCustomAdd,'+',None,'#F0F0F0',msg='Set custom window')     

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

        row +=1
        Label(WindX['Frame1'], text='ICO Size', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['e_ICO_Size'] = StringVar()
        e=Entry(WindX['Frame1'], justify=CENTER, relief=FLAT, textvariable= WindXX['e_ICO_Size'],width=4)
        e.insert(0,64)
        e.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        Label(WindX['Frame1'], text='pixel, 1~255', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=3,sticky=W) 

        row +=1
        Label(WindX['Frame1'], text='Display Scale', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=1,sticky=W)
        WindXX['e_WinDisplayScale'] = StringVar()
        e=Entry(WindX['Frame1'], justify=CENTER, relief=FLAT, textvariable= WindXX['e_WinDisplayScale'],width=4)
        e.insert(0,125)
        e.grid(row=row,column=2,sticky=E+W,pady=0,padx=5) 
        Label(WindX['Frame1'], text='% (80-250)', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=3,sticky=W)    

        row +=1
        WindXX['e_AddTimeStamp'] = IntVar()
        ef_chkb = Checkbutton(WindX['Frame1'], text= "Add time stamp", variable= WindXX['e_AddTimeStamp'], justify=LEFT, fg=Lfg, relief=FLAT)
        ef_chkb.grid(row=row,column=1,sticky=W, columnspan=5)
        WindXX['e_AddTimeStamp'].set(1)

    if WindX['Frame2']:
        row =0
        col2 = -1

        col2+=1
        b=iButton(WindX['Frame2'],row,col2, GUI_Hide,'⇡',msg='Hide Window')  
        WindX['e_HideToolbar'] = b.b

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,ShowHideBasic,'⋀',msg='Show / Hide')
        WindX['e_HideBase'] = b.b

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,ShowHideMoreButtons,'Step#',msg='Show more ...') 
        #Label(WindX['Frame2'], text='Step#', justify=LEFT, relief=FLAT,pady=3,padx=3,fg=Lfg).grid(row=row,column=col2,sticky=W)
        
        col2+=1
        WindXX['ImageOrder'] = StringVar()
        e=Entry(WindX['Frame2'], justify=CENTER, relief=FLAT, textvariable= WindXX['ImageOrder'],width=4)
        e.grid(row=row,column=col2,sticky=E+W+N+S,padx=0)
        WindX['e_ImageOrder'] = e
        if WindX['ImageOrderStr']:
            e.insert(0,WindX['ImageOrderStr'])
        else:
            e.insert(0,'1')

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,PicCatch,'Win','red',msg='[Win]: Catch the window which is selected in the field [Catch Window]')

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,lambda:SetWindow("snip_edit"),'S+E','red',msg='[S+E]: Snip window and edit image\nPress [Esc] key to quit its mask window')

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,lambda:SetWindow("snip_edit2"),'S+X','red',msg='[S+X]: Snip window immediately and edit image\nPress [Esc] key to quit its mask window')

        col2+=1
        b=iButton(WindX['Frame2'],row,col2,lambda:SetWindow("snip_gif"),'GIF','red',msg='[GIF]: Snip window and make GIF')
        WindX['e_snip_gif'] = b.b
        
    if WindX['Frame3']:
        row =0
        col2 = -1

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,TBD,'')

        col2+=1        
        e=Entry(WindX['Frame3'], justify=CENTER, relief=FLAT, width=4, bg='#E0E0E0')
        e.grid(row=row,column=col2,sticky=E+W+N+S,padx=0)

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,PreviousPicOrder,'<',msg='Step -1')

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,NextPicOrder,'>',msg='Step +1')

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,PicCatchEdit,'W+E','red',msg='[W+E]: Catch the whole widhow and edit')

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,lambda:SetWindow("snip"),'Snip','red',msg='[Snip]: Snip window then save')

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,lambda:DrawRectangleOnScreen(),'Rect','red',msg='[Rect]: Draw a rectangle on the screen.\n-- Right click to remove last rectangle.')
        WindX['e_add_rectagle'] = b.b

        col2+=1
        b=iButton(WindX['Frame3'],row,col2,lambda:DrawRectangleOnScreen(True),'Wall','red',msg='[Wall]: Draw a rectangle on the screen and fill it as a wall.')
        WindX['e_add_rectagle_wall'] = b.b

    if WindX['Frame4']:
        row =0
        e = Label(WindX['Frame4'], text='', justify=LEFT, fg='#009900',relief=FLAT,pady=3,padx=3)
        e.grid(row=row,column=0,sticky=E+W+N+S,pady=0,padx=0)  #,columnspan=int(col2*3/4)
        WindX['e_ImageCateched'] = e

        #'''
        #row +=1
        e = ttk.Progressbar(WindX['Frame4'], orient=HORIZONTAL, length=200, mode='determinate',value=0,maximum=100) #indeterminate
        #e.grid(row=row,column=int(col2*3/4),sticky=E+W+N+S,pady=0,padx=0,columnspan=20)
        e.grid(row=row,column=1,sticky=E+W+N+S,pady=0,padx=0)
        WindX['e_progressbar'] = e
        WindX['e_progressbar']['maximum'] = 100
        WindX['e_progressbar']['value'] = 0
        WindX['e_progressbar'].grid_remove()
        #'''

    if IsInit:
        HideConsole()
        WindX['main'].update()
        GUI_Hide()

    WindX['load_times'].append([time.time(), 'UI loaded - end.'])
    stime = WindX['load_times'][0][0]
    for s in WindX['load_times']:
        time_used = usedTime(0,s[0] - stime)
        if s[0] == stime:
            time_used = "00:00:00.000"
        print(time.strftime("%H:%M:%S",time.localtime(s[0])), "+"+time_used, s[1])

    mainloop()

def TBD():
    return ""

def WinFrameHide(event=None):
    ToplevelRectHide(idx='win_frame_123456')

def WinFrameShow(event=None):
    GetPara()
    if len(WindX['CatchPoint']):
        ToplevelRect(sizes=[int(WindX['CatchPoint'][0]), int(WindX['CatchPoint'][1])], xys=[int(WindX['CatchPoint'][2]), int(WindX['CatchPoint'][3])], icolor='colorful', idx='win_frame_123456')

def WinCustomAdd(event=None):
    #SetWindow("snip_edit", action_tag='WinCustomAdd')
    WindX['WinCustomAdd_Class'] = TopCustomWind()

def ShowHideMoreButtons(event=None):
    if WindX['ShowHideMoreButtons']:
        WindX['ShowHideMoreButtons'] = False
        WindX['Frame3'].grid_remove()
    else:
        WindX['ShowHideMoreButtons'] = True
        WindX['Frame3'].grid()

def DrawRectangleOnScreen(is2fill=False):
    WindX['DrawRectangleOnScreen_is2fill'] = is2fill

    if WindX['DrawRectangleOnScreen']:
        WindX['DrawRectangleOnScreen'] = 0
        if is2fill:
            WindX['e_add_rectagle_wall'].configure(fg='red')
        else:
            WindX['e_add_rectagle'].configure(fg='red')
    else:
        WindX['DrawRectangleOnScreen'] = 1
        if is2fill:
            WindX['e_add_rectagle_wall'].configure(fg='green')
        else:
            WindX['e_add_rectagle'].configure(fg='green')

class TopCustomWind:
    def __init__(self):
        self.winGUI()

    def winGUI(self):
        self.top = Toplevel()
        self.top.title("Set Custom Window, clik [OK] to complete setting")
        WindX['Toplevels'].append(self.top)
        self.top.wm_attributes('-topmost',1)
        self.canvas= Canvas(self.top,
                    width=500,
                    height=500,
                    bg="white",
                    relief=FLAT,
                    bd = 0,
                    )
        self.canvas.configure(highlightthickness = 0)
        self.canvas.place(x=0,y=0)

        self.buttonOK = Button(self.top,
                text='OK', 
                justify= CENTER, 
                relief= FLAT,
                padx= 5,
                pady= 5,        
                bg = 'red',        
                fg = 'white',    
                command= self.OK_SetCustomWind
            )
        self.buttonOK.place(x=0,y=0)

        self.top.update()
        gs = re.split(r'x|\+', self.top.geometry()) #506x152+-1418+224
        self.top.geometry('500x500+'+ str(gs[2]) +'+' + str(gs[3]))
        self.top.update()        
        self.image_catch = None

        self.top.bind("<Button-1>",self.CanvasImageRefresh)
        self.top.bind("<Motion>",self.CanvasImageRefresh)
        self.top.protocol("WM_DELETE_WINDOW", self.Frame_Close)
        #self.canvas.bind("<Button-1>",self.CanvasImageRefresh)
        
        self.canvas_image = None
        self.last_geometry = None
        self.CanvasImageRefresh()

    def OK_SetCustomWind(self):
        HWND = self.top.winfo_id()
        rect = win32gui.GetWindowRect(HWND)  #left top right bottom   l, t, r, b
        #print("\n", WindX['b_CatchPoint']['values'])
        vlist = list(WindX['b_CatchPoint']['values'])
        vlist.append('[Custom] ' + str(int(rect[2] - rect[0])) + ',' + str(int(rect[3] - rect[1])) + ',' + str(int(rect[0])) + ',' + str(int(rect[1])))
        WindX['b_CatchPoint']['values'] = vlist
        WindX['b_CatchPoint'].current(len(vlist) - 1)
        self.Frame_Close()

    def set_frame_on_window(self, hwind=None):
        if not hwind:
            hwind = self.top.winfo_id()
        rect = []
        try:
            rect = win32gui.GetWindowRect(hwind)  #left top right bottom   l, t, r, b
            ToplevelRect(sizes=[int(rect[2] - rect[0]), int(rect[3] - rect[1])], xys=[int(rect[0]), int(rect[1])], idx= WindX['TopCustomWind_frame_id'])
            
            if not hwind == self.top.winfo_id():
                self.top.geometry(str(int(rect[2] - rect[0])) + 'x' + str(int(rect[3] - rect[1])) + '+' + str(int(rect[0])) +'+' + str(int(rect[1])))
                t1 = threading.Timer(0.1,self.correct_position, args=[rect])
                t1.start()
        except:
            print("\nset_frame_on_window: hwind=", hwind)
            print(sys._getframe().f_lineno, traceback.format_exc())

        return rect

    def correct_position(self, rect=[]):
        hwind = self.top.winfo_id()
        rect1 = win32gui.GetWindowRect(hwind)
        if not (rect1[0] == rect[0] and rect1[1] == rect[1]):
            dx = rect[0] - rect1[0]
            dy = rect[1] - rect1[1]
            self.top.geometry('+' + str(int(rect[0] + dx)) +'+' + str(int(rect[1] + dy)))

        t1 = threading.Timer(0.1,self.CanvasImageRefresh_Go, args=[rect])
        t1.start()

    def Frame_Close(self, event=None):
        ToplevelRectHide(idx=WindX['TopCustomWind_frame_id'])
        self.top.destroy()
        WindX['WinCustomAdd_Class'] = None


    def CanvasImageRefresh(self, event=None):
        geo = self.top.geometry()
        if self.last_geometry and geo == self.last_geometry:
            #print('self.last_geometry=',self.last_geometry)
            return
        self.CanvasImageRefresh_Go()

    def CanvasImageRefresh_Go(self, rect=[]):
        geo = self.top.geometry()   
        self.last_geometry = geo

        self.top.wm_attributes('-topmost',1)
        if not len(rect):
            rect = self.set_frame_on_window()

        gs = re.split(r'x|\+', geo) #506x152+-1418+224
        self.top.geometry(gs[0] + 'x0+'+ str(gs[2]) +'+' + str(gs[3]))
        self.canvas.config(width= int(rect[2] - rect[0]), height=int(rect[3] - rect[1]))

        self.top.update()
        self.image_catch = self.GetThisImage(rect=rect)
        self.top.geometry(geo)

        #print("CanvasImageRefresh image:",im, im.size)
        if isinstance(self.image_catch, Image.Image):
            self.canvas_image_imk = ImageTk.PhotoImage(self.image_catch)       # have to store the image at first or can not show on this self.canvas      
            self.canvas_image = self.canvas.create_image(int(self.image_catch.size[0]/2),int(self.image_catch.size[1]/2),image = self.canvas_image_imk)

    def GetThisImage(self, event=None, rect=[]):
        im,err = ScreenShotXY(
            width =int(rect[2] - rect[0]),
            height=int(rect[3] - rect[1]),
            xSrc  =int(rect[0]),
            ySrc  =int(rect[1])
        )
        return im

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
                    colspan=1,msg=None,width=0,
                    p=[LEFT,FLAT,3,1,'#FFFF66','#FFFF99',5,E+W+N+S,0,0]):

        if width:
            p[6] = width

        self.b = Button(frm, 
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
        GUIonFrame2Motion()
        #if self.message:
        #    WindX['e_ImageCateched'].config(text=self.message) 

    def iLeave(self,event):
        self.b.config(bg = self.bg)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, bg=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, width=500, height=300)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical",   command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        gui_style = ttk.Style()
        if bg:
            gui_style.configure('My.TFrame', background=bg) #, background='#E0E0E0'
        else:
            gui_style.configure('My.TFrame') #, background='#E0E0E0'
        self.scrollable_frame = ttk.Frame(self.canvas,style='My.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        #container.bind("<Motion>", self.canvasMotion)
        #container.bind("<Leave>",  self.canvasLeave)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.grid(row=0,column=0,sticky=E+W+N+S)
        self.scrollbar_y.grid(row=0,column=1,sticky=N+S)
        self.scrollbar_x.grid(row=1,column=0,sticky=E+W)   

    def canvasMotion(self,e):
        self.scrollbar_x.grid()
        self.scrollbar_y.grid()

    def canvasLeave(self,e):
        self.scrollbar_x.grid_remove()
        self.scrollbar_y.grid_remove()

def handlerAdaptor(fun,**kwds):
    return lambda event,fun=fun,kwds=kwds:fun(event,**kwds) 

WindX['DrawRectangleOnScreen_fillWins'] = []
def ToplevelRectFill(idx=""):    
    sel_color = numpy.random.choice(numpy.array(GetColors(istart=16711680, n=40)), 3, replace=False)
    bg_color = sel_color[1]
    try:
        tl = Toplevel(bg= bg_color)
        tl.geometry(str(WindX['DrawRectangleOnScreen_fillRect'][0]) + 'x'+ str(WindX['DrawRectangleOnScreen_fillRect'][1]) +'+'+ str(WindX['DrawRectangleOnScreen_fillRect'][2]) +'+' + str(WindX['DrawRectangleOnScreen_fillRect'][3]))
        
        xbutton = Button(tl, text='x', relief=FLAT,pady=5, padx=5, command=lambda:ToplevelRectFillClose(tl=tl))
        xbutton.pack(side=LEFT, fill=Y, anchor=CENTER)

        xbutton2 = None
        xbutton2 = Button(tl, text='', relief=FLAT, bg= bg_color, command=lambda:ToplevelRectFillSetColor(tl=xbutton2))
        xbutton2.pack(side=RIGHT, expand=True, fill=BOTH, anchor=CENTER)

        #tl.bind('<Button-1>', func=handlerAdaptor(ToplevelRectFillSetColor, tl=tl))
        tl.wm_attributes('-topmost',1)
        #tl.wm_attributes('-alpha',0.95)
        tl.overrideredirect(1)
        WindX['DrawRectangleOnScreen_fillWins'].append(tl)
    except:
        print(traceback.format_exc())
    
    ToplevelRectHide(idx)

def ToplevelRectFillWinsOnTop():
    try:
        tls = []
        for tl in WindX['DrawRectangleOnScreen_fillWins']:
            try:
                if tl:
                    print("ToplevelRectFillWinsOnTop:",tl, tl.geometry())
                    tl.overrideredirect(0)
                    tl.update()
                    tl.wm_attributes('-topmost',1)
                    tl.overrideredirect(1)
                    tls.append(tl)
            except:
                pass
        WindX['DrawRectangleOnScreen_fillWins'] = tls
    except:
        pass

def ToplevelRectFillSetColor(event=None, tl=None):
    if tl:
        try:
            sel_color = icolorchooser.askcolor()
            print("\nselected color", sel_color, "\n")
            tl.configure(background= sel_color[1])
        except:
            pass

def ToplevelRectFillClose(event=None, tl=None):
    print("\n======= close:", tl, '=======\n')
    try:
        tl.destroy()
        tl = None
    except:
        print(traceback.format_exc())                            

def ToplevelRect(sizes=[], xys=[], icolor='#FF0000',idx='123456'):
    if not WindX['toplevel_Rect'].__contains__(idx):
        WindX['toplevel_Rect'][idx] = []

    try:
        x1 = xys[0] - 1 
        y1 = xys[1] - 1
        x2 = xys[0] + sizes[0] + 1
        y2 = xys[1] + sizes[1] + 1

        WindX['DrawRectangleOnScreen_fillRect'] = [
            sizes[0],
            sizes[1],
            x1, 
            y1           
        ]
            
        if len(WindX['toplevel_Rect'][idx]):
            ToplevelRectShow(isShow=True, xy=[x1,y1,x2,y2],sizes=sizes, icolor=icolor,idx=idx)
            return

        #if icolor=='colorful':
        #    icolor = 'red'
        lineWidth, icolors = ToplevelRect_ColorList(icolor)

        try:                                               #x,y,width,height,color,notAppend=False  
            WindX['toplevel_Rect'][idx].append(ToplevelLine(x1,y1,sizes[0]+2, lineWidth, icolors[0], notAppend=True))  #0 top
            WindX['toplevel_Rect'][idx].append(ToplevelLine(x1,y2,sizes[0]+2, lineWidth, icolors[1], notAppend=True))  #1 bottom

            WindX['toplevel_Rect'][idx].append(ToplevelLine(x1,y1, lineWidth,sizes[1]+2, icolors[2], notAppend=True))  #2 left
            WindX['toplevel_Rect'][idx].append(ToplevelLine(x2,y1, lineWidth,sizes[1]+2, icolors[3], notAppend=True))  #3 right

            tl = Toplevel()
            tl.geometry('12x12+'+ str(x1) +'+' + str(y1))
            
            for tlx in WindX['toplevel_Rect'][idx]:
                tlx[1].bind('<Motion>', func=handlerAdaptor(ToplevelRectButtonShow, isShown=True,  idx=idx))
                tlx[1].bind('<Leave>' , func=handlerAdaptor(ToplevelRectButtonShow, isShown=False, idx=idx, delay=3))

            font_type = None 
            try:
                font_type = tkFont.Font(family="Lucida Grande", size=8)
            except:
                pass

            xbutton = Button(tl, text='x', relief=FLAT,pady=1,padx=1, bg= icolors[4], fg= ColorHex_Reversed(icolors[4]), font=font_type, command=lambda:ToplevelRectHide(idx=idx))
            xbutton.pack(side=TOP)
 
            tl.wm_attributes('-topmost',1)
            tl.overrideredirect(1)
            WindX['toplevel_Rect'][idx].append([tl, xbutton, None])
            tl.withdraw()
            
        except:
            print(traceback.format_exc())
    except:
        print(traceback.format_exc())

def ToplevelRectButtonShow(event=None, isShown=False, idx=None, delay=0):
    try:
        if idx and WindX['toplevel_Rect'].__contains__(idx):
            if isShown:
                WindX['toplevel_Rect'][idx][4][0].deiconify()
            else:
                if delay:
                    if WindX['toplevel_Rect'][idx][4][2]:
                        try:
                            WindX['toplevel_Rect'][idx][4][2].cancel()
                        except:
                            pass

                    t1 = threading.Timer(delay, ToplevelRectButtonShow, args=[None,False,idx,0])
                    WindX['toplevel_Rect'][idx][4][2] = t1
                    t1.start()
                else:
                    WindX['toplevel_Rect'][idx][4][0].withdraw()
    except:
        pass

def ToplevelRectHide(idx=''):
    if not idx:
        idx = max(sorted(WindX['toplevel_Rect'].keys()))

    if idx and WindX['toplevel_Rect'].__contains__(idx):
        ToplevelRectShow(isShow=False, idx=idx)
    
    ToplevelRectFillWinsOnTop()

def ToplevelRectShow(isShow=True, xy=[],sizes=[],icolor='#FF0000',idx='123456'):
    if len(WindX['toplevel_Rect'][idx]):
        if isShow:
            lineWidth, icolors = ToplevelRect_ColorList(icolor)

            WindX['toplevel_Rect'][idx][0][1].configure(width= sizes[0]+2, height=lineWidth, bg=icolors[0])   #canvas top
            WindX['toplevel_Rect'][idx][0][0].geometry('+'+ str(xy[0]) +'+' + str(xy[1])) #toplevel
            WindX['toplevel_Rect'][idx][0][0].deiconify() #toplevel

            WindX['toplevel_Rect'][idx][1][1].configure(width= sizes[0]+2, height=lineWidth, bg=icolors[1])   #canvas bottom
            WindX['toplevel_Rect'][idx][1][0].geometry('+'+ str(xy[0]) +'+' + str(xy[3])) #toplevel
            WindX['toplevel_Rect'][idx][1][0].deiconify() #toplevel

            WindX['toplevel_Rect'][idx][2][1].configure(height= sizes[1]+2, width=lineWidth, bg=icolors[2])   #canvas left
            WindX['toplevel_Rect'][idx][2][0].geometry('+'+ str(xy[0]) +'+' + str(xy[1])) #toplevel
            WindX['toplevel_Rect'][idx][2][0].deiconify() #toplevel

            WindX['toplevel_Rect'][idx][3][1].configure(height= sizes[1]+2, width=lineWidth, bg=icolors[3])   #canvas right
            WindX['toplevel_Rect'][idx][3][0].geometry('+'+ str(xy[2] - lineWidth) +'+' + str(xy[1])) #toplevel
            WindX['toplevel_Rect'][idx][3][0].deiconify() #toplevel
            
            #print([s for s in WindX['toplevel_Rect'][idx]])
            WindX['toplevel_Rect'][idx][4][1].configure(bg=icolors[4], fg= ColorHex_Reversed(icolors[4]))   #button
            WindX['toplevel_Rect'][idx][4][0].geometry('+'+ str(xy[2] - 13) +'+' + str(xy[1] + 2)) #toplevel button
            WindX['toplevel_Rect'][idx][4][0].deiconify() #toplevel
        else:
            for tl in WindX['toplevel_Rect'][idx]:
                tl[0].destroy()
            
            del WindX['toplevel_Rect'][idx]

def ToplevelRect_ColorList(icolor):
    icolors=[icolor,icolor,icolor,icolor,icolor]
    lineWidth = 1
    if icolor == 'colorful':
        icolors = numpy.random.choice(numpy.array(GetColors(istart=16711680, n=40)), 5, replace=False)  #*random.randint(1,100)
        lineWidth = 2
    
    return lineWidth, icolors

def ColorRGB_to_Hex(rgb):
    RGB = []
    if type(rgb) == list:
        RGB = rgb
    else:
        RGB = rgb.split(',')
    color = '#'
    for i in RGB:
       num = int(i)
       color += str(hex(num))[-2:].replace('x', '0').upper()
    #print(color)
    return color

def ColorHex_to_RGB(hex):
    r = int(hex[1:3],16)
    g = int(hex[3:5],16)
    b = int(hex[5:7], 16)
    rgb = [r,g,b]
    #print(rgb)
    return rgb

def ColorHex_Reversed(hex):  #FF0000
    rgb = ColorHex_to_RGB(hex)
    return ColorRGB_to_Hex([255 - rgb[0], 255 - rgb[1], 255 - rgb[2]])

def GetColors(istart=16711680, n=10):
    colors = []
    a = numpy.linspace(istart,255,n)
    #print(a)
    for i in a:
        c = int(i)
        colors.append('#%06x'%c)
    #print(colors)
    return colors

def ForeGroundWindow():
    try:
        fgwHandle = win32gui.GetForegroundWindow()
        if fgwHandle:
            return fgwHandle
    except:
        print(sys._getframe().f_lineno, traceback.format_exc()) 
        return ''

def MouseOnClick(x, y, button, pressed):
    #print(button,'{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    DrawRectangleOnScreen_JustOff = 0
    if re.match(r'.*left',str(button),re.I):
        if pressed:
            #print('In:', len(WindX['mouse_left_pressed_on_screen']), WindX['mouse_left_pressed_on_screen'])
            if WindX['DrawRectangleOnScreen']:                
                if len(WindX['mouse_left_pressed_on_screen'])==3:
                    WindX['mouse_left_pressed_on_screen'].extend([x,y])
                    WindX['DrawRectangleOnScreen'] = 0
                    if WindX['DrawRectangleOnScreen_is2fill']:
                        WindX['e_add_rectagle_wall'].configure(fg='red')
                        if len(WindX['DrawRectangleOnScreen_fillRect']):
                            ToplevelRectFill(WindX['mouse_left_pressed_on_screen'][2])
                    else:
                        WindX['e_add_rectagle'].configure(fg='red')
                    WindX['DrawRectangleOnScreen_is2fill']  = False
                    WindX['DrawRectangleOnScreen_fillRect'] = []

                elif len(WindX['mouse_left_pressed_on_screen'])==5 or len(WindX['mouse_left_pressed_on_screen'])==0:
                    WindX['mouse_left_pressed_on_screen'] = [x,y,time.time()]
            else:
                WindX['mouse_left_pressed_on_screen'] = []
            #print('Out:', len(WindX['mouse_left_pressed_on_screen']), WindX['mouse_left_pressed_on_screen'], '\n')
        else:                        
            WindX['mouse_click_points'].append([x,y])

            if WindX['WinCustomAdd_Class']:
                WindX['WinCustomAdd_Class'].CanvasImageRefresh()

                fgwHandle = ForeGroundWindow()
                title = win32gui.GetWindowText(fgwHandle)
                if not re.match(r'^Screen\s+Catch|^Set\s+Custom\s+Window', title, re.I) and WindX['WinCustomAdd_Class']: 
                    WindX['WinCustomAdd_Class'].set_frame_on_window(fgwHandle)                    

    elif pressed:
        #print(button,'{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        if WindX['DrawRectangleOnScreen']:
            WindX['DrawRectangleOnScreen'] = 0
            if WindX['DrawRectangleOnScreen_is2fill']:
                WindX['e_add_rectagle_wall'].configure(fg='red')                
            else:
                WindX['e_add_rectagle'].configure(fg='red')
            WindX['DrawRectangleOnScreen_is2fill'] = False
            WindX['DrawRectangleOnScreen_fillRect'] = []

        elif len(WindX['toplevel_Rect'].keys()):
            ToplevelRectHide()

def MouseOnMove(x, y):
    WindX['mouse_move_points'].append([x,y])
    if len(WindX['mouse_left_pressed_on_screen'])==3 and WindX['DrawRectangleOnScreen']:
        xx = sorted([x, WindX['mouse_left_pressed_on_screen'][0]])
        yy = sorted([y, WindX['mouse_left_pressed_on_screen'][1]])
        
        ToplevelRect(
            sizes=[
                    xx[1] - xx[0],
                    yy[1] - yy[0],
                ], 
            xys  = [xx[0], yy[0]],
            icolor='colorful',
            idx = WindX['mouse_left_pressed_on_screen'][2]
            )

def MouseListener():
    with Listener(on_click=MouseOnClick, 
                  on_move=MouseOnMove,

                 ) as listener: #(on_move=on_move, on_click=on_click, on_scroll=on_scroll) 
        listener.join()

def Keyboard_on_press(key):
    #print(key,'press')
    #Print2Log('', sys._getframe().f_lineno, '{0} released'.format(key))
    if key == keyboardX.Key.esc:
        # if mask is on, close all toplevel windows
        if len(WindX['top_level_masks']):
            try:
                for tl in WindX['top_level_masks']:
                    tl.destroy()
            except:
                pass

def KeyboardListener():
    #return #not record key board input
    # Collect events until released
    with keyboardX.Listener(
            on_press=Keyboard_on_press) as listener:
        listener.join()

def pytesseractLanguages():
    '''
    for s in re.split(r'\n+', langstr):
        ss = re.split(r'\s+', s)
        name = re.sub(r'^{}\s+|\s+{}.traineddata'.format(ss[0],ss[0]),'',s)
        print("\t'" + ss[0] + "': \"" + name + "\",")
    '''
    langNames= {
        'afr': "Afrikaans",
        'amh': "Amharic",
        'ara': "Arabic",
        'asm': "Assamese",
        'aze': "Azerbaijani",
        'aze_cyrl': "Azerbaijani �?Cyrillic",     
        'bel': "Belarusian",
        'ben': "Bengali",
        'bod': "Tibetan",
        'bos': "Bosnian",
        'bul': "Bulgarian",
        'cat': "Catalan; Valencian",
        'ceb': "Cebuano",
        'ces': "Czech",
        'chi_sim': "Chinese �?Simplified",
        'chi_tra': "Chinese �?Traditional",
        'chr': "Cherokee",
        'cym': "Welsh",
        'dan': "Danish",
        'deu': "German",
        'dzo': "Dzongkha",
        'ell': "Greek, Modern (1453-)",
        'eng': "English",
        'enm': "English, Middle (1100-1500)",
        'epo': "Esperanto",
        'est': "Estonian",
        'eus': "Basque",
        'fas': "Persian",
        'fin': "Finnish",
        'fra': "French",
        'frk': "German Fraktur",
        'frm': "French, Middle (ca. 1400-1600)",
        'gle': "Irish",
        'glg': "Galician",
        'grc': "Greek, Ancient (-1453)",
        'guj': "Gujarati",
        'hat': "Haitian; Haitian Creole",
        'heb': "Hebrew",
        'hin': "Hindi",
        'hrv': "Croatian",
        'hun': "Hungarian",
        'iku': "Inuktitut",
        'ind': "Indonesian",
        'isl': "Icelandic",
        'ita': "Italian",
        'ita_old': "Italian �?Old",
        'jav': "Javanese",
        'jpn': "Japanese",
        'kan': "Kannada",
        'kat': "Georgian",
        'kat_old': "Georgian �?Old",
        'kaz': "Kazakh",
        'khm': "Central Khmer",
        'kir': "Kirghiz; Kyrgyz",
        'kor': "Korean",
        'kur': "Kurdish",
        'lao': "Lao",
        'lat': "Latin",
        'lav': "Latvian",
        'lit': "Lithuanian",
        'mal': "Malayalam",
        'mar': "Marathi",
        'mkd': "Macedonian",
        'mlt': "Maltese",
        'msa': "Malay",
        'mya': "Burmese",
        'nep': "Nepali",
        'nld': "Dutch; Flemish",
        'nor': "Norwegian",
        'ori': "Oriya",
        'pan': "Panjabi; Punjabi",
        'pol': "Polish",
        'por': "Portuguese",
        'pus': "Pushto; Pashto",
        'ron': "Romanian; Moldavian; Moldovan",
        'rus': "Russian",
        'san': "Sanskrit",
        'sin': "Sinhala; Sinhalese",
        'slk': "Slovak",
        'slv': "Slovenian",
        'spa': "Spanish; Castilian",
        'spa_old': "Spanish; Castilian �?Old",
        'sqi': "Albanian",
        'srp': "Serbian",
        'srp_latn': "Serbian �?Latin",
        'swa': "Swahili",
        'swe': "Swedish",
        'syr': "Syriac",
        'tam': "Tamil",
        'tel': "Telugu",
        'tgk': "Tajik",
        'tgl': "Tagalog",
        'tha': "Thai",
        'tir': "Tigrinya",
        'tur': "Turkish",
        'uig': "Uighur; Uyghur",
        'ukr': "Ukrainian",
        'urd': "Urdu",
        'uzb': "Uzbek",
        'uzb_cyrl': "Uzbek �?Cyrillic",
        'vie': "Vietnamese",
        'yid': "Yiddish"
    }

    return langNames

def main():   
    t1 = threading.Timer(1,MouseListener)
    t1.start()
    t2 = threading.Timer(1,KeyboardListener)
    t2.start() 
    GUI(1)

if __name__ == "__main__":          
    main()


