##############################  FUNCTIONS ###############################################################################

from tkinter import filedialog as fd
from tkinter import messagebox as mb
import logging

logging.basicConfig(filename='Erros.log', level=logging.DEBUG)

import sys,os

def select_folder():

    global wdir

    wdir = fd.askdirectory(title='Select image folder . . ',initialdir='' )

    while wdir == '':

        if mb.askretrycancel(title='Error', message='Folder is not selected . . !') == False:

            break

        else:
            wdir = fd.askdirectory(title='Select image folder . . ', initialdir='')

    img_folder.insert(0,wdir)       #Get entry from selected folder

    return wdir


def get_coordinates():

    global coords

    left = int(input_left.get())  # left,top,right,bottom
    top = int(input_top.get())
    right = int(input_right.get())
    bottom = int(input_bottom.get())

    coords = left, top, right, bottom

    print(coords)

    return coords


def image_list(filetype):

    import glob
    global img_name_list

    img_name_list = []

    for filename in glob.glob(wdir + '/' + '*.' + filetype):
        img_nam = filename.partition('\\')[-1]
        img_name_list.append(img_nam)

        #print(img_name_list)

    return img_name_list

def crop():

    from PIL import Image

    try:

        n = len(img_name_list)
        iteration = 1
        if n == 0:
            mb.showerror(title='Error', message='No images found in selected directory...!'
                                                '\n\nPlease select the valid image type'
                                                '\n\nProcess restarted...')
        else:
            pass

        progress.config(value=0)

        step = 100 / n

        progress.step(amount=step)

        os.chdir(wdir)

        dest_dir = './cropped'

        try:

            os.mkdir(dest_dir,777)

        except OSError:

            logging.error('OSError' + str(OSError))

            print('Destination directory is already exists...')

            pass

        else:

            print('Directory is successfully created')

        for x in img_name_list:

            dest_filename = dest_dir + '/' + x
            image_obj = Image.open(x)
            cropped_image = image_obj.crop(coords)
            cropped_image.save(dest_filename)
            iteration = iteration+1

            progress.step(amount=step)

            progress.update()

        progress.config(value=100)

        mb.showinfo(title='Status', message='Cropping done. . .')

    except ZeroDivisionError as zde:

        logging.error('ZeroDivisionError ' + str(zde))

        print('Exception: division by zero')



def check_img_folder():

    global message

    wdir = img_folder.get()

    if wdir == '':

        message = 'False'

    else:

        message = 'True'

    while True:

        if message == 'False':

            mb.showerror(title='Error',message='Select image folder')

            break

        else:

            break

    return message



def check_img_type():

    global err_img_type

    filetype = imageextn.get()

    if filetype == 'Select image type' or filetype == '':

        err_img_type = 'False'

    else:

        err_img_type = 'True'
        image_list(filetype)

    while True:

        if err_img_type == 'False':

            mb.showerror(title='Error',message='Select valid image type')

            break

        else:

            break

    return err_img_type,filetype


def initiate_crop():

    global filetype

    try:
        get_coordinates()

        check_img_folder()

        if message == 'True':

            print('Folder_exists')

            check_img_type()

        else:

            print('crop process cant be initiated')

        if message == 'True' and err_img_type == 'True':

            print('Crop process initiation success')
            crop()

        else:

            print('Crop process initiation not successfull')

    except ValueError as ve:

        logging.error('ValueError' + str(ve))

        mb.showerror(title="Error", message='Enter the values for coordinates')



def help():

    from PIL import ImageTk,Image
    secondary_window = Toplevel()
    secondary_window.title('Help')
    secondary_window.resizable(0,0)
    secondary_window.iconbitmap(r'./bin/icon1.ico')
    help_icon = ImageTk.PhotoImage(Image.open(r'./bin/help.png'))
    canvas = Canvas(secondary_window, width=600, height=328)
    canvas.pack()
    canvas.create_image(10, 10, anchor=NW, image=help_icon)
    mainloop()

def del_data():

    input_left.delete(0,tk.END)   #1000 indicates the no of letters to delete
    input_top.delete(0,tk.END)
    input_right.delete(0,tk.END)
    input_bottom.delete(0,tk.END)
    img_folder.delete(0,tk.END)
    imageextn.delete(0, tk.END)
    progress.config(value=0)

def reset():

    del_data()
    input_left.insert(0, '225')
    input_top.insert(0, '0')
    input_right.insert(0, '2180')
    input_bottom.insert(0, '1080')
    imageextn.current(0)
    progress.config(value=0)


def check_img_size():

    global width,height

    try:

        from PIL import Image

        import PIL

        img = fd.askopenfilename(title = 'Select Image for it\'s size check ...')

        print(img)

        img_data = Image.open(img)


        width,height = img_data.size


        input_left.delete(0,tk.END)   #1000 indicates the no of letters to delete
        input_top.delete(0,tk.END)
        input_right.delete(0,tk.END)
        input_bottom.delete(0,tk.END)

        input_left.insert(0, '0')
        input_top.insert(0, '0')
        input_right.insert(0, width)
        input_bottom.insert(0, height)

    except AttributeError as ae:

        print('AttributeError')

        logging.error('Atribute error' + str(ae))



