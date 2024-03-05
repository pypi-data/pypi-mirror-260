#!/usr/bin/env python
#Author : J. A. Hernandez-Jimenez
#Task module

import numpy as np
from numpy.polynomial import polynomial as P
from numpy.polynomial.chebyshev import chebval,chebfit

from scipy.optimize import leastsq
from scipy.stats import skew, skewtest, kurtosis
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.colors import *
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy.io import fits

import os

import functions as func

from colorama import Fore

global ax

# new color map
mapb_rgb = { 'red'  : ((0.0, 0.0, 0.0),
                       (0.25, 0.0, 0.0),
                       (0.5, 1.0, 1.0),
                       (1.0, 1.0, 1.0)),

            'green' : ((0.0, 0.0, 0.0),
                       (0.5, 0.0, 0.0),
                       (0.75, 1.0, 1.0),
                       (1.0, 1.0, 1.0)),

            'blue' :  ((0.0, 0.0, 0.0),
                       (0.25, 1.0, 1.0),
                       (0.5, 0.0, 0.0),
                       (0.75, 0.0, 0.0),
                       (1.0, 1.0, 1.0)),
           }
mapb = LinearSegmentedColormap('b',mapb_rgb)
plt.register_cmap(cmap=mapb)


# Dictionary of the laboratory wavelength
diclines = {
            'OII': 0.5*(3726.0 + 3728.8), 'OII_a': 3726.0, 'OII_b':3728.8,
            'hdelta': 4102.892, 'hgamma': 4340.464, 'heII': 4685.71,
            'hbeta': 4861.325, 'OIII3': 4363.210, 'OIII2': 4958.911,
            'OIII': 5006.843, 'heI': 5875.6, 'OI': 6300.304,
            'halpha': 6562.80, 'NII3': 5754.644, 'NII2': 6548.04,
            'NII': 6583.46, 'SII': 6716.44, 'SII2': 6730.81,'SIII':6312.1,
            'CaII_H': 3933.663, 'CaII_K' : 3968.468,
            'Mgb': (5167.3212+5172.6844+5183.6043)/3., 'MgbI': 5167.3212,
            'MgbII': 5172.6844, 'MgbIII' : 5183.6043,
            'MgbI_II': (5167.3212+5172.6844)*0.5,
            'Na_D': (5889.951+5895.924)*0.5,
            'Na_DI': 5889.951, 'Na_DII': 5895.924,

            'Ca IIa': 8498.0200,
            'Ca IIb': 8541.8800,
            'Ca IIc': 8661.8500,

            # Lick Indexes
            'CN_1'   :(4142.125 + 4177.125)*0.5,
            'CN_2'   :(4142.125 + 4177.125)*0.5,
            'Ca4227' :(4222.250 + 4234.750)*0.5,
            'G4300'  :(4281.375 + 4316.375)*0.5,
            'Fe4383' :(4369.125 + 4420.375)*0.5,
            'Ca4455' :(4452.125 + 4474.625)*0.5,
            'Fe4531' :(4514.250 + 4559.250)*0.5,
            'Fe4668' :(4634.000 + 4720.250)*0.5,
            'Fe5015' :(4977.750 + 5054.000)*0.5,
            'Mg_1'   :(5069.125 + 5134.125)*0.5,
            'Mg_2'   :(5154.125 + 5196.625)*0.5,
            'Fe5270' :(5245.650 + 5285.650)*0.5,
            'Fe5335' :(5312.125 + 5352.125)*0.5,
            'Fe5406' :(5387.500 + 5415.000)*0.5,
            'Fe5709' :(5696.625 + 5720.375)*0.5,
            'Fe5782' :(5776.625 + 5796.625)*0.5,
            'TiO_1'  :(5936.625 + 5994.125)*0.5,
            'TiO_2'  :(6189.625 + 6272.125)*0.5,


            # Fe lines
            #'FEI_a': 5159.05,
            'FEI_a': 5157.11,
            'FEI_b': 5242.49,
            'FEI_c': 5253.03,
            'FEI_d': 5288.52,
            'FEI_e': 5321.1 ,
            'FEI_f': 5322.04,
            'FEI_g': 5364.87,
            'FEI_h': 5367.46,
            'FEI_i': 5373.7,

            '26_01':  5159.05,
            '26_02':  5242.49,
            '26_03':  5253.03,
            '26_04':  5288.52,
            '26_05':  5321.10,
            '26_06':  5322.04,
            '26_07':  5364.87,
            '26_08':  5367.46,
            '26_09':  5373.70,
            '26_10':  5389.47,
            '26_11':  5410.91,
            '26_12':  5417.03,
            '26_13':  5441.33,
            '26_14':  5445.04,
            '26_15':  5522.44,
            '26_16':  5554.89,
            '26_17':  5560.21,
            '26_18':  5584.76,
            '26_19':  5624.02,
            '26_20':  5633.94,
            '26_21':  5635.82,
            '26_22':  5638.26,
            '26_23':  5691.49,
            '26_24':  5705.46,
            '26_25':  5717.83,
            '26_26':  5731.76,
            '26_27':  5806.72,
            '26_28':  5814.80,
            '26_29':  5852.21,
            '26_30':  5883.81,
            '26_31':  5916.24,
            '26_32':  5934.65,
            '26_33':  6024.05,
            '26_34':  6027.05,
            '26_35':  6056.00,
            '26_36':  6079.00,
            '26_37':  6093.64,
            '26_38':  6096.66,
            '26_39':  6120.24,
            '26_40':  6151.61,
            '26_41':  6157.72,
            '26_42':  6165.36,
            '26_43':  6170.50,
            '26_44':  6173.33,
            '26_45':  6187.99,
            '26_46':  6200.31,
            '26_47':  6322.68,
            '26_48':  6380.74,
            '26_49':  6392.53,
            '26_50':  6419.95,
            '26_51':  6436.40,
            '26_52':  6469.19,
            '26_53':  6518.36,
            '26_54':  6551.67,
            '26_55':  6574.22,
            '26_56':  6591.31,
            '26_57':  6593.87,
            '26_58':  6597.56,
            '26_59':  6608.02,
            '26_60':  6609.11,
            '26_61':  6646.93,
            '26_62':  6653.85,
            '26_63':  6699.14,
            '26_64':  6703.56,
            '26_65':  6704.48,
            '26_66':  6710.31,
            '26_67':  6713.74,
            '26_68':  6739.52,
            '26_69':  6745.95,
            '26_70':  6750.15,
            '26_71':  6752.70,
            '26_72':  6783.70,
            '26_73':  6793.25,
            '26_74':  6806.84,
            '26_75':  6810.26,
            '26_76':  6820.37,
            '26_77':  6851.63,
            '26_78':  6858.15,
            '26_79':  7130.92,
            '26_80':  7132.98,

            '26.1_01': 4993.34,
            '26.1_02': 5132.65,
            '26.1_03': 5197.55,
            '26.1_04': 5234.61,
            '26.1_05': 5284.09,
            '26.1_06': 5325.55,
            '26.1_07': 5414.04,
            '26.1_08': 5425.24,
            '26.1_09': 5991.36,
            '26.1_10': 6084.09,
            '26.1_11': 6149.24,
            '26.1_12': 6247.54,
            '26.1_13': 6416.92,
            '26.1_14': 6432.68,

            '8_01': 7771.94,
            '8_02': 7774.17,
            '8_03': 7775.39,

            '11_01':   5148.84,
            '11_02':   5682.63,
            '11_03':   6154.23,
            '11_04':   6160.75,

            '12_01':   7387.69,
            '12_02':   7691.55,
            '12_03':   8712.69,
            '12_04':   8717.83,
            '12_05':   8736.02,
            '12_06':   7387.69,

            '13_01':   6696.02,
            '13_02':   6698.67,
            '13_03':   7362.30,
            '13_04':   7835.31,
            '13_05':   7836.13,
            '13_06':   8772.87,
            '13_07':   8773.90,

            '39.1_01':	4883.68,
            '39.1_02':	5087.43,
            '39.1_03':	5123.21,
            '39.1_04':	5200.42,
            '39.1_05':	5205.72,
            '39.1_06':	5289.82,
            '39.1_07':	5402.78,

            '40_01':    5385.13,
            '40_02':    6127.46,
            '40_03':    6134.57,
            '40_04':    6143.18,

            '57.1_01':   5303.53,
            '57.1_02':   5880.63,
            '57.1_03':   6390.48,

            '58.1_01':     4628.16,
            '58.1_02':     5187.46,
            '58.1_03':     5274.24,
            '58.1_04':     5472.30,

            '60.1_01':     4811.34,
            '60.1_02':     4959.12,
            '60.1_03':     5130.59,
            '60.1_04':     5234.19,
            '60.1_05':     5311.46,
            '60.1_06':     5319.81,
            '60.1_07':     5740.88
            }

linelatex = {'heI':'{\\rm HeI}', 'heII':'{\\rm HeII}',
             'hdelta': '{\\rm H}_{\\delta}',
             'hgamma':'{\\rm H}_{\\gamma}', 'hbeta':'{\\rm H}_{\\beta}',
             'OI':'[{\\rm OI}]\\,\\lambda 6300',
             'OII':'[{\\rm OII}]\\,\\lambda 3727',
             'OIII3':'[{\\rm OIII}]\\,\\lambda 4363',
             'OIII2':'[{\\rm OIII}]\\,\\lambda 4959',
             'OIII':'[{\\rm OIII}]\\,\\lambda 5007',
             'halpha':'{\\rm H}_{\\alpha}',
             'NII':'[{\\rm NII}]\\,\\lambda 6583',
             'NII2':'[{\\rm NII}]\\,\\lambda 6548',
             'NII3': '[{\\rm NII}]\\,\\lambda 5755',
             'SII':'[{\\rm SII}]\\,\\lambda 6716',
             'SII2':'[{\\rm SII}]\\,\\lambda 6731',
             'SIII':'[{\\rm SIII}]\\,\\lambda 6312'}

# Light speed (km/sec)
speedc = 299792.0
# FWHM
gfwhm = 2*np.sqrt(2*np.log(2))


def z_vsys(nline, lline, rline=0, rspeedc=0):
    '''
    The function determines for a reference line (e.g., halfa, hbeta, etc) the
    redshift and system velocity from the observed wavelength.

    Parameters
    ----------
    nline: str,
        line name, look at the line dictionary: diclines.
    lline: float,
        line observed wavelength.
    rline: float,
        laboratory wavelength for the line in case that it is not at diclines.
    rspeedc: float,
        value of speed of light given by the user.

    Return
    ------

    z, vsys

    '''
    if rline == 0:
        rline = diclines[nline]
    if rspeedc == 0:
        rspeedc = speedc

    z = (lline - rline)/rline
    vsys = z*rspeedc
    print ("The wavelength of reference for {0}  is {1}.\nThe c speed value"
            + " used is: {2}").format(nline,  rline, rspeedc)
    print ("   z               vsys:")
    print (z, vsys)

    return z, vsys


def input_lin(alines, velshift):
    '''
    For a given recessional or system velocity (vsys) the script calculates what
    would be the new wavelength of the lines.

    Parameters
    ----------
    alines: array (type=str),
        a list of names of lines, look at the line dictionary: diclines.
    shift: float,
        recessional or system velocity value.
    Return
    ------
    an array (type=float) with the new calculated wavelength
    '''
    nlines   = np.zeros(len(alines))
    lablines = np.zeros(len(alines))
    for i, line in enumerate (alines):
            nlines[i] = (diclines[line]*(velshift/speedc)) + (diclines[line])
            lablines[i] = diclines[line]

    print ("Lines: ", alines)
    print ("Wavelength at laboratory", lablines)
    nlines = [round(s, 2) for s in nlines]
    print ("With a vsys={0} km/s the wavelengths observed are: ".format(
           velshift), nlines)


    return nlines

def slidecube(cuben, wrange, outputn, hedkey=['CRVAL3','CDELT3','0']):
    """
    From a given range (continuum, line, band), the script collapses
    (make the mean) into a single image.
    """

    # Load Cube
    specn = fits.open(cuben)
    spec = specn[int(hedkey[2])].data
    # Header of the  Cubo
    #hdr  = pf.getheader(cuben, ext=int(hedkey[2]))
    hdr = spec[int(hedkey[2])].header

    #y = spec.shape[1]
    #x = spec.shape[2]

    lref = hdr[hedkey[0]]
    ldel = hdr[hedkey[1]]

    # line profile array
    wrange_l = lamb2idex(wrange[0], lref, ldel)
    wrange_r = lamb2idex(wrange[1], lref, ldel)

    moutspec = spec[wrange_l:wrange_r+1, :, :]
    outspec = np.nanmean(moutspec, axis=0, dtype=np.float64)         # Mean continuum


    fits.writeto(outputn, outspec, overwrite=True)

    return outspec


def intgspec(cuben, maskn, outputn, hedkey=['CRVAL3','CDELT3','0']):
    """
    From a given mask, the script collapses all spectra inside it into a
    single spectrum.

    """
    ## Load Cube
    #spec = pf.getdata(cuben)
    ## Header of the  Cubo
    #hdr  = pf.getheader(cuben, ext=int(hedkey[2]))
    ## Load mask
    #amask = pf.getdata(maskn)

    # Load Cube
    specn = fits.open(cuben)
    spec = specn[int(hedkey[2])].data
    # Header of the  Cubo
    hdr = specn[int(hedkey[2])].header
    amask = fits.open(maskn)[0].data

    i = 0
    for index, pix0 in np.ndenumerate(spec[0,:,:]):

        y = index[0]
        x = index[1]
        if amask[y,x] == 0:
            if i == 0:
                Tspec = spec[:, y, x]
                i = 1
            else:
                Tspec += spec[:, y, x]

    Ospec=fits.PrimaryHDU(Tspec)
    Ospec.header['CTYPE1'] = 'LINEAR '
    Ospec.header['CRPIX1'] = 1
    Ospec.header['CRVAL1'] = hdr[hedkey[0]]
    Ospec.header['CDELT1'] = hdr[hedkey[1]]

    fits.writeto(outputn, Tspec, Ospec.header, overwrite=True)

    return Tspec


def matspec(nspec,namedic,rootname='a',cr='crval1',cd='cdelt1'):
    '''
    The function creates a matrix of a set of one-dimensional spectra

    Parameters
    ----------
    nspec : int or array-type
       number of spectra or [nub_ini,nub_fin]
    namedic : str,
       name of dicretory that has the spectra
    rootname : str, optional
       root name of the spectra; default: 'a'.
    cr : str, optional
       header keyword for crval; default: 'crval1'.
    cd : str, optional
       header keyword for cdelt; default: 'cdelt1'

    Returns
    -------
    A list with the following elements

    perf : 2d array
       each row is a spectrum
    hdr : object,
       image header; pyfits.getheader
    wl : 1d array,
       wavelength array
    n : list,
       prefix number for each spectrum (e.g., '0001', '0002', etc)

    '''
    salida = []
    espectro = namedic +'/'+ rootname +'.'+ ordnum(1) + '.fits'
    #spec = pf.getdata(espectro)
    specn = fits.open(espectro)
    spec = specn[0].data
    n = []
    try :
        nubspec = np.arange(nspec[0], nspec[1]+1)
        perf = np.zeros([len(nubspec), spec.shape[0]])

    except :
        nspec   = int(nspec)
        nubspec =  np.arange(1, nspec+1)
        perf = np.zeros([len(nubspec), spec.shape[0]])

    j=0
    for i in nubspec :

        m=ordnum(i)
        espectro = namedic +'/'+ rootname +'.'+ m + '.fits'
        #spec = pf.getdata(espectro)
        specn = fits.open(espectro)
        spec = specn[0].data
        perf[j, :] =  spec
        #hdr = pf.getheader(espectro)
        hdr = specn[0].header
        wl = linspace(hdr[cr], (len(spec)-1)*hdr[cd]+hdr[cr], len(spec))
        n.append(m)
        j+=1


    salida.append(perf)
    salida.append(hdr)
    salida.append(wl)
    salida.append(n)

    return salida



