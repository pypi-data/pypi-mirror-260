#!python
#Author : J. A. Hernandez-Jimenez

# Import Modules
import sys
import os
import time
import warnings
warnings.filterwarnings("ignore")
import argparse
from astrocubelib import *
from astropy.io.votable import parse
from astropy.table import Table, Column

from astropy import wcs
from astropy.io import fits


parser = argparse.ArgumentParser(description='Fit a set of emission or'
             ' absorbtion lines given a data cube')
parser.add_argument("inputf", nargs='?', metavar='input', help="input file")
parser.add_argument("-i", "--info", action="store_true",
                    help='give a example how to built input file')
parser.add_argument("-l", "--lines", action="store_true",
                    help='print a list of available lines')

args = parser.parse_args()

if args.info:
    print('\nThe input file must contains the following parameters:'


          '\n\nhalfa,NII     # Lines to fit* (e.g.,halfa,OIII)'
          '\n2,2             # sigma line guesses (A)'
          '\n0               # center guesses for deblend lines (A)'
          '\n0               # guesses for sigmas deblend lines'
          '\n0,0             # sigma fixes, 0 to free or 1 to fix**'
          '\n0,0             # center fixes, 0 to free or 1 to fix**'
          '\n0,0             # core  fixes, 0 to free or 1 to fix**'
          '\n3,3,3,3       # to mask the pixels around the lines (-n*sig,n*sig)'
          '\n10.0,10.0       # left and right limits for fit interval (A)'
          '\n60.0,15.0       # left and right continuum limits*** (A)'
          '\n40,20           # left and right continuum intervals (A)'
          '\npoly,1,no       # function fit to continuum****'
          "\n0.02953465      # value; 0 (z) or (1) vsys; 'yes' for Relt. Corc."
          '\ncrval3,cdelt3,0 # Header Keywords (crval,cdelt,ext)'
          '\ncube.fits       # cube name'
          '\nnone            # mask name '
          '\nhalfa_NII       # output table name'
           '\n-              # verbose'
          '\n\n * to see a list of available lines just type: '
          '\n   $ cube_channel.py -l'
          '\n\n ** you can create a set of lines that share the same sigma ( '
          '\n    center or keep a ratio constant, like NII(6548, 6583)), for'
          '\n    example, if you want to fit NII2,halfa,NII,SII,SII2 at the'
          '\n    same time, and those lines have the same sigma, you can say:'
          '\n\n        1,1,1,1,1  # sigma fixes, 0 to free or 1 to fix**'
          '\n\n    now, if you want that NII2,halfa,NII have the same sigma,'
          '\n    but SII,SII2 have another sigma but the same each other, then'
          '\n\n        1,1,1,2,2  # sigma fixes, 0 to free or 1 to fix**'
          '\n\n *** give two distance (in A), the first one is the distance'
          '\n     to continuum from the line with smaller wavelenght. The'
          '\n     second one is the distance to continuum from the line'
          '\n     with larger wave lenght.'
          '\n\n **** functions to be used to fit the continuum you can choose'
          '\n      between polynomial or chebchiv functions, the second'
          '\n      parameter is the degree of the functions, and the last'
          '\n      one you can choose if you want the continnum be fit'
          '\n      along the lines or not.'
         )
    sys.exit()

if args.lines:
   print('A list of available lines:'
       '\n\nCaII_H: 3933.663'
       '\nCaII_K: 3968.468'
       '\nMgb: 5174.537'
       '\nMgbI: 5167.3212'
       '\nMgbII: 5172.6844'
       '\nMgbIII: 5183.6043'
       '\nMgbI_II: 5170.0028'
       '\nNII: 6583.46'
       '\nNII2: 6548.04'
       '\nNII3: 5754.644'
       '\nNa_D: 5892.9375'
       '\nNa_DI: 5889.951'
       '\nNa_DII: 5895.924'
       '\nOI: 6300.304'
       '\nOIII: 5006.843'
       '\nOIII2: 4958.911'
       '\nOIII3: 4363.21'
       '\nSII: 6716.44'
       '\nSII2: 6730.81'
       '\nhalfa: 6562.8'
       '\nhbeta: 4861.325'
       '\nhdelta: 4102.892'
       '\nheI: 5875.6'
       '\nheII: 4685.71'
       '\nhgamma: 4340.464')
   sys.exit()

if args.inputf:
   finput = open(args.inputf).read().splitlines()
   j=0
