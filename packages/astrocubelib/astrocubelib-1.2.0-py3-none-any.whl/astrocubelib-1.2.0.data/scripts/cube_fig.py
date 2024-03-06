#!python
#Author : J. A. Hernandez-Jimenez

import numpy as np
from astrocubelib import speedc, diclines, linelatex, mapa
import os, sys
import warnings
warnings.filterwarnings("ignore")
from astropy.io import fits

try:
    finput=open(sys.argv[1]).read().splitlines()
    i=0

    espectro = finput[i].split()[0].split(','); i+=1
    hedkey   = finput[i].split()[0].split(','); i+=1
    scale    = finput[i].split()[0].split(','); i+=1
    line     = finput[i].split()[0]; i+=1
    z        = finput[i].split()[0].split(','); i+=1
    usermask = finput[i].split()[0]; i+=1
    landa    = [ float(s) for s in finput[i].split()[0].split(',')]; i+=1
    lsigma   = [ float(s) for s in finput[i].split()[0].split(',')]; i+=1
    subsig   = [ float(s) for s in finput[i].split()[0].split(',')]; i+=1
    sn       = float(finput[i].split()[0]); i+=1
    mchi     = float(finput[i].split()[0]); i+=1
    flux_err_lim = float(finput[i].split()[0]); i+=1
    nfactor  = [ float(s) for s in finput[i].split()[0].split(',')]; i+=1
    fmt      = finput[i].split()[0].split(','); i+=1
    cmaps    = finput[i].split()[0].split(','); i+=1
    print ("\nFactor de normatization of line flux: {}".format(nfactor[0]))
    print ("\nFactor de normatization of the continuum: {}".format(nfactor[1]))

except:
    print ('The input program are:')
    print ('\n../zcuboR4.fits        # input cube (fits)')
    print ('crval3,cdelt3            # Header keywords (crval, cdelt, ext)')
    print ('1,pix                    # scale (e.g., 0.146 arc/pix), unit')
    print ('halfa                    # line file output (e.g., halfa, OIII)')
    print ("8919,1,no          # value; 0 (z) or (1) vsys; 'yes' for Relt. Corc.")
    print ('none                     # user mask (fits)')
    print ('10,10           # mask in wavelength: lower_limt, higher_limt (A)')
    print ('0.9,5  # mask in sigma: lower_limt (take as instrumental ' +
           'resolution), higher_limt (A)')
    print ('9.1,3  # thermal broading (9.1), natural width of line (3)' +
           ' (in  km/s)')
    print ('5          # mask in signal-to-noise at line: lower limit (>)')
    print ('2          # mask in chi^2 at line: higher limit (<)')
    print ('50          # mask in relative error of flux (>)')
    print ('1,1        # normalization factor: line flux, continuum')
    print ('png,log,0.1 # image format (png), flux in log (log) or normal' +
           '(nor), barpad (0.1)')
    print ('inferno,seismic,hot_r,viridis # cmaps: ints, vel, sigma, chi(S/N)')
    print ('\n')

    sys.exit()

if len(espectro)==1:
   spec = fits.open(espectro[0])[0].data
   hdr = fits.open(espectro[0])[0].header
else:
   ext = int(espectro[1])
   spec = fits.open(espectro[0])[ext].data
   hdr = fits.open(espectro[0])[ext].header


print ("\nspectral scale: ", hdr[hedkey[1]])

y=spec.shape[1]
x=spec.shape[2]

axislab = scale[1]; dx = float(scale[0]); dy = float(scale[0])
axiscoord = [-x*dx*0.5, x*dx*0.5, -y*dy*0.5, y*dy*0.5]

imafmt = fmt[0]
imasc  = fmt[1]

## Z of the system
z[0] = float(z[0])
z[1] = float(z[1])
# Eq. Relativistic
if z[2] == 'yes':
    if z[1] == 1.0:
        vsys = z[0]
        beta = vsys/speedc
        Z = np.sqrt((1. + beta)/(1. - beta))
    else:
        Z = z[0]
        beta = (np.square(1+z) -1.0)/(np.square(1+1) + 1.0)
        vsys = beta*speedc
# Eq. no Relativistic
else:
    if z[1] == 1.0:
        vsys = z[0]
        Z = vsys/speedc
    else:
        vsys = speedc*z[0]
        Z = z[0]
# Redshift of line
f = Z + 1.0
lc = f*diclines[line]



nafile = 'fit.' + line + '.dat'


#    core  Center  Sigma  mcont  scont   SNC  SNL chi^2  chi_all^2  L_err (vel)
#0    1     2       3      4      5      6    7    8        9        10

#L_err_R  Fluxg  Fluxl  Fluxl_err  EW  EW_err EWg  EWg_err\n
# 11       12      13      14      15   16     17    18

#skew   kurtosis  sk_stat   sk_pval
#19      20         21         22

#GH_core   GH_cent  GH_sig   h3    h4
#23         24        25     26    27




vmap = np.loadtxt(nafile, usecols=[2,3,4,5,6,7,8,10,11,12,13,14,15,16])

linecent  = vmap[:, 0]
linesigma = vmap[:, 1]
cont      = vmap[:, 2]
contsigma = vmap[:, 3]
lineSN_C  = vmap[:, 4]
lineSN_L  = vmap[:, 5]
fitchi    = vmap[:, 6]
line_err  = vmap[:, 7]
line_err_R= vmap[:, 8]
fluxgauss = vmap[:, 9]
fluxline  = vmap[:, 10]
fluxline_err = vmap[:, 11]
EW        = vmap[:, 12]
EW_err    = vmap[:, 13]

###################
#  Masks          #
###################

# filter wavelenth
mask_wl = np.where((linecent<lc-landa[0]) | (linecent>lc+landa[1]))[0]

# filter s/n
mask_sn = np.where((lineSN_L < sn) | (np.isnan(lineSN_L)))[0]

# filter sigma line
mask_sig = np.where((linesigma<lsigma[0]) | (linesigma>lsigma[1]) )[0]

# filter chi^2
mask_chi = np.where((fitchi>mchi))[0]

# filter relative error in flux
relat_err = fluxline_err/fluxline*100
mask_err =  np.where((relat_err>flux_err_lim))[0]


if usermask != 'none':
    mask_user = fits.open(usermask)[0].data
else:
    mask_user = np.zeros((y,x))

# Printing masks
Mmask = np.zeros(len(linecent))
np.put(Mmask, mask_wl, np.nan)
Mmask = Mmask.reshape(y,x)
fits.writeto('mask_lambda.fits', Mmask, header=hdr, overwrite=True)

Mmask=np.zeros(len(linecent))
np.put(Mmask,mask_sn,np.nan)
Mmask=Mmask.reshape(y,x)
fits.writeto('mask_SN.fits', Mmask, header=hdr, overwrite=True)

Mmask=np.zeros(len(linecent))
np.put(Mmask, mask_sig, np.nan)
Mmask=Mmask.reshape(y, x)
fits.writeto('mask_sigma.fits', Mmask, header=hdr, overwrite=True)

Mmask=np.zeros(len(linecent))
np.put(Mmask, mask_chi, np.nan)
Mmask=Mmask.reshape(y, x)
fits.writeto('mask_chi.fits', Mmask, header=hdr, overwrite=True)

Mmask=np.zeros(len(linecent))
np.put(Mmask, mask_err, np.nan)
Mmask=Mmask.reshape(y, x)
fits.writeto('mask_relt_err_flux.fits', Mmask, header=hdr, overwrite=True)



#####################
# Flux gaussian map #
#####################

# masking
fluxgauss_raw = np.copy(fluxgauss)
np.put(fluxgauss, mask_wl, np.nan)
np.put(fluxgauss, mask_sn, np.nan)
np.put(fluxgauss, mask_sig, np.nan)
np.put(fluxgauss, mask_chi, np.nan)
np.put(fluxgauss, mask_err, np.nan)

# normalization
fluxgauss = fluxgauss/nfactor[0]

imaname  = 'mapflux_gauss.'
labelbar = 'F($'+linelatex[line]+'$)'

if imasc == 'log':
    fluxgauss = np.log10(fluxgauss)
    imaname  = 'mapflux_gauss_log.'
    labelbar = '$\log\,('+linelatex[line]+')$'

fluxgmap = fluxgauss.reshape(y,x)
fluxgmap = fluxgmap + mask_user

