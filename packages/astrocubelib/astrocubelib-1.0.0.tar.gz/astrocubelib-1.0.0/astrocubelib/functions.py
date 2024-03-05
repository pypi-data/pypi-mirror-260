import numpy as np
import scipy as sc
from scipy import odr

from numpy.polynomial.chebyshev import chebval


def residuals(p, f, y, x):
   err = y-f(x, p)
   return err

def chisqg(ydata,ymod,sd=None):
    """
    Returns the chi-square error statistic as the sum of squared errors between
    Ydata(i) and Ymodel(i). If individual standard deviations (array sd) are
    supplied, then the chi-square error statistic is computed as the sum of
    squared errors divided by the standard deviations. Inspired on the IDL
    procedure linfit.pro.
    See http://en.wikipedia.org/wiki/Goodness_of_fit for reference.

    x,y,sd assumed to be Numpy arrays. a,b scalars.
    Returns the float chisq with the chi-square statistic.

    Rodrigo Nemmen
    http://goo.gl/8S1Oo
    """
    # Chi-square statistic (Bevington, eq. 6.9)
    if sd==None:
         chisq=sum((ydata-ymod)**2)
    else:
         chisq=sum(((ydata-ymod)/sd)**2 )

    return chisq

def redchisqg(ydata,ymod,deg=2,sd=None):
    """
    Returns the reduced chi-square error statistic for an arbitrary model,
    chisq/nu, where nu is the number of degrees of freedom. If individual
    standard deviations (array sd) are supplied, then the chi-square error
    statistic is computed as the sum of squared errors divided by the standard
    deviations. See http://en.wikipedia.org/wiki/Goodness_of_fit for reference.

    ydata,ymod,sd assumed to be Numpy arrays. deg integer.

    Usage:
    >>> chisq=redchisqg(ydata,ymod,n,sd)
    where
     ydata : data
     ymod : model evaluated at the same x points as ydata
     n : number of free parameters in the model
     sd : uncertainties in ydata

    Rodrigo Nemmen
    http://goo.gl/8S1Oo
    """
    # Chi-square statistic
    if sd==None:
         chisq=sum((ydata-ymod)**2)
    else:
         chisq=sum(((ydata-ymod)/sd)**2 )

    # Number of degrees of freedom assuming 2 free parameters
    nu=ydata.size - deg
    #print ydata.size, chisq, nu

    return chisq/nu


def fit(func, xrang, yrang, param, weighty=None, weightx=None, fix=None,
        verbose=None):
    """
    Odr fucntions

    fix : array_like of ints of rank-1, optional sequence of integers with the
          same length as param(beta0) that determines which parameters are held
          fixed. A value of 0 fixes the parameter, a value > 0 makes the
          parameter free.

    futher information in:

    http://docs.scipy.org/doc/scipy/reference/odr.html
    http://docs.scipy.org/doc/external/odrpack_guide.pdf
    """
    functask = {'multiline': odr.Model(multi),
                'g_hermite': odr.Model(gaussian_hermite_b),
                'g_hermite_p': odr.Model(gaussian_hermite)}

    linear = functask[func]

    if weighty != None :
        weighty=1./np.square(weighty)
    if weightx != None :
        weightx=1./np.square(weightx)
    # wd (input variable) we (response variable))
    mydata = odr.Data(xrang, yrang, we=weighty, wd=weightx)
    cparam=np.copy(param)
    myodr  = odr.ODR(mydata, linear, cparam,ifixb=fix)
    myoutput = myodr.run()

    if verbose==True :
        print (myoutput.pprint())

    return myoutput.beta,myoutput.sd_beta


def gauss(p,x):
    """
    x is vector are the coordinates a and
    p[0] = continum
    p[1] = core
    p[2] = center
    p[3] = sigma
    fwhm = p[3]*2.355
    """
    return p[0] + p[1] * np.exp (-0.5*(((x-p[2])/abs(p[3]))**2))

