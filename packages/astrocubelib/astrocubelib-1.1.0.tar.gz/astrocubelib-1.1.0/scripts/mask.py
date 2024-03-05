#!/usr/bin/env python
#Author : J. A. Hernandez-Jimenez

import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

from multiprocessing import Process
import time

from astrocubelib import ordnum, cubofit

global ima, lx, ly, temp, imageg, masknameg, AX, ima_lx, ima_ly
global cuben, cubev, tablev, wl_t#hdrv, hedkey
poly=np.zeros([100,2])
i = int(0)

def calli(image, maskname, colormapn='viridis') :

    global ima, lx, ly, temp, imageg, masknameg, contlimg, AX, ima_lx, ima_ly
    imageg = image; masknameg=maskname

    iman = fits.open(image)
    ima = iman[0].data
    ima_lx = ima.shape[1]
    ima_ly = ima.shape[0]
    ima_ext = [1, ima_lx, 1, ima_ly]

    plt.clf()
    fig = plt.figure(1)
    AX = fig.add_subplot(111)

    AX.minorticks_on()
    ima_v = np.copy(ima)
    ima_v = ima_v.ravel()
    ima_v = ima_v[~np.isnan(ima_v)]

    AX.imshow(ima, origin='lower', interpolation='none', extent=ima_ext,
              vmin=np.percentile(ima_v,5), vmax=np.percentile(ima_v,95),
              cmap=colormapn)

    ly,lx=np.shape(ima)
    x=np.arange(lx)
    y=np.arange(ly)
    X,Y=np.meshgrid(x,y)
    X=np.reshape(X,(lx*ly))
    Y=np.reshape(Y,(lx*ly))
    temp=np.column_stack((X,Y))

    cid = pl.connect('key_press_event', click)
    #disconnect(cid)
    plt.show()

def callcubo(cubename,cubet, tablet, wl_t):
    global cuben, cubev, tablev, wl
    cuben  = cubename
    cubev  = cubet
    tablev = tablet
    wl = wl_t