mapa(fluxgmap, imaname + imafmt, axiscoord, axislab, axislab,
     labelbar, cmap=cmaps[0], barpad=float(fmt[2]))
fits.writeto(imaname + 'fits', fluxgmap, header=hdr, overwrite=True)
fits.writeto(imaname[0:-1] + '_raw.fits', fluxgauss.reshape(y, x),
             header=hdr, overwrite=True)

#####################
# Flux line map     #
#####################

# masking
fluxline_raw = np.copy(fluxline)
np.put(fluxline, mask_wl, np.nan)
np.put(fluxline, mask_sn, np.nan)
np.put(fluxline, mask_sig, np.nan)
np.put(fluxline, mask_chi, np.nan)
np.put(fluxline, mask_err, np.nan)

fluxline = fluxline/nfactor[0]

imaname  = 'mapflux_line.'
labelbar = 'F($'+linelatex[line]+'$)'

if imasc == 'log':
    fluxline = np.log10(fluxline)
    imaname  = 'mapflux_line_log.'
    labelbar = '$\log\,('+linelatex[line]+')$'

fluxlmap = fluxline.reshape(y,x)
fluxlmap = fluxlmap + mask_user

mapa(fluxlmap, imaname + imafmt, axiscoord, axislab, axislab, labelbar,
     cmap=cmaps[0], barpad=float(fmt[2]))
fits.writeto(imaname + 'fits', fluxlmap, header=hdr, overwrite=True)
fits.writeto(imaname[0:-1] + '_raw.fits', fluxline_raw.reshape(y, x),
             header=hdr, overwrite=True)


##################
# Flux error map #
##################

# flux_err = sig_cont*np.sqrt(N(1+EW/(N*delta_lambda)) (castellanos 2002, ref.
# taken from Lagos et al. 2009, Garcia-Benito et al. 2010)
fluxline_err_raw = np.copy(fluxline_err)
np.put(fluxline_err, mask_wl, np.nan)
np.put(fluxline_err, mask_sn, np.nan)
np.put(fluxline_err, mask_sig, np.nan)
np.put(fluxline_err, mask_chi, np.nan)
np.put(fluxline_err, mask_err, np.nan)

fluxline_err = fluxline_err/nfactor[0]

imaname  = 'mapflux_line_err'
if imasc == 'log':
   fluxline_err = fluxline_err/(10**(fluxline))
   imaname  = 'mapflux_line_err_log'

fluxl_err_map = fluxline_err.reshape(y,x)
fluxl_err_map = fluxl_err_map + mask_user
fits.writeto(imaname + '.fits', fluxl_err_map, header=hdr, overwrite=True)
fits.writeto(imaname + '_raw.fits', fluxline_err_raw.reshape(y, x),
             header=hdr, overwrite=True)



##########################
# Relative Error of flux #
##########################

imaname  = 'mapflux_line_err_relt.'
labelbar = "%"

flux_err_relt = (fluxl_err_map/fluxlmap)*100.
mapa(flux_err_relt, imaname + imafmt, axiscoord, axislab, axislab, labelbar,
     vmin=0, vmax=100,
     cmap='Paired', barpad=0.1)
fits.writeto(imaname + 'fits', flux_err_relt, header=hdr, overwrite=True)

# raw map fo relative error of flux wihtout masking
# no correction for logarithmic scale
flux_err_relt_raw = (fluxline_err_raw/fluxline_raw)*100.
fits.writeto(imaname[0:-1] + '_raw.fits', flux_err_relt_raw.reshape(y, x),
             header=hdr, overwrite=True)

###################
#  centroid map   #
###################

centroidmap = np.copy(linecent)

# masking
np.put(centroidmap, mask_wl, np.nan)
np.put(centroidmap, mask_sn, np.nan)
np.put(centroidmap, mask_sig, np.nan)
np.put(centroidmap, mask_chi, np.nan)
np.put(centroidmap, mask_err, np.nan)

# plotting
centroidmap = centroidmap.reshape(y,x)
centroidmap = centroidmap + mask_user

fits.writeto('mapcentroid.fits', centroidmap, header=hdr, overwrite=True)

###################
#  Velocity map   #
###################

# convertion wavelenth to velocity
zcube  = ((linecent-diclines[line])/diclines[line])
vel = speedc*zcube