def multi_old(p,x) :
    '''
    The two last p array values are :
    p[-2] : the poly type; 0 for normal, 1 for chevpoly
    p[-1] : the poly degree

    The number of poly parameters (num_par) is p[-1] + 1
    '''

    num_par = int(p[-1]) + 1 + 2
    if p[-2] == 0:
        y = polyval(p[-num_par:-2][::-1], x)
    else:
        y = chebval(x, p[-num_par:-2])

    n_id = -(num_par + 1)
    n    = int(p[n_id])
    num_SG = p[n_id-n:n_id]
    num_Z  = p[n_id-n-n/2:n_id-n]
    num_CN = p[n_id-n-n/2-n:n_id-n-n/2]
    num_CR = p[n_id-n-n/2-n-n:n_id-n-n/2-n]

    acent=np.zeros([n])
    for i in np.arange(n):
        acent[i] = p[i*3+1]

    for i in np.arange(n/2)+1 :
        SG_t = np.where(num_SG==i)[0]
        CN_t = np.where(num_CN==i)[0]
        CR_t = np.where(num_CR==i)[0]
        # sigma
        for j in SG_t[1::]:
            p[j*3 + 2] = p[SG_t[0]*3 + 2]
        # center
        for k in SG_t:
            acent[k] = acent[k]*num_Z[i-1]
        # core
        for l in CR_t[1::]:
            p[l*3]  = p[CR_t[0]*3]*(3.0/0.98)

    # Sum of the multiples gaussians
    for i in arange(n):
        # gaussian parameters: cont, core, cent, sigma
        y = y + gauss([0, p[i*3], acent[i], p[i*3+2]], x)

#    if acent[2] > (6562. + 30) or acent[2] < (6562. - 30):
#        y = y*nan

    return y


def multi(p,x) :
    '''

    '''
    # Number of lines
    num_lines = int(p[-1])
    # initiator of auxilar parameters
    nbef = -1


    # A copy of parameter array
    prun = np.copy(p)


    ##### sigma #####
    # Number of systems with same sigma
    num_sys_sigma = int(p[-2])
    nbef -= 1
    # sigma array
    array_sigma = p[nbef-num_sys_sigma:nbef]
    nbef -= num_sys_sigma
    # systems of sigma
    sys_sigma = p[nbef-num_lines:nbef]
    nbef -= num_lines
    #print (array_sigma, sys_sigma)
    for i in np.arange(num_lines) :
        if sys_sigma[i] > 0:
            prun[i*3+2] = array_sigma[int(sys_sigma[i])-1]


    ####### central wavelength ######
    num_sys_cent = int(p[nbef-1:nbef])
    nbef -= 1
    # cent array
    array_cent = p[nbef-num_sys_cent:nbef]
    nbef -= num_sys_cent
    # systems of cent
    sys_cent = p[nbef-num_lines:nbef]
    nbef -= num_lines
    for i in np.arange(num_lines) :
        if sys_cent[i] > 0:
            prun[i*3+1] = p[i*3+1]*array_cent[int(sys_cent[i])-1]

    ####### core ######
    num_sys_core = int(p[nbef-1:nbef])
    nbef -= 1
    # core array
    array_core = p[nbef-num_sys_core:nbef]
    nbef -= num_sys_core
    # systems of core
    sys_core = p[nbef-num_lines:nbef]
    nbef -= num_lines
    for i in np.arange(num_sys_core):
        term1 = np.where(sys_core==i+1)[0][0]
        term2 = np.where(sys_core==i+1)[0][1]
        prun[term1*3] = array_core[i]*(0.98/3)
        prun[term2*3] = array_core[i]

    y=0
    # Sum of the multiples gaussians
    for i in np.arange(num_lines):
        # gaussian parameters: cont, core, cent, sigma
        y = y + gauss([0, prun[i*3], prun[i*3+1], prun[i*3+2]], x)

    return y

def rad_bub(L, pho, t, gamma=5./3.):

   fact = ((375*(gamma-1.)) / (28*(9*gamma-4.)*np.pi))**(1./5.)
   #print fact, fact*(3./5.)
   R = fact * ((L/pho)**(1./5.)) * (t**(3./5.))

   return R/(pc*100)

def vel_bub(L, pho, t, gamma=5./3.):

   fact = ((375*(gamma-1.)) / (28*(9*gamma-4.)*np.pi))**(1./5.)
   Vel = (fact*(3./5.)) * ((L/pho)**(1./5.)) * (t**(-2./5.))

   return Vel/1e5