def cubo2fits(namef,pref='s',namedic='./',crval='CRVAL3',cdelt='CDELT3',
              contlim=None,mask=None):
    '''
    The function unpacks a cube into single spectra.

    Parameters
    ----------
    namef : str
       cube name (e.g., 'cube.fits')
    pref : str, optional
       prefix name of unpacked spectra; default : 's'
    namedic : str, optional
       destiny folder; default : './'
    crval : str, optional
       header keyword for crval; default : 'CRVAL3'.
    cdelt : str, optional
       header keyword for cdelt; default : 'CDELT3'
    contlim = array_like,
        indexes of the interval to calculate S/N of the spectrum (e.g, [10,50])
    mask    = array_line,
        indexes of the intervals to mask any region in the spectrum
        (e.g, [200,250,300,310])

    Returns
    -------
    A matrix with the S/N for each spectrum from cube.

    '''

    # loading cube
    #spec = pf.getdata(namef)
    #hdr  = pf.getheader(namef)
    specn = fits.open(namef)
    spec = specn[0].data
    hdr = sepcn[0].header

    # x and y cube dimensions
    dx = spec.shape[2]
    dy = spec.shape[1]

    sn = np.zeros([dx*dy])

    if not os.path.exists(namedic): os.mkdir(namedic)

    for i in nditer(np.arange(dx)):
        m=ordnum(i+1)
        for j in nditer(np.arange(dy)):
            n=ordnum(j+1)
            nspec = pref+ '_x_'+ m +  '_y_' +  n + '.fits'
            print (i, j)
            fspec=fits.PrimaryHDU(spec[:, j, i])
            fspec.header['CTYPE1'] = 'LINEAR '
            fspec.header['CRPIX1'] = 1
            fspec.header['CRVAL1'] = hdr[crval]
            fspec.header['CDELT1'] = hdr[cdelt]
            if contlim is not None :
                mc = np.nanmean(spec[:, j, i][contlim[0]:contlim[1]])
                sc = np.nanstd(spec[:, j, i][contlim[0]:contlim[1]])
                sn[k] = nan_to_num(abs(mc/sc))
                if mask is not None :
                    for l in range(len(mask)/2) :
                        spec[mask[l*2]:mask[l*2+1], j, i]=mc
            fits.writeto(nspec, spec[:, j, i], fspec.header, overwriter=True)
            os.system("mv %s %s" %(nspec, namedic))

    print ('reference pixel at : ', hdr[crval], 'delta lambda: ',hdr[cdelt])
    print ('final pixel at : ', hdr[crval]+(spec.shape[0]-1)*hdr[cdelt])
    xp = floor(np.nanargmax(sn)/dy) ; yp = np.nanargmax(sn)-(dy*floor(np.nanargmax(sn)/dy))
    print ('The spectrum with the maximum S/N is x = {} y = {}'.format(xp, yp))

    return sn


def spectra2fits(namef, pref='s', namedic='./', contlim=None, mask=None,
                 cnoise='cte'):
    '''
    The function unpacks a multiple extension file.

    Parameters
    ----------
    namef   = str,
        name of multiple extension file.
    pref    = str,
        output prefix
    namedic = str,
        destiny folder
    contlim = array_like,
        indexes of the interval to calculate S/N of the spectrum (e.g, [10,50])
    mask    = array_line,
        indexes of the intervals to mask any region in the spectrum
        (e.g, [200,250,300,310])
    cnoise  = str,
        type of noise to be added to mask range (cte,normal or poisson)

    Return
    ------
    It returns a .fits for each spectrum that makes part of multiple extension
    file
    '''

    #spec = pf.getdata(namef)
    #hdr = pf.getheader(namef)
    specn = fits.open(namef)
    spec = specn[0].data
    hdr = specn[0].header

    dx=spec.shape[0]

    sn=np.zeros([dx])

    if not os.path.exists(path): os.mkdir(namedic)

    k=0
    for i in nditer(np.arange(dx)):
        m=ordnum(i+1)
        nspec = pref + '.' + m + '.fits'
        print (i, nspec)

        if contlim is not None :
            mc    = np.nanmean(spec[i,:][contlim[0]:contlim[1]])
            sc    = np.nanstd(spec[i,:][contlim[0]:contlim[1]])
            sn[k]=nan_to_num(abs(mc/sc))

            if mask is not None :
                for l in range(len(mask)/2) :
                    nub_c = len(spec[i,mask[l*2]:mask[l*2+1]])
                    print (mc)
                    if cnoise == 'cte':
                        spec[i, mask[l*2]:mask[l*2+1]] = mc
                    if cnoise == 'poisson':
                        spec[i, mask[l*2]:mask[l*2+1]] = random.poisson(mc,
                                                                        nub_c)
                    if cnoise == 'normal':
                        spec[i, mask[l*2]:mask[l*2+1]] = random.normal(mc, sc,
                                                                       nub_c)
                    #print random.poisson(mc,nub_c)
                    print (random.normal(mc,sc,nub_c))
        fits.writeto(nspec,spec[i,:],hdr, overwrite=True)
        os.system("mv %s %s" %(nspec,namedic))
        k=k+1

    print ('reference pixel at : {} delta lambda:  {}'.format(hdr['crval1'],
                                                             hdr['cdelt1']))
    print ('final pixel at : ', hdr['crval1']+(spec.shape[1]-1)*hdr['cdelt1'])
    print (('The spectrum with the maximum S/N ({:.2f}) is a' +
            ' number {}').format(max(sn), np.nanargmax(sn)+1))
    return sn

tab_len = 31