def click(event):
    global poly,f,i,g,temp, lx, ly, ima, imageg, masknameg, AX, ima_lx, ima_ly
    global cuben, cubev, tablev, hdrv, hedkey

    if (event.key != 'd' and event.key != 'p' and event.key !='m' and
        event.key !='z' and event.key !='c' and event.key !='q' and
        event.key !='x' and event.key !='t' and
        event.key !='i' and event.inaxes) :
        print ("Only use 'd', 'p', 'm', 'z', 'x', 'c' and 'q' keys")

    elif event.key =='d':
        poly[i,0],poly[i,1] = event.xdata,event.ydata
        plt.plot(poly[0:i+1,0],poly[0:i+1,1],'rs-')
        plt.axis([1, lx, 1, ly])
        plt.draw()
        i += 1


    elif event.key=='p':
        poly[i,0],poly[i,1] = poly[0,0],poly[0,1]
        plt.plot(poly[0:i+1,0], poly[0:i+1,1],'rs-')
        plt.axis([1, lx, 1, ly])
        plt.draw()
        time.sleep(2)
        poly = np.resize(poly,(i+1,2))

        try :
            from matplotlib import path
            pa=path.Path(poly)
            inside = path.Path.contains_points(pa,temp)
        except :
            import matplotlib.nxutils as nx
            inside = nx.points_inside_poly(temp, poly)

        insidepix=np.nonzero(inside)[0]
        skyv=[ima[temp[e,1],temp[e,0]]    for e in insidepix]
        print ("\nSky mean : %s" %(np.round(np.mean(skyv),2)))
        print ("Sky median : %s" %(np.round(np.median(skyv),2)))
        print ("Sky standard deviation : %s" %(np.round(np.std(skyv),2)))
        print ("Sky area : %s"%(len(skyv)))
        print ("Sky flux : %s"%(np.round(np.sum(skyv),2)))
        print ("Sky maximum : %s"%(np.max(skyv)))
        print ("Sky minimum : %s"%(np.min(skyv)))

        filla=np.zeros([len(insidepix),2])
        filla[:,0]=[temp[e,0] for e in insidepix]
        filla[:,1]=[temp[e,1] for e in insidepix]
        plt.plot(filla[:,0],filla[:,1],'r.')

        fig=plt.figure(2)
        ax = fig.add_subplot(111)
        ax.hist(skyv, 10,facecolor='green', alpha=0.75)
        ax.set_xlabel('Counts')
        ax.set_ylabel('Number Pixels')
        plt.show()

        poly=np.zeros([100,2])
        i=0

    elif event.key=='c':
        #plt.close(1)
        plt.clf()
        #plt.imshow(ima,origin='lower',aspect='auto')
        poly=np.zeros([100,2])
        i=0
        time.sleep(2)
        calli(imageg, masknameg)
        plt.show()
        plt.draw()

    elif event.key=='m':
        poly[i,0],poly[i,1] = poly[0,0],poly[0,1]
        plt.plot(poly[0:i+1,0],poly[0:i+1,1],'rs-')
        plt.axis([0, lx, 0, ly])
        #poly = np.resize(poly,(i+1,2))
        polym = np.copy(poly[0:i+1,0:i+1])
        plt.draw()
        time.sleep(2)

        # load image in matrix
        imagemn = fits.open(imageg)
        imagem = imagemn[0].data

        # region mask
        regmask = maskpoly(polym,temp,imagem*np.nan)

        # saving the mask image
        fits.writeto(masknameg,regmask*0.0,overwrite=True)
        # plotting the mask image
        plt.clf()
        plt.imshow(regmask,origin='lower')
        plt.show()
        plt.draw()

    elif event.key=='z':
        mx, my = int(event.xdata), int(event.ydata)
        AX.vlines(mx, 1, ima_ly)
        AX.hlines(my, 1, ima_lx)
        tname  = str(ordnum(mx)) + '_' + str(ordnum(my))
        print ("\nResults for pixel x: {} and y:{}\n".format(mx, my))
        #p = Process(target=cubofit, args=([tablev, tname, cubev, wl, [8,5]]))
        #p.start()
        #p.join()
        if tablev !=0:
            cubofit(tablev, tname, cubev, wl, [8,5])
            plt.draw()
        else:
            fig = plt.figure(5)
            AX5=fig.add_subplot(1,1,1)
            #print(cubev)
            print(cubev.shape)
            AX5.plot(wl, cubev[:,my-1,mx-1], label='spectrum')
            AX5.set_title('Spectrum of spaxel central 37, 37')
            AX5.set_xlabel('$\lambda \, [\AA]$')
            AX5.set_ylabel('flux')
            #AX5.legend()
            plt.show()

    elif event.key=='x':
        mx, my = int(event.xdata), int(event.ydata)
        AX.vlines(mx, 1, ima_ly)
        AX.hlines(my, 1, ima_lx)
        AX.draw
        tname  = str(ordnum(mx)) + '_' + str(ordnum(my))
        print ("\nResults for pixel x: {} and y:{}\n".format(mx, my))
        #p = Process(target=cubofit, args=([tablev, tname, cubev, wl, [8,5]]))
        #p.start()
        #p.join()
        cubofit(tablev, tname, cubev, wl, [8,5], GH_plot='yes')


    elif event.key=='i':
        cx,cy = str(int(event.xdata)), str(int(event.ydata))
        spec=cuben+'['+cx+','+cy+',*]'
        import os
        print (spec)
        os.system('plot_spec.py %s'%(spec))

    elif event.key=='t':
        cx,cy = int(event.xdata), int(event.ydata)
        AX.vlines(cx, 1, ima_ly)
        AX.hlines(cy, 1, ima_lx)
        AX.draw
        print ("\nThe spectrum for the spaxel x: {} and y:{}\n".format(cx, cy))
        plt.figure(figsize=[8,5])
        specp = cubev[:, cy-1, cx-1]
        plt.plot(wl, specp, label='spectrum')
        plt.title('Spectrum of spaxel central {}, {}'.format(cx, cy))
        plt.xlabel('$\lambda \, [\AA]$')
        plt.ylabel('flux')
        plt.ylim(np.nanpercentile(specp,1),np.nanpercentile(specp,99))
        plt.legend()
        plt.show()


    elif event.key=='q':
        import sys
        sys.exit()

def maskpoly(poly,temp,imav):

    try:
        from matplotlib import path
        pa=path.Path(poly)
        inside = path.Path.contains_points(pa,temp)
    except:
        import matplotlib.nxutils as nx
        inside = nx.points_inside_poly(temp, poly)

    insidepix=np.nonzero(inside)[0]
    for e in insidepix :
        imav[temp[e,1],temp[e,0]] = 0.0

    return imav