# masking
vel_raw = np.copy(vel)
np.put(vel, mask_wl, np.nan)
np.put(vel, mask_sn, np.nan)
np.put(vel, mask_sig, np.nan)
np.put(vel, mask_chi, np.nan)
np.put(vel, mask_err, np.nan)

# plotting
velmap = vel.reshape(y,x)
velmap = velmap + mask_user

mapa(velmap, 'mapvel_rad.' + imafmt, axiscoord, axislab, axislab,
     '$V\,('+linelatex[line]+')\,(km/s)$', cmap=cmaps[1], barpad=float(fmt[2]))
fits.writeto('mapvel_rad.fits', velmap, header=hdr, overwrite=True)

velmap = velmap - vsys

mapa(velmap, 'mapvel.' + imafmt, axiscoord, axislab, axislab,
     '$V\,('+linelatex[line]+')\,(km/s)$', cmap=cmaps[1], barpad=float(fmt[2]))
fits.writeto('mapvel.fits', velmap, header=hdr, overwrite=True)
fits.writeto('mapvel_raw.fits', vel_raw.reshape(y, x), header=hdr,
             overwrite=True)


###############################
# Relativistic Velocity map   #
###############################

# convertion wavelenth to velocity
zcube  = ((linecent-diclines[line])/diclines[line])
beta = (np.square(zcube+1.0) -1.0)/(np.square(zcube+1.0) + 1.0)
vel_R = speedc*beta

# masking
vel_R_raw = np.copy(vel_R)
np.put(vel_R, mask_wl, np.nan)
np.put(vel_R, mask_sn, np.nan)
np.put(vel_R, mask_sig, np.nan)
np.put(vel_R, mask_chi, np.nan)
np.put(vel_R, mask_err, np.nan)

# plotting
vel_R_map = vel_R.reshape(y,x)
vel_R_map = vel_R_map + mask_user

mapa(vel_R_map, 'mapvel_rad_R.' + imafmt, axiscoord, axislab, axislab,
     '$V\,('+linelatex[line]+')\,(km/s)$', cmap=cmaps[1], barpad=float(fmt[2]))
fits.writeto('mapvel_rad_R.fits', vel_R_map, header=hdr, overwrite=True)
fits.writeto('mapvel_rad_R_raw.fits', vel_R_raw.reshape(y, x),
             header=hdr, overwrite=True)


vel_R_map = vel_R_map - vsys

mapa(vel_R_map, 'mapvel_R.' + imafmt, axiscoord, axislab, axislab,
     '$V\,('+linelatex[line]+')\,(km/s)$', cmap=cmaps[1], barpad=float(fmt[2]))
fits.writeto('mapvel_R.fits', vel_R_map, header=hdr, overwrite=True)
fits.writeto('mapvel_R_raw.fits', vel_R_raw.reshape(y, x)-vsys,
             header=hdr, overwrite=True)


###########################
# Velocity Error map
###########################
line_err_raw = np.copy(line_err)
np.put(line_err, mask_wl, np.nan)
np.put(line_err, mask_sn, np.nan)
np.put(line_err, mask_sig, np.nan)
np.put(line_err, mask_chi, np.nan)
np.put(line_err, mask_err, np.nan)

vel_err_map = line_err.reshape(y, x)
vel_err_map = vel_err_map + mask_user

fits.writeto('mapvel_err.fits', vel_err_map, header=hdr, overwrite=True)
fits.writeto('mapvel_err_raw.fits', line_err_raw.reshape(y, x),
             header=hdr, overwrite=True)


##################################
# Velocity Relativistic Error map
##################################
line_err_R_raw = np.copy(line_err_R)
np.put(line_err_R, mask_wl, np.nan)
np.put(line_err_R, mask_sn, np.nan)
np.put(line_err_R, mask_sig, np.nan)
np.put(line_err_R, mask_chi, np.nan)
np.put(line_err_R, mask_err, np.nan)

vel_err_R_map = line_err_R.reshape(y,x)
vel_err_R_map = vel_err_R_map + mask_user

fits.writeto('mapvel_err_R.fits', vel_err_R_map, header=hdr, overwrite=True)
fits.writeto('mapvel_err_R_raw.fits', line_err_R_raw.reshape(y, x),
              header=hdr, overwrite=True)