def fitmultiline(*args,**kwargs) :
    '''
    Parameters
    -----------
    wl   : array_like; wavelength
    spec : array_like; flux
    lref : float, wavelenght of reference
    ldel : float, delta wavelenght of the spectrum
    line : array_like; [dic,diccont_l,diccont_r]  dic(e.g., hbeta, OIII, halfa)
    linessing : array_like; guess sigma to the lines
    z    : float, redshift of the line
    l1   : float, limit by the left of the range to fit the line
    l2   : float, limit by the right of the range to fit the line
    d_l  : float, range of the interval for the continum to the left
    d_r  : float, range of the interval for the continum to the right
    plot : str, it make a plot of the fit
    figtit  : str, figure title
    figname : str, figure name (e.g., fig.png)
    direc   : str, path where the image will be put
    nubspec : str, number of the spectrum assigned by the user

    Return
    -----------
    grev     : array_like; parameters fitted
    grev_erf : array_like; error of parameters fitted
    meancont : float; mean of the continum
    sigcont  : float; sigma of the continum
    csig     : float; signal-to-noise continum
    lsig     : float; signal-to-nose line
    lerr     : float; error at the line
    fgauss   : float; flux in the gaussian function fitted
    fline    : float; flux in the profile line
    fline_err: float; error at flux in the profile line
    W        : float; equivalent width
    W_err    : float; error at the equivalente width
    '''
    # args
    wl = args[0]; spec = args[1]
    lines_str = args[2]; linessig = args[3]

    #if np.isnan(spec).all():
    #    spec = np.nan_to_num(spec,0.0)
    if float(len(spec[np.isnan(spec)]))/float(len(spec)) > 0.2:
        spec = np.nan_to_num(spec,0.0)

    # kwargs
    if 'linesguess' in kwargs:
        linesguess = kwargs['linesguess']
    else:
        linesguess = np.zeros(len(lines_str))
    linesb  = kwargs['linesb']      if 'linesb' in kwargs else np.array([])
    linessigb = kwargs['linessigb'] if 'linessigb'in kwargs else np.array([])
    inputcore = kwargs['inputcore'] if 'inputcore'in kwargs else None
    z       = kwargs['z']       if 'z'      in kwargs else 1
    lineslim= kwargs['lineslim']if'lineslim'in kwargs else [10, 10]
    cont_l  = kwargs['cont_l']  if 'cont_l' in kwargs else [20, 70]
    cont_r  = kwargs['cont_r']  if 'cont_r' in kwargs else [20, 70]
    contfunc= kwargs['contfunc']if'contfunc'in kwargs else ['poly', '1', 'yes']
    plot    = kwargs['plot']      if 'plot'   in kwargs else 'yes'
    figxlim = kwargs['figxlim']   if 'figxlim' in kwargs else ([30, 30])
    figylim = kwargs['figylim']   if 'figylim' in kwargs else None
    figsize  = kwargs['figsize']  if 'figsize' in kwargs else None
    figlabel = kwargs['figlabel'] if 'figlabel' in kwargs else (['no'])
    figtit  = kwargs['figtit']  if 'figtit' in kwargs else None
    figname = kwargs['figname'] if 'figname'in kwargs else None
    direc   = kwargs['direc']   if 'direc'  in kwargs else None
    nubspec = kwargs['nubspec'] if 'nubspec'in kwargs else '--'
    nflog   = kwargs['nflog']   if 'nflog'  in kwargs else 'fit.log'
    fclick  = kwargs['fclick']  if 'fclick' in kwargs else None
    showt   = kwargs['showt']   if 'showt'  in kwargs else (['no'])
    showp   = kwargs['showp']   if 'showp'  in kwargs else 'yes'
    sprefit = kwargs['sprefit']   if 'sprefit'  in kwargs else None
    verbose = kwargs['verbose'] if 'verbose'in kwargs else '+'
    line_masks = kwargs['line_masks'] if'line_masks' in kwargs else 'no'
    emi_line   = kwargs['emi_line']   if 'emi_line'  in kwargs else False
    abs_line   = kwargs['abs_line']   if 'abs_line'  in kwargs else False
    GH_plot = kwargs['GH_plot']   if 'GH_plot' in kwargs else 'no'
    NSIG = kwargs['NSIG']   if 'NSIG' in kwargs else 4.0


    # creating ionizing lines array
    lines = np.array([diclines[i]  for i in lines_str])
    for i,e in enumerate(lines) :
      if linesguess[i] == 0:
          lines[i] = e*(z + 1.0)
      else:
          lines[i] = linesguess[i]

    # concatenating ionizing and blend lines arrays
    aline  = np.concatenate((lines, linesb))
    asigma = np.concatenate((linessig, linessigb))

    # number of lines
    nlines = len(aline)

    # sorting by wavelegth
    order  = np.argsort(aline)

    acenter = np.sort(aline)
    asigma  = np.take(asigma, order)

    # array to mask the pixels n*sigma around the lines
    if line_masks == 'no':
        amask = np.ones((len(acenter)*2))*3
    else:
        amask = np.copy(line_masks)

    # limits of fit range
    ll_lamb = acenter[0]-lineslim[0] ; lr_lamb = acenter[-1]+lineslim[1]
    ll  = np.nanargmin(abs(wl-ll_lamb))
    lr  = np.nanargmin(abs(wl-lr_lamb))
    y   = spec[ll:lr]
    x   = wl[ll:lr]

    if nflog is not None:
        flog=open(nflog,'a')

    step=np.copy(x[1::])
    for i, e in enumerate(x[1::]):
        step[i] = e-x[i]
    mldelg = np.nanmean(step)

    tout = "\nThe spectrum has a spectral scale of: {:.3f} A".format(mldelg)
    if nflog is not None:
        flog.write(tout)
    if verbose == '+':
        print(tout)

    # Limits for  both red and blue parts of the continuum
    cl1 = acenter[0]  - cont_l[0];   cl2 = acenter[0]  - cont_l[1]
    cl3 = acenter[-1] + cont_r[0];   cl4 = acenter[-1] + cont_r[1]

    c1 = np.nanargmin(abs(wl-cl1)); c2 = np.nanargmin(abs(wl-cl2))
    c3 = np.nanargmin(abs(wl-cl3)); c4 = np.nanargmin(abs(wl-cl4))

    tout  = "\n\nPseudo-continuum interval: "
    tout1 = "\nLeft [{:.3f}, {:.3f}]".format(cl1, cl2)
    tout2 = "\nRight [{:.3f}, {:.3f}]".format(cl3, cl4)
    if nflog is not None:
        flog.write(tout + tout1 + tout2)
    if verbose == '+':
        print(tout + tout1 + tout2)

    # Sigma-clipping parameters
    try:
        sigl = float(contfunc[3])
        sigu = float(contfunc[4])
        niteration =  int(contfunc[5])
        grow = int(contfunc[6])
        kernel = float(contfunc[7])
        pcont_joint = contfunc[8]
        pcont_sigclip =  contfunc[9]
    except:
        kernel = 0
        pcont_joint = 'yes'
        pcont_sigclip =  'yes'


    # Making a statitical of psuedo-continuum joint
    # both Left and Right intervals?
    if pcont_joint == 'yes':

        conty    = np.concatenate([spec[c1:c2], spec[c3:c4]]) # y continuum
        contx    = np.concatenate([wl[c1:c2], wl[c3:c4]])     # x continuum

        conty = np.array(conty, dtype=np.float64)
        contx = np.array(contx, dtype=np.float64)

        # Performing sigma-clipping
        if pcont_sigclip == 'yes':

            tout = ("\n\nPerforming sigma-clipping on the pseudo-continuum")
            if nflog is not None:
                flog.write(tout)
            if verbose == '+':
                print(tout)
            try:
                conty_clip = clipping(np.copy(conty),sigl=sigl,sigu=sigu,
                             niteration=niteration, grow=grow,verbose=verbose)
                # updating the discarted points in the case the fit of the
                # continuum includes region between lines
                cont_nan = np.where(np.isnan(conty_clip))[0]
                cont_nan[ cont_nan> (c2-c1) ] += c3-c2

                conty = conty[~np.isnan(conty_clip)]
                contx = contx[~np.isnan(conty_clip)]
            except:
                tout = ("\n\nIt was not possible to do sigma-clipping on " +
                        "pseudo-continuum interval")
                if nflog is not None:
                    flog.write(tout)
                if verbose == '+':
                    print(tout)
                cont_nan = ([])

        else:
             cont_nan = ([])

        contmean = np.nanmean(conty, dtype=np.float64)          # Mean
        contsig  = np.nanstd(conty, ddof=1, dtype=np.float64)   # Sigma
        cont_sn  = abs(contmean/contsig)                  # S/N
        #cont_err = sqrt(abs(contmean))
        cont_err = contsig

        tout = "\n\nStatistics of the pseudo-continuum:"
        tout1 = "\n------------------------------------"
        tout2 = "\nS/N of the pseudo-continuum: {:.3f}".format(cont_sn)
        tout3 = "\nSigma of the pseudo-continuum: {:.3e}".format(contsig)
        tout4 = "\nMean value of pseudo-continuum: {:.3e}".format(contmean)
        if nflog is not None:
            flog.write(tout + tout1 + tout2 + tout3 + tout4)
        if verbose == '+':
            print(tout + tout1 + tout2 + tout3 + tout4)

    # Making a statitics of psuedo-continuum separately for both blue and red
    # parts
    else:
        conty_i    = np.array(spec[c1:c2], dtype=np.float64)
        contx_i    = np.array(wl[c1:c2], dtype=np.float64)

        conty_d    = np.array(spec[c3:c4], dtype=np.float64)
        contx_d    = np.array(wl[c3:c4], dtype=np.float64)

        # Statitics for Left continuum

        # Performing sigma-clipping
        if pcont_sigclip == 'yes':

            tout = ("\n\nPerforming sigma-clipping on Left pseudo-continuum")
            if nflog is not None:
                flog.write(tout)
            if verbose == '+':
                print(tout)
            try:
                conty_i_clip = clipping(np.copy(conty_i), sigl=sigl, sigu=sigu,
                                        niteration=niteration, grow=grow,
                                        verbose=verbose)
                # updating the discarted points in the case the fit of the
                # continuum includes region between lines
                cont_nan_i = np.where(np.isnan(conty_i_clip))[0]

                conty_i = conty_i[~np.isnan(conty_i_clip)]
                contx_i = contx_i[~np.isnan(conty_i_clip)]
            except:
                tout = ("\n\nIt was not possible to do sigma-clipping on " +
                        "Left pseudo-continuum interval")
                if nflog is not None:
                    flog.write(tout)
                if verbose == '+':
                    print(tout)
                cont_nan_i = ([])

        else:
            cont_nan_i = ([])
            tout = ("\n\nIt was not done sigma-clipping on " +
                    "Left pseudo-continuum interval")
            if nflog is not None:
                flog.write(tout)
            if verbose == '+':
                print(tout)


        contmean_i = np.nanmean(conty_i, dtype=np.float64)        # Mean
        contsig_i  = np.nanstd(conty_i, ddof=1, dtype=np.float64) # Sigma
        cont_sn_i  = abs(contmean_i/contsig_i)              # S/N
        cont_err_i = contsig_i

        tout = "\n\nStatistics of the Left pseudo-continuum:"
        tout1 = "\n------------------------------------"
        tout2 = "\nS/N of the pseudo-continuum: {:.3f}".format(cont_sn_i)
        tout3 = "\nSigma of the pseudo-continuum: {:.ef}".format(contsig_i)
        tout4 = "\nMean value of pseudo-continuum: {:.ef}".format(contmean_i)
        if nflog is not None:
            flog.write(tout + tout1 + tout2 + tout3 + tout4)
        if verbose == '+':
            print(tout + tout1 + tout2 + tout3 + tout4)

        # Statitics for Right continuum

        # Performing sigma-clipping
        if pcont_sigclip == 'yes':

            tout = ("\n\nPerforming sigma-clipping on Right pseudo-continuum")
            if nflog is not None:
                flog.write(tout)
            if verbose == '+':
                print(tout)
            try:
                conty_d_clip = clipping(np.copy(conty_d), sigl=sigl, sigu=sigu,
                                        niteration=niteration, grow=grow,
                                        verbose=verbose)
                # updating the discarted points in the case the fit of the
                # continuum includes region between lines
                cont_nan_d = np.where(np.isnan(conty_d_clip))[0] + (c3-c2)

                conty_d = conty_d[~np.isnan(conty_d_clip)]
                contx_d = contx_d[~np.isnan(conty_d_clip)]


            except:
                tout = ("\n\nIt was not possible to do sigma-clipping on " +
                    " Right pseudo-continuum interval")
                if nflog is not None:
                    flog.write(tout)
                if verbose == '+':
                    print(tout)
                cont_nan_d = ([])

        else:
            cont_nan_d = ([])
            tout = ("\n\nIt was not done sigma-clipping on " +
                    "Right pseudo-continuum interval")
            if nflog is not None:
                flog.write(tout)
            if verbose == '+':
                print(tout)


        contmean_d = np.nanmean(conty_d, dtype=np.float64)        # Mean
        contsig_d  = np.nanstd(conty_d, ddof=1, dtype=np.float64) # Sigma
        cont_sn_d  = abs(contmean_d/contsig_d)              # S/N
        cont_err_d = contsig_d

        tout = "\n\nStatistics of the Right pseudo-continuum:"
        tout1 = "\n------------------------------------"
        tout2 = "\nS/N of the pseudo-continuum: {:.3f}".format(cont_sn_d)
        tout3 = "\nSigma of the pseudo-continuum: {:.3e}".format(contsig_d)
        tout4 = "\nMean value of pseudo-continuum: {:.3e}".format(contmean_d)
        if nflog is not None:
            flog.write(tout + tout1 + tout2 + tout3 + tout4)
        if verbose == '+':
            print(tout + tout1 + tout2 + tout3 + tout4)

        # joint the two pseudo continuum intervals
        conty = np.concatenate([conty_i, conty_d])
        contx = np.concatenate([contx_i, contx_d])
        cont_nan = np.concatenate([cont_nan_i, cont_nan_d]).tolist()

        contmean  = np.nanmean(conty, dtype=np.float64)                # Mean
        contsig  = ((float(len(conty_i))/len(conty))*contsig_i +   # Sigma
                     (float(len(conty_d))/len(conty))*contsig_d)
        cont_sn  = ((float(len(conty_i))/len(conty))*cont_sn_i +   # S/N
                    (float(len(conty_d))/len(conty))*cont_sn_d)
        cont_err  = contsig

        tout = "\n\nStatistics of the pseudo-continuum total:"
        tout1 = "\n------------------------------------"
        tout2 = "\nS/N weighted of the pseudo-continuum: {:.3f}".format(cont_sn)
        tout3 = "\nSigma weighted of the pseudo-continuum: {:.3e}".format(contsig)
        tout4 = "\nMean value of pseudo-continuum: {:.3e}".format(contmean)
        if nflog is not None:
            flog.write(tout + tout1 + tout2 + tout3 + tout4)
        if verbose == '+':
            print(tout + tout1 + tout2 + tout3 + tout4)


    # Fitting the continuum among the lines?
    contfit = contfunc[2]
    if contfit == 'yes':
        tout0 = ("\n\nThe pseudo-continuum will be fitted including pseudo-" +
                 "continuum intervals and the regions between lines")
        tout01 = "\n------------------------------------"
        tout = ("\nThe psuedo-continuum would be fitted between {:.3f} and" +
                   " {:.3f} A").format(cl1, cl4)
        tout1 = "\nNow, masking the points of the lines within +/- n*sigma"
        if nflog is not None:
            flog.write(tout0 + tout01 + tout + tout1)
        if verbose == '+':
            print(tout0 + tout01 + tout + tout1)

        conty_fit = np.copy(spec[c1:c4])
        contx_fit = np.copy(wl[c1:c4])

        # Masking the clipped continuum points
        conty_fit[cont_nan] = np.nan
        contx_fit[cont_nan] = np.nan

        # Masking the lines
        for lcenter, lsigma, nmask in zip(acenter, asigma, order):
            ll_l = lcenter - amask[nmask*2]*lsigma
            lr_l = lcenter + amask[nmask*2+1]*lsigma
            ll_l  = np.nanargmin(abs(wl-ll_l))
            lr_l  = np.nanargmin(abs(wl-lr_l))
            conty_fit[ll_l-c1:lr_l-c1] = np.nan
            contx_fit[ll_l-c1:lr_l-c1] = np.nan
    else:
        tout = ("\n\nThe pseudo-continuum will be fitted only considering" +
                 " the psuedo-continuum intervals")
        tout1 = "\n------------------------------------"
        if nflog is not None:
            flog.write(tout0 + tout01 + tout + tout1)
        if verbose == '+':
            print(tout + tout1)

        conty_fit = np.copy(conty)
        contx_fit = np.copy(contx)

    # Smoothing the continuum
    if kernel != 0:
        tout = "\nSmoothing the continuum (kernel={})...".format(kernel)
        if nflog is not None:
            flog.write(tout)
        if verbose == '+':
            print(tout)
        from astropy.convolution import convolve, Gaussian1DKernel, Box1DKernel
        gauss_kernel = Gaussian1DKernel(kernel)
        conty_fit = convolve(conty_fit, gauss_kernel)
        conty_fit[np.isnan(contx_fit)] = np.nan


    # Parameters to fit the pseudo continuum
    series  = contfunc[0]
    graup   = int(contfunc[1])
    if series == 'poly':
        adegree = np.array([0, graup])
    else:
        adegree = np.array([1, graup])


    # Fitting the pseudo continuum
    tout = ("\nFitting the pseudo-continuum " +
            "(making sigma-clipping analysis)...")
    if nflog is not None:
        flog.write(tout)
    if verbose == '+':
        print(tout)
    try:
        nan_ycont, nan_xcont, p0cont = cont_clipping(np.copy(contx_fit),
                              np.copy(conty_fit),
                              series=series,
                              degree=graup, smooth=0,
                              v_std = contsig, sigl=sigl, sigu=sigu,
                              niteration=niteration, grow=grow,
                              verbose=verbose)
    except:
        tout = ("\nIt was not possible to fit the pseudo continuum, now" +
                "\nRunning the fitting without sigma-clipping...")
        if nflog is not None:
            flog.write(tout)
        if verbose == '+':
           print(tout)

        contx_fit = contx_fit[~np.isnan(contx_fit)]
        conty_fit = conty_fit[~np.isnan(conty_fit)]

        if series == 'poly':
             p0cont  = P.polyfit(contx_fit, conty_fit, graup, full=False)
        else:
             p0cont = chebfit(contx_fit, conty_fit, graup, full=False)
        nan_ycont=np.copy(conty_fit)
        nan_xcont=np.copy(contx_fit)


    # Calculating the input for core parameter of the Gaussian and Blended
    # lines and central wavelength for the gaussians
    acore = np.zeros(len(lines) + len(linesb))
    nlines_sig = len(lines)
    alinetmp = np.zeros(len(lines) + len(linesb))*np.nan

    # Gaussian lines
    for i,e in enumerate(lines):
        # looking for the maximum/minimum in a range lambda_cent +/- 1*sigma
        lc_l = np.nanargmin(abs(wl-(e - 2*linessig[i])))
        lc_r = np.nanargmin(abs(wl-(e + 2*linessig[i])))
        line_int_x = np.copy(wl[lc_l:lc_r])
        line_int_y = np.copy(spec[lc_l:lc_r])

        if series == 'poly':
              cont_int_y = np.polyval(p0cont[::-1], line_int_x)
        else:
              cont_int_y = chebval(line_int_x, p0cont)

        mean_cont_int_y  = np.nanmean(cont_int_y)
        m_line = np.nanmean(line_int_y - mean_cont_int_y)

        if len(line_int_y[~np.isnan(line_int_y)]) > 0:

            if m_line >= 0:
                acore[i] = max(line_int_y) - mean_cont_int_y
                alinetmp[i] = line_int_x[np.nanargmax(line_int_y)]
            else:
                acore[i] = min(line_int_y) - mean_cont_int_y
                alinetmp[i] = line_int_x[np.nanargmin(line_int_y)]
        else:
            acore[i] =   abs(mean_cont_int_y)
            alinetmp[i] =  np.nanmean(line_int_x)

        # Imposition to only fit emission Lines
        if emi_line:
            acore[i] = max(line_int_y) - mean_cont_int_y
            alinetmp[i] = line_int_x[np.nanargmax(line_int_y)]
        # Impostion to only fit absorption lines
        if abs_line:
            acore[i] = min(line_int_y) - mean_cont_int_y
            alinetmp[i] = line_int_x[np.nanargmin(line_int_y)]

    # Blended lines
    for i,e in enumerate(linesb):
        # looking for the maximum/minimum in a range [+/-2 lambda_cent]
        lc = np.nanargmin(abs(wl-e))
        line_int_x = np.copy(wl[lc-2:lc+2])
        line_int_y = np.copy(spec[lc-2:lc+2])

        if series == 'poly':
              cont_int_y = np.polyval(p0cont[::-1], line_int_x)
        else:
              cont_int_y = chebval(line_int_x, p0cont)

        mean_cont_int_y = np.nanmean(cont_int_y)
        m_line = np.nanmean(line_int_y - mean_cont_int_y)

        #if m_line >= 0:
        #    acore[nlines_sig+i] = max(line_int_y) - mean_cont_int_y
        #else:
        #    acore[nlines_sig+i] = min(line_int_y) - mean_cont_int_y

        # Imposition to only fit emission Lines
        if emi_line:
            acore[nlines_sig+i] = max(line_int_y) - mean_cont_int_y
        # Impostion to only fit absorption lines
        if abs_line:
            acore[nlines_sig+i] = min(line_int_y) - mean_cont_int_y

        lines_str.append('deblend_'+str(i+1))


    # ordering by wavelength
    acore = np.take(acore, order)
    lines_str  = np.take(lines_str, order)

    if any(linesguess)== 0.0:
        alinetmp = np.take(alinetmp, order)
        acenter[~np.isnan(alinetmp)] = alinetmp[~np.isnan(alinetmp)]

    # user core input
    if inputcore is not None:
        acore=inputcore

    tout0 = "\n\nInput Parameters\n----------------\n"
    tout  ="\ninput for core parameter: {}".format(acore)
    tout1 ="\ninput for center parameter: {}".format(acenter)
    tout2 ="\ninput for sigma parameter: {}".format(asigma)
    if nflog is not None:
        flog.write(tout0 + tout + tout1 + tout2)
    if verbose == '+':
        print (tout0 + tout + tout1 + tout2)


    # Creating input parameter array
    p0 = np.array([])
    for core, center, sigma in zip(acore, acenter, asigma):
        p0 = np.concatenate((p0, ([core, center, sigma])))
    fixpar = np.ones((len(p0)))

    # fixing core parameter
    if 'linescorefix' in kwargs:
        pcore0 = kwargs['linescorefix']
    else:
        pcore0 = np.zeros(nlines)
    pcore0 = ([int(i) for i in pcore0])

    fixcore = np.zeros(nlines)
    var_core = np.zeros((max(pcore0)))
    for i in np.arange(max(pcore0)):
        term = np.where(pcore0==i+1)[0]
        var_core[i] = p0[term[1]*3]
        fixpar[term*3] = 0

    fixcore=np.concatenate((fixcore,np.ones((max(pcore0))),np.array([0])))
    pcore=np.concatenate((pcore0,var_core,np.array([max(pcore0)])))

    # fixing center parameter
    if 'linescentfix' in kwargs:
        pcent0 = kwargs['linescentfix']
    else:
        pcent0 = np.zeros(nlines)
    pcent0 = ([int(i) for i in pcent0])

    fixcent = np.zeros(nlines)
    var_cent = np.ones((max(pcent0)))
    for i in np.arange(max(pcent0)):
        term = np.where(pcent0==i+1)[0]
        fixpar[term*3+1] = 0

    fixcent = np.concatenate((fixcent,np.ones((max(pcent0))),np.array([0])))
    pcent   = np.concatenate((pcent0,var_cent,np.array([max(pcent0)])))

    # fixing sigma parameter
    if 'linessigfix' in kwargs:
        psig0 = kwargs['linessigfix']
    else:
        psig0 = np.zeros(nlines)
    psig0 = ([int(i) for i in psig0])

    fixsig = np.zeros(nlines)
    var_sig = np.zeros((max(psig0)))
    for i in np.arange(max(psig0)):
        term = np.where(psig0==i+1)[0]
        var_sig[i] = p0[term[0]*3+2]
        fixpar[term*3+2] = 0

    fixsig = np.concatenate((fixsig,np.ones((int(max(psig0)))),np.array([0])))
    psig   = np.concatenate((psig0,var_sig,np.array([max(psig0)])))

    # Concatenating gaussian parameters, constrains for core, cent and sigma
    p0_c  = np.concatenate((p0, pcore, pcent, psig, np.array([nlines])))
    fix = np.concatenate((fixpar, fixcore, fixcent, fixsig, np.array([0])))


    tout  = "\nThe Fit of the line(s) will perform in the interval:"
    tout1 = "\n[{:.3f}, {:.3f}] A\n".format(ll_lamb, lr_lamb)
    if nflog is not None:
        flog.write(tout + tout1)
    if verbose == '+':
        print(tout + tout1)

    # Creating the continuum array
    if series == 'poly':
        fcont = np.polyval(p0cont[::-1], x)
    else:
        fcont = chebval(x, p0cont)

    # Defining the lambda array
    alamb = [ll_lamb, lr_lamb, cl1, cl2, cl3, cl4]

    # plotting input parameters
    if sprefit is not None:
        num_param = len(np.where(fix>0)[0])
        chipre=func.redchisqg(y-fcont, func.multi(p0_c, x), deg= num_param, sd=cont_err)

        if plot == 'yes':
            ax = plotfit(wl, spec, alamb, contfunc,
                         np.concatenate((p0_c,p0cont,adegree)), lines_str,
                         ([]), contmean, contsig,
                         figxlim=figxlim, figylim=figylim, figsize=figsize,
                         figlabel=figlabel,
                         figtit='Pre fitting with input parameters',
                         figname=sprefit,
                         direc=direc, fclick=fclick, showt=showt, showp=showp,
                         chi_res=chipre, nan_xcont=nan_xcont,
                         nan_ycont=nan_ycont, NSIG=NSIG)

    ###########################
    # fit of the emission lines
    yin = np.copy(y-fcont)
    xin = np.copy(x[~np.isnan(yin)])
    yin = np.copy(yin[~np.isnan(yin)])
    grev, grev_erf = func.fit('multiline', xin, yin, p0_c, weighty=None,
                         weightx=None, fix=fix, verbose=False)

    # Allocation of core parameters
    fitcore = np.copy(grev[len(p0)+nlines:len(p0)+nlines+max(pcore0)])
    for i in np.arange(int(max(pcore0))):
        term = np.where(pcore0==i+1)[0]
        grev[term[0]*3] = fitcore[i]*(0.98/3.)
        grev[term[1]*3] = fitcore[i]

    # Allocation of central wave length parameters
    fitcent = np.copy(grev[len(p0)+len(pcore)+nlines:
                   len(p0)+len(pcore)+nlines+max(pcent0)])
    for i in np.arange(int(max(pcent0))):
        term = np.where(pcent0==i+1)[0]
        for e in term:
            grev[e*3+1] = grev[e*3+1]*fitcent[i]

    # Allocation of sigma parameters
    fitsig = np.copy(grev[len(p0)+len(pcore)+len(pcent)+nlines:
                   len(p0)+len(pcore)+len(pcent)+nlines+max(psig0)])
    for i in np.arange(int(max(psig0))):
        term = np.where(psig0==i+1)[0]
        grev[term*3+2] = fitsig[i]

    # Chi squared of fit
    num_param = len(np.where(grev_erf>0)[0])
    chi_all_red = func.redchisqg(y-fcont, func.multi(grev, x), deg= num_param,
                            sd=cont_err)

    tout  = "\nNumber of parameters fitted {}".format(num_param)
    tout1 = "\nNumber of degrees of  freedom {}".format(y.size-num_param)
    tout2 = "\nreduced Chi square of the fit {}".format(chi_all_red)
    if nflog is not None:
        flog.write(tout + tout1 + tout2)
        flog.close()
    if verbose == '+':
        print(tout + tout1 + tout2)


    # adding parameters of the continuum fit to grev and grev_erf arrays
    grev = np.concatenate((grev, p0cont, adegree))
    grev_erf = np.concatenate((grev_erf, np.zeros((len(p0cont))),
                            np.zeros((len(adegree)))))

    ytot = len(y)
    ytotnan = len(y[np.isnan(y)])
    if ytotnan/ytot > 0.2 :
        outfit = []
        for i, e in enumerate(lines_str):
           eoutfit = [np.nan]*30
           eoutfit[0] = grev[i*3]
           eoutfit[1] = grev[i*3+1]
           eoutfit[2]  = abs(grev[i*3+2])
           outfit.append(eoutfit)
        ax = 0
        return  outfit, lines_str, alamb, contfunc, grev, grev_erf, ax


    outline = []
    outfit  = []
    for i, e in enumerate(lines_str):
       core = grev[i*3]
       cent = grev[i*3+1]
       sig  = grev[i*3+2]

       if (3*abs(sig) > mldelg and abs(sig) < (lineslim[0]+lineslim[1])  and
           (ll_lamb<cent<lr_lamb)):

          # Line Signal-to-Noise is calculated from the ratio of  line mean
          # flux inside FWHM over the continuum sigma
          w_l  = cent - abs(sig)*0.5*gfwhm
          w_r  = cent + abs(sig)*0.5*gfwhm
          iw_l = np.nanargmin(abs(wl-w_l))
          iw_r = np.nanargmin(abs(wl-w_r))
          line_sn = np.nanmean(spec[iw_l:iw_r+1])/contsig

          # Gaussian flux of line
          flux_g = core*abs(sig)*np.sqrt(2.0*np.pi)

          # Line array, [-3*sigma, +3*sigma]
          fll  = np.nanargmin(abs(wl-(cent - NSIG*abs(sig))))
          flr  = np.nanargmin(abs(wl-(cent + NSIG*abs(sig))))
          fy = spec[fll:flr+1] ; fx = wl[fll:flr+1]
          fygauss  = func.gauss([0, core, cent, sig], fx)

          # Number of pixels
          N = len(fx)

          # Continuum array
          if series == 'poly':
              fyc = np.polyval(grev[-(graup+1+2):-2][::-1], fx)
          else:
              fyc = chebval(fx, grev[-(graup+1+2):-2])

          # Line flux
          flux_l = np.trapz(fy-fyc, fx)


          # Profile line without continuum
          prof_l = np.copy(fy - fyc)

          # Gauss-Hermite Fit
          p0_GH = ([np.sqrt(np.pi*2)*core, cent, sig, 0.1, 0.1])
          #p0_GH = ([core, cent, sig, 0.1, 0.1])

          fix_GH = ([1, 1, 1, 1, 1])
          par_GH, par_GH_erf = func.fit('g_hermite', fx, prof_l, p0_GH,
                                         weighty=None, weightx=None,
                                         fix=fix_GH, verbose=False)
          #par_GH, par_GH_erf = curve_fit(gaussian_hermite, fx, prof_l, p0_GH)

          GH_core = par_GH[0]
          GH_cent = par_GH[1]
          GH_sig = par_GH[2]
          GH_h3 = par_GH[3]
          GH_h4 = par_GH[4]

          fyGH = func.gaussian_hermite_b(par_GH, fx)

          flux_GH = np.trapz(fyGH, fx)

          # statistic of the line
          l_skew = skew(prof_l, bias=False, nan_policy = 'omit')

          # The skewtest needs at minimum of 8 elements to perform the test
          if len(prof_l[~np.isnan(prof_l)]) >= 8:
              l_skewtest_stat, l_skewtest_pval = skewtest(prof_l,
                                                          nan_policy = 'omit')
          else:
              l_skewtest_stat = np.nan
              l_skewtest_pval = np.nan
          l_kurtosis = kurtosis(prof_l, bias=False)

          '''
          Expression for uncertanty of velocity gave by Keel (1996)
          '''
          #fwhm = gfwhm*abs(sig)
          #if series == 'poly':
          #    contcent = np.polyval(grev[-(graup+1+2):-2][::-1], cent)
          #else:
          #    contcent = chebval(cent, grev[-(graup+1+2):-2])

          #l_err = ((0.8*contsig*speedc)/ \
          #        ( (abs(core)+abs(contcent) )*cent ))*(fwhm**1.5/sqrt(ldel))

          ## Velocity Uncertainty (Diniz et al. 2017)
          #l_err =  (speedc/cent)*((sqrt(N)*abs(core))/flux_l)*(ldel)
          ## taking into account the factor 1/sqrt(N)
          ##l_err =  (speedc/cent)*(abs(core)/flux_l)*(ldel)

          '''
          Expressions for uncertanty of velocity derived  by
          Hernandez-Jimenez in prep.
          '''
          try:
              l_ref = diclines[e]
          except:
              l_ref = cent

          # mean ldel
          step=np.copy(fx[1::])
          for i, e in enumerate(fx[1::]):
              step[i] = e-fx[i]
          mldel = np.nanmean(step)
          #print (np.nanmean(step), median(step), ldel)

          # No relativistic case
          F_t = np.sum(fy-fyc)
          F_i = np.sqrt(np.sum(np.square(fy-fyc)))
          l_err =  (speedc/l_ref)*(F_i/F_t)*(mldel)

          # Relativistic case
          F_t = np.sum(fy-fyc)
          F_i = np.sqrt(np.sum(np.square(fy-fyc)))
          term1 = (F_i/F_t)*(mldel)
          term2 = (cent*np.square(l_ref))/np.square(np.square(cent) + np.square(l_ref))
          l_err_R = 4*speedc*term1*term2

          # EW definition taken from Eq 1 of Vollmann & Eversberg (2006)
          W      = np.trapz(1.-(fy/fyc), fx)
          Wgauss = np.trapz(1.-((fygauss+fyc)/fyc), fx)
          WGH    = np.trapz(1.-((fyGH+fyc)/fyc), fx)

          # Aproximation to EW taken from Eq 3 of Vollmann & Eversberg (2006)
          #W = (1. - np.nanmean(fy)/np.nanmean(fyc))*(fx[-1]-fx[0])
          '''
          The error in the EW is computed using Eq 7 of Vollmann & Eversberg
          (2006) Added the term 1/sqrt(N) by Riffel & Vale (2010)

          There is a mistake in a term of Taylor Serie expasion made by
          Vollmann & Eversberg (2006), they considered the uncertainties of
          line and continuum fluxes instead of considering the mean
          uncertainties of them. Therefore, their final expression for EW
          uncertainty has not the factor 1/sqrt(N), for more details see
          Hernandez-Jimenenez in prep.
          '''
          W_err      = (np.sqrt( 1. + (np.nanmean(fyc)/np.nanmean(fy)) )*(abs((fx[-1]-fx[0]) -
                              W)/cont_sn))/np.sqrt(N)

          Wgauss_err = (np.sqrt( 1. + (np.nanmean(fyc)/np.nanmean(fyc + fygauss)) )*(abs((fx[-1]
                              - fx[0])- Wgauss)/cont_sn))/np.sqrt(N)

          WGH_err = (np.sqrt( 1. + (np.nanmean(fyc)/np.nanmean(fyc + fyGH)) )*(abs((fx[-1]
                              - fx[0])- WGH)/cont_sn))/np.sqrt(N)


          # Error in the flux Gonzales-Delgado et al. (1994)
          # add fator ldel*
          #flux_l_err = contsig*sqrt( N*( 1. + (abs(W)/(N*ldel)) ) )
          '''
          Expression for flux error Hernandez-Jimenez et al. (1994)
          '''
          flux_l_err = contsig*np.sqrt(N)


          # Chi square of the fit, the model and the data were normalized
          if series == 'poly':
              model_l = (func.gauss([0, core, cent, sig], fx) +
                         np.polyval(grev[-(graup+1+2):-2][::-1], fx))
          else:
              model_l = (func.gauss([0, core, cent, sig], fx) +
                         chebval(fx, grev[-(graup+1+2):-2]))
          try:
              chi = func.redchisqg(fy, model_l, deg=3, sd=cont_err)

          except:
              chi=np.nan
       else:
           line_sn = np.nan;  flux_g = np.nan; flux_l = np.nan;  l_err = np.nan;
           l_err_R = np.nan; W = np.nan; W_err = np.nan; Wgauss = np.nan;
           Wgauss_err = np.nan; flux_l_err = np.nan; chi = np.nan;
           l_skew = np.nan;  l_skewtest_stat= np.nan; l_skewtest_pval = np.nan;
           l_kurtosis = np.nan;
           GH_core = np.nan; GH_cent = np.nan; GH_sig = np.nan; GH_h3 = np.nan;
           GH_h4 = np.nan; flux_GH = np.nan; WGH = np.nan; WGH_err = np.nan

       eoutfit = [core, cent, abs(sig), contmean, contsig, cont_sn, line_sn,
                  chi, chi_all_red, l_err, l_err_R, flux_g, flux_l, flux_l_err,
                  W, W_err, Wgauss, Wgauss_err, l_skew, l_kurtosis,
                  l_skewtest_stat, l_skewtest_pval, GH_core, GH_cent, GH_sig,
                  GH_h3, GH_h4, flux_GH, WGH, WGH_err]

       outfit.append(eoutfit)

    #  print the output of the fit
    print_output(lines_str, np.array(outfit).ravel(), nflog=nflog,
                 verbose = verbose)

    alamb = [ll_lamb, lr_lamb, cl1, cl2, cl3, cl4]

    if plot == 'yes':
        ax = plotfit(wl, spec, alamb, contfunc, grev, lines_str,
                   np.array(outfit).ravel(), contmean, contsig,
                   figxlim=figxlim, figylim=figylim, figsize=figsize,
                   figlabel=figlabel,
                   figtit=figtit, figname=figname,
                   direc=direc, fclick=fclick, showt=showt, showp=showp,
                   chi_res=chi_all_red, nan_xcont=nan_xcont,
                   nan_ycont=nan_ycont, GH_plot= GH_plot, NSIG=NSIG)
    else:
        ax = 0

    return  outfit, lines_str, alamb, contfunc, grev, grev_erf, ax


