#!python
#Author : J. A. Hernandez-Jimenez

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

from numpy import *
from scipy.ndimage import filters

import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from os.path import expanduser
home = expanduser("~")
from astropy.io import fits

#import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import Modules
import os,sys
import datetime
import astrocubelib

speedc=astrocubelib.speedc

sys.setrecursionlimit(10000)

def fitspec(event = None):

    global perf, hdr, wl, z, direc, I, aspec
    global lines, linessig, linessigfix, linescentfix, linescorefix
    global linesguess, linesb, linessigb, lineslim, contl, contr, contfunc
    global vfit, rootspec
    global ax
    global figxlim, figlabel, showt
    global line_masks


    print ("\n*fit for the spectro %g " %(I+1))
    spec = perf[0,:]
    rootspec = aspec[I]
    # format image
    if len(showt[2]) < 4:
        fig  = rootspec.split('.')[0]  + '.'  + showt[2]
    else:
        fig = showt[2]

    if showt[1] == 'no':
       figtit = None
    else:
       figtit = rootspec

    # This option is when it has given system velocity instead z.
    z_I = float(z[I])
    if z_I > 10.0 or z_I < -10.0:
        z_I = (z_I/speedc)
    else:
        z_I =  z_I


    nflog=var15.get()
    flog = open(nflog, 'a')
    flog.write("\n\n%s \n"%(rootspec))
    now = datetime.datetime.now()
    flog.write(now.strftime("%Y-%m-%d %H:%M\n"))
    flog.write("\ninput parameters:\n")
    flog.write("----------------- \n")
    flog.write("lines: %s\n"%lines)
    flog.write("linesguess: %s\n"%linesguess)
    flog.write("linessig : %s\n"%linessig)
    flog.write("linesb: %s\n"%linesb)
    flog.write("linessigb : %s\n"%linessigb)
    flog.write("linessigfix: %s\n"%linessigfix)
    flog.write("linescentfix: %s\n"%linescentfix)
    flog.write("linescorefix: %s\n"%linescorefix)
    flog.write("lineslim:  %s contl: %s contr: %s\n"%(lineslim, contl, contr))
    flog.write("contfunc : %s\n\n"%(contfunc))
    flog.close()

    if len(showt) > 6:
        sprefit=showt[6]
    else:
        sprefit=None

    if linesb[0] == 0:
        vfit_tmp=astrocubelib.fitmultiline(wl, spec, lines,
                              linessig, linessigfix = linessigfix,
                              linescentfix = linescentfix,
                              linescorefix = linescorefix,
                              linesguess = linesguess,
                              z = z_I, lineslim = lineslim, cont_l = contl,
                              cont_r = contr, figxlim= figxlim,
                              contfunc = contfunc,
                              plot = 'yes', showt= showt, sprefit=sprefit,
                              figlabel=figlabel,
                              figtit = figtit, figname = fig, showp='no',
                              direc = direc, fclick = click, nflog = nflog,
                              line_masks = line_masks)

    else :
        vfit_tmp=astrocubelib.fitmultiline(wl, spec, lines,
                              linessig, linessigfix=linessigfix,
                              linescentfix = linescentfix,
                              linescorefix = linescorefix,
                              linesguess = linesguess, linesb=linesb,
                              linessigb = linessigb, z = z_I,
                              lineslim = lineslim, cont_l = contl,
                              cont_r = contr, figxlim= figxlim,
                              contfunc = contfunc, plot = 'yes', showt=showt,
                              sprefit=sprefit, figlabel = figlabel,
                              figtit = figtit, figname = fig, direc = direc,
                              fclick = click, nflog = nflog, showp='no',
                              line_masks = line_masks)

    vfit = []
    for a,b in zip (vfit_tmp[1],vfit_tmp[0]):  vfit.append([a]+b)
    ax  = vfit_tmp[-1]
    cursor = Cursor(ax, useblit=True, color='blue', linewidth=2)

    #from multiprocessing import Process
    #p = Process(target=plt.show)
    #p.start()


    #plt.show(block=False)

    ## more code

    #plt.show()
    plt.show()

def go(event=None):

    global lines0,linessig0, linescentfix0, linessigfix0,  linescorefix0
    global linesguess0, linesb0, linessigb0, lineslim0, contl0, contr0
    global contfunc0
    global I
    global ax
    loadspec()
    (lines0, linessig0, linessigfix0, linescentfix0, linescorefix0,
     linesguess0, linesb0, linessigb0, lineslim0, contl0, contr0,
     contfunc0, line_masks0) = loadparfit()
    fitspec()
    global savekey
    savekey = True
    fsave()



def next(event=None):

    global lines, linessig, linessigfix, linescentfix, linescorefix
    global linesguess, linesb, linessigb, lineslim, contl, contr, contfunc
    global lines0,linessig0,linessigfix0, linescentfix0, linesguess0
    global linescorefix0, linesb0, linessigb0, lineslim0, contl0, contr0
    global contfunc0
    global I
    global line_masks, line_masks0

    write_log()

    lines = lines0; linessig = linessig0; linessigfix = linessigfix0;
    linescentfix =  linescentfix0; linescorefix = linescorefix0
    linesguess = linesguess0;linesb = linesb0; linessigb = linessigb0
    lineslim = lineslim0; contl = contl0; contr= contr0; contfunc = contfunc0
    line_masks = line_masks0
    I+=1
    loadspec()
    fitspec()

def write_log(event=None):

    global vfit,rootspec

    for i in arange(len(vfit)):
     tfit=vfit[i]
     nfilelog = './' + direc + '/fit.'+vfit[i][0]+'.dat'
     tfit.pop(0)
     tfit.insert(0,rootspec)

     outline = ('{:>10s} {:>10.3e} {:>10.2f} {:>10.2f} {:>10.3e} {:>10.3e} ' +
                '{:>10.2f} {:>10.3f} {:>10.2f} {:>10.3f} {:>10.2f} {:>10.3e}' +
                ' {:>10.3e} {:>10.3e} {:>10.2f} {:>10.2f} {:>10.2f}' +
                ' {:>10.2f}').format(*tfit)

     try :
      if rootspec in open(nfilelog).read():
        os.system("sed -i 's/.*%s.*/%s/' %s"%(rootspec, outline, nfilelog))
      else :
        nfile=open(nfilelog, 'a')
        nfile.write(outline+'\n')
        nfile.close()
     except :
       nfile=open(nfilelog, 'a')
       headerfile = ('#%s   core       Center       Sigma    mcont       ' +
                     'scont        SNC        SNL     chi^2    chiall^2' +
                     '   L_err   Fluxg      Fluxl    Fluxl_err       EW' +
                     '       EW_err     EWtec    EWtec_err\n')%(
                                                              ''*len(rootspec))
       nfile.write(headerfile)
       nfile.write(outline+'\n')
       nfile.close()

     print ('the parameters fitted were written in', nfilelog)

def update_par0(event=None):

    global lines, linessig, linessigfix, linescentfix, linescorefix
    global linesguess, linesb, linessigb, lineslim, contl, contr, contfunc
    global lines0, linessig0, linessigfix0, linescentfix0, linescorefix0
    global linesguess0, linesb0, linessigb0, lineslim0, contl0, contr0
    global contfunc0
    global line_masks, line_masks0

    lines0 = lines; linessig0 = linessig; linessigfix0 = linessigfix
    linescentfix0 = linescentfix; linescorefix0 = linescorefix
    linesguess0 = linesguess;linesb0 = linesb; linessigb0 = linessigb
    lineslim0 = lineslim; contl0 = contl; contr0 = contr; contfunc0 = contfunc
    line_masks0 = line_masks
    print ("the input parameters were updated")

def inputpar (event=None):

    global lines0, linessig0, linessigfix0, linescentfix0, linescorefix0
    global linesguess0, linesb0
    global linessigb0, lineslim0, contl0, contr0, contfunc0
    global line_masks0

    print ("input parameters: ")
    print ("----------------- ")
    print ("lines        : ", lines0)
    print ("linessig     : ", linessig0)
    print ("linesguess   : ", linesguess0)
    print ("linesb       : ", linesb0)
    print ("linessigb    : ", linessigb0)
    print ("linessigfix  : ", linessigfix0)
    print ("linescentfix : ", linescentfix0)
    print ("linescorefix : ", linescorefix0)
    print ("line_masks   : ", line_masks0)
    print ("lineslim     : ", lineslim0)
    print ("contl        : ", contl0)
    print ("contr        : ", contr0)
    print ("contfunc     : ", contfunc0)

def actualpar (event=None):

    global lines, linessig, linessigfix, linescentfix, linescorefix
    global linesguess, linesb
    global linessigb, lineslim, contl, contr, contfunc
    global lineslim
    global line_masks

    print ("actual parameters: ")
    print ("----------------- ")
    print ("lines        : ", lines)
    print ("linessig     : ", linessig)
    print ("linesguess   : ", linesguess)
    print ("linesb       : ", linesb)
    print ("linessigb0   : ", linessigb)
    print ("linessigfix  : ", linessigfix)
    print ("linescentfix : ", linescentfix)
    print ("linescorefix : ", linescorefix)
    print ("line_masks   : ", line_masks)
    print ("lineslim     : ", lineslim)
    print ("contl        : ", contl)
    print ("contr        : ", contr)
    print ("contfunc0    : ", contfunc)

def redo(event=None):

    loadparfit()
    fitspec()
    global savekey
    savekey = True
    fsave()


def click(event):
    global ax
    if event.key == 'd':
       linesb = [float(s) for s in var6.get().split(',')]

       if linesb[0] == 0:
         var6.set(str(round(event.xdata,2)))
         plt.ioff
         ax.axvline(x=event.xdata, c='k', ls='--')
         plt.draw()

       if linesb[0] != 0:
         linesb = sort(linesb + [round(event.xdata, 2)])
         a_blend = str(linesb[0])
         for e in linesb[1::]:
             a_blend = a_blend + ',' + str(e)
         var6.set(a_blend)
         plt.ioff
         ax.axvline(x=event.xdata, c='k', ls='--')
         plt.draw()

    if event.key == 'r':
        linesguess= var13.get()
        linesguess= linesguess + ',' + str(round(event.xdata, 2))
        var13.set(linesguess)
        plt.ioff()
        ax.axvline(event.xdata, c = 'k', ls= '--')
        plt.draw()




def loadspec(event=None):

    global perf, hdr, wl, z, direc
    global I, aspec

    nspec = var1.get()
    #namedic = var2.get()
    z_t   = var12.get()
    direc = var14.get()

    # loading spectrum
    if nspec[0] == '@':
        aspec = open(nspec[1:]).read().splitlines()
        spec  = fist.open(aspec[I])[0].data
        hdr0  = fits.open(aspec[I])[0].header
        hdr   = [hdr0['crval1'], hdr0['cdelt1']]
    elif nspec.find(',') != -1:
        aspec = [nspec.replace(',', '_')]
        nspec, cubx, cuby = nspec.split(',')
        spec  = fits.open(nspec)[0].data[:, int(cuby) - 1, int(cubx) - 1]
        hdr0  = fits.open(nspec)[0].header
        try:
            hdr = [hdr0['crval3'], hdr0['cdelt3']]
        except:
            hdr = [hdr0['crval3'], hdr0['cd3_3']]

    else:
        aspec = [nspec]
        spec  = fits.open(nspec)[0].data
        hdr0  = fits.open(nspec)[0].data
        hdr   = [hdr0['crval1'], hdr0['cdelt1']]

    perf = zeros([1,spec.shape[0]])
    perf[0,:] =  spec
    wl = linspace(hdr[0], (len(spec)-1)*hdr[1] + hdr[0], len(spec))

    # loading z
    if z_t[0] == '@':
        z = open(z_t[1:]).read().splitlines()
    else:
        z = array([z_t])

    # output directory
    if not os.path.exists('./'+ direc):
        os.mkdir(direc)