def moffat_func(p, x):
    """
    x is a position array
    Parameters:
    ------------
    p[0] = cte
    p[1] = alpha
    p[2] = beta
    fwhm = p[3]*2.355

    Information from PSFMEASURE help (noao/obsutils)

    I(r) = (1 + (r/alpha)**2)) ** (-beta)               Moffat

    MFWHM = 2 * alpha * sqrt (2 ** (1/beta) - 1)

    alpha = MFWHM / (2 *  sqrt (2 ** (1/beta) - 1))

    beta = log (2) / log ( (MFWHM/2*alpha)**2 + 1)

    The ellipticity and positional angle of an object are  derived  from
    the second central intensity weighted moments.  The moments are:

            Mxx = sum { (I - B) * x * x } / sum { I - B }
            Myy = sum { (I - B) * y * y } / sum { I - B }
            Mxy = sum { (I - B) * x * y } / sum { I - B }

    where  x  and  y  are the distances from the object center, I is the
    pixel intensity and B is the background intensity.  The sum is  over
    the  same  subpixels  used  in  the  enclosed  flux  evaluation with
    intensities  above  an  isophote  which  is   slightly   above   the
    background.   The  ellipticity  and position angles are derived from
    the moments by the equations:

            M1 = (Mxx - Myy) / (Mxx + Myy)
            M2 = 2 * Mxy / (Mxx + Myy)
            ellip = (M1**2 + M2**2) ** 1/2
            pa = atan (M2 / M1) / 2

    where ** is the exponentiation operator and atan is the arc  tangent
    operator.   The ellipticity is essentially (a - b) / (a + b) where a
    is a major axis scale length and b is a minor axis scale length.   A
    value  of  zero corresponds to a circular image.  The position angle
    is given in degrees counterclockwise from the x or column axis.

    """
    cte   = p[0]
    alpha = p[1]
    beta  = -1.0*p[2]

    return  cte*((1. + np.square(x/alpha))**(beta))

def gaussian_hermite_b(p,x):
    """
    Gaussian-Hermite Serie, van der Marel (1993), Cappellari (2004) and
    Riffel (2010)

    Parameters
    ----------

    x is vector are the coordinates a and
    p[0] = Amplitud of the Gaussian-Hermite Serie (A)
    p[1] = the peak wavelength (lc)
    p[2] = sigma  (sig)
    p[3] = h3
    p[4] = h4
    """

    A   = p[0]
    lc  = p[1]
    sig = p[2]
    h3  = p[3]
    h4  = p[4]
    #print (A, lc, sig, h3, h4)

    y = (x - lc)/sig
    alpha_y = (1./(sig*np.sqrt(2*np.pi)))*np.exp(-0.5*np.square(y))
    H3 = (1./np.sqrt(6))*(2*np.sqrt(2)*(y**3) - 3*np.sqrt(2)*y)
    H4 = (1./np.sqrt(24))*(4*(y**4) - 12*np.square(y) + 3.)

    return A*alpha_y*(1. + h3*H3 + h4*H4)


def gaussian_hermite(x,A,lc,sig,h3,h4):
    """
    Gaussian-Hermite Serie, van der Marel (1993), Cappellari (2004) and
    Riffel (2010)

    Parameters
    ----------

    x is vector are the coordinates a and
    p[0] = Amplitud of the Gaussian-Hermite Serie (A)
    p[1] = the peak wavelength (lc)
    p[2] = sigma  (sig)
    p[3] = h3
    p[4] = h4
    """

#    A   = p[0]
#    lc  = p[1]
#    sig = p[2]
#    h3  = p[3]
#    h4  = p[4]

    y = (x - lc)/sig
    alpha_y = (1./(sig*np.sqrt(2*np.pi)))*np.exp(-0.5*np.square(y))
    H3 = (1./np.sqrt(6))*(2*np.sqrt(2)*(y**3) - 3*np.sqrt(2)*y)
    H4 = (1./np.sqrt(24))*(4*(y**4) - 12*np.square(y) + 3.)

    return A*alpha_y*(1. + h3*H3 + h4*H4)