def lamb2idex (lamb, lref, ldel):

    return int((lamb-lref)/ldel)


def plotfit (*args,**kwargs):
    '''
    Parameters
    -----------
    wl    : array_like; wavelength
    spec  : array_like; flux
    lref  : float, wavelenght of reference
    ldel  : float, delta wavelenght of the spectrum
    alamb : array_like; (ll,lr,c1,c2,c3,c4)
    contfunc : array_like; ['type of poly','degree']
    grev  : array_like; output of the fit
    lines : array_line; fit lines
    outline  : array_line, fit parameters for each line

    Keyword parameters:
    -------------------
    figlabel : array_line str,
             (x position, y position, label, fontsize, color)

    showt : array_like str,
           (print fitted parameters, print  Chi^2,
            plot didnt discard points, plot EW areas)
    showp : str,
          yes or no to show the figure
    figtit  : str,
          figure title
    figname : str,
          figure name (e.g., fig.png)
    direc   : str,
          path where the image will be save

    Return
    -----------
    ax     : object figure
    '''

    import matplotlib as mpl
    mpl.rcParams['axes.labelsize']= 15
    mpl.rcParams['xtick.major.size']= 8
    mpl.rcParams['xtick.minor.size']= 4
    mpl.rcParams['ytick.major.size']= 8
    mpl.rcParams['ytick.minor.size']= 4
    mpl.rcParams['xtick.labelsize']= 15
    mpl.rcParams['ytick.labelsize']= 15

    # length of out table


    # args
    wl = args[0]; spec = args[1]
    alamb = args[2]
    contfunc = args[3]; series=contfunc[0]; graup=int(contfunc[1])
    grev = args[4]
    lines = args[5]
    outline = [float(s) for s in args[6]]
    szoutline = len(outline)/len(lines)
    contmean = args[7]
    contsig  = args[8]


    # kwargs
    figxlim  = kwargs['figxlim']  if 'figxlim' in kwargs else ([30, 30])
    figylim  = kwargs['figylim']  if 'figylim' in kwargs else ([0, 0, 2, 2])
    figsize  = kwargs['figsize']  if 'figsize' in kwargs else None
    figlabel = kwargs['figlabel'] if 'figlabel' in kwargs else (['no'])
    figtit   = kwargs['figtit']   if 'figtit' in kwargs else None
    figname  = kwargs['figname']  if 'figname'in kwargs else None
    direc    = kwargs['direc']    if 'direc'  in kwargs else None
    showt_dic = ['yes','no','no','no']
    showt   = kwargs['showt']     if 'showt'  in kwargs else showt_dic
    showp   = kwargs['showp']     if 'showp'  in kwargs else 'yes'
    fclick  = kwargs['fclick']    if 'fclick' in kwargs else None
    chi_res = kwargs['chi_res']   if 'chi_res' in kwargs else 0.0
    GH_plot = kwargs['GH_plot']   if 'GH_plot' in kwargs else 'no'
    NSIG = kwargs['NSIG']   if 'NSIG' in kwargs else 3.0
    fnorm = kwargs['fnorm']   if 'fnorm' in kwargs else 1e17
    yunits = kwargs['yunits']   if 'yunits' in kwargs else 'Flux (Arbitrary Unit)'
    yresunits = kwargs['yresunits']   if 'yresunits' in kwargs else 'Residuals'
    xunits = kwargs['xunits']   if 'xunits' in kwargs else '$\lambda\,(\AA)$'

    if len(showt) < 2:
       showt = showt + showt_dic[1:]

    nan_ycont = kwargs['nan_ycont']  if 'nan_ycont' in kwargs else []
    nan_xcont = kwargs['nan_xcont']  if 'nan_xcont' in kwargs else []

    if showt[0] == 'yes':
        figtext = ('line       core        Center     Sigma     fluxg       ' +
                   'ccont         SNC        SNL      chi^2    chi_all^2' +
                   '    vel\n')
        for i, line in enumerate(lines):
            try:
                cent = outline[i*szoutline+1]
                vel_rad =((cent-diclines[line])/diclines[line])*speedc
                figout = outline[i*szoutline:(i+1)*szoutline]
                figout.append(vel_rad)
                figtext = figtext + ('{0:>10s} {1:>10.2e} {2:>10.1f} ' +
                    '{3:>10.1f} {11:>10.2e} {4:>10.2e} {6:>10.1f} {7:>10.1f}' +
                    ' {8:>10.1f} {9:>10.1f} {' + str(tab_len) +
                     ':>10.1f}\n').format(line, *figout)
            except:
                figout = outline[i*szoutline:(i+1)*szoutline]
                figout.append(0.0)
                figtext = figtext + ('{0:>10s} {1:>10.2e} {2:>10.1f} ' +
                    '{3:>10.1f} {11:>10.2e} {4:>10.2e} {6:>10.1f} {7:>10.1f}' +
                    '{8:>10.1f} {9:>10.1f} {' + str(tab_len) +
                    ':>10.1f}\n').format(line, *figout)

    # limits by lelt (ll) and right (lr) of the fit range
    ll  = np.nanargmin(abs(wl-alamb[0]))
    lr  = np.nanargmin(abs(wl-alamb[1]))
    y   = spec[ll:lr]*fnorm
    x   = wl[ll:lr]

    # limits by lelt (index) and right (index1) of the continuum range
    c1 = np.nanargmin(abs(wl-alamb[2])); c2 = np.nanargmin(abs(wl-alamb[3]))
    c3 = np.nanargmin(abs(wl-alamb[4])); c4 = np.nanargmin(abs(wl-alamb[5]))