####################
# Sigma line map   #
####################

# masking
sigma_raw = np.copy(linesigma)
np.put(linesigma, mask_wl, np.nan)
np.put(linesigma, mask_sn, np.nan)
np.put(linesigma, mask_sig, np.nan)
np.put(linesigma, mask_chi, np.nan)
np.put(linesigma, mask_err, np.nan)

fits.writeto('mapsig_line.fits', linesigma.reshape(y, x) + mask_user, header=hdr,
             overwrite=True)

# Discount of the instrumental sigma and convert to velocity
linesigma = np.sqrt((np.square(linesigma)-np.square(lsigma[0])))*speedc/diclines[line]

'''
Thermal width
sqrt (k*Te*m_h) ~ 9.1 km/s (O'dell & Townsley 1988, the ref was taken from
Cardiel-Zaragoza et al. 2014 and the eq. from lagos et al. 2009)
'''
sigma_th = subsig[0];

'''
Natural with ~ 3 km/s (Clegg et al. 1999, ref from Cardiel-Zaragoza et al. 2014)
'''
sigma_nat = subsig[1]

linesigma = np.sqrt(np.square(linesigma) - np.square(sigma_th) - np.square(sigma_nat))

sigmamap = linesigma.reshape(y,x)
sigmamap = sigmamap + mask_user

mapa(sigmamap, 'mapsig.' + imafmt, axiscoord, axislab, axislab,
     '$\sigma\,(km/s)$', cmap=cmaps[2], barpad=float(fmt[2]))
fits.writeto('mapsig.fits', sigmamap, header=hdr, overwrite=True)

# raw map of sigma without masking
fits.writeto('mapsig_lambda_raw.fits', sigma_raw.reshape(y, x), header=hdr,
             overwrite=True)
sigma_raw = np.sqrt((np.square(sigma_raw)-np.square(lsigma[0])))*speedc/diclines[line]
sigma_raw = np.sqrt(np.square(sigma_raw) - np.square(sigma_th) - np.square(sigma_nat))
fits.writeto('mapsig_raw.fits', sigma_raw.reshape(y, x), header=hdr,
             overwrite=True)


###################
# EW              #
###################

# masking
EW_raw = np.copy(EW)
np.put(EW, mask_wl, np.nan)
np.put(EW, mask_sn, np.nan)
np.put(EW, mask_sig, np.nan)
np.put(EW, mask_chi, np.nan)
np.put(EW, mask_err, np.nan)

#EW = abs(EW)
imaname  = 'mapEW.'
labelbar = 'EW'

if imasc == 'log':
    EW = np.log10(EW)
    imaname  = 'mapEW_log.'
    labelbar = '$\log\,$EW'

pmax = np.percentile(EW[~np.isnan(EW)],98)
pmin = np.percentile(EW[~np.isnan(EW)],2)


EWmap = EW.reshape(y,x)
EWmap = EWmap + mask_user

mapa(EWmap, imaname + imafmt, axiscoord, axislab, axislab, labelbar,
     cmap=cmaps[0], vmin = pmin, vmax=pmax, barpad=float(fmt[2]))
fits.writeto(imaname + 'fits', EWmap, header=hdr, overwrite=True)
fits.writeto(imaname[0:-1] + '_raw.fits', EW_raw.reshape(y, x), header=hdr,
             overwrite=True)

# error matrix
EW_err_raw = np.copy(EW_err)
np.put(EW_err, mask_wl, np.nan)
np.put(EW_err, mask_sn, np.nan)
np.put(EW_err, mask_sig, np.nan)
np.put(EW_err, mask_chi, np.nan)

imaname  = 'mapEW_err.'

if imasc == 'log':
    EW_err = EW_err/EW
    imaname  = 'mapEW_err_log.'

EWmap_err = EW_err.reshape(y, x)
EWmap_err = EWmap_err + mask_user

fits.writeto(imaname + 'fits', EWmap_err, header=hdr, overwrite=True)
fits.writeto(imaname[0:-1] + '_raw.fits', EW_err_raw.reshape(y, x),
             header=hdr, overwrite=True)

##################
# Cont           #
##################

ccont = np.copy(cont)