###################################   GUI ################################################################################

from tkinter import Tk
from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import ttk

import os,sys

def exit():

    sys.exit()

# window

root = tk.Tk()
root.geometry('600x300+700+100')
root.resizable(0,0)
root.title('Hey, Welcome . . . !')
root.iconbitmap('./bin/icon.ico')

colour1 = 'dark slate grey'

##frame
title_frame = Frame(root,width=594,height=80,bg=colour1)
title_frame.grid(columnspan=2,row=0,sticky=W,padx=3,pady=3)

coordinate_frame = Frame(root,width=394,height=208,bg=colour1)
coordinate_frame.grid(column=0,row=1,sticky=W,padx=3,pady=0)

command_frame = Frame(root,width=194,height=208,bg=colour1)
command_frame.grid(column=1,row=1,sticky=SE,padx=3,pady=3)


## Labels
Label_font = font.Font(family='calibri',size=12)
tool_name_font = font.Font(family='Calibri',size=18,weight='bold')
version_font = font.Font(family='calibri',size=10)

tool_name_lbl = Label(title_frame,text='Image corpping tool',bg=colour1,fg ='yellow',font=tool_name_font).place(x=5,y=5)
version_lbl = Label(title_frame,text='Version 1.1',bg=colour1,fg ='yellow',font=version_font).place(x=5,y=50)
copyright_lbl = Label(title_frame,text='© aradtimo@gmail.com ',bg=colour1,fg ='yellow',font=version_font).place(x=450,y=50)

left_coor_lbl = Label(coordinate_frame,text='Left coordinate (X1)',bg=colour1,fg ='white',font=Label_font).place(x=15,y=20)
top_coor_lbl = Label(coordinate_frame,text='Top coordinate (Y1)',bg=colour1,fg ='white',font=Label_font).place(x=15,y=55)
right_coor_lbl = Label(coordinate_frame,text='Right coordinate (X2)',bg=colour1,fg ='white',font=Label_font).place(x=15,y=90)
bottom_coor_lbl = Label(coordinate_frame,text='Bottom coordinate (Y2)',bg=colour1,fg ='white',font=Label_font).place(x=15,y=125)
img_folder_lbl = Label(coordinate_frame,text='Select folder :',bg=colour1,fg ='white',font=Label_font).place(x=15,y=160)

## Entry

input_left = Entry(coordinate_frame)
input_left.place(x=180, y=25)         # Sepatrately defined so that input_left.get() can be used
input_top = Entry(coordinate_frame)
input_top.place(x=180, y=60)
input_right = Entry(coordinate_frame)
input_right.place(x=180, y=95)
input_bottom = Entry(coordinate_frame)
input_bottom.place(x=180, y=130)
img_folder = Entry(coordinate_frame)
img_folder.place(x=180, y=165)

#Entry_prefilled_coordinates
input_left.insert(0,'225')
input_top.insert(0,'0')
input_right.insert(0,'2180')
input_bottom.insert(0,'1080')



## Buttons

from tkinter import PhotoImage
folder_icon= PhotoImage(file=r'./bin/folder.png')


crop_btn = Button(command_frame, text='Initiate crop', bg='light green',command=initiate_crop, width=15).place(x=45,y=120)
exit_btn = Button(command_frame, text='Exit', bg='red1', command=exit, width=15).place(x=45,y=170)
folder_sel_btn = Button(coordinate_frame,image=folder_icon,heigh=15,width=18,bg=colour1, command=select_folder).place(x=310,y=165)
help_btn = Button(coordinate_frame,text='Help',bg=colour1,fg='yellow', command=help,width=5).place(x=345,y=5)
clear_btn = Button(coordinate_frame,text='Clear',bg=colour1,fg='yellow', command=del_data,width=5).place(x=345,y=35)
reset_btn = Button(coordinate_frame,text='Reset',bg=colour1,fg='yellow', command=reset,width=5).place(x=345,y=65)


check_img_btn = Button(coordinate_frame,text='Size',bg=colour1,fg='yellow', command=check_img_size,width=5).place(x=345,y=95)



## Progress bar
progress = ttk.Progressbar(command_frame,length = 113,maximum = 100,mode ='determinate')
progress.place(x=45, y=70)

## Dropdown menu

n = tk.StringVar()
imageextn = ttk.Combobox(command_frame, width=15, textvariable =n)
imageextn.place(x=45,y=20)
imageextn['values'] = ('Select image type','jpg','png','tif','gif')
imageextn.current(0)   #Default jpg file


root.mainloop()


# #Progressbar test function
# def test():
#     i=10000
#     step=100/i
#
#     n=0
#
#     while n<=i:
#
#         progress.step(amount=step)
#         progress.update()
#         n=n+1
#
#     progress.configure(value=100)