#    if showp == 'yes':
#        plt.ion()

    from matplotlib import gridspec
    fig = plt.figure()
    #plt.clf()

    if showt[0] == 'yes':
        gs = gridspec.GridSpec(2, 1, hspace=0.2, height_ratios=[4,1])
        ax = plt.subplot(gs[0])
        ax1 = plt.subplot(gs[1], sharex=ax)
    else:
        gs = gridspec.GridSpec(2, 1, hspace=0.05, height_ratios=[4,1])
        ax = plt.subplot(gs[0])
        ax1 = plt.subplot(gs[1], sharex=ax)

    # Ploting the spectrum
    ax.plot(wl, spec*fnorm, 'k-')#, label='data')

    # Plotting the continuum fitted
    if series == 'poly':
        ax.plot(wl, np.polyval(grev[-(graup+1+2):-2][::-1],wl)*fnorm, 'g-') #,
        #        label='pseudo-cont.')
    else:
        ax.plot(wl, chebval(wl,grev[-(graup+1+2):-2])*fnorm, 'g-' )#,
        #        label='pseudo-cont.')

    # Plotting the guassians fitted
    xresidual = np.linspace(wl[0], wl[-1], len(wl)*4)
    xsmooth = np.linspace(x[0], x[-1], len(y)*10)
    if series == 'poly':
        yc = np.polyval(grev[-(graup+1+2):-2][::-1], xsmooth)*fnorm
        yc_res = np.polyval(grev[-(graup+1+2):-2][::-1], xresidual)*fnorm
    else:
        yc = chebval(xsmooth, grev[-(graup+1+2):-2])*fnorm
        yc_res = chebval(xresidual, grev[-(graup+1+2):-2])*fnorm

    yt_res = yc_res
    yt = yc
    labelg = 'yes'
    labels = 'yes'
    labeld = 'no'

    for i in np.arange(len(lines)) :
        gaussl  = func.gauss(np.concatenate((([0]), grev[i*3:(i+1)*3])), xsmooth)*fnorm
        gaussl_res = func.gauss(np.concatenate((([0]), grev[i*3:(i+1)*3])), xresidual)*fnorm

        if GH_plot != 'no':
            eoutlines = outline[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
            GHl = func.gaussian_hermite_b(eoutlines[22::], xsmooth)*fnorm
            GHl_res = func.gaussian_hermite_b(eoutlines[22::], xresidual)*fnorm

        # plot for each gaussian
        if lines[i].find('deblend') ==-1:
            if labelg == 'yes':
                if GH_plot == 'no':
                    ax.plot(xsmooth, yc + gaussl, 'b-')
                    #ax.plot(xsmooth, yc + gaussl, 'b-', label='gaussians')
                    #ax.plot(xsmooth, yc + gaussl, 'b-', label='Set 1')
                    #ax.plot(xsmooth, yc + gaussl, 'b-',label='Narrow components')
                else:
                    ax.plot(xsmooth, yc + GHl, 'b-')
                labelg = 'no'; labeld='yes'
            else:
                if GH_plot == 'no':
                    ax.plot(xsmooth, yc + gaussl, 'b-')
                else:
                    ax.plot(xsmooth, yc + GHl, 'b-')
        else:
            if labels == 'yes' and labeld == 'yes':
                if GH_plot == 'no':
                    ax.plot(xsmooth, yc + gaussl, 'g-', lw=3)
                    #ax.plot(xsmooth, yc + gaussl, 'g-', lw=3, label='Set 2')
                    #ax.plot(xsmooth, yc + gaussl, 'g-', lw=3,
                    #        label='Broad component')
                else:
                    ax.plot(xsmooth, yc + GHl, 'g-', lw=3)
                labels = 'no'
            else:
                if GH_plot == 'no':
                    ax.plot(xsmooth, yc + gaussl, 'g-', lw=2)
                else:
                    ax.plot(xsmooth, yc + GHl, 'g-', lw=2)

        if GH_plot == 'no':
            yt = yt + gaussl
            yt_res = yt_res + gaussl_res
        else:
            yt = yt + GHl
            yt_res = yt_res + GHl_res

    # Plotting the total fit
    ax.plot(xsmooth, yt, 'r-', label='Total fit')


    # Plotting the points used to fit the continuum
    if showt[2] == 'yes':
        ax.scatter(nan_xcont, nan_ycont*fnorm, s=100, c='k', marker='*')

    # Plotting of the continuum intervals
    ax.plot(wl[c1:c2], spec[c1:c2]*fnorm,'r-', lw=3, label='Pseudo-continuum')
    ax.plot(wl[c3:c4], spec[c3:c4]*fnorm,'r-', lw=3)

    # Y limits for the main plot
    """
    It takes the minimun and maximum value among the fit lines to set ylim.
    """
    if not figylim:
        figylim = [0, 0, 6, 6]
        print ("Limits in Y-axis setted automatically!")
    if figylim[0]!=0.0  and figylim[1]!=0.0:
            ax.set_ylim(figylim[0], figylim[1])
    else:
        aline_cent = np.array([])
        for i,nline in enumerate(lines):
            l_cent = grev[i*3+1]
            l_sig  = grev[i*3+2]
            l_cent_l = np.nanargmin(abs(wl-(l_cent - NSIG*l_sig)))
            l_cent_r = np.nanargmin(abs(wl-(l_cent + NSIG*l_sig)))
            aline_cent = np.concatenate((aline_cent, spec[l_cent_l:l_cent_r+1]))
        try:
            miny = np.nanmin(aline_cent*fnorm)
            maxy = np.nanmax(aline_cent*fnorm)
            rangy = (maxy - miny)*0.2
            ax.set_ylim(miny - rangy, maxy + rangy)
        except:
            print('It was not possible to define limits for y-axis')


    # X limits for all plot
    try:
        if  (wl[c4] + figxlim[1]) < wl[-1]:
            limright = wl[c4] + figxlim[1]
        else:
            limright = wl[-1] + figxlim[1]
    except:
          limright = wl[-1] + figxlim[1]
    try:
        if  wl[0] < (wl[c1] - figxlim[0]):
            limleft = wl[c1] - figxlim[0]
        else:
            limleft = wl[0] - figxlim[0]
    except:
        limleft = wl[0] - figxlim[0]
    ax.set_xlim(limleft, limright)

    # Plotting the residuals
    yt_intep = np.interp(wl, xresidual, yt_res)
    yt_residual = spec*fnorm - yt_intep
    ax1.plot(wl, yt_residual, 'k-')
    #ax1.plot(wl[ll:lr], yt_residual[ll:lr], 'r-', label='fit range')

    # Plotting 3-sigma lines
    sig_pos = np.copy(wl)*0.0 + contsig*3.
    sig_neg = np.copy(wl)*0.0 - contsig*3.
    ax1.plot(wl, sig_pos*fnorm, 'k--')
    ax1.plot(wl, sig_neg*fnorm, 'k--')

    ##################################
    # Y limits for the residual plot #
    ##################################

    txtsig_p = r"$+3\,\sigma$"
    txtsig_n = r"$-3\,\sigma$"
    txtsig_x = limleft + (limright - limleft)*0.15
    ax1.text(txtsig_x, sig_pos[0]*1.4*fnorm, txtsig_p, fontsize=10)
    ax1.text(txtsig_x, sig_neg[0]*1.7*fnorm, txtsig_n, fontsize=10)

    ax1.set_ylim(sig_neg[0]*figylim[2]*fnorm, sig_pos[0]*figylim[3]*fnorm)

    # Plot EW areas
    if showt[3] == 'yes':
        for i, e in enumerate(lines) :
            core = grev[i*3]
            cent = grev[i*3+1]
            sig  = grev[i*3+2]

            fll  = np.nanargmin(abs(wl-(cent - NSIG*abs(sig))))
            flr  = np.nanargmin(abs(wl-(cent + NSIG*abs(sig))))
            fy = spec[fll:flr+1] ; fx = wl[fll:flr+1]
            print (fll,flr)
            print (min(fy))
            if series == 'poly':
               fyc = np.polyval(grev[-(graup+1+2):-2][::-1], fx)
            else:
               fyc = chebval(fx, grev[-(graup+1+2):-2])

            ax.fill_between(fx, (miny-rangy)*fnorm, fyc*fnorm, color='r', alpha=0.3)
            ax.fill_between(fx, (miny-rangy)*fnorm, fy*fnorm, color='b', alpha=0.3)


    # set title, xlabel, ylabel, and plot graph
    if figtit is not None : ax.set_title(figtit)

    ax1.set_xlabel(xunits)
    ax1.set_ylabel(yresunits)

    ax1.minorticks_on()
    ax1.locator_params(axis='y',nbins=6)


    plt.setp(ax.get_xticklabels(), visible=False)
    #ax.set_ylabel('Fluxo (contagens)')
    ax.set_ylabel(yunits)
    ax.legend(loc='best', frameon=False)
    ax.minorticks_on()
    if fclick is not None:
        cid = plt.connect('key_press_event', fclick)


    # Plot the text of the fitted parameters
    if showt[0] == 'yes':
        gs.tight_layout(fig, rect=[0, 0.3, 1, 1])
        fig.text(0.95, 0.05, figtext, horizontalalignment='right',
                 transform = ax.transAxes)

    # Plot text in figure, for intance (a)
    if figlabel[0] != 'no':
        ax.text(float(figlabel[0]), float(figlabel[1]),
                figlabel[2], fontsize=float(figlabel[3]),
                color=figlabel[4])


    # Print Chi^2 on the plot
    if showt[1] == 'yes':
        txtchi = r"$\chi^{2}_{\nu}$ = " + "{:.2f}".format(chi_res)
        fig.text(0.19, 0.7, txtchi, size=20, horizontalalignment='left',
                 transform = ax.transAxes)

    # Figure size
    if figsize:
        fig.set_size_inches((15.8,9.5), forward=True)
    else:
        fig.set_size_inches((figsize[0],figsize[1]), forward=True)

    if figname is not None:
        try:
            plt.savefig(figname, format=figname.split('.')[-1],
                        bbox_inches = 'tight')
        except:
            print("The option bbox=inches='tight' didn't work")
            plt.savefig(figname, format=figname.split('.')[-1])

    if showp == 'yes':
        plt.show()

    if direc is not None:
        # output directory
        if not os.path.exists('./'+ direc):
            os.mkdir(direc)
        os.system("mv %s %s" %(figname, direc))
        #os.system("evince %s/%s"%(direc, figname))

    return ax

def cubofit (tabfit, tabcol, cubofit, wl, figsize=[15.8,9.5], tabout='long',
             GH_plot='no', fnorm=1, figylim=([0, 0, 2, 2]), showp='yes',
             figtit='indexes', yunits = 'Flux (Arbitrary Unit)',
             yresunits = 'Residuals', xunits = '$\lambda\,(\AA)$'):

    my = int(tabcol.split('_')[1])-1;  mx = int(tabcol.split('_')[0])-1
    y = cubofit[:, my, mx]

    outlines = list(map(float, tabfit[tabcol][0].split(',')))
    lines = tabfit[tabcol][1].split(',')
    if tabout == 'long':
        print_output(lines, outlines)
    if tabout == 'short':
        print_output_short(lines, outlines)

    alamb = list(map(float,tabfit[tabcol][2].split(',')))
    contfunc = tabfit[tabcol][3].split(',')
    grev = list(map(float, tabfit[tabcol][4].split(',')))


    cont_mean = outlines[3]
    cont_sig  = outlines[4]

    if  figtit == 'indexes':
        figtit=tabcol
    ax = plotfit(wl, y, alamb, contfunc, grev, lines, outlines,
                 cont_mean, cont_sig, figtit=figtit, showp=showp, showt=['no'],
                 figsize=figsize, GH_plot=GH_plot, fnorm=fnorm, figylim=figylim,
                 yunits=yunits, yresunits=yresunits, xunits=xunits)

    return ax

def print_output(lines, outlines, nflog=None, verbose = '+'):

    # Open log file
    if nflog is not None:
        flog=open(nflog,'a')

    thead = (Fore.BLUE + '\n      line       core     Center      Sigma\n')
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    # Printing the fitted parameters
    for i, nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3e} {:>10.2f} {:>10.2f}'.format(nline,
                eoutfit[0], eoutfit[1], eoutfit[2]))
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    thead = (Fore.BLUE +'\n      line      mcont      scont        SNC        SNL\n')
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    for i, nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3e} {:>10.3e} {:>10.2f} {:>10.2f}').format(
                nline,  eoutfit[3], eoutfit[4], eoutfit[5], eoutfit[6])
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    thead = Fore.BLUE + '\n      line      chi^2  chi_all^2      L_err     Lerr_R\n'
    if verbose == '+':
         print (thead)
    if nflog is not None:
         flog.write(thead)
    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}').format(nline,
                 eoutfit[7], eoutfit[8], eoutfit[9], eoutfit[10])
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    thead = Fore.BLUE + '\n      line      Fluxg      Fluxl  Fluxl_err\n'
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)

    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3e} {:>10.3e} {:>10.3e} '.format(nline,
                 eoutfit[11], eoutfit[12], eoutfit[13]))
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')


    thead = Fore.BLUE + '\n      line         EW     EW_err    EWgauss  EWgauss_e\n'
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}').format(nline,
                 eoutfit[14], eoutfit[15], eoutfit[16], eoutfit[17])
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')


    thead = Fore.BLUE + '\n      line       skew   kurtosis    sk_stat    sk_pval\n'
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.4f} {:>10.4f} {:>10.4f} {:>10.4f}').format(nline,
                 eoutfit[18], eoutfit[19], eoutfit[20], eoutfit[21])
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    thead = Fore.BLUE + '\n      line    GH_core    GH_cent     GH_sig      GH_h3     GH_h4\n'
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3e} {:>10.4f} {:>10.4f} {:>10.4f}' +
                '{:>10.4f}').format(nline, eoutfit[22], eoutfit[23],
                                    eoutfit[24], eoutfit[25], eoutfit[26])
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    thead = Fore.BLUE + '\n      line    GH_flux      GH_EW  GH_EW_err\n'
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    for i,nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (Fore.BLACK + '{:>10s} {:>10.3e} {:>10.4f} {:>10.4f}').format(nline,
                 eoutfit[27], eoutfit[28], eoutfit[29])
        if verbose == '+':
            print (tout + '\n')
        if nflog is not None:
            flog.write(tout + '\n')


    # Close log file
    if nflog is not None:
        flog.close()

