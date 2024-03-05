#!/usr/bin/python
#Author : J. A. Hernandez-Jimenez

#Note: to read html table you should install
#     :  python-beautifulsoup
#     :  python-bs4

import sys

if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    from tkinter.filedialog import *
    from tkinter.messagebox import *
    print ("Loading libraries of python 3")
else:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
    from tkFileDialog import *
    from tkMessageBox import *

from os.path import expanduser
home = expanduser("~")

import numpy as np
from scipy.ndimage import filters
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
from multiprocessing import Process


root = Tk()
root.title('Mask Programm')

global image
image = StringVar()
global openkey, savekey
openkey = True; savekey = True

def askopenfile(event=None):

    global image
    image =askopenfilename(filetypes=[("allfiles","*")])

    import mask

    maskname=var1.get().split()[0]
    colormapn = var5.get().split()[0]
    mask.calli(image,maskname, colormapn)

def loadcube (event=None):

    import mask

    cuben   = var2.get()
    tablen  = var3.get()
    hedkey  = var4.get().split(',')

    cubeext = int(hedkey[0])
    cubekind = hedkey[1]
    cubehed  = hedkey[2:5]
    verbose = hedkey[5]

    # Printing Cube information
    cube = fits.open(cuben)
    if verbose == '+':
        print ('printing the extensions of the cube...')
        print (cube.info())

    ##################
    # Loading the cube
    cubev = cube[cubeext].data
    hdr0 = cube[cubeext].header

    # printing the header
    if verbose == '+':
        print (cubev.shape)
        print ('printing the  header of the cube...')
        print (hdr0.values)

   ##################
   # Loading the Html
    try:
        tablev = Table.read(tablen,format='html')
    except:
        print('table was not found')
        tablev = 0

    #################################
    # Loading wavelength (wl) array

    # MaNGA cubes
    if 'manga' in  cubekind:
            wl = cube['WAVE'].data
            print ('manga wavelength loaded')

    # "Normal" cubes
    else:
        try:
            # crval  = cubehed[0]
            # cd3_3  = cubehed[0]
            # crpix3 = cubehed[1]
            hdr   = [hdr0[cubehed[0]], hdr0[cubehed[1]]]
            try:
                hdr[0] = hdr[0]  + (1 - hdr0[cubehed[2]])*hdr[1]
            except:
                print ('It was not given CRPIX, then was taken CRPIX=1')
        except:
            raise ValueError('The keywords doesnt exits or are mispelled')
        spec0 = cubev[:, 0, 0]
        wl = np.linspace(hdr[0], (len(spec0)-1)*hdr[1] + hdr[0], len(spec0))

    # Calling cube function from mask file
    mask.callcubo(cuben,cubev,tablev, wl)
    print ("Data cube loaded!")
    fsavekey = True
    fsave()

def quit(event=None):
    import sys
    sys.exit()

def fopen(event=None):

    global openkey
    if openkey:
        filename = '{}/.guiparm/guimask.parm'.format(home)
        openkey = False
    else:
        filename =askopenfilename(filetypes=[("allfiles", "*")])

    try:
        finput=open(filename).read().splitlines()
        k=0
        var1.set(finput[k].split()[0]); k+=1       # Mask name
        var2.set(finput[k].split()[0]); k+=1       # Cube name
        var3.set(finput[k].split()[0]); k+=1       # Fittable name
        var4.set(finput[k].split()[0]); k+=1       # Keywords

    except:
        showwarning("Open file","Cannot open this file")
        return

def fsave(event = None):

    global savekey

    if savekey:
        filename = '{}/.guiparm/guimask.parm'.format(home)
        savekey = False

    else:
        fileo = asksaveasfile(mode='w')
        filename = fileo.name

    fs=open(filename,'w')
    fs.write('%s          # Mask name    \n'  %(var1.get()))
    fs.write('%s          # Cube name    \n'  %(var2.get()))
    fs.write('%s          # Fittable name\n'  %(var3.get()))
    fs.write('%s          # Keywords     \n'  %(var4.get()))
    fs.close()