def loadparfit(event=None):

    global lines, linessig, linessigfix, linescentfix, linescorefix
    global linesguess, linesb, linessigb, lineslim, contl, contr, contfunc
    global figxlim, figlabel, showt
    global line_masks

    lines    = var4.get().split(',')
    linessig = [float(s) for s in var5.get().split(',')]
    linessigfix  = [float(s) for s in var16.get().split(',')]
    linescentfix = [float(s) for s in var17.get().split(',')]
    linescorefix = [float(s) for s in var18.get().split(',')]
    linesguess = [float(s) for s in var13.get().split(',')]
    linesb     = [float(s) for s in var6.get().split(',')]
    linessigb  = [float(s) for s in var7.get().split(',')]

    line_masks  = [float(s) for s in var2.get().split(',')]

    lineslim   = [float(s) for s in var8.get().split(',')]
    linesc = [float(s) for s in var9.get().split(',')]
    linesw = [float(s) for s in var10.get().split(',')]
    contl  = [linesc[0] + linesw[0], linesc[0]]
    contr  = [linesc[1], linesc[1] + linesw[1]]

    figxlim =  [float(s) for s in var19.get().split(',')]

    figlabel = var20.get().split(',')
    showt = var21.get().split(',')

    contfunc = var11.get().split(',')

    return (lines, linessig, linessigfix, linescentfix, linescorefix,
            linesguess, linesb, linessigb, lineslim, contl, contr,
            contfunc, line_masks)

def quit(event=None):
    import sys
    sys.exit()

def fopen(event=None):


    global openkey
    if openkey:
        filename = home + '/.guiparm/guisplot.parm'
        openkey = False
    else:
        filename =askopenfilename(filetypes=[("allfiles","*")])

    try:
        # Numbers the spectros
        # Name Dic spectra
        # Lines to analysis
        # input sigma for the lines
        # input sigma fixed
        # fix center?
        # input core fixed
        # guess for lines to analysis
        # deblen lines
        # input sigma for deblen lines
        # range of the lines [e.g, -10 NII2, NII +10]
        # limit continum left  [e.g, 6500,6550]
        # limit continum rigth [e.g, 6600,6650]]
        # serie (poly,cheb), serie degree, fit on emission lines region
        # z or velocity systemic
        # Output Directory
        # log file
        finput=open(filename).read().splitlines()
        k=0
        var1.set(finput[k].split()[0]);k+=1
        #var2.set(finput[k].split()[0]);k+=1
        var4.set(finput[k].split()[0]);k+=1
        var13.set(finput[k].split()[0]);k+=1
        var5.set(finput[k].split()[0]);k+=1
        var6.set(finput[k].split()[0]);k+=1
        var7.set(finput[k].split()[0]);k+=1
        var16.set(finput[k].split()[0]);k+=1
        var17.set(finput[k].split()[0]);k+=1
        var18.set(finput[k].split()[0]);k+=1
        var2.set(finput[k].split()[0]);k+=1
        var8.set(finput[k].split()[0]);k+=1
        var9.set(finput[k].split()[0]);k+=1
        var10.set(finput[k].split()[0]);k+=1
        var19.set(finput[k].split()[0]);k+=1
        var11.set(finput[k].split()[0]);k+=1
        var12.set(finput[k].split()[0]);k+=1
        var20.set(finput[k].split("#")[0].strip());k+=1
        var21.set(finput[k].split()[0]);k+=1
        var14.set(finput[k].split()[0]);k+=1
        var15.set(finput[k].split()[0]);k+=1

    except:
        showwarning("Open file","Cannot open this file")
        return

def fsave(event = None):

    global savekey

    if savekey:
        path = '{}/.guiparm/'.format(home)
        if not os.path.exists(path):
              os.mkdir(path)
        filename = '{}/.guiparm/guisplot.parm'.format(home)
        savekey = False
    else:
        fileo = asksaveasfile(mode='w')
        filename = fileo.name

    fs=open(filename,'w')
    fs.write('%s             # Spectrum names      \n'  %(var1.get()))
    #fs.write('%s             # Target directory          \n'  %(var2.get()))
    fs.write('%s             # Lines to analysis         \n'  %(var4.get()))
    fs.write('%s             # Input for the line centers  \n'%(var13.get()))
    fs.write('%s             # input for the line sigmas \n'  %(var5.get()))
    fs.write('%s             # Blends lines\n'  %(var6.get()))
    fs.write('%s             # input sigma for blend linesfix \n'%(var7.get()))
    fs.write('%s             # fix sigmas? 0-free 1-fix \n'  %(var16.get()))
    fs.write('%s             # fix centers? \n'  %(var17.get()))
    fs.write('%s             # fix cores? \n'  %(var18.get()))
    fs.write(('%s            # points of the lines masked (n*sig_L, n*sig_R)' +
              ' \n')%(var2.get()))
    fs.write(('%s            # Fit range of the lines ' +
              '[e.g, -10 NII2, NII +10] \n')%(var8.get()))
    fs.write(('%s       # Continuum limits [Left, Rigth]\n')%(var9.get()))
    fs.write(('%s       # Continuum width [L_width, R_width]\n')%(var10.get()))
    fs.write(('%s       # Continuum limits to plot [L,R]]\n')%(var19.get()))
    fs.write(('%s       # Serie (poly,cheb), serie degree, fit together with' +
        'the emis. lines, s_low, s_upp, niter, grow, kernel \n')%(var11.get()))
    fs.write('%s             # z or velocity systemic\n'  %(var12.get()))
    fs.write('%s       # text (x, y, text, fontsize, color)\n'  %(var20.get()))
    fs.write(('%s       # print output pars, ima_title, ima_format, ' +
      'print chi, plot points used to the fitting, EW areas\n')%(var21.get()))
    fs.write('%s             # Output directory   \n'  %(var14.get()))
    fs.write('%s             # log file   \n'  %(var15.get()))
    fs.close()