def print_output_short(lines, outlines, nflog=None, verbose = '+'):

    # Open log file
    if nflog is not None:
        flog=open(nflog,'a')

    thead = ('\n      line      Center      Sigma        SNC        SNL'+
             '      L_err      Fluxg      Fluxl  Fluxl_err         EW     ' +
             'EW_err\n')
    if verbose == '+':
        print (thead)
    if nflog is not None:
        flog.write(thead)
    # Printing the fitted parameters
    for i, nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = (('{:>10s}  {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f}' +
                  ' {:>10.3f} {:>10.3e} {:>10.3e} {:>10.3e}' +
                 ' {:>10.3f} {:>10.3f}').format(nline,
                  eoutfit[1], eoutfit[2],  eoutfit[5], eoutfit[6], eoutfit[9],
                  eoutfit[11], eoutfit[12], eoutfit[13], eoutfit[14],
                  eoutfit[15]))
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')

    # Close log file
    if nflog is not None:
        flog.close()

def print_output_table(nspec, lines, outlines, nflog=None, pheader='yes',
                       verbose = '+'):
    # Open log file
    if nflog is not None:
        flog=open(nflog,'a')

    thead = ('#    nspec       line       core     Center      Sigma' +
             '      mcont      scont        SNC        SNL' +
             '      chi^2  chi_all^2      L_err     Lerr_R' +
             '      Fluxg      Fluxl  Fluxl_err' +
             '         EW     EW_err    EWgauss   EWgauss_e'+
             '       skew   kurtosis   sk_stat   sk_pval'+
             '    GH_core    GH_cent    GH_sig     GH_h3      GH_h4' +
             '    GH_flux      GH_EW GH_EW_ERR')
    text_tab = ('{:>10.3e} {:>10.2f} {:>10.2f} {:>10.3e} {:>10.3e} ' +
           '{:>10.2f} {:>10.2f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f} ' +
           '{:>10.3e} {:>10.3e} {:>10.3e} {:>10.3f} {:>10.3f} {:>10.3f} ' +
           ' {:>10.3f} {:>10.4f} {:>10.4f} {:>10.4f} {:>10.4f}' +
           ' {:>10.3e} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}' +
           ' {:>10.3e} {:>10.3f} {:>10.3f}')
    # Printing header of the table
    if pheader == 'yes':
        if verbose == '+':
            print (thead)
        if nflog is not None:
            flog.write(thead + '\n')
    # Printing the fitted parameters
    for i, nline in enumerate(lines):
        eoutfit = outlines[i*(tab_len-1):i*(tab_len-1)+(tab_len-1)]
        tout = ('{:>10s} {:>10s} ' + text_tab).format(nspec, nline, *eoutfit)
        if verbose == '+':
            print (tout)
        if nflog is not None:
            flog.write(tout + '\n')
    # Close log file
    if nflog is not None:
        flog.close()

def ordnum(num) :

    if num < 10    : snum='00'+str(num)
    elif num < 100 : snum='0'+str(num)
    else           : snum=str(num)

    return snum

def ordnum2(num) :

    if num < 10     : snum='000'+str(num)
    elif num < 100  : snum='00'+str(num)
    elif num < 1000 : snum='0'+str(num)
    else            : snum=str(num)

    return snum


def mapa(ima, nima=None, cxy=None, labx=0, laby=0, labb=None, ltit=None,
         vmin=0, vmax=0, cmap = 'jet', asp = 'equal', interp = 'none',
         subplot=None, gsubplot=None, figu=None, txtfig=None,
         locbar=[0.87, 0.1, 0.02, 0.8], onclf = True, barformat = '%.2f',
         barpad=0.1):
    '''
    Parameters
    ------------
    ima  = array_like;
        Image
    nima = str;
        Figure name
    cxy  = array_like;
        Image coordinates [xi,xf,yi,yf]
    labx = str;
        x-axis label
    laby = str;
        y-axis label
    labb = str;
        bar label
    ltit = str;
        Image title
    vmin1 = float;
        Minimum fluxlevel to be displayed
    vmax1 = float;
        Maximum fluxlevel to be displayed
    cmap  = str;
        Color map for image; default 'jet'
    aspect = str;
        relation between axes; default 'equal'
    interporlation: str,
        default 'none'
    subplot = array_like;
        [nrows,ncols,ID]
    figu  = object_like;
        object image
    txtfig = array_like;
        [x,y,'text','x-small']
    locbar = array_like;
        [posx,posy,dx,dy]
    onclf = str,
        True or False
    '''

    # subplots

    if gsubplot is not None:
        ax = plt.subplot(gsubplot)
    if subplot is not None:
        ax = plt.subplot(subplot[0], subplot[1], subplot[2])
    if gsubplot is None and subplot is None:
        ax = 0
    if onclf:
        plt.clf()

    plt.minorticks_on()
    # image coordinates
    if cxy is None:
        cxy = ([-ima.shape[1]*0.5, ima.shape[1]*0.5, -ima.shape[0]*0.5,
                ima.shape[0]*0.5])

    axc = plt.gca()
    # plot image
    if vmin != 0 or vmax != 0:
        im = plt.imshow(ima, origin='lower', cmap = cmap, vmin=vmin, vmax=vmax,
                        extent=[cxy[0], cxy[1], cxy[2], cxy[3]],
                        aspect=asp, interpolation=interp)

    else:
        im = plt.imshow(ima, origin='lower',  cmap = cmap,
                        extent=[cxy[0], cxy[1], cxy[2], cxy[3]],
                        aspect=asp, interpolation=interp)

    # figure text
    if txtfig is not None:
        plt.text(txtfig[0], txtfig[1], txtfig[2], fontsize=txtfig[3])

    # axis labels
    if labx != 0 :
        plt.xlabel(labx, size= 'x-large')
    else :
        plt.setp(axc.get_xticklabels(), visible=False)

    if laby != 0 :
        plt.ylabel(laby, size= 'x-large')
    else :
        plt.setp(axc.get_yticklabels(), visible=False)

    # plot bar
    # in a subplot
    if labb is not None  and subplot is not None:
        cbar_ax = figu.add_axes(locbar)
        cb = plt.colorbar(im, format=barformat, cax=cbar_ax)
        cb.set_label(labb,size=17)
    # not subplot
    if labb is not None  and subplot is None:
        divider = make_axes_locatable(axc)
        cax = divider.append_axes("right", size="5%", pad=barpad)
        cb  = plt.colorbar(im, format=barformat, cax=cax)
        cb.set_label(labb, size='x-large')

    # image title
    if ltit is not None :
        plt.title(ltit)
    if nima is not None :
        plt.savefig(nima, format=nima.split('.')[-1], bbox_inches = 'tight')
    return ax

def mapaax(AX, ima, nima=None, cxy=None, labx=0, laby=0, labb=None, ltit=None,
            vmin=0, vmax=0, cmap = 'jet', asp = 'equal', interp = 'none',
            txtfig=None, barformat = '%.1f'):
    '''
    Parameters
    ------------
    AX  = object_like;
        subplot object
    ima  = array_like;
        Image
    nima = str;
        Figure name
    cxy  = array_like;
        Image coordinates [xi,xf,yi,yf]
    labx = str;
        x-axis label
    laby = str;
        y-axis label
    labb = str;
        bar label
    ltit = str;
        Image title
    vmin1 = float;
        Minimum fluxlevel to be displayed
    vmax1 = float;
        Maximum fluxlevel to be displayed
    cmap  = str;
        Color map for image; default 'jet'
    aspect = str;
        relation between axes; default 'equal'
    interporlation: str,
        default 'none'
    txtfig = array_like;
        [x,y,'text','x-small']
    barformat = str;
        format to tick labels of bar
    '''

    # minorticks on
    AX.minorticks_on()

    # image coordinates
    if cxy is None :
        cxy = ([-ima.shape[1]*0.5, ima.shape[1]*0.5, -ima.shape[0]*0.5,
                ima.shape[0]*0.5])

    #plot image
    ax = plt.gca()
    if vmin != 0 or vmax != 0 :
        # Paper Suzi
        #im = AX.imshow(ima[:,::-1], origin='lower', cmap = cmap,
        im = AX.imshow(ima, origin='lower', cmap = cmap,
                        vmin=vmin, vmax=vmax,
                        extent=[cxy[0], cxy[1], cxy[2], cxy[3]],
                        aspect=asp, interpolation=interp)
                        #interpolation=interp)

    else:
        # Paper Suzi
        #im = AX.imshow(ima[:,::-1], origin='lower',  cmap = cmap,
        im = AX.imshow(ima, origin='lower',  cmap = cmap,
                       extent=[cxy[0], cxy[1], cxy[2], cxy[3]],
                       aspect=asp, interpolation=interp)

#    AX.plot(0, 0, 'kx', markersize=10, mew=4, scalex=False, scaley=False)
#    #plt.draw()
#
#    #paper suzi
#    if txtfig[2] == '70 km/s':
#        circ_xy = np.array([8.5-55*0.5, 27.7-93*0.5])*0.05
#        circ = plt.Circle(circ_xy, 0.35, color='k', fill=False, lw=3)
#        AX.add_artist(circ)
#        AX.text(circ_xy[0]-0.1, circ_xy[1]-0.1, '3', fontsize=txtfig[3],
#                color=txtfig[4])
#    if txtfig[2] == '-96 km/s':
#        circ_xy = np.array([46.4-55*0.5, 35.8-93*0.5])*0.05
#        circ = plt.Circle(circ_xy, 0.35, color='k', fill=False, lw=3)
#        AX.add_artist(circ)
#        AX.text(circ_xy[0]-0.1, circ_xy[1] - 0.1, '2', fontsize=txtfig[3],
#                color=txtfig[4])
#    if txtfig[2] == '-180 km/s':
#        circ_xy = np.array([29.33-55*0.5, 86.2-93*0.5])*0.05
#        circ = plt.Circle(circ_xy, 0.35, color='k', fill=False, lw=3)
#        AX.add_artist(circ)
#        AX.text(circ_xy[0] - 0.1, circ_xy[1] - 0.1, '1', fontsize=txtfig[3],
#                color=txtfig[4])
#        circ_xy = np.array([46.4-55*0.5, 35.8-93*0.5])*0.05
#        circ = plt.Circle(circ_xy, 0.35, color='k', fill=False, lw=3)
#        AX.add_artist(circ)
#        AX.text(circ_xy[0]-0.1, circ_xy[1] - 0.1, '2', fontsize=txtfig[3],
#                color=txtfig[4])
#    if txtfig[2] == '489 km/s':
#        circ_xy = np.array([48.43-55*0.5, 58.39-93*0.5])*0.05
#        circ = plt.Circle(circ_xy, 0.35, color='k', fill=False, lw=3)
#        AX.text(circ_xy[0] - 0.1, circ_xy[1] - 0.1, '4', fontsize=txtfig[3],
#                color=txtfig[4])
#        AX.add_artist(circ)
#
#    circ_xy = np.array([0., 0.])
#    circn = plt.Circle(circ_xy, 12*0.05, color='k', fill=False, lw=3)
#    AX.add_artist(circn)
#
#    from plot_functions import bar, zetas
#
#    bar([55*0.5,93*0.5], 0.05, (100./175.), "100 pc", parr='1', larrow=5.0,
#        nx=1.5, ny=1.0,
#        postxt=1.6, cbar='k-', ctex='k', linew=5, AX=AX, bartexs='x-large')
#
#        #zetas(image, delta, scale, parr='3', larrow=5.0, nx=2.0, ny=2.0, lhat=1.16,
#    #      postxtn=1.5, postxte=1.5, carr='k', ctex='k', linew=2, AX=None):
#    zetas([65,155],[27,47], 0.05, parr='2', larrow=3.0, nx=1.0, ny=0.5, AX=AX)


    # figure text
    if txtfig is not None:
        AX.text(txtfig[0], txtfig[1], txtfig[2], fontsize=txtfig[3],
                color=txtfig[4])

    # axis labels
    if labx != 0:
        AX.set_xlabel(labx, fontsize='x-large')
    if laby != 0:
        AX.set_ylabel(laby, fontsize='x-large')
    if labb is not None:
        cb = AX.cax.colorbar(im, format=barformat, pad=0.1)
        cb.set_label_text(labb, fontsize=txtfig[3])

    # image title
    if ltit is not None:
        AX.set_title(ltit)
    if nima is not None:
        plt.savefig(nima, format=nima.split('.')[-1], bbox_inches = 'tight')