else:
   parser.print_usage()
   sys.exit()

# Input Parameters

clines  = finput[j].split()[0].split(',');j+=1
linesig = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linesb   = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linesigb = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linessigfix  = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linescentfix = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linescorefix = [float(s) for s in finput[j].split()[0].split(',')];j+=1
line_masks = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linesin = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linesc   = [float(s) for s in finput[j].split()[0].split(',')];j+=1
linesw   = [float(s) for s in finput[j].split()[0].split(',')];j+=1
contfunc = finput[j].split()[0].split(',');j+=1
z        = finput[j].split()[0].split(',');j+=1
#z        = [float(s) for s in finput[j].split()[0].split(',')];j+=1

hedkey   = finput[j].split()[0].split(',');j+=1
espectro = finput[j].split()[0];j+=1
mask     = finput[j].split()[0];j+=1
nametab  = finput[j].split()[0];j+=1
verbose  = finput[j].split()[0];j+=1

# Begin Time
start_time = time.time()

# Load Cubo
#spec = pf.getdata(espectro)
# Header of the  Cubo
hdr  = pf.getheader(espectro, ext=int(hedkey[2]))
# Wavelenght spectrum
#wl   = linspace(hdr[hedkey[0]], (len(spec)-1)*hdr[hedkey[1]] + hdr[hedkey[0]],
                len(spec))


spec = np.transpose(cube['FLUX'].data, axes=(2, 1, 0))
#ivar = np.transpose(cube['IVAR'].data, axes=(2, 1, 0))
#mask = np.transpose(cube['MASK'].data, axes=(2, 1, 0))

wl = cube['WAVE'].data
#flux_header = cube['FLUX'].header

# Load mask
if mask != 'none':
    amask = pf.getdata(mask)
else:
    amask = zeros(spec.shape[1::])


z[0] = float(z[0])
z[1] = float(z[1])
# Eq. Relativistic
if z[2] == 'yes':
    if z[1] == 1.0:
        velr = z[0]
        beta = velr/speedc
        z = sqrt((1. + beta)/(1. - beta))
    else:
        z = z[0]
# Eq. no Relativistic
else:
    if z[1] == 1.0:
        velr = z[0]
        z = velr/speedc
    else:
        z = z[0]

# array with the line wavelengths in rest  lines_lambda
lines_lambda=[]
for i in clines:
    lines_lambda.append(diclines[i])

# add to lines_lambda the deblend lines
# create a array with the name of all lines linestmp
linestmp = clines
numd=1
for i in linesb:
    if i!=0 :
        lines_lambda.append(i)
        linestmp.append('deblend_'+str(numd))
        numd += 1

# sort in wavelength the arrays
linesort = array(lines_lambda[:]).argsort()
linestmp = take(linestmp,linesort)
print ('lines to fit ', linestmp)


# to create the fit directoty or confirm its exitence
direc = []
for i, line in enumerate(linestmp):
    path = './'+ 'fit.'+ line
    direc.append('fit.'+ line)
    if not os.path.exists(path):
        os.mkdir(direc[i])

# name of the output files containing the fit information for each line
fitname = []
if mask == 'none':
    for line in linestmp :
        fitname.append('fit.' + line + '.dat')
else:
    for line in linestmp :
        os.system('rm -fv ./fit.{0}/fit.{0}.dat.tmp'.format(line))
        fitname.append('fit.' + line + '.dat.tmp')

# create or open the output table
if mask == 'none':
     tabfit = Table()
else:
     tabfit = Table.read('fit_'+nametab+'.html',format='html')

# create deblend temporate fit file
deb_tname = []

text_tab = ('{:>10s} {:>10.3e} {:>10.2f} {:>10.2f} {:>10.3e} {:>10.3e} ' +
           '{:>10.2f} {:>10.2f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f} ' +
           '{:>10.3e} {:>10.3e} {:>10.3e} {:>10.2f} {:>10.2f} {:>10.2f} ' +
           ' {:>10.2f}')
len_tab = 19

for index, pix0 in ndenumerate(spec[0,:,:]):

    y = index[0]
    x = index[1]
    deb_tname.append(ordnum(x+1) + '_' + ordnum(y+1))
    if amask[y,x] == 0:

        vspec = spec[:, y, x]
        tname = ordnum(x+1) + '_' + ordnum(y+1)
        fig   = 's_'+ tname + '.png'
        wng   = 'no'
        print ("*fit for the spectro {0} of the Emission Line {1} ".format(
               tname, clines))

        if linesb[0] == 0:
            vfit_tmp = fitmultiline(wl,vspec,hdr[hedkey[0]], hdr[hedkey[1]],
                       clines, linesig, linessigfix=linessigfix,
                       linescentfix=linescentfix,
                       linescorefix=linescorefix,
                       z=z, lineslim=linesin,
                       line_masks=line_masks,
                       cont_l=[linesc[0]+linesw[0],linesc[0]],
                       cont_r=[linesc[1],linesc[1]+linesw[1]],
                       contfunc=contfunc,
                       plot='no', figtit=fig, figname=fig, direc=direc,
                       showp='no', verbose=verbose, nflog = None
                       )

        else:
            clines    = finput[0].split()[0].split(',')
            vfit_tmp  = fitmultiline(wl, vspec,hdr[hedkey[0]], hdr[hedkey[1]],
                       clines, linesig, linessigfix=linessigfix,
                       linescentfix=linescentfix,
                       linescorefix=linescorefix,
                       linesb=linesb, linessigb=linesigb,
                       z=z, lineslim=linesin,
                       line_masks=line_masks,
                       cont_l=[linesc[0] + linesw[0], linesc[0]],
                       cont_r=[linesc[1], linesc[1] + linesw[1]],
                       contfunc=contfunc,
                       plot='no', figtit=fig, figname=fig, direc=direc,
                       showp='no', verbose=verbose, nflog = None
                       )


        vfit   = array(vfit_tmp[0])
        if mask != 'none':
            tabfit.remove_column(tname)

        tabfit.add_column(Column(data=[
            ','.join(map(str,asarray(vfit_tmp[0]).ravel())),
            ','.join(vfit_tmp[1]),
            ','.join(map(str,asarray(vfit_tmp[2]).ravel())),
            ','.join(vfit_tmp[3]),
            ','.join(map(str,asarray(vfit_tmp[4]).ravel())),
            ','.join(map(str,asarray(vfit_tmp[5]).ravel())),
            ], name=tname))


        for i, tfit  in enumerate(vfit):
            nfilelog = './' + direc[i] + '/' + fitname[i]

            outline = text_tab.format(tname, *tfit)

            try:
                if tname in open(nfilelog).read():
                    os.system("sed -i 's/.*%s.*/%s/' %s"%(tname, outline,
                              nfilelog))
                else:
                    nfile=open(nfilelog, 'a')
                    nfile.write(outline + '\n')
                    nfile.close()

            except:
                nfile=open(nfilelog, 'a')
                nfile.write(outline + '\n')
                nfile.close()

print ('Printing data files...')
if mask != 'none':
    for line in linestmp:

        print (line)
        ndat='./fit.{0}/fit.{0}.dat'.format(line)
        ndattmp='./fit.{0}/fit.{0}.dat.tmp'.format(line)
        vnamespectmp = loadtxt(ndattmp,dtype='string', usecols=([0]))
        vdatatmp  = loadtxt(ndattmp, usecols=arange(1,len_tab))

        if os.path.exists(ndat):

            vnamespec = loadtxt(ndat,dtype='string', usecols=([0]))
            vdata = loadtxt(ndat, usecols=arange(1,len_tab))

            for i, namespec in enumerate(vnamespectmp):
                vdata[vnamespec[:]==namespec, :] = vdatatmp[i, :]

            nfile = open(ndat,'w')

            for j, namespec in enumerate(vnamespec):

                outline = text_tab.format(namespec, *vdata[j,:])
                nfile.write(outline + '\n')

            nfile.close()

        else:
            nfile = open(ndat,'w')
            for  tname in deb_tname:

                tfit  = ones((len_tab-1))*nan
                if any(array(vnamespectmp)==tname):
     	            tfit = vdatatmp[vnamespectmp==tname, :][0]

                outline = text_tab.format(tname, *tfit)
                nfile.write(outline+'\n')

            nfile.close()

if os.path.exists('fit_'+nametab+'.html'):
    os.system("rm -rf fit_{0}.html".format(nametab))
print ('writing fit table ...')
tabfit.write('fit_'+nametab+'.html',format='html')

# Time Lapsed
timet=(time.time() - start_time)/60.0
print ('Time total lapsed:')
print ('%2.1f' %(fix(timet)), 'minutes', '%2.1f' %((timet-fix(timet))*60.0),
       'seconds')