global perf, hdr, wl, z, rootname, direc
global lines, linessig, linesguess, linesb, linessigb
global lineslim, contl, contr, contfunc
global lines0, linessig0, linesguess0, linesb0, linessigb0, lineslim0
global contl0, contr0, contfunc0
global line_masks
global I, aspec
I = 0
global savekey, openkey
savekey = True; openkey = True
global vfit,rootspec
global ax
blend = zeros([100, 2])

root = Tk()
root.title('splot ')

rowl = 0
Label(root, text="       ").grid(row=rowl, column=0, sticky=W)
rowl+= 1
Label(root, text="       ").grid(row=rowl, column=0, sticky=W)

sizentry = 30
span = 1
exp = 2

rowl+= 1
Label(root, text="nspec").grid(row=rowl, column=0)
global var1; var1 = StringVar()
Entry(root, bd =5, textvariable=var1, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="input name (spectrum, cube)").grid(row=rowl, column=exp, sticky=W)

#rowl+= 1
#Label(root, text="namedic").grid(row=rowl, column=0)
#global var2; var2 = StringVar()
#Entry(root, bd =5, textvariable=var2, width=sizentry).grid(row=rowl, column=1,
#                                                           columnspan=span)
#Label(root, text="directory name ").grid(row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="lines").grid(row=rowl, column=0)
global var4; var4 = StringVar()
Entry(root, bd =5, textvariable=var4, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="fit lines").grid(row=rowl, column=exp, sticky=W)



rowl+= 1
Label(root, text="L_cent").grid(row=rowl, column=0)
global var13; var13 = StringVar()
Entry(root, bd =5, textvariable=var13, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="user input for emission line centers ").grid(row=rowl,
                                                            column=exp,
                                                            sticky=W)


rowl+= 1
Label(root, text="L_sig").grid(row=rowl, column=0)
global var5; var5 = StringVar()
Entry(root, bd =5, textvariable=var5, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="input for line sigmas").grid(row=rowl, column=exp,
                                                    sticky=W)



rowl+= 1
Label(root, text="BL_cent").grid(row=rowl,column=0)
global var6; var6 = StringVar()
Entry(root, bd =5, textvariable=var6, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="input for Blend Line (DL) centers").grid(row=rowl,
      column=exp, sticky=W)

rowl+= 1
Label(root, text="BL_sig").grid(row=rowl, column=0)
global var7; var7 = StringVar()
Entry(root, bd =5, textvariable=var7, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="input for Blend Line (BL) sigmas ").grid(row=rowl,
      column=exp, sticky=W)


rowl+= 1
Label(root, text="sigfix").grid(row=rowl, column=0)
global var16; var16 = StringVar()
Entry(root, bd =5, textvariable=var16,width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="fix sigma? 0-free  1-fix").grid(row=rowl, column=exp,
sticky=W)

rowl+= 1
Label(root, text="centfix").grid(row=rowl, column=0)
global var17; var17 = StringVar()
Entry(root, bd =5, textvariable=var17,width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="fix center? ").grid(row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="corefix").grid(row=rowl, column=0)
global var18; var18 = StringVar()
Entry(root, bd =5, textvariable=var18, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="fix core? ").grid(row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="l_masked").grid(row=rowl, column=0)
global var2; var2 = StringVar()
Entry(root, bd =5, textvariable=var2, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="points of the lines masked  (+/- n*sig)").grid(row=rowl,
      column=exp, sticky=W)