def channelvel(spec, line, lcent, lrange, lrefs, lcont, vsys,
               nima=None, cxy=None, labx=0, laby=0, labb=None,
               lim_Ints=[None,None,0,0], cmap=['jet', '%0.1f'], vsubplot=None,
               txtfig=None, writeVC='no'):

     '''
     spec : array_like;
         Flux
     line : str;
        Line name, e.g., 'halfa', 'OIII', etc.
     lcent : float,
         central wavelenght (A)
     lrange: array_like,
         [left, right, step]
     lrefs : array_like,
         [lref, ldel] (A)
     lcont : array_like,
         [L1, L2, R1, R2] (A)
     vsys : float,
         system velocity
     nima : str,
         name figure, if it is None, then each channel will have a plot
     cxy  : array_like; t
         the image coordinates [xi,xf,yi,yf]
     labxy : array_like,
         [x-axis, y-axis] labels
     labb : str,
         bar label
     ltit : str,
         image title
     lim_Ints = array_like,
         [flux_min, flux_max, 0 or 1 (log), n (to cutoff pixs < n*sigma]
     cmap  = str, color map for channelmaps
     vsubplot = array_like,
         [nrows,ncols, size image]
     txtfig = array_like,
         [x,y,'x-small']
     writeVC = str,
         yer or no to write a .fits for each velocity channel.
     '''

     import matplotlib as mpl
     mpl.rcParams['axes.labelsize']= 15
     mpl.rcParams['legend.fontsize']= 15
     mpl.rcParams['xtick.major.size']= 12
     mpl.rcParams['xtick.minor.size']= 6
     mpl.rcParams['ytick.major.size']= 12
     mpl.rcParams['ytick.minor.size']= 6
     #mpl.rcParams['xtick.labelsize']=15
     #mpl.rcParams['ytick.labelsize']= 15


     y = spec.shape[1]
     x = spec.shape[2]

     lref = lrefs[0]
     ldel = lrefs[1]

     # line profile array
     lcent_id = lamb2idex(lcent, lref, ldel)
     lleft    = int(lrange[0])
     lright   = int(lrange[1]) + 1
     lstep    = int(lrange[2])
     slide = np.arange(lcent_id - lstep*lleft, lcent_id + lstep*lright, lstep)


     # limits by lelt (index)) and right(index1) of the continuum range
     cl1 = lcent - lcont[0]; cl2 = lcent - lcont[1]
     cl3 = lcent + lcont[2]; cl4 = lcent + lcont[3]

     c1 = lamb2idex(cl1, lref, ldel); c2 = lamb2idex(cl2, lref, ldel)
     c3 = lamb2idex(cl3, lref, ldel); c4 = lamb2idex(cl4, lref, ldel)

     c_1 = lamb2idex(5500, lref, ldel)
     c_2 = lamb2idex(5700, lref, ldel)
     cont = spec[c_1:c_2]

     # creating continuum array
     #cont     = np.concatenate([spec[c1:c2, :, :], spec[c3:c4, :, :]]) # continuum
     vcont    = np.nanmean(cont, axis=0, dtype=np.float64)             # Mean continuum
     contsig  = np.nanstd(cont, axis=0, dtype=np.float64, ddof=1)      # Sigma continuum
     cont_sn  = abs(vcont/contsig)                            # S/N continuum


     # subplot arange and image size
     if vsubplot is None:
         nr = ceil(len(slide)/4.); nc=4 ; wfig=10.0
     else:
         nr = int(vsubplot[0]); nc = int(vsubplot[1]); wfig = vsubplot[2]

     # Subplot labels
     lfigu = ( (([0,laby])+([0,0])*(nc-1))*(nr-1) +
               ([labx,laby])+([labx,0])*(nc-1) )

     plt.clf()
     from mpl_toolkits.axes_grid1 import ImageGrid
     fig = plt.figure(1)
     fig.set_size_inches(wfig,  wfig*float(nr)/nc, forward=True)

     grid = ImageGrid(fig, 111,               # similar to subplot(111)
                      nrows_ncols = (nr, nc), # creates 2x2 grid of axes
                      ngrids=len(slide),
                      axes_pad=0.0,           # pad between axes in inch.
                      cbar_location="right",
                      cbar_mode="single",
                      cbar_size="5%",
                      cbar_pad=0.05
                     )

     for j, i in enumerate(slide):

         # it mask the pixel with the filters: wavelength,sn and sigma line
         slidef = spec[i, :, :]

         # Absolute value of channel maps (flux always positive!)
         slidef = abs(slidef)

         # subtration of the contimum
         slidef = slidef - vcont
         slidef[slidef<=0] = np.nan

         # Masking pixels with a flux smaller than n*contsig
         if lim_Ints[3] != 0:
            slidef[slidef<contsig*lim_Ints[3]] = np.nan

         # scaling the channel map (norm or log)
         if lim_Ints[2]==1:
             slidef = log10(slidef)

         # Masking pixels with a flux smaller than lim_Ints[0]
         if lim_Ints[0] !=0:
            slidef[slidef<lim_Ints[0]] = np.nan

         # Velocity for each wavelength
         linew = i*ldel + lref
         vel   = ((linew - diclines[line])/diclines[line])*speedc - vsys

         # text in the figure and name file
         ltit='%d'%(vel)+' km/s'
         if txtfig is not None :
             ltit = '%d'%(vel)+' km/s'
             txtfig1 = ([txtfig[0], txtfig[1], ltit, txtfig[2], txtfig[3]])

         # name file-typefit
         tit  = 'map{:0>3d}_{:d}'.format(j,int(vel)) + '.png'
         if writeVC == 'yes':
             nfit = 'map{:0>3d}_{:d}'.format(j,int(vel)) + '.fits'
             #pf.writeto(nfit, slidef, clobber=True)
             fits.writeto(nfit, slidef, overwrite=True)

         # printing flux minimum and maximum for each channel
         maxf = slidef[np.isnan(slidef)==False].max()
         minf = slidef[np.isnan(slidef)==False].min()
         print("value max and min for channel (vel= {:.0f}) {} "
               "{}".format(vel, maxf, minf))

         if nima == None:
             mapa(slidef, tit, cxy, labx, laby, labb, ltit, lim_Ints[0],
                  lim_Ints[1])
         else:
            if j+1 != len(slide):
                mapaax(grid[j], slidef, None, cxy, lfigu[j*2],
                        lfigu[j*2+1], None, None, lim_Ints[0], lim_Ints[1],
                        cmap[0], 'equal', 'none', txtfig1, cmap[1])
            # last channel, draw colorbar and save the figure
            else:
                mapaax(grid[j], slidef, nima, cxy, lfigu[j*2],
                        lfigu[j*2+1], labb, None, lim_Ints[0], lim_Ints[1],
                        cmap[0], 'equal', 'none', txtfig1, cmap[1])



def clipping(ivector, sigl=3.0, sigu=3.0, niteration=3, grow=0, verbose='-'):
    '''
    Given an array this function does a clipping for lower and higher outliner
    points in the array.

    Parameters
    ----------
    vetor : array_like,
        Array containg elements to clip
    sigl : float,
        Sigma-clip criterion for upper deviant points, 0 for no clip
    sigu : float,
        Sigma-clip criterion for lower deviant points, 0 for no clip
    niteration : float,
        Number of sigma-clip iterations

    Return
    ------
    clipvector : ndarray,
        An array with the same size that input array, all elements clipped
        were assined NaN

    '''
    vector = np.copy(ivector)
    ToT_remove_l = 0
    ToT_remove_u = 0

    v_mean = np.nanmean(vector)
    v_std  = np.nanstd(vector, ddof=1)
    if verbose == '+':
        print (('\nPrevius values before the sigma-clipping: mean={:.4} std= '+
                '{:.4}').format(v_mean, v_std))
        print (('Setup of the parameters:\nsigl={}, sigu={}, niteration={}, ' +
                'grow={}').format(sigl, sigu, niteration, grow))
    for i in range(int(niteration)):

        if sigl != 0.0:

           prev_nan = vector[np.isnan(vector)].size
           ind_sigl = np.where(vector < (v_mean-sigl*v_std))[0]
           vector[ind_sigl] = np.nan
           remove_l = vector[np.isnan(vector)].size - prev_nan

           j=0
           while j < grow:
               j+=1
               prev_nan = vector[np.isnan(vector)].size
               del_ind = np.copy(ind_sigl)+j
               del_ind = del_ind[(del_ind>-1) & (del_ind<vector.size)]
               vector[del_ind] = np.nan

               del_ind = np.copy(ind_sigl)-j
               del_ind = del_ind[(del_ind>-1) & (del_ind<vector.size)]
               vector[del_ind] = np.nan

               remove_l+=   vector[np.isnan(vector)].size - prev_nan

        else:
            remove_l = 0

        if sigu != 0.0:
            prev_nan = vector[np.isnan(vector)].size
            ind_sigu = np.where(vector > (v_mean+sigu*v_std))[0]
            vector[ind_sigu] = np.nan

            remove_u =  vector[np.isnan(vector)].size - prev_nan

            j=0
            while j < grow:
               j+=1
               prev_nan = vector[np.isnan(vector)].size
               del_ind = np.copy(ind_sigu)+j
               del_ind = del_ind[(del_ind>-1) & (del_ind<vector.size)]
               vector[del_ind] = np.nan

               del_ind = np.copy(ind_sigu)-j
               del_ind = del_ind[(del_ind>-1) & (del_ind<vector.size)]
               vector[del_ind] = np.nan

               remove_u+= vector[np.isnan(vector)].size - prev_nan

        else:
            remove_u = 0
        v_mean = np.nanmean(vector)
        v_std  = np.nanstd(vector, ddof=1)
        if verbose == '+':
            print (('itera: {} mean: {:.4} std: {:.4}  ToT_Nout {} ' +
                   'Nout_lower: {} Nout_upper: {}' +
                   '').format(i+1, v_mean, v_std, remove_l + remove_u,
                    remove_l, remove_u))

        ToT_remove_l += remove_l
        ToT_remove_u += remove_u
    if verbose == '+':
        print (('All_data: {} ToT_Nout: {} ToT_Nout_lower: {}' +
               ' ToT_Nout_upper: {}').format(vector.size,
                vector[np.isnan(vector)].size, ToT_remove_l, ToT_remove_u))


    return vector




def cont_clipping(intv_x, intv_y, series='poly', degree=0, smooth=0, v_std = 0,
                  sigl=3.0, sigu=3.0, niteration=3, grow=0, verbose='-'):
    '''
    Given an array this function does a clipping for lower and higher outliner
    points in the array.

    Parameters
    ----------
    vetor : array_like,
        Array containg elements to clip
    sigl : float,
        Sigma-clip criterion for upper deviant points, 0 for no clip
    sigu : float,
        Sigma-clip criterion for lower deviant points, 0 for no clip
    niteration : float,
        Number of sigma-clip iterations

    Return
    ------
    clipvector : ndarray,
        An array with the same size that input array, all elements clipped
        were assigned NaN

    '''
    #vector = np.copy(ivector)
    ToT_remove_l = 0
    ToT_remove_u = 0

    prev_nan = intv_y[np.isnan(intv_y)].size

    #intv_x = intv_x[~np.isnan(intv_x)]
    #intv_y = intv_y[~np.isnan(intv_y)]

    if verbose == '+':
        print (('\nPrevius values before the sigma clipping:' +
                'std= {:.4}, nan points= {:}').format(v_std, prev_nan))
        print (('Setup of the parameters:\nseries={}, degree={}, smooth={}, ' +
              'v_std = {}\nsigl={}, sigu={}, niteration={}, grow={}').format(
                series, degree, smooth, v_std, sigl, sigu, niteration, grow))

    for i in range(int(niteration)):

        #print intv_x, intv_y, degree

        intv_x_t = intv_x[~np.isnan(intv_x)]
        intv_y_t = intv_y[~np.isnan(intv_y)]


        if series == 'poly':
            p0cont = P.polyfit(intv_x_t, intv_y_t, degree, full=False)
            intv_y_mod = np.polyval(p0cont[::-1], intv_x)
        else:
            p0cont =   chebfit(intv_x_t, intv_y_t, degree, full=False)
            intv_y_mod = chebval(intv_x, p0cont)

        intv_res = intv_y - intv_y_mod

        #print intv_y_mod
        #print intv_res

        if sigl != 0.0:
           prev_nan = intv_y[np.isnan(intv_y)].size
           ind_sigl = np.where(intv_res < (-sigl*v_std))[0]
           intv_y[ind_sigl] = np.nan
           intv_x[ind_sigl] = np.nan

           remove_l = intv_y[np.isnan(intv_y)].size - prev_nan

           j=0
           while j < grow:
               j+=1
               prev_nan = intv_y[np.isnan(intv_y)].size
               del_ind = np.copy(ind_sigl)+j
               del_ind = del_ind[(del_ind>-1) & (del_ind<intv_y.size)]
               intv_y[del_ind] = np.nan
               intv_x[del_ind] = np.nan


               del_ind = np.copy(ind_sigl)-j
               del_ind = del_ind[(del_ind>-1) & (del_ind<intv_y.size)]
               intv_y[del_ind] = np.nan
               intv_x[del_ind] = np.nan

               remove_l+=   intv_y[np.isnan(intv_y)].size - prev_nan

        else:
            remove_l = 0

        if sigu != 0.0:
            prev_nan = intv_y[np.isnan(intv_y)].size
            ind_sigu = np.where(intv_res > (sigu*v_std))[0]
            intv_y[ind_sigu] = np.nan
            intv_x[ind_sigu] = np.nan

            remove_u =  intv_y[np.isnan(intv_y)].size - prev_nan

            j=0
            while j < grow:
               j+=1
               prev_nan = intv_y[np.isnan(intv_y)].size
               del_ind = np.copy(ind_sigu)+j
               del_ind = del_ind[(del_ind>-1) & (del_ind<intv_y.size)]
               intv_y[del_ind] = np.nan
               intv_x[del_ind] = np.nan



               del_ind = np.copy(ind_sigu)-j
               del_ind = del_ind[(del_ind>-1) & (del_ind<intv_y.size)]
               intv_y[del_ind] = np.nan
               intv_x[del_ind] = np.nan


               remove_u+= intv_y[np.isnan(intv_y)].size - prev_nan

        else:
            remove_u = 0
        if verbose == '+':
            print (('itera: {} ToT_Nout {} ' +
                   'Nout_lower: {} Nout_upper: {}' +
                   '').format(i+1, remove_l + remove_u, remove_l, remove_u))

        ToT_remove_l += remove_l
        ToT_remove_u += remove_u
    if verbose == '+':
        print (('All_data: {} ToT_Nout: {} ToT_Nout_lower: {}' +
               ' ToT_Nout_upper: {}').format(intv_y.size,
               ToT_remove_l + ToT_remove_u, ToT_remove_l, ToT_remove_u))


    return intv_y, intv_x, p0cont


def Ufitmultiline(name_spec, clines, linesguess, linesig, linesb,
              linessigb, inputcore, emi_line, abs_line,
              linessigfix, linescentfix, linescorefix,
              line_masks, lineslim, linesc, linesw, contfunc,  z,
              plot, figsize, figname, figtit, figlabel, sprefit, figxlim,
              figylim,
              direc, showt, showp, verbose, nflog,
              nspec_t, name_table, pheader_t, verbose_t, verb_ext='-',
              verb_hed='-', GH_plot='no', NSIG=3.0):

    """
    Upper function of fitmultiline
    Parameters
    ===========
    name_spec = array_like,
              it can be two kind of inputs long-slit or cube

              for a long-slit:
              'spect', 'inputfile.fits', 'crval1', 'cdelt1','crpix1',
              'the name or number of the extension for the data',
              'the name or number of the extension for the header'
              'the name or number of the extension for the wave'
              for a cube
              'cube', 'inputfile.fits','x', 'y',
              'the name or number of the extension for the data',
              'crval1', 'cdelt1','crpix1',
              'the name or number of the extension for the header'
              'the name or number of the extension for the wave'
    """
    cube = fits.open(name_spec[1])
    if verb_ext == '+':
        print ('printing the extensions of the cube...')
        print (cube.info())

    if name_spec[0] == 'spect':
        if len(name_spec) >= 6:
            spec  = cube[name_spec[5]].data
        else:
            spec  = cube[0].data

        if len(name_spec) >= 7:
            hdr = cube[name_spec[6]].header
        else:
            hdr0 = cube[0].header

        try:
            hdr   = [hdr0[name_spec[2]], hdr0[name_spec[3]]]
            try:
                hdr[0] = hdr[0]  + (1 - hdr0[name_spec[4]])*hdr[1]
            except:
                    print ('It was not given CRPIX, then was taken CRPIX=1')
        except:
            raise ValueError('The keywords doesnt exits or are mispell')

        try:
            wl = cube[name_spec[7]].data
        except:
            wl = np.linspace(hdr[0], (len(spec)-1)*hdr[1] + hdr[0], len(spec))


    if name_spec[0] == 'cube':
        CX = int(name_spec[2])
        CY = int(name_spec[3])
        print(name_spec[4])
        spec = cube[name_spec[4]].data[:, CY - 1, CX - 1]
        #ivar = np.transpose(cube['IVAR'].data, axes=(2, 1, 0))
        #mask = np.transpose(cube['MASK'].data, axes=(2, 1, 0))

        hdr0 = cube[name_spec[8]].header

        try:
            hdr   = [hdr0[name_spec[5]], hdr0[name_spec[6]]]
            try:
                hdr[0] = hdr[0]  + (1 - hdr0[name_spec[7]])*hdr[1]
            except:
                print ('It was not given CRPIX, then was taken CRPIX=1')
        except:
            raise ValueError('The keywords doesnt exits or are mispell')

        try:
            wl = cube[name_spec[9]].data
        except:
            wl = np.linspace(hdr[0], (len(spec)-1)*hdr[1] + hdr[0], len(spec))



    if verb_hed == '+':
        print ('printing the  header of the cube...')
        print (hdr0.values)



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

    vfit_tmp  = fitmultiline(wl, spec,
                             clines, linesig, linesguess=linesguess,
                             inputcore=inputcore,
                             emi_line = emi_line, abs_line = abs_line,
                             linessigfix=linessigfix,
                             linescentfix=linescentfix,
                             linescorefix=linescorefix,
                             linesb=linesb, linessigb=linessigb,
                             z=z, lineslim=lineslim,
                             line_masks=line_masks,
                             cont_l=[linesc[0] + linesw[0], linesc[0]],
                             cont_r=[linesc[1], linesc[1] + linesw[1]],
                             contfunc=contfunc,
                             plot=plot, figsize=figsize, figtit=figtit,
                             figname=figname,
                             figlabel = figlabel, figxlim = figxlim,
                             figylim=figylim,
                             direc=direc, showt = showt, sprefit=sprefit,
                             showp=showp, verbose=verbose, nflog = nflog,
                             GH_plot= GH_plot, NSIG = NSIG
                            )
    print_output_table(nspec_t, vfit_tmp[1],
                            np.array(vfit_tmp[0]).ravel(),
                            nflog=name_table, pheader=pheader_t,
                            verbose = verbose_t)

    return   vfit_tmp

def Ufitcontinuum(name_spec, clines, linesguess, linesig, linesb,
              linessigb,inputcore,
              linessigfix, linescentfix, linescorefix,
              line_masks, lineslim, linesc, linesw, contfunc,  z,
              ):

    """
    Upper function of fitmultiline
    """
    if name_spec[0] == 'spect':
        try:
            #spec  = pf.getdata(name_spec[1])
            #hdr0  = pf.getheader(name_spec[1])
            specn = fits.open(name_spec[1])
            spec = specn[0].data
            hdr0 = specn[0].header

            hdr   = [hdr0[name_spec[2]], hdr0[name_spec[3]]]
            try:
                hdr[0] = hdr[0]  + (1 - hdr0[name_spec[4]])*hdr[1]
            except:
                print ('It was not given CRPIX, then was taken CRPIX=1')
        except:
            raise ValueError('The file doesnt exist or the header parameters')

    if name_spec[0] == 'cube':
        try:
            #spec  = pf.getdata(name_spec[1])[:, CY - 1, CX - 1]
            #hdr0  = pf.getheader(name_spec[1])
            specn = fits.open(name_spec[1])
            spec = specn[0].data[:, CY - 1, CX - 1]
            hdr0 = specn[0].header

            CX = int(name_spec[2])
            CY = int(name_spec[3])
            hdr   = [hdr0[name_spec[4]], hdr0[name_spec[5]]]
            try:
                hdr[0] = hdr[0]  + (1 - hdr0[name_spec[4]])*hdr[1]
            except:
                print ('It was not given CRPIX1, then was taken CRPIX=1')
        except:
            raise ValueError('The file doesnt exist or the header parameters')

    wl = linspace(hdr[0], (len(spec)-1)*hdr[1] + hdr[0], len(spec))

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

    vfit_tmp  = fitcontinuum(wl, spec,hdr[0], hdr[1],
                             clines, linesig, linesguess=linesguess,
                             inputcore=inputcore,
                             linessigfix=linessigfix,
                             linescentfix=linescentfix,
                             linescorefix=linescorefix,
                             linesb=linesb, linessigb=linessigb,
                             z=z, lineslim=lineslim,
                             line_masks=line_masks,
                             cont_l=[linesc[0] + linesw[0], linesc[0]],
                             cont_r=[linesc[1], linesc[1] + linesw[1]],
                             contfunc=contfunc
                            )
    #print_output_table(nspec_t, vfit_tmp[1],
    #                        np.asnp.array(vfit_tmp[0]).ravel(),
    #                        nflog=name_table, pheader=pheader_t,
    #                        verbose = verbose_t)
    return vfit_tmp

def fitcontinuum(*args,**kwargs) :
    '''
    Parameters
    -----------
    wl   : array_like; wavelength
    spec : array_like; flux
    lref : float, wavelenght of reference
    ldel : float, delta wavelenght of the spectrum
    line : array_like; [dic,diccont_l,diccont_r]  dic(e.g., hbeta, OIII, halfa)
    linessing : array_like; guess sigma to the lines
    z    : float, redshift of the line
    l1   : float, limit by the left of the range to fit the line
    l2   : float, limit by the right of the range to fit the line
    d_l  : float, range of the interval for the continum to the left
    d_r  : float, range of the interval for the continum to the right
    plot : str, it make a plot of the fit
    figtit  : str, figure title
    figname : str, figure name (e.g., fig.png)
    direc   : str, path where the image will be put
    nubspec : str, number of the spectrum assigned by the user

    Return
    -----------
    grev     : array_like; parameters fitted
    grev_erf : array_like; error of parameters fitted
    meancont : float; mean of the continum
    sigcont  : float; sigma of the continum
    csig     : float; signal-to-noise continum
    lsig     : float; signal-to-nose line
    lerr     : float; error at the line
    fgauss   : float; flux in the gaussian function fitted
    fline    : float; flux in the profile line
    fline_err: float; error at flux in the profile line
    W        : float; equivalent width
    W_err    : float; error at the equivalente width
    '''
    # args
    wl = args[0]; spec = args[1]; lref = args[2]; ldel = args[3];
    lines_str = args[4]; linessig = args[5]

    # kwargs
    if 'linesguess' in kwargs:
        linesguess = kwargs['linesguess']
    else:
        linesguess = np.zeros(len(lines_str))
    linesb  = kwargs['linesb']      if 'linesb' in kwargs else np.array([])
    linessigb = kwargs['linessigb'] if 'linessigb'in kwargs else np.array([])
    inputcore = kwargs['inputcore'] if 'inputcore'in kwargs else None
    z       = kwargs['z']       if 'z'      in kwargs else 1
    lineslim= kwargs['lineslim']if'lineslim'in kwargs else [10, 10]
    cont_l  = kwargs['cont_l']  if 'cont_l' in kwargs else [20, 70]
    cont_r  = kwargs['cont_r']  if 'cont_r' in kwargs else [20, 70]
    contfunc= kwargs['contfunc']if'contfunc'in kwargs else ['poly', '1', 'yes']
    plot    = kwargs['plot']      if 'plot'   in kwargs else 'yes'
    figxlim = kwargs['figxlim']   if 'figxlim' in kwargs else ([30, 30])
    figylim = kwargs['figylim']   if 'figylim' in kwargs else None
    figsize  = kwargs['figsize']  if 'figsize' in kwargs else None
    figlabel = kwargs['figlabel'] if 'figlabel' in kwargs else (['no'])
    figtit  = kwargs['figtit']  if 'figtit' in kwargs else None
    figname = kwargs['figname'] if 'figname'in kwargs else None
    direc   = kwargs['direc']   if 'direc'  in kwargs else None
    nubspec = kwargs['nubspec'] if 'nubspec'in kwargs else '--'
    nflog   = kwargs['nflog']   if 'nflog'  in kwargs else 'fit.log'
    fclick  = kwargs['fclick']  if 'fclick' in kwargs else None
    showt   = kwargs['showt']   if 'showt'  in kwargs else (['no'])
    showp   = kwargs['showp']   if 'showp'  in kwargs else 'yes'
    sprefit = kwargs['sprefit']   if 'sprefit'  in kwargs else None
    verbose = kwargs['verbose'] if 'verbose'in kwargs else '+'
    line_masks = kwargs['line_masks'] if'line_masks' in kwargs else 'no'

    # creating ionizing lines array
    lines = np.array([diclines[i]  for i in lines_str])
    for i,e in enumerate(lines) :
      if linesguess[i] == 0:
          lines[i] = e*(z + 1.0)
      else:
          lines[i] = linesguess[i]

    # concatenating ionizing and blend lines arrays
    aline  = np.concatenate((lines, linesb))
    asigma = np.concatenate((linessig, linessigb))

    # number of lines
    nlines = len(aline)

    # sorting by wavelegth
    order  = np.argsort(aline)

    acenter = np.sort(aline)
    asigma  = np.take(asigma, order)

    # array to mask the pixels n*sigma around the lines
    if line_masks == 'no':
        amask = np.ones((len(acenter)*2))*3
    else:
        amask = np.copy(line_masks)

    # limits of fit range
    ll_lamb = acenter[0]-lineslim[0] ; lr_lamb = acenter[-1]+lineslim[1]
    ll  = lamb2idex(ll_lamb, lref, ldel)
    lr  = lamb2idex(lr_lamb, lref, ldel)
    y   = spec[ll:lr]
    x   = wl[ll:lr]

    if nflog is not None:
        flog=open(nflog,'a')

    tout = "\nThe spectrum has a spectral scale of: {} A".format(ldel)
    if nflog is not None:
        flog.write(tout)
    if verbose == '+':
        print(tout)

    # limits for  both red and blue parts of the continuum
    cl1 = acenter[0]  - cont_l[0];   cl2 = acenter[0]  - cont_l[1]
    cl3 = acenter[-1] + cont_r[0];   cl4 = acenter[-1] + cont_r[1]

    c1 = lamb2idex(cl1, lref, ldel); c2 = lamb2idex(cl2, lref, ldel)
    c3 = lamb2idex(cl3, lref, ldel); c4 = lamb2idex(cl4, lref, ldel)

    conty    = np.concatenate([spec[c1:c2], spec[c3:c4]]) # y continuum
    contx    = np.concatenate([wl[c1:c2], wl[c3:c4]])     # x continuum

    conty = np.array(conty, dtype=np.float64)
    contx = np.array(contx, dtype=np.float64)



    # Sigma-clipping parameters
    try:
        sigl = float(contfunc[3])
        sigu = float(contfunc[4])
        niteration =  int(contfunc[5])
        grow = int(contfunc[6])
        kernel = float(contfunc[7])

        # Making the clipping on continuum interval
        tout  = "\n\nPerforming sigma-clipping on pseudo-continuum interval "
        tout1 = "\nRight [{}, {}]".format(cl1, cl2)
        tout2 = "\nLeft [{}, {}]".format(cl3, cl4)
        if nflog is not None:
            flog.write(tout + tout1 + tout2)
        if verbose == '+':
            print(tout + tout1 + tout2)

        conty_clip = clipping(conty,sigl=sigl,sigu=sigu,niteration=niteration,
                              grow=grow,verbose=verbose)

        # updating the discarted points in the case the fit of the continuum
        # includes region between lines
        cont_nan = np.where(np.isnan(conty_clip))[0]
        cont_nan[ cont_nan> (c2-c1) ] += c3-c2

        conty = conty[~np.isnan(conty_clip)]
        contx = contx[~np.isnan(conty_clip)]
    except:
        tout = ("\n\nIt was not possible to do sigma-clipping on " +
                "pseudo-continuum interval")
        if nflog is not None:
            flog.write(tout)
        if verbose == '+':
            print(tout)
        kernel = 0

    contmean = np.nanmean(conty, dtype=np.float64)              # Mean continuum
    contsig  = np.nanstd(conty, ddof=1, dtype=np.float64)       # Sigma continuum
    cont_sn  = abs(contmean/contsig)                      # S/N continuum
    #cont_err = sqrt(abs(contmean))
    cont_err = contsig

    tout = "\n\nStatistics of the pseudo-continuum:"
    tout1 = "\n------------------------------------"
    tout2 = "\nS/N of the pseudo-continuum: {}".format(cont_sn)
    tout3 = "\nSigma of the pseudo-continuum: {}".format(contsig)
    tout4 = "\nMean value of pseudo-continuum: {}".format(contmean)
    if nflog is not None:
        flog.write(tout + tout1 + tout2 + tout3 + tout4)
    if verbose == '+':
        print(tout + tout1 + tout2 + tout3 + tout4)


    # Fitting the continuum among the lines?
    contfit = contfunc[2]
    if contfit == 'yes':
        tout = ("\nThe psuedo-continuum would be fitting between {} and" +
                   " {} A").format(cl1, cl4)
        tout1 = "\nNow, masking the points of the lines within +/- n*sigma"
        if nflog is not None:
            flog.write(tout + tout1)
        if verbose == '+':
            print(tout + tout1)

        conty_fit = np.copy(spec[c1:c4])
        contx_fit = np.copy(wl[c1:c4])

        # Masking the clipped continuum points
        conty_fit[cont_nan] = np.nan
        contx_fit[cont_nan] = np.nan

        # Masking the lines
        for lcenter, lsigma, nmask in zip(acenter, asigma, order):
            ll_l = lcenter - amask[nmask*2]*lsigma
            lr_l = lcenter + amask[nmask*2+1]*lsigma
            ll_l  = lamb2idex(ll_l, lref, ldel)
            lr_l  = lamb2idex(lr_l, lref, ldel)
            conty_fit[ll_l-c1:lr_l-c1] = np.nan
            contx_fit[ll_l-c1:lr_l-c1] = np.nan
    else:
        conty_fit = np.copy(conty)
        contx_fit = np.copy(contx)

    # Smoothing the continuum
    if kernel != 0:
        tout = "\nSmoothing the continuum (kernel={})...".format(kernel)
        if nflog is not None:
            flog.write(tout)
        if verbose == '+':
            print(tout)
        from astropy.convolution import convolve, Gaussian1DKernel, Box1DKernel
        gauss_kernel = Gaussian1DKernel(kernel)
        conty_fit = convolve(conty_fit, gauss_kernel)
        conty_fit[np.isnan(contx_fit)] = np.nan


    # Parameters to fit the pseudo continuum
    series  = contfunc[0]
    graup   = int(contfunc[1])
    if series == 'poly':
        adegree = np.array([0, graup])
    else:
        adegree = np.array([1, graup])


    # Fitting the pseudo continuum
    tout = ("\nFitting the pseudo-continuum " +
            "(including sigma-clipping analysis)...")
    if nflog is not None:
        flog.write(tout)
    if verbose == '+':
        print(tout)
    try:
        nan_ycont, nan_xcont, p0cont = cont_clipping(np.copy(contx_fit),
                              np.copy(conty_fit),
                              series=series,
                              degree=graup, smooth=0,
                              v_std = contsig, sigl=sigl, sigu=sigu,
                              niteration=niteration, grow=grow,
                              verbose=verbose)
    except:
        tout = ("\nIt was not possible to fit the pseudo continuum, now" +
                "\nRunning the fitting without sigma-clipping...")
        if nflog is not None:
            flog.write(tout)
        if verbose == '+':
           print(tout)

        contx_fit = contx_fit[~np.isnan(contx_fit)]
        conty_fit = conty_fit[~np.isnan(conty_fit)]

        if series == 'poly':
             p0cont  = P.polyfit(contx_fit, conty_fit, graup, full=False)
        else:
             p0cont = chebfit(contx_fit, conty_fit, graup, full=False)
        nan_ycont=np.copy(contx_fit)
        nan_xcont=np.copy(conty_fit)



    # Creating the continuum array
    if series == 'poly':
        fcont = np.polyval(p0cont[::-1], x)
    else:
        fcont = chebval(x, p0cont)


    return  wl, spec, x, y, fcont, c1, c2, c3, c4, nan_xcont, nan_ycont, p0cont