# masking
cont_raw = np.copy(cont)
#np.put(cont, mask_wl, np.nan)
np.put(cont, mask_sn, np.nan)
#np.put(cont, mask_sig, np.nan)
#np.put(cont, mask_chi, np.nan)
#np.put(cont, mask_err, np.nan)

imaname  = 'mapcont.'
labelbar = '$\\rm{F_{cont}}$'

cont=cont/nfactor[1]

if imasc == 'log':
    cont = np.log10(cont)
    imaname  = 'mapcont_log.'
    labelbar = '$\log\,(\\rm{F_{cont}})$'

contmap = cont.reshape(y, x)
contmap = contmap + mask_user

mapa(contmap, imaname + imafmt, axiscoord, axislab, axislab, labelbar,
     cmap=cmaps[0], barpad=float(fmt[2]))

fits.writeto(imaname + 'fits', contmap, header=hdr, overwrite=True)
fits.writeto(imaname[0:-1] + '_raw.fits', cont_raw.reshape(y, x),
             header=hdr, overwrite=True)


####################
# Chi squared      #
####################
# masking
fitchi_raw = np.copy(fitchi)
np.put(fitchi, mask_wl, np.nan)
np.put(fitchi, mask_sn, np.nan)
np.put(fitchi, mask_sig, np.nan)
np.put(fitchi, mask_chi, np.nan)
np.put(fitchi, mask_err, np.nan)

chimap = fitchi.reshape(y, x)
chimap = chimap + mask_user

mapa(chimap, 'mapchi.png', axiscoord, axislab, axislab, '$\chi^{2}$',
     cmap=cmaps[3], barpad=float(fmt[2]))
fits.writeto('mapchi.fits', chimap, header=hdr, overwrite=True)

# rawmap of chi squared without masking
fits.writeto('mapchi_raw.fits', fitchi_raw.reshape(y, x), header=hdr,
             overwrite=True)

#########################
# Signal-to-noise  Line #
#########################

# masking
snmap_L_raw = np.copy(lineSN_L)
np.put(lineSN_L, mask_wl, np.nan)
np.put(lineSN_L, mask_sn, np.nan)
np.put(lineSN_L, mask_sig, np.nan)
np.put(lineSN_L, mask_chi, np.nan)
np.put(lineSN_L, mask_err, np.nan)

snmap_L = lineSN_L.reshape(y, x)
snmap_L = snmap_L + mask_user

mapa(snmap_L,'mapSN_L.' + imafmt, axiscoord, axislab, axislab,
     '$Signal\,to\,noise$', cmap=cmaps[3], barpad=float(fmt[2]))
fits.writeto('mapSN_L.fits', snmap_L, header=hdr, overwrite=True)

# raw map of S/n map without mapping
fits.writeto('mapSN_L_raw.fits', snmap_L_raw.reshape(y, x), header=hdr,
             overwrite=True)


##############################
# Signal-to-noise  continuum #
##############################

# masking
lineSN_C_raw = np.copy(lineSN_C)
np.put(lineSN_C, mask_wl, np.nan)
np.put(lineSN_C, mask_sn, np.nan)
np.put(lineSN_C, mask_sig, np.nan)
np.put(lineSN_C, mask_chi, np.nan)
np.put(lineSN_C, mask_err, np.nan)

snmap_C = lineSN_C.reshape(y, x)
snmap_C = snmap_C + mask_user

mapa(snmap_C,'mapSN_C.' + imafmt, axiscoord, axislab, axislab,
     '$Signal\,to\,noise$', cmap=cmaps[3], barpad=float(fmt[2]))
fits.writeto('mapSN_C.fits', snmap_C, header=hdr, overwrite=True)
fits.writeto('mapSN_C_raw.fits', lineSN_C_raw.reshape(y,x), header=hdr,
             overwrite=True)