rowl=0
Label(root, text="  ").grid(row=rowl,column=0,sticky=W)
rowl+=1
Label(root, text="press 'd': to draw the region points").grid(row=rowl,
      column=0, sticky=W)
rowl+=1
Label(root, text="press 'p': to print region statistic ").grid(row=rowl,
      column=0, sticky=W)
rowl+=1
Label(root, text="press 'm': to mask a region ").grid(row=rowl,
      column=0, sticky=W)
rowl+=1
Label(root, text="press 'z': to plot the Gaussian fit ").grid(row=rowl, column=0,
      sticky=W)
rowl+=1
Label(root, text="press 'x': to plot the GH fit").grid(row=rowl, column=0,
      sticky=W)
rowl+=1
Label(root, text="press 't': to plot the total spaxel spectrum").grid(row=rowl, column=0,
      sticky=W)
rowl+=1
Label(root, text="press 'i': to plot the spaxel in splot/iraf").grid(row=rowl, column=0,
      sticky=W)
rowl+=1
Label(root, text="press 'c': to clean up ").grid(row=rowl, column=0, sticky=W)
rowl+=1
Label(root, text="press 'q': to exit ").grid(row=rowl, column=0, sticky=W)
rowl+=1

sizentry=30
rowl+=1
Label(root, text="mask").grid(row=rowl, column=0)
global var1
var1 = StringVar()
Entry(root, bd =5, textvariable=var1,width=sizentry).grid(row=rowl, column=1)
var1.set('mask.fits')
Label(root, text=" Mask name").grid(row=rowl ,column=2,sticky=W)

sizentry=30
rowl+=1
Label(root, text="cube").grid(row=rowl, column=0)
global var2
var2 = StringVar()
Entry(root, bd =5, textvariable=var2,width=sizentry).grid(row=rowl,column=1)
var2.set('zcuboR4.fits')
Label(root, text=" Cube name").grid(row=rowl, column=2, sticky=W)

sizentry=30
rowl+= 1
Label(root, text="table").grid(row=rowl,column=0)
global var3
var3 = StringVar()
Entry(root, bd =5, textvariable=var3, width=sizentry).grid(row=rowl, column=1)
var3.set('fit_halfa.html')
Label(root, text=" Html table name").grid(row=rowl, column=2, sticky=W)

sizentry=30
rowl+= 1
Label(root, text="header keys").grid(row=rowl,column=0)
global var4
var4 = StringVar()
Entry(root, bd =5, textvariable=var4,width=sizentry).grid(row=rowl,column=1)
var4.set('crval3,cd3_3,0')
text = " EXT, normal or manga, CRVAL, CDDELT, CRPIX, verbose(+ or -)"
Label(root, text=text).grid(row=rowl,column=2,sticky=W)

sizentry=30
rowl+= 1
Label(root, text="Colormap").grid(row=rowl,column=0)
global var5
var5 = StringVar()
Entry(root, bd =5, textvariable=var5,width=sizentry).grid(row=rowl,column=1)
var5.set('viridis')
Label(root, text=" Color maps, e.g., viridis, Spectral_r, etc.").grid(row=rowl,
      column=2,sticky=W)


Label(root, text=" ").grid(row=rowl,column=0,sticky=W)
rowl+=1
Button(root, text = 'open image', command = askopenfile).grid(row=rowl,
       column=0)
Button(root, text = 'load cubo', command = loadcube).grid(row=rowl, column=1)
Button(root, text = 'oper parm', command = fopen).grid(row=rowl, column=2)
Button(root, text = 'save', command = fsave).grid(row=rowl, column=3)
Button(root, text = 'close', command = quit).grid(row=rowl, column=4)
fopen()
root.mainloop()
