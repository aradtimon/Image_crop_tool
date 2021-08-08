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

    return wdi