try:
    vmap = np.loadtxt(nafile, usecols=[19, 20, 26, 27])
    l_skew = vmap[:, 0]
    l_kurt = vmap[:, 1]
    l_h3 = vmap[:, 2]
    l_h4 = vmap[:, 3]

    #########################
    # Skew  Line #
    #########################

    # masking
    l_skew_raw = np.copy(l_skew)
    np.put(l_skew, mask_wl, np.nan)
    np.put(l_skew, mask_sn, np.nan)
    np.put(l_skew, mask_sig, np.nan)
    np.put(l_skew, mask_chi, np.nan)
    np.put(l_skew, mask_err, np.nan)

    map_skew = l_skew.reshape(y, x)
    map_skew = map_skew + mask_user

    vmin = np.percentile(map_skew[~np.isnan(map_skew)],95)
    vmax = np.percentile(map_skew[~np.isnan(map_skew)],5)

    mapa(map_skew,'mapskew.' + imafmt, axiscoord, axislab, axislab,
         'Skewness', cmap=cmaps[3], barpad=float(fmt[2]), vmin=vmin, vmax=vmax)
    fits.writeto('mapskew.fits', map_skew, header=hdr, overwrite=True)

    # raw map of skewness without masking
    fits.writeto('mapskew_raw.fits', l_skew_raw.reshape(y, x),
                 header=hdr, overwrite=True)


    #########################
    # Kurtosis  Line #
    #########################

    # masking
    l_kurt_raw = np.copy(l_kurt)
    np.put(l_kurt, mask_wl, np.nan)
    np.put(l_kurt, mask_sn, np.nan)
    np.put(l_kurt, mask_sig, np.nan)
    np.put(l_kurt, mask_chi, np.nan)
    np.put(l_kurt, mask_err, np.nan)

    map_kurt = l_kurt.reshape(y, x)
    map_kurt = map_kurt + mask_user

    vmin = np.percentile(map_kurt[~np.isnan(map_kurt)],95)
    vmax = np.percentile(map_kurt[~np.isnan(map_kurt)],5)

    mapa(map_kurt,'mapkurt.' + imafmt, axiscoord, axislab, axislab,
         'Kurtosis', cmap=cmaps[3], barpad=float(fmt[2]), vmin=vmin, vmax=vmax)
    fits.writeto('mapkurt.fits', map_kurt, header=hdr, overwrite=True)

    # raw map of kurtosis without masking
    fits.writeto('mapkurt_raw.fits', l_kurt_raw.reshape(y, x), header=hdr,
                 overwrite=True)


    #########################
    # h3  Line #
    #########################

    # masking
    l_h3_raw = np.copy(l_h3)
    np.put(l_h3, mask_wl, np.nan)
    np.put(l_h3, mask_sn, np.nan)
    np.put(l_h3, mask_sig, np.nan)
    np.put(l_h3, mask_chi, np.nan)
    np.put(l_h3, mask_err, np.nan)

    map_h3 = l_h3.reshape(y, x)
    map_h3 = map_h3 + mask_user

    vmin = np.percentile(map_h3[~np.isnan(map_h3)],95)
    vmax = np.percentile(map_h3[~np.isnan(map_h3)],5)

    mapa(map_h3,'maph3.' + imafmt, axiscoord, axislab, axislab,
         'h3', cmap=cmaps[3], barpad=float(fmt[2]), vmin=vmin, vmax=vmax)
    fits.writeto('maph3.fits', map_h3, header=hdr, overwrite=True)

    # raw map of kurtosis without masking
    fits.writeto('maph3_raw.fits', l_h3_raw.reshape(y, x),
                 header=hdr, overwrite=True)


    #########################
    # h4  Line #
    #########################

    # masking
    l_h4_raw = np.copy(l_h4)
    np.put(l_h4, mask_wl, np.nan)
    np.put(l_h4, mask_sn, np.nan)
    np.put(l_h4, mask_sig, np.nan)
    np.put(l_h4, mask_chi, np.nan)
    np.put(l_h4, mask_err, np.nan)

    map_h4 = l_h4.reshape(y, x)
    map_h4 = map_h4 + mask_user

    vmin = np.percentile(map_h4[~np.isnan(map_h4)],95)
    vmax = np.percentile(map_h4[~np.isnan(map_h4)],5)

    mapa(map_h4,'maph4.' + imafmt, axiscoord, axislab, axislab,
         'h4', cmap=cmaps[3], barpad=float(fmt[2]), vmin=vmin, vmax=vmax)
    fits.writeto('maph4.fits', map_h4, header=hdr, overwrite=True)

    # raw map of kurtosis without masking
    fits.writeto('maph4_raw.fits', l_h4_raw.reshape(y, x), header=hdr,
                 overwrite=True)

except:
   a=0
