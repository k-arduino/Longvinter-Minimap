from multiprocessing import Process
from tkinter import *
import time
import pytesseract
from PIL import Image
from PIL import ImageGrab
import cv2
import threading
import random
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def map(x,input_min,input_max,output_min,output_max):
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min

def UIstart():
    UI = Tk()
    UI.title("MINIMAP")
    UI.geometry("326x300+1586+749")
    UI.resizable(False, False)
    UI.attributes('-topmost',True)
    UI.iconbitmap('map.ico')
    wall = PhotoImage(file = "Longvinter world map ui2.png")
    point = PhotoImage(file = "location.png")
    canvas = Canvas(UI, width=326, height=300, bd=0, highlightthickness=0)
    canvas.pack()
    canvas.create_image(163,150, image=wall)
    location = canvas.create_image(198,150, image=point)

    while True:
        #Image capture
        img = ImageGrab.grab()
        imgCrop = img.crop((1730,40,1884,73))
        saveas="{}{}".format('D:\coordinate','.png')
        imgCrop.save(saveas)
        
        #Image filtering
        img_color = cv2.imread('D:\coordinate.png')
        height,width = img_color.shape[:2]
        img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
        lower_blue = (15-10, 30, 30)
        upper_blue = (15+10, 255, 255)
        img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
        img_result = cv2.bitwise_and(img_color, img_color, mask = img_mask)
        cv2.imwrite("D:\coordinate.png",img_mask)

        #OCR
        a = Image.open('D:\coordinate.png')
        result = pytesseract.image_to_string(a)
        print(result)
        
        #Cleaning
        half = result.split('/',1)
        print(half)
        left = (half[0])
        right = (half[-1])
        lefthalf = left.split('°',1)
        righthalf = right.split('°',1)
        leftnumber = (lefthalf[0])
        leftdirection = (lefthalf[-1])
        rightnumber1 = (righthalf[0])
        rightdirection = (righthalf[-1])
        rightnumber = rightnumber1.replace(" " , "")
        print(leftnumber)
        print(leftdirection)
        print(rightnumber)
        print(rightdirection)
        Cleftnumber = leftnumber.strip()
        Cleftdirection = leftdirection.strip()
        Crightnumber = rightnumber.strip()
        Crightdirection = rightdirection.strip()
        # print('1',Cleftdirection,'1')
        # print('1',rightdirection,'1')
        # print('1',leftdirection,'1')
        # print('1',leftdirection,'1')
        if Cleftnumber.isnumeric == False:
            print('error, goto first code')
            # continue
        elif Crightnumber.isnumeric == False:
            print('error, goto first code')
            # continue
        elif Cleftdirection.isalpha == False:
            print('error, goto first code')
            # continue
        elif Crightdirection.isalpha == False:
            print('error, goto first code')
            # continue

        try:
            #1사분면
            if Cleftdirection == 'N' and Crightdirection == 'E':
                Xline = map(int(Crightnumber),0,30,198,299) #맵핑
                print(Xline) #변환된 값
                Yline = map(int(Cleftnumber),0,35,150,25) #맵핑
                print(Yline) #변환된 값
                canvas.delete(location)         
                UI.update()
                location = canvas.create_image(Xline,Yline, image=point)
                UI.update()
                print('1')
            
            #2사분면
            elif Cleftdirection == 'N' and Crightdirection == 'W':
                Xline = map(int(Crightnumber),1,48,198,30) #맵핑
                print(Xline) #변환된 값
                Yline = map(int(Cleftnumber),0,35,150,25) #맵핑
                print(Yline) #변환된 값
                canvas.delete(location)
                UI.update()
                location = canvas.create_image(Xline,Yline, image=point)
                UI.update()
                print('2')
            
            #3사분면
            elif Cleftdirection == 'S' and Crightdirection == 'W':
                Xline = map(int(Crightnumber),1,48,198,30) #맵핑
                print(Xline) #변환된 값
                Yline = map(int(Cleftnumber),1,36,150,273) #맵핑
                print(Yline) #변환된 값
                canvas.delete(location)
                UI.update()
                location = canvas.create_image(Xline,Yline, image=point)
                UI.update()
                print('3')
            
            #4사분면
            elif Cleftdirection == 'S' and Crightdirection == 'E':
                Xline = map(int(Crightnumber),0,30,198,299) #맵핑
                print(Xline) #변환된 값
                Yline = map(int(Cleftnumber),1,36,150,273) #맵핑
                print(Yline) #변환된 값
                canvas.delete(location)
                UI.update()
                location = canvas.create_image(Xline,Yline, image=point)
                UI.update()
                print('4')
        except ValueError:
            continue

        UI.update()
        time.sleep(0.1)
        Xline = None
        Yline = None
    UI.mainloop()

#Multiprocessing
if __name__=='__main__':
    program = Process(target = UIstart)
    program.start()