#!python
#Author : J. A. Hernandez-Jimenez

# Import Modules
from numpy import *
import sys
import warnings
warnings.filterwarnings("ignore")
import argparse
from astrocubelib import *

parser = argparse.ArgumentParser(description='Create a velocity channel map')
parser.add_argument("inputf", nargs='?', metavar='input', help="input file")
parser.add_argument("-i", "--info", action="store_true",
                    help='give a example how to built input file')
parser.add_argument("-l", "--lines", action="store_true",
                    help='print a list of available lines')
parser.add_argument("-w", choices=['yes', 'no'],
                    dest='writeVC', default='no',
                    help='write a .fits for each velocity channel, default no')

args = parser.parse_args()

if args.info:
   print('\nThe input file must contains the following parameters:'
         '\n\ncube.fits           # cube name'
         '\ncrval3,cdelt3,0     # Header Keywords (crval, cdelt, ext)'
         '\n0.1,arcsec          # scale, unit '
         '\nhalfa               # Line name* (e.g., halfa, OIII)'
         '\n8919,1              # value, 0 (z) or (1) vsys'
         '\n5,4,1               # limits channel velocity (left, '
         'right, step) '
         '\n20,30               # limit continum left, rigth (A)'
         '\n30,30               # width continum left, rigth (A)'
         '\n-18,-16,1,0         # '
         'flux nivels [vmin, vmax, scale (0=norm, 1=log), n;'
         'cutoff pixels with < n*sigma] '
         "\njet                 # color map, bar format, e.g, %0.1f "
         '\n3,4,15.0            # nrow, ncols, sizeima (inch)'
         '\n0.6,1.8,medium,k      # velocity text in channels x , y,'
         'sizetxt, color; x,y in unit use by image'
         '\nchannel.png         # output image name'
         '\n\n * to see a list of available lines just type: '
         '\n  $ cube_channel.py -l'
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
   i=0
else:
   parser.print_usage()
   sys.exit()

# Input Parameters

espectro = finput[i].split()[0];i+=1
hedkey   = finput[i].split()[0].split(',');i+=1
scale    = finput[i].split()[0].split(',');i+=1
line     = finput[i].split()[0];i+=1
z        = finput[i].split()[0].split(',');i+=1
chlim    = [int(s) for s in finput[i].split()[0].split(',')];i+=1
linesc   = [float(s) for s in finput[i].split()[0].split(',')];i+=1
linesw   = [float(s) for s in finput[i].split()[0].split(',')];i+=1
fluxv    = [float(s) for s in finput[i].split()[0].split(',')];i+=1
cmap     = finput[i].split()[0].split(',');i+=1
chszima  = [ float(s) for s in finput[i].split()[0].split(',')];i+=1
chtext   = finput[i].split()[0].split(',');i+=1
mapname  = finput[i].split()[0];i+=1

spec = pf.getdata(espectro)
hdr  = pf.getheader(espectro, ext=int(hedkey[2]))

y=spec.shape[1]
x=spec.shape[2]

axislab=scale[1]; dx=float(scale[0]); dy=float(scale[0])
axiscoord=[-x*dx*0.5, x*dx*0.5, -y*dy*0.5, y*dy*0.5]

# Calculating the redshift of the study line (e.g., 'halfa')
if z[1] == '1':
    z = float(z[0])
    vsys = z
    z = (z/speedc) + 1.0
    # redshift of the study line
    lc = z*diclines[line]
else:
    z = float(z[0])
    vsys = speedc*z
    z = z + 1.0
    # redshift of the study line
    lc = z*diclines[line]

nchannels = chlim[0] + chlim[1] + 1
nrows = int(chszima[0])
ncols = int(chszima[1])

if ncols*nrows < nchannels:
     raise AttributeError('The number of channels <= ncols*nrows')


chtext=[float(chtext[0]), float(chtext[1]), chtext[2], chtext[3]]

labelbar = '$\\rm{F}_{'+linelatex[line]+'}$'

if fluxv[2] == 1.0:
    labelbar = '$\log\,('+linelatex[line]+')$'


# Channel maps
channelvel(spec, line, lc, chlim, [hdr[hedkey[0]], hdr[hedkey[1]]],
           [linesc[0]+linesw[0], linesc[0], linesc[1], linesc[1]+linesw[1]],
           vsys, mapname, axiscoord,
           axislab, axislab, labelbar, fluxv, cmap,
           chszima, chtext, args.writeVC)