rowl+= 1
Label(root, text="L_lim").grid(row=rowl, column=0)
global var8; var8 = StringVar()
Entry(root, bd =5, textvariable=var8, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="fit range [e.g, -10 , +10] ").grid(row=rowl,
      column=exp, sticky=W)

rowl+= 1
Label(root, text="C_lim").grid(row=rowl,column=0)
global var9; var9 = StringVar()
Entry(root, bd =5, textvariable=var9, width=sizentry).grid(row=rowl, column=1,
                                                           columnspan=span)
Label(root, text="Continuum limits [left, right] ").grid(row=rowl,
                                                          column=exp, sticky=W)

rowl+= 1
Label(root, text="C_wid").grid(row=rowl,column=0)
global var10; var10 = StringVar()
Entry(root, bd =5, textvariable=var10, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="Continuum width [left_w, right_w] ").grid(row=rowl,
                                                          column=exp, sticky=W)


rowl+= 1
Label(root, text="C_plot").grid(row=rowl,column=0)
global var19; var19 = StringVar()
Entry(root, bd =5, textvariable=var19, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="Continuum limits to plot [left, right] ").grid(row=rowl,
                                                          column=exp, sticky=W)





rowl+= 1
Label(root, text="C_func").grid(row=rowl, column=0)
global var11; var11 = StringVar()
Entry(root, bd =5, textvariable=var11, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="poly or cheb, degree, fit together  " +
      "with the emission lines, s_low, s_upp, niter, grow, kernel").grid(
      row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="z").grid(row=rowl, column=0)
global var12; var12 = StringVar()
Entry(root, bd =5, textvariable=var12, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="z or system velocity").grid(row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="text").grid(row=rowl, column=0)
global var20; var20 = StringVar()
Entry(root, bd =5, textvariable=var20, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="text (x, y, text, fontsize, color)").grid(row=rowl,
column=exp, sticky=W)


rowl+= 1
Label(root, text="output").grid(row=rowl, column=0)
global var21; var21 = StringVar()
Entry(root, bd =5, textvariable=var21, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text=("print output pars, ima_title, ima_name, print_chi, " +
                  "plot points used to the fitting, EW areas")).grid(row=rowl,
                  column=exp, sticky=W)

rowl+= 1
Label(root, text="outdirec").grid(row=rowl, column=0)
global var14; var14 = StringVar()
Entry(root, bd =5, textvariable=var14, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="output directory").grid(row=rowl, column=exp, sticky=W)

rowl+= 1
Label(root, text="logfile").grid(row=rowl, column=0)
global var15; var15 = StringVar()
Entry(root, bd =5, textvariable=var15, width=sizentry).grid(row=rowl, column=1,
                                                            columnspan=span)
Label(root, text="logfile").grid(row=rowl, column=exp, sticky=W)


rowl+= 1
Label(root, text="       ").grid(row=rowl, column=0, sticky=W)
rowl+= 1
Label(root, text="Press key 'd' for a guess " +
                 "for blend lines or 'r' for a guess for emission lines").grid(
      row=rowl,
      column=0, columnspan=3)
rowl+= 1
Label(root, text="       ").grid(row=rowl, column=0, sticky=W)
rowl+= 1

rowl+= 1
Button(root, text='go', command=go).grid(row=rowl, column=0)
Button(root, text='close', command=quit).grid(row=rowl, column=1)
Button(root, text='open file', command=fopen).grid(row=rowl, column=2)
Button(root, text='save file',command=fsave).grid(row=rowl, column=3)
rowl+= 1
Button(root, text='next', command=next).grid(row=rowl, column=0)
Button(root, text='redo', command=redo).grid(row=rowl, column=1)
Button(root, text='write_log', command=write_log).grid(row=rowl, column=2)
Button(root, text='update_par0', command=update_par0).grid(row=rowl, column=3)
rowl+= 1
Button(root, text='see_par0', command=inputpar).grid(row=rowl, column=0)
Button(root, text='see_par',  command=actualpar).grid(row=rowl, column=1)

fopen()

root.mainloop()
