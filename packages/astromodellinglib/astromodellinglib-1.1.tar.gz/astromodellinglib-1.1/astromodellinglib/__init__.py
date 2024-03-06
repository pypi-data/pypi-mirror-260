#from numpy import *
import numpy as np
import scipy as sc
from scipy.optimize import leastsq
from scipy import odr
import scipy.special as sp
import scipy.integrate as si
from math import erf
from math import gamma
from numpy.polynomial.chebyshev import chebval, chebfit
from scipy.special import hyp2f1
import configparser
from scipy.special import gammaincinv
from scipy.interpolate import interp1d
import scipy.optimize as op
from astropy.convolution import convolve

from IPython.display import display, Math

#######constant###########

g = 6.67428e-11            # m^3 kg^-1 s^-2

pc = 3.08568025e16         # m

arcsec = 129.445252857     # pc/arcsec

masssun = 1.9891e30        # kg

year = 3.1536e7            # seg

const = 4*np.pi*g             # const
cte   = masssun/(pc**2)    # kg/m^2
cte2  = masssun/(pc**3)    # kg/m^3

##########################

# Fit Function

def residuals(p, f, y, x):
   err = y-f(x, p)
   return err

def vaucou(s,z):
    '''
    The integrand of the integral of the eq. 5. in Simonneau & Prada (2004).
    This intregral has solution for n>=0.

    Parameters
    ----------
    s  = r/Re, where Re is the efective radius,i.e., the "radius" of the
         isophote that encloses one half of the total luminosity.
    kn = 2*n-0.324 (see Ciotti 1991), for n>=1 can be estimated with error
         smaller than 0.1%.
    '''
    global kn, n
    #print (kn,n)
    return (np.exp(-kn*(z**(1.0/n))*(z**(1.0/n-1.0)))/np.sqrt(np.square(z)-np.square(s)))

def vaucou_gauss(s,x):
    '''
    The integrand of the integral of the eq. 9. in Simonneau & Prada (2004).
    This intregral has solution for n>1. It can be resolved using gaussian
    numerical integration. s=r/Re, where Re is the efective radius,i.e., the
    "radius" of the isophote that encloses one half of the total luminosity.
    kn=2*n-0.324 (see Ciotti 1991), for n>=1 can be estimated with error
    smaller than 0.1%.
    '''
    global kn, n
    x1=(1.0-np.square(x))**(-1.0/(n-1.0))
    x2=(1.0-np.square(x))**((2.0*n)/(n-1.0))

    return (np.exp(-kn*(s**(1.0/n))*x1)/np.sqrt(1.0-x2))*x


def curv_exp(p, x, cml=1.0):
    '''
    The circular speed of the exponential disk (Freeman 1970).
    Binney & Treamine (2008) eq. 2.165 pag. 101.

    Parameters
    ----------
    p[0]=central surface brigthness
    p[1]=scale length
    p[2]=M/L ratio to the disk
    return square velocity (km/sec)^2
    '''
    # When there is a valeu for M/L
    try:
        cml=p[2]
    except:
        nothing=0.0

    r = x/(2*p[1])

    k0=sp.k0(r)
    k1=sp.k1(r)

    # Avoiding singularity at r = 0
    np.put(k0, np.where(k0==np.inf)[0],0) ; np.put(k1, np.where(k1==np.inf)[0],0)

    bessel  = sp.i0(r)*k0
    bessel1 = sp.i1(r)*k1


    return (((const*p[0]*p[1]*cml)*(r**2))*(bessel-bessel1))/np.square(1000.0)

def bulge_curv_exp(p,x):
    '''
    The circular speed of the exponential disk (Freeman 1970) plus sersic bulge
    (Simonneau & Prada 2004).

    Parameters
    -----------
    p[0]=central surface brigthness
    p[1]=scale length
    p[2]=M/L ratio to the disk
    p[3]=Central Intensity Io
    p[4]=Effective radius, the radius of the isophote that encloses onte the
         half of the total luminosity
    p[5]=n
    p[6]=M/L ratio

    Return
    -------
    Square velocity (km/sec)^2
    '''

    disp = [p[0],p[1],p[2]]
    bulp = [p[3],p[4],p[5],p[6]]

    if p[6] >= 0.0 :
      if p[5] >= 1.0:
       bulge = mass_sersic_gauss(bulp,x)[0]
      else:
       bulge = mass_sersic(bulp,x)[0]
    else :
       bulge = np.zeros(len(x))

    if p[2] >= 0.0 :
       disc = curv_exp(disp,x)
    else :
       disc = np.zeros(len(x))

    return disc + bulge


def jaffe(p,x):
    """
    Circular velocity for Jaffe density profile (Jaffe 1983).
    we obtained of the eq. 2.64 pag. 70 Binney & Tremaine (2008)
    To determine the circular velocity, we used : V^2=(G*M(R))/R.

    Parameters
    ----------
    p[0] is the density inicial
    p[1] is a core radius

    Return
    ------
    Square velocity in (km/sec)^2, and Mass in solar mass
    """
    pho = p[0]
    a   = p[1]
    M = 4.*np.pi*pho*np.square(a)*(x/np.sqrt(1.0+(x/a)))

    return ((g*M)/x)/np.square(1000.0), M/masssun

def hernquist(p,x):
    """
    Circular velocity for Hernquist density profile (Herquist 1990).
    we obtained of the eq. 2.66 pag. 71 Binney & Tremaine (2008)
    To determine the circular velocity, we used : V^2=(G*M(R))/R.

    Parameters
    ----------
    p[0] is the density initial
    p[1] is a core radius

    Return
    ------
    Square velocity in (km/sec)^2, and Mass in solar mass
    """
    a=p[1]
    M=4.*np.pi*p[0]*(a**3)*(np.square(x/a)/(2*np.square(1.0+x/a)))
    return ((g*M)/x)/ np.square(1000.0), M/masssun

def halohernq(p,x):
    """
    The acumulative mass profile M for the halo in Hernquist 1993
    eq. 2.4
    To determine the circular velocity we used : V^2=(G*M(R))/R
    p[0] is the halo mass
    p[1] is the core radius
    p[2] is the cutoff radius
    """
    r  = x
    M  = abs(p[0])  # M is the halo mass
    a  = p[1]       # gamma is a core radius
    rc = p[2]       # rc is a cutoff radius
    q  = a/rc
    alfa = 1.0/( 1.0 - np.sqrt(np.pi)*q*np.exp(np.square(q))*(1.0-erf(q)) )

    # integral of the e.q.2,4
    mass = []
    for rad in r :
     intg = si.quad(lambda z:(np.square(z)*np.exp(-np.square(z)))/(np.square(z)+np.square(q)),
                              0,rad/rc)
     mass = append(mass,2*M*alfa*intg[0]/np.sqrt(np.pi))

    return g*mass/(x*np.square(1000)), mass/masssun

def bulgehernq(p,x):
    """
    Circular Velocity for Hernquist  bulge profile from Hernquist 1990
    was taken from eq. 10.
    The cumulative mass distributions was taken from
    eq. 3. See also hernq functions, for surface bright profile.
    p[0] is total mass
    p[1] is a scale length
    return the velocity in (km/sec)^2, and Mass in solar mass
    """

    a = p[1]; M = p[0]
    r=x
    masscum = (M*(np.square(r)/np.square(r+a)))/masssun
    V2 = ( (g*M/(12.*a))*( (12*r*(r+a)**3/a**4)*np.log((r+a)/r) -
           (r/(r+a))*(25. + 52.*r/a + 42.*np.square(r/a) + 12.*(r/a)**3) ) )
    return V2/np.square(1000.0), masscum


def nfw(p,x):
    """
    Mass for Navarro density profile (Navarro, Frenk & White 1995).
    we obtained of the eq. 2.66 pag. 71 Binney & Tremaine (2008).
    To determine the circular velocity, we used : V^2=(G*M(R))/R
    p[0] is the central density
    p[1] is a core radius
    return the velocity in (km/sec)^2, and Mass in solar mass
    """
    Pho = p[0]
    a   = p[1]
    r   = np.copy(x)

    M = 4*np.pi*Pho*(a**3)*( np.log(1.0+(r/a)) - (r/a)/(1.0+(r/a)) )

    # Avoiding the singularity at r=0
    sing = np.where(x==0.0)[0]
    np.put(r, sing, 1e-20)
    out1 = ((g*M)/r)/np.square(1000.0);
    np.put(out1, sing, 0.0)

    return out1, M/masssun

def nfwm200(p,x,h=73.):
    """
    Mass for Navarro density profile (Navarro, Frenk & White 1995).
    Using as input the parameters c and M_200.
    To determine the circular velocity, we used : V^2=(G*M(R))/R
    p[0] = c, concentration parameter
    p[1] = m_200, its the halo mass, the radius r_200 at which the mean
           density is 200 times the cosmological critical density, pho_0.
    p[2] = h, hubble constant.
    return the velocity in (km/sec)^2, and Mass in solar mass
    """

    # Hubble constant km/sec/Mpc
    try:
       h = p[2]
    except:
      nothing=0.0

    # Hubble constant in sec
    H=(h*1e3)/((1e6)*pc)
    # Critical density in kg/m^3
    pho_0=(3./(8.*np.pi))*(np.square(H)/g)

    # Definition of M_200 and R_200
    #m_200=(10**(p[1]))*1e12*masssun  # kg
    m_200 = p[1]   # kg
    r_200 = ((m_200)*(3./4.)*(1./np.pi)*(1./200.)*(1./pho_0))**(1./3) # m
    # Characteristic overdensity  in kg/m^3
    c = (p[0])
    pho_c = ( (200./3.)*(c**3)*pho_0 )/(np.log(1.+c)-c/(1.+c))
    # Core radius in m
    r_c = r_200/c

    M = 4*np.pi*pho_c*(r_c**3)*( np.log(1.0+(x/r_c)) - (x/r_c)/(1.0+(x/r_c)) )

    out1 = ((g*M)/x)/np.square(1000.0); out2 = M/masssun
    # Avoiding singularity at r = 0
    np.put(out1, np.where(x==0)[0],0) ; np.put(out2, np.where(x==0)[0],0)

    return out1, out2

def iso(p,x):
    """
    Circular velocity for an isothermal sphere  (Kravtsove etal. 1998).
    we obtained of the eq. 5 pag. 15 Fuentes-Carrera (2004), they inspered in
    the work of Blais-Ouellette et al. 2001.
    To determine the circular velocity, we used : V^2=(G*M(R))/R
    p[0] is the central density
    p[1] is a core radius
    return the velocity in (km/sec)^2, and Mass in solar mass
    """
    pho = p[0]
    a   = p[1]
    M = 4*np.pi*pho*(a**3)*(np.log( (x/a) + np.sqrt(np.square(x/a) + 1.0) )
                         - (x/a)/np.sqrt( np.square(x/a) + 1.0 ) )

    return ( (g*M)/x )/np.square(1000.0), M/masssun

def pseudoiso(p,x):
    """
    Circular velocity for an isothermal sphere  (Begeman 1987).
    we obtained of the eq. 5 pag. 15 Fuentes-Carrera (2004), they inspered in
    the work of Blais-Ouellette et al. 2001.
    To determine the circular velocity, we used : V^2=(G*M(R))/R
    p[0] is the central density
    p[1] is a core radius
    return the velocity in (km/sec)^2, and Mass in solar mass
    """
    pho = p[0]
    a   = p[1]
    M   = 4*np.pi*pho*(a**3)*(x/a-arctan(x/a))
    return ((g*M)/x)/np.square(1000.0), M/masssun

def curv_exp_jaffe(p,x):

    return bulge_curv_exp(p[0:7],x) + jaffe(p[7::],x)[0]

def curv_exp_hernquist(p,x):

    return bulge_curv_exp(p[0:7],x) + hernquist(p[7::],x)[0]

def curv_exp_bulgehernq(p,x):

    return bulge_curv_exp(p[0:7],x) + bulgehernq(p[7::],x)[0]

def curv_exp_halohernq(p,x):

    return bulge_curv_exp(p[0:7],x) + halohernq(p[7::],x)[0]

def curv_exp_nfw(p,x):

    return bulge_curv_exp(p[0:7],x) + nfw(p[7::],x)[0]

def curv_exp_nfwm200(p,x):

    return bulge_curv_exp(p[0:7],x) + nfwm200(p[7::],x)[0]

def curv_exp_iso(p,x):

    return bulge_curv_exp(p[0:7],x) + iso(p[7::],x)[0]

def curv_exp_pseudoiso(p,x):

    return bulge_curv_exp(p[0:7],x) + pseudoiso(p[7::],x)[0]


def mass_disk_tot(p,cml=1.0):
    """
    The total mass of the exponential disc is taken from Eq. 11 of
    Freeman (1970).

    Parameters
    ----------
    p[0] = Central Intensity
    p[1] = scale radius
    p[2] = M/L ratio

    Return
    ------
    The total mass in solar units
    """
    try:
        cml = p[2]
    except:
       nothing = 0.0

    return (2*np.pi*p[0]*np.square(p[1])*cml)/masssun

def mass_disk_accum(p,x,cml=1.0):
    """
    The accumulative mass for an exponetial disc is taken from
    the equation 2.166 of Binney & Tremaine (2008) pag.101

    Parameters
    ----------
    p[0] = Central Intensity
    p[1] = scale radius
    p[2] = M/L ratio

    Return
    ------
    The accumulative mass
    """
    try:
        cml = p[2]
    except:
       nothing = 0.0
    pho = p[0]
    rd  = p[1]

    return (2*np.pi*pho*np.square(rd)*cml*(1.-np.exp(-(x/rd))*(1.+x/rd)))/masssun

def mass_sersic_tot(p,cml=1.0):
    """
    The used expression for the total mass for a sersic profile is the
    equation (3) from simonneaou & prada (2004).
    p[0] = Central Intensity Io
    p[1] = Effective radius, the radius of the isophote that encloses onte the
           half of the total luminosity
    p[2] = n
    p[3] = M/L ratio
    """
    try:
        cml = p[3]
    except:
       nothing = 0.0
    #kn = 2.0*p[2]-0.324
    kn = gammaincinv(2*p[2],0.5)
    n2 = 2*p[2]
    return (p[0]*np.square(p[1])*np.pi*(n2/(kn**n2))*gamma(n2)*cml)/masssun

def vaucou_eval(s, lim_sup):

    ret_int=si.quad(lambda x: vaucou(s,x), s, lim_sup)
    return ret_int[0], ret_int[1]

def vaucou_gauss_eval(s):
    ret_int = si.fixed_quad(lambda x: vaucou_gauss(s,x), 0.0, 1.0)
    return  ret_int


def int_mass(r, r_0, f_pho, step=100):

    x = np.linspace(r_0, r, step)

    return si.simps(np.square(x)*f_pho(x), x)*4.*np.pi



def mass_sersic_new(p, x, cml=1.0, step=100):
    """
    integrator to density profile of the sersic law
    this integral was taked from Simonneau & Prada 2004 equation (5)
    it is applied for n>= 0
    we have performed the integration by means of quadrature integration.

    Parameters
    ----------
    p[0]=Central Intensity Io
    p[1]=Effective radius, the radius of the isophote that encloses onte the
         half of the total luminosity
    p[2]=n
    p[3]=M/L ratio

    Return
    ------
    return the square velocity (km/sec)^2, the Mass in solar units
    """
    global kn, n

    try:
        cml = p[3]
    except:
        nothing = 0.0

    Io = p[0]
    Re = p[1]
    n  = p[2]

    #kn = 2.0*p[2]-0.324
    kn = gammaincinv(2*p[2],0.5)

    v_vaocou = np.vectorize(vaucou_eval)
    #print (v_vaocou(rad))
    temp=v_vaocou(x/Re, np.inf)
    pho_rad  = ((kn*Io)/(np.pi*n*Re))*temp[0]
    pho_rad_err = temp[1]

    v_int_mass = np.vectorize(int_mass)
    f_b_n = interp1d(x, pho_rad)

    f_mass_acc = cml*v_int_mass(x, x[0], f_b_n, step)*np.square(pc)  # kg

    vel_sq = ((g*f_mass_acc)/(x*pc))*1e-6   # km/s

    f_mass_acc = f_mass_acc/masssun  # M_sun

    if x[0] == 0:
        vel_sq[0] = 0
        f_mass_acc[0] = 0
        pho_rad[0] = 0
        pho_rad_err[0] = 0

    return vel_sq, f_mass_acc, pho_rad, pho_rad_err


def mass_sersic_gauss_new(p, x, cml=1.0, step=100):

    try:
        cml=p[3]
    except:
        nothing=0.0

    global kn, n
    Io = p[0]
    Re = p[1]     # pc
    n  = p[2]
    #kn = 2.0*p[2]-0.324
    kn = gammaincinv(2*p[2],0.5)
    # x in pc

    v_vaocou = np.vectorize(vaucou_gauss_eval)
    temp = v_vaocou(x/Re)
    pho_rad = ((kn*Io*2.0*(x/Re)**((1.0/n)-1.0))/(np.pi*Re*(n-1.0)))*temp[0]

    if x[0] == 0:
        pho_rad[0] = 0

    v_int_mass = np.vectorize(int_mass)
    f_b_n = interp1d(x, pho_rad)

    f_mass_acc = cml*v_int_mass(x, x[0], f_b_n, step)*np.square(pc)  # kg

    vel_sq = ((g*f_mass_acc)/(x*pc))*1e-6   # km/s

    f_mass_acc = f_mass_acc/masssun  # M_sun

    if x[0] == 0:
        vel_sq[0] = 0
        f_mass_acc[0] = 0

    return vel_sq, f_mass_acc, pho_rad


def mass_sersic(p, x, cml=1.0, step=1000, step2=32):
    """
    integrator to density profile of the sersic law
    this integral was taked from Simonneau & Prada 2004 equation (5)
    it is applied for n>= 0
    we have performed the integration by means of quadrature integration.

    Parameters
    ----------
    p[0]=Central Intensity Io
    p[1]=Effective radius, the radius of the isophote that encloses onte the
         half of the total luminosity
    p[2]=n
    p[3]=M/L ratio

    Return
    ------
    return the square velocity (km/sec)^2, the Mass in solar units
    """
    global kn, n

    try:
        cml = p[3]
    except:
        nothing = 0.0

    Io = p[0]
    Re = p[1]
    n  = p[2]

    kn = 2.0*p[2]-0.324
    #kn = gammaincinv(2*p[2],0.5)

    # Avoiding singularity at r = 0
    if x[0]==0:
        x=x[1::]
        orig=np.array([0])
    else:
        orig=np.array([])

    mass_tot=array([])

    for el in range(len(x)):
        if el==0:
            #print x[el]
            rad0 = linspace(1.0, x[el], step)
            rad0 = rad0/Re
            mass_rad0 = array([])

            for s in rad0:
                # Density Integral
                val = si.quad(lambda x: vaucou(s,x), s, np.inf)
                # pho(R) = factor* Density integral
                pho_rad  = ((kn*Io)/(np.pi*n*Re))*val[0]
                # Integrand of the mass integral R^2*pho(R)
                mass_rad0 = append(mass_rad0,np.square(s*Re)*pho_rad)

            # Mass(R) = 4*np.pi*int(R^2*pho(R))
            mass_tot = append(mass_tot,si.simps(mass_rad0,rad0*Re)*4.*np.pi)
        else:
            delta = (x[el] - x[el-1])/step2
            rad   = linspace(x[el-1] + delta, x[el], step2)
            rad   = rad/Re
            mass_rad = array([])

            for s in rad :
                # Density Integral
                val = si.quad(lambda x: vaucou(s,x), s, np.inf)
                # pho(R) = factor*integral density
                pho_rad  = ((kn*Io)/(np.pi*n*Re))*val[0]
                # Integrand of the mass integral R^2*pho(R)
                mass_rad = append(mass_rad,np.square(s*Re)*pho_rad)

#            v_vaocou = np.vectorize(vaucou_eval)
#            #print (v_vaocou(rad))
#            pho_rad  = ((kn*Io)/(np.pi*n*Re))*v_vaocou(rad)[0]
#            #    # Integrand of the mass integral R^2*pho(R)
#            mass_rad = append(mass_rad,np.square(s*Re)*pho_rad)

            mass_rad0 = concatenate((mass_rad0[0:-1], mass_rad))
            rad0 = concatenate((rad0[0:-1], rad))
            # Mass(R) = 4*np.pi*int(R^2*pho(R))
            mass_tot = append(mass_tot, si.simps(mass_rad0, rad0*Re)*4*np.pi)

    mass_tot = np.array([mass_tot])
    x = np.array([x])

    mass_tot =   mass_tot.ravel()
    x = x.ravel()

    #vel_sq = concatenate((orig, g*mass_tot*cml/(x*np.square(1000))))
    #Mt     = concatenate((orig, (mass_tot*cml)/masssun))

    vel_sq = np.array(g*mass_tot*cml)/np.array(x*np.square(1000))
    Mt  = np.array(mass_tot*cml)/masssun

    if orig.size != 0:
        vel_sq = concatenate((orig, vel_sq))
        Mt     = concatenate((orig, Mt))

    return vel_sq, Mt

def mass_sersic_gauss(p, x, cml=1.0, step=1000, step2=32):
    """
    integrator to density profile of the sersic law
    this integral was taked from Simonneau & Prada 2004 equation (9)
    it just apply for n>= 1
    we have performed the integration by means of a Gaussian numerical
    integration.
    The order of the approximation is N=5. For the case with N=5 the
    difference between p(s)_n=5 and p(s)+n=40 is always less than 1%

    Parameters
    ----------
    p[0]=Central Intensity Io
    p[1]=Effective radius, the radius of the isophote that encloses onte the
         half of the total luminosity
    p[2]=n
    p[3]=M/L ratio

    Return
    ------
    the square velocity (km/sec)^2, the Mass in solar units
    """

    # when is given the contant of mass-to-luminosity  ratio (cml)
    try:
        cml=p[3]
    except:
        nothing=0.0

    global kn, n
    Io = p[0]
    Re = p[1]
    n  = p[2]
    kn = 2.0*p[2]-0.324
    #kn = gammaincinv(2*p[2],0.5)

    mass_tot=array([])

    # Avoiding singularity at r = 0
    if x[0]==0 :
        x=x[1::]
        orig=([0])
    else :
        orig=([])

    for el in range(len(x)):

      if el==0:
          #print x[el]
          rad0 = linspace(1.0,x[el],step)
          # new the varible R/Re
          rad0 = rad0/Re
          # mass inside radius
          mass_rad0 = array([])

          for s in nditer(rad0) :
              # integral density
              val = si.fixed_quad(lambda x: vaucou_gauss(s,x), 0.0, 1.0)
              # pho(R) = factor*integral density
              pho_rad = ((kn*Io*2.0*s**((1.0/n)-1.0))/(np.pi*Re*(n-1.0)))*val[0]
              # term to mass integral R^2*pho(R)
              mass_rad0 = append(mass_rad0,np.square(s*Re)*pho_rad)
          # Mass(R) = 4*np.pi*int(R^2*pho(R)
          mass_tot = append(mass_tot, si.simps(mass_rad0,rad0*Re)*4.*np.pi)

      else:
          delta    = (x[el] - x[el-1])/step2
          rad      = linspace(x[el-1]+delta, x[el], step2)
          # new the varible R/Re
          rad      = rad/Re
          # mass inside radius
          mass_rad = array([])

          for s in nditer(rad) :
               # integral density
               val      = si.fixed_quad(lambda x: vaucou_gauss(s,x), 0.0, 1.0)
               # pho(R) = factor*integral density
               pho_rad  = ((kn*Io*2.0*s**((1.0/n)-1.0))/(np.pi*Re*(n-1.0)))*val[0]
               # term to mass integral R^2*pho(R)
               mass_rad = append(mass_rad,np.square(s*Re)*pho_rad)

          mass_rad0=concatenate((mass_rad0[0:-1],mass_rad))
          rad0=concatenate((rad0[0:-1],rad))
          # Mass(R) = 4*np.pi*int[R^2*pho(R)]
          mass_tot=append(mass_tot,si.simps(mass_rad0,rad0*Re)*4.*np.pi)


    vel_sq = concatenate((orig,g*mass_tot*cml/(x*np.square(1000))))
    Mt     = concatenate((orig,(mass_tot*cml)/masssun))

    return vel_sq, Mt

def nohalo(p,x,phi) :

    return np.zeros(len(x)), np.zeros(len(x))


apa=([25.000000,25.000000,25.000000,25.000000,25.000000,
25.000000,25.000001,25.000001,25.000001,24.999999,
25.000000,25.000000,0.000000 ,204.99999,204.99999,
204.99999,204.99999,204.99999,204.99999,204.99999,
205.00000,205.00000,205.00000,205.00000,205.00000,
205.00000])

#def bertola(p,x,pa=deg2rad(apa)):
def bertola(xv, p):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''
    x=xv[:,0]; pa=xv[:,1]
    A = p[0];  c = p[1];  pind = p[2]; i = p[3]; nod = p[4]
    vsys  = p[5]; rsys = p[6]
    phi   = pa-nod;  r = x-rsys
    print (np.square(c)*np.square(cos(i)), i)
    denom = ( np.square(r)*(np.square(np.sin(phi)) + np.square(np.cos(i))*np.square(np.cos(phi)))
                  + np.square(c)*np.square(np.cos(i)) )**(pind*0.5)
    return vsys + ( ( A*r*np.cos(phi)*np.sin(i)*(np.cos(i)**pind) )/denom )




def bertolaori(r,p):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''
    A = p[0] ;  c = p[1] ;  pind = p[2]
    return (A*r) / ( (np.square(r)+np.square(c))**(pind*0.5) )


def bertolacube_old(cubexy_obs, A, c, pind, vsys, cx, cy, nodpa, i=-42):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''
    # Pa and i
    nod = np.deg2rad(nodpa); i = np.deg2rad(i)

    cubexy_mod = np.copy(cubexy_obs)

    for xy, velxy in np.ndenumerate(cubexy_obs):
        if ~np.isnan(velxy):
            x = (xy[1] + 1) - cx
            y = (xy[0] + 1) - cy
            r = np.hypot(y, x)
            pa = np.arctan2(y, x)
            if pa<0.0:
                pa += 2*np.pi
            phi = pa-nod
            denom = ( np.square(r)*(np.square(np.sin(phi)) +
                      np.square(np.cos(i))*np.square(np.cos(phi))) +
                      np.square(c)*np.square(np.cos(i)) )**(pind*0.5)
            cubexy_mod[xy] = (vsys +
                              ((A*r*np.cos(phi)*np.sin(i)*(np.cos(i)**pind))/denom) )
        else:
            cubexy_mod[xy] = nan

    return cubexy_mod

def bertolacube(cubexy_obs, A, c, pind, vsys, cx, cy, nodpa, i=-42, psf=0):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''
    # Pa and i
    nod = np.deg2rad(nodpa)
    i = np.deg2rad(i)

    cubexy_mod = np.copy(cubexy_obs)

    nx, ny = (cubexy_obs.shape[1], cubexy_obs.shape[0])
    x = np.arange(nx)
    y = np.arange(ny)
    xv, yv = np.meshgrid(x, y)

    x = xv+1 - cx
    y = yv+1 - cy

    r = np.hypot(y, x)
    pa = np.arctan2(y, x)
    pa[pa<0.0]+= 2*np.pi
    phi = pa-nod

    denom = ( np.square(r)*(np.square(np.sin(phi)) +
              np.square(np.cos(i))*np.square(np.cos(phi))) +
              np.square(c)*np.square(np.cos(i)) )**(pind*0.5)
    cubexy_mod = (vsys +
                      ((A*r*np.cos(phi)*np.sin(i)*(np.cos(i)**pind))/denom) )

    if isinstance(psf, (list, tuple, np.ndarray)):
        cubexy_mod = sc.signal.fftconvolve(cubexy_mod, psf, mode='same')

    cubexy_mod[np.isnan(cubexy_obs)] = np.nan

    return cubexy_mod


def bertolaxy(coord,A,c,pind,vsys,cx,cy,nodpa):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''

    # Pa and i for AM2058
    #nod=deg2rad(356);i=deg2rad(-58)
    #nod=deg2rad(nodpa);i=deg2rad(-58)

    # Pa and i for AM1228
    #nod=deg2rad(64);i=deg2rad(-64)
    #nod=deg2rad(4);i=deg2rad(-64)
    #nod=deg2rad(nodpa);i=deg2rad(-64)

    # Pa and i for AM2306
    #nod=deg2rad(nodpa); i=deg2rad(-57.3)
    ##nod=deg2rad(245.6);i=deg2rad(-57.3)

    # Pa and i for NGC4656
    nod=np.deg2rad(nodpa); i=np.deg2rad(82)



    # cx = p[4]
    # cy = p[5]

    #x=coord[0]-cx; y=coord[1]-cy
    x=coord[:,0]-cx; y=coord[:,1]-cy
    print("hola")


    r=np.hypot(y,x)
    pa=np.arctan2(y,x)
    for j in range(len(pa)) :
      if pa[j] < 0.0 : pa[j]+=2*np.pi

#    A = p[0] ;  c = p[1] ;  pind = p[2] ; i = p[3] ; nod = p[4]
#    vsys  = p[5] ; rsys = p[6]

#    A = p[0] ;  c = p[1] ;  pind = p[2] ;  vsys  = p[3]
#    print r

    phi   = pa-nod ; #r = x-rsys
    denom = ( np.square(r)*( np.square(np.sin(phi)) + np.square(np.cos(i))*np.square(np.cos(phi)) )
              + np.square(c)*np.square(np.cos(i)) )**(pind*0.5)
    return vsys + ( ( A*r*np.cos(phi)*np.sin(i)*(np.cos(i)**pind) )/denom )


def radialcube(cubexy_obs, rdal, vsys, cx, cy, nodpa, i=-42, psf=0):
    '''
    Equation 2. (pag. 8) from Bertola et al. (1991)
    A = p[0] ,  c = p[1] ,  pind = p[2] ,  i = p[3]
    nod = p[4] , vsys = p[5] ,  rsys = p[6]

    This rotation curves rises linearly in the center, and is proportional to
    r^(1-p) at larger r. For p=1 the rotation curve is asymptotically flat,
    while p = 3/2, the system has a finite total mass. Hence, for applications
    to galaxies, we espect 1 <= p <= 3/2.

    Return a array with the velocity (km/sec)
    '''
    # Pa and i
    nod = deg2rad(nodpa); i = deg2rad(i)

    cubexy_mod = copy(cubexy_obs)

    nx, ny = (cubexy_obs.shape[1], cubexy_obs.shape[0])
    x = np.arange(nx)
    y = np.arange(ny)
    xv, yv = np.meshgrid(x, y)

    x = xv+1 - cx
    y = yv+1 - cy

    r = np.hypot(y, x)
    pa = np.arctan2(y, x)
    pa[pa<0.0]+= 2*np.pi
    phi = pa-nod

    denom = np.sqrt(1.0 - np.square(np.sin(i))*np.square(np.cos(phi)))
    cubexy_mod = vsys + ((rdal*np.sin(phi)*np.sin(i))/denom)

    if isinstance(psf, (list, tuple, np.ndarray)):
        cubexy_mod = sc.signal.fftconvolve(cubexy_mod, psf, mode='same')

    cubexy_mod[np.isnan(cubexy_obs)] = np.nan

    return cubexy_mod


def chi2(theta):

    A, c, pind, vsys, cx, cy, nodpa, i = theta
    model = bertolacube(yobs, A, c, pind, vsys, cx, cy, nodpa, i)

    inv_sigma2 = 1.0/np.square(yerrp)
    return np.sum(np.square(yobs-model)*(inv_sigma2))

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

def gr2BV(g,r):
    V = r + 0.466*(g - r) - 0.003 # value calculate of 13.92
    B = V + 0.952*(g - r) + 0.219 # value calculate of 15.13
    R = V - 1.190*(V - r) - 0.155

    # Sloan transformations
    #http://www.sdss.org/dr7/algorithms/sdssUBVRITransform.html
    ## search objects http://skyserver.sdss3.org/dr9/en/tools/explore/obj.asp

    # Lupton (2005)
    # B2 = g + 0.3130*(g - r) + 0.2271 # value calculate of 15.04
    # V2 = g - 0.5784*(g - r) - 0.0038 # value calculate of 13.87
    R2 = r - 0.1837*(g - r) - 0.0971

    # Jester et al. (2005)   All stars with Rc-Ic < 1.15
    # B2 = g + 0.39*(g-r) + 0.21  # value calculate of 15.09
    # V2 = g - 0.59*(g-r) - 0.01  # value calculate of 13.85

    # Quasars at z <= 2.1 (synthetic)
    V2 =  g - 0.52*(g-r) - 0.03
    B2 = V2+0.62*(g-r) + 0.15
    BV = 0.62*(g-r) + 0.15

    # in these equation there was a mistake of the calculate
    # V = r + 0.426*(g - r) - 0.012
    # B = V + 0.870*(g - r) + 0.200

    # V = r + 0.466*(g - r) - 0.217
    # B = V + 0.952*(g - r) - 0.219

    print ("Fukugita (1996) and sloan ")
    print ("mag B  V  R  B2 V2 R2 B-V")
    return B, V,  R , B2, V2, R2, BV

def distance(m, r, scpix, dmp, aband, av=0.0, printmag='none',
             printfile='none', configfile='none', name_var=['I0', 'Rs'],
             inc_gal=0):
    '''
    Return a file with parameters convert to units solar_mass/pc^2 (Io) and pc
    (scale radius) This functions can also return the Absolute magnitude (M)
    and Luminosity in sun units.

    Parameters
    ----------
    m :  mag/arcsec^2
    r :  scale radius or Re (arcsec). When calculating Mabs setting as 1
    scpc  : scale pix/arcsec. When calculating Mabs setting as 1
    dmp   : distance (Mpc)
    aband : Analsys band ['u','g','ri','z','U','B','V','R','I','J','H','K']
    av    : user Extinction
    printmag  : print Absolute magnitude and Luminosity
    printfile : print a file with the parameter converted to sunmass/pc^2
                and pc

    Magnitudes Absolutes for each band can be found in these links:
    http://www.ucolick.org/~cnaw/sun.html
    http://mips.as.arizona.edu/~cnaw/sun.html
    '''

#    band = { 'u':6.80, 'g':5.45, 'r':4.76, 'i':4.58,'z':4.51,
#             'U':5.61, 'B':5.48, 'V':4.83, 'R':4.42,'I':4.08,
#             'J':3.64, 'H':3.32, 'K':3.28 }

    # http://mips.as.arizona.edu/~cnaw/sun.html
    # update sloan magnitudes AB system
    band = { 'u':6.39, 'g':5.11, 'r':4.65, 'i':4.53,'z':4.50,
             'U':5.61, 'B':5.48, 'V':4.83, 'R':4.42,'I':4.08,
             'J':3.64, 'H':3.3, 'K':3.28 }


     #'H':3.32



    # calculate arcsec/pc
    scpc=(dmp*1e6)*np.tan(np.deg2rad(1.0/3600.0))
    print (scpc, dmp)

    # calculate of the absulute magnitud m-M=5logd -5 + Ak;
    # d is the distance in parsec;
    # Ak is the value for the Galactic Extinction in the k-band (0.01)

    #corr = 2.5*log10(np.square(scpix))
    corr = 0
    if av == 0.0:
        M = -5.0*log10(dmp*1e6) + 5.0 + m + corr
    else:
        M = -5.0*log10(dmp*1e6) + 5.0 + m + corr -av

    # calculate in Sun's Fflux =>  m_(sun)-M=2.5*np.log(F/F_(sun) ; m_(sun) is the
    # absulute magnitud in ?-band
    # (from Binney and Merrifield 1998, Galactic Astronomy, Table 2.1)

    # Flux in solar luminosity
    fluxsun=10**((1.0/2.5)*(band[aband]-M));
    # Solar luminosity  pc^-2
    cor_inc = np.cos(np.deg2rad(inc_gal))**-1
    surf_fluxsun=fluxsun/(cor_inc*np.square(scpc*scpix))

    if printmag != 'none':
     print ("Mag Absolute : ", M)
     print ("Luminosity in sun unit:%1.2e"%fluxsun  )

    # Calculate in solar mass
    masstot = fluxsun*masssun                               # mass kg arcsec^-2
    masstot_pc = masstot/(cor_inc*np.square(scpc*scpix))    # mass kg pc^-2
    masstot_m  = masstot/(cor_inc*np.square(scpc*scpix*pc)) # mass kg m^-2

    if printfile != 'none':
        rs = r[0]
        rs_pc = rs*scpc
        rs_pc_err = r[1]*scpc
        fileo = open(printfile,'a')
        fileo.write(('%s = %g   mag/arcsec^2  | Io = %g ' +
                    'solar_mass/pc^2 \n')%(name_var[0], m, surf_fluxsun))
        fileo.write(('%s = %g   arcsec        | Rs = %g +/-  ' +
                    '%g pc\n')%(name_var[1],rs, rs_pc,rs_pc_err))
        fileo.write('Scale of anaysis : %g  arcsec/pc\n'%(scpc))

    fopen = open('in_kine_parphot.ini', 'a')
    fopen.write('\n{} = {}\n'.format(name_var[0], surf_fluxsun))
    fopen.write('{} = {}'.format(name_var[1], rs_pc))
    fopen.close()

    #if configfile != 'none':
    #    config_parphot = configparser.ConfigParser()
    #    config_parphot['DEFAULT'] = {'Io' : surf_fluxsun,
    #    name_var[0]:rs_pc,
    #    'Io_mag' : m,
    #    }
    #
    #    with open('in_kine_parphot.ini', 'a') as configfile:
    #        config_parphot.write(configfile)

    return M, fluxsun, masstot, masstot_pc, masstot_m

def lum2mag(fluxsun,dmp,aband,av=0.0):

    band = { 'u':[6.80,0.0], 'g':[5.45,0.0], 'r':[4.76,0.0], 'i':[4.58,0.0],
             'z':[4.51,0.0], 'U':[5.61,1.6],'B':[5.48,1.33],'V':[4.83,1.00],
             'R':[4.42,0.64],'I':[4.08,0.42],'J':[3.64,0.24],'H':[3.32,0.18],
             'K':[3.28,0.090] }

    #calculate arcsec/pc
    scpc=(dmp*1e6)*tan(deg2rad(1.0/3600.0))


    M = band[aband][0]-2.5*log10(fluxsun)     # Magnitude absolute


    if av == 0.0 : m = 5.0*log10(dmp*1e6) - 5.0 + M
    else         : m = 5.0*log10(dmp*1e6) - 5.0 + M - av

    print ("Mag apparente : ", m)
    print ("Mag Absolute  : ", M)

def flux(fluxt,sky=0.0,texp=1.0,scpix=1.0,zp=0.0):
    """
    Return magnitude in arcsec square

    Parameters
    ----------

    fluxt : flux in UDI units
    sky   : sky value in units
    texp  : exposition time
    scpix : scale the pixels in arcsec
    zp    : constant of calibration
    """

    return -2.5*log10((fluxt-sky)/(texp*(scpix**2)))+zp

def intens(magt,sky=0.0,texp=1.0,scpix=1.0,zp=0.0):
    """
    Return intens in du units

    Parameters
    ----------

    magt  : mag in arcsec square
    sky   : sky value in units
    texp  : exposition time
    scpix : scale the pixels in arcsec
    zp    : constant of calibration
    """

    return (10**((magt-zp)/-2.5))*(texp*(scpix**2))+sky

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
    functask = {'sersic': odr.Model(sersic), 'herqn': odr.Model(hernq),
                'bhubble': odr.Model(bhubble),
                'sersicg': odr.Model(sersicgauss),
                'vauco': odr.Model(vauco), 'disk': odr.Model(disk),
                'lens': odr.Model(lens), 'sersiclens': odr.Model(sersiclens),
                'sersicbar': odr.Model(sersicbar),
                'sersicbr': odr.Model(sersicbr),
                'hernquist': odr.Model(curv_exp_hernquist),
                'bulgehernq': odr.Model(curv_exp_bulgehernq),
                'halohernq': odr.Model(curv_exp_halohernq),
                'jaffe': odr.Model(curv_exp_jaffe),
                'nfw': odr.Model(curv_exp_nfw),
                'nfwm200': odr.Model(curv_exp_nfwm200),
                'iso': odr.Model(curv_exp_iso),
                'pseudoiso': odr.Model(curv_exp_pseudoiso),
                'bulgedisk': odr.Model(bulge_curv_exp),
                'gauss': odr.Model(gauss),
                'barellip': odr.Model(barellip), 'barflat': odr.Model(barflat),
                'barsersic': odr.Model(barsersic),
                'ring': odr.Model(ring),
                'barring': odr.Model(barring), 'bertola': odr.Model(bertola),
                'multiline': odr.Model(multi),
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

def sersic(p,x):
    """
    The Sersic profile (Eq. (1), Simonneau & prada 2004) is given by
    """
    I_serc = p[0]
    r_serc = p[1]
    n      = p[2]

    bn=2.0*n-0.324

    return I_serc*np.exp(-bn*( (x/r_serc)**(1/n) ))


def sersicf(x,I_serc, r_serc, n):
    """
    The Sersic profile (Eq. (1), Simonneau & prada 2004) is given by
    """

    bn=2.0*n-0.324

    return I_serc*np.exp(-bn*( (x/r_serc)**(1/n) ))





def sersict(p):
    """
    The luminosity for Sersic Profile is given by
    (Simonneau & prada 2004, eq. (2))
    """
    I_serc = p[0]
    r_serc = p[1]
    n      = p[2]

    bn=2.0*n-0.324

    return I_serc*np.square(r_serc)*np.pi*( (2*n)/(bn**(2*n)) )*math.gamma(2*n)

def sersiccaon(p,x):
    """
    Equation from caon, capaccioli, d'onofrio 1991
    """
    # equa. 3
    bn=0.868*p[2]-0.142
    # equa. 6
    return p[0]*10**(-bn*( (x/p[1])**(1/p[2]) -1 ))

def vauco(p,x):

    return p[0]*np.exp(-(7.67*((x/p[1])**0.25)-1.0))

def hernq(p,x):
    """
    Hernquist  profile from Hernquist 1990
    eq. 32, 33 and 34
    p[0] is total mass
    p[1] is a scale length
    """
    s=x/p[1]
    Xs=np.zeros([len(s)])
    Xsi=np.where(s<=1.0)
    Xs[Xsi]=(1./(1.-s[Xsi]**2)**0.5)*(np.log((1. +(1.-s[Xsi]**2)**0.5)/s[Xsi]))
    Xsi=np.where(s>=1.0)
    Xs[Xsi]=(1./(s[Xsi]**2-1.)**0.5)*(np.arccos(1./s[Xsi]))

    return (p[0]/(2.*np.pi*(p[1]**2)*(1.-s**2)**2))*((2.+s**2)*Xs-3.)

def lens(p,x):

    y=np.zeros([len(x)])
    for i in np.arange(len(x)):
     if x[i]<=p[1] : y[i]=p[0]*(1.0-(x[i]/p[1])**2)
     else: y[i]=0.0

    return y

def sersicgauss(p,x) :
    #0.747812 # 0.31828
    #0.490417504
    return sersic([p[0],p[1],p[2]],x) +  gauss([0,p[3],0,0.31828],x)

def sersiclens(p,x) :

#   y=np.zeros([len(x)])
#   for i in arange(len(x)):
#    if x[i]<=p[4] : y[i]=sersic([p[0],p[1],p[2]],x[i]) + lens([p[3],p[4]],x[i])
#    else: y[i]=y[i]=sersic([p[0],p[1],p[2]],x[i])
#
#   return y
    return sersic([p[0], p[1], p[2]], x) +  lens([p[3], p[4]], x)
    #return sersic([p[0],p[1],p[2]],x) +  barellip([p[3],p[4]],x)

def disk(p,x):

    return (p[0]*np.exp(-(x/p[1])))
#   return (p[0]/(2*np.pi*p[1]**2)*exp(-(x/p[1])))

def barellip(p,x):
    """
    Equation from Cabrera-Lavers & Garzon (2004) Table 6 (Freeman 1966)
    p[0] = Ibar
    p[1] = a
    """
    y=np.zeros([len(x)])
    for i in range(len(x)):
      if x[i]<p[1] : y[i]=abs(p[0])*np.sqrt(1.0-np.square(x[i]/p[1]))
      else : y[i] =0.0
    return y

def barellip_plot(p,x):
    """
    Equation from Cabrera-Lavers & Garzon (2004) Table 6 (Freeman 1966)
    p[0] = Ibar
    p[1] = a
    """
    y=np.zeros([len(x)])
    y = abs(p[0])*np.sqrt(1.0-np.square(x/p[1]))
    return y



def barflat(p,x):
    """
    Equation from Cabrera-Lavers & Garzon (2004) Table 6 (Prieto et al 1997,
                                                          2001)
    p[0] = Ibar
    p[1] = r1
    """
    return p[0]/(1.0 + np.exp(0.5*(x-p[1])) )

def barsersic(p,x):
    """
    Equation of the sersic function for a bar
    Ie = p[0]
    re = p[1]
    n  = p[2]
    lbar = p[2]
    """

    Ie = p[0]
    re = p[1]
    n  = p[2]
    bn = 2.0*n-0.324
    lbar = p[3]

    y=np.zeros([len(x)])
    for i in range(len(x)):
      if x[i]<lbar : y[i]=Ie*np.exp(-bn*((x[i]/re)**(1/n)))
      else : y[i] =0.0
    return y

def ring(p,x):
    """
    equation from Cabrera-Lavers & Garzon (2004) Table 6 (Buta 2006)
    p[0] = Iao
    p[1] = ra
    p[2] = sigma
    """
    return abs(p[0])*np.exp(-0.5*np.square( (x-p[1])/abs(p[2]) ) )

def barring(p,x):
    """
    This function returning the sum between a elliptical bar and a
    ring functions.
    """

    return barellip([p[0],p[1]],x) + ring([p[2],p[3],p[4]],x)

def sersicbr(p,x):
    """
    This function returning the sum between sersic, a elliptical bar and a
    ring functions.
    """

    return ( sersic([p[0],p[1],p[2]],x) + barellip([p[3],p[4]],x) +
                  ring([p[5],p[6],p[7]],x) )

def sersicbar(p,x):
    """
    This function returning the sum between sersic and barellip functions.
    """
    return sersic([p[0],p[1],p[2]],x) + barellip([p[3],p[4]],x)

def bhubble(p,x):
    """
    This function returning the Hubble profile for a bulge.
    """
    return p[0]/np.square(1.+(x/p[1]))

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



def peri_ellip_exact(a, b):
    t = np.square((a-b)/(a+b))
    return np.pi*(a+b)*hyp2f1(-0.5, -0.5, 1, t)

def peri_ellip_approx(a, b):
    t = np.square((a-b)/(a+b))
    return np.pi*(a+b)*(1 + 3*t/(10 + np.sqrt(4 - 3*t)))

# Semimajor and semiminor axes for Halley's comet orbit
#a = 2.667950e9 # km
#b = 6.782819e8 # km
#print (exact(a, b))
#print (approx(a, b))


def RoundIt (Number) :
    """
    Rounds a number up to its three first significative numbers

    """
    if (Number == 0) :
        return 0
    else :
        Rounded = round(Number, -int(floor(log10(abs(Number))))+3)
        return Rounded

def integrand(x,n,r0) :
    """
    integrand of the density

    """
    return np.exp(- b(n) * x**(1/n)) * (x**(1/n - 1)) / np.sqrt(x**2 - r0**2)

def getNU(x,n) :
    """
    constructs the grid of density values

    """
    # Checks if x = r/R_e is an array
    if (np.isscalar(x)) :
        x = np.asarray([x])
    # Checks if n is an array
    if (np.isscalar(n)) :
        n = np.asarray([n])
    nu = np.zeros((len(x),len(n)))
    for i in range(0,len(x)) :
        for j in range(0,len(n)) :
            # computes X-critical (c.f. Vitral & Mamon 2020a)
            x_crit = (9*np.log(10)/b(n[j]))**n[j]
            norm   = 2*b(n[j])**(2*n[j]+1) / (np.pi * n[j]**2 * gamma(2*n[j]))
            if (x_crit <= x[i]) :
                integ   = si.quad(integrand, x[i], np.inf, args=(n[j],x[i]),
                              epsrel=1e-4,epsabs=0,limit=1000)[0]

                nu[i,j] = norm * integ
            else :
                int1   = si.quad(integrand, x[i], x_crit, args=(n[j],x[i]),
                              epsrel=1e-4,epsabs=0,limit=1000)[0]
                int2   = si.quad(integrand, x_crit, np.inf, args=(n[j],x[i]),
                              epsrel=1e-4,epsabs=0,limit=1000)[0]
                nu[i,j] = norm * (int1 + int2)
    return nu

def integrandM1(x,n) :
    """
    first integrand of the mass (c.f. Vitral & Mamon 2020a)

    """
    integral = np.exp(- b(n) * x**(1/n)) * (x**(1/n + 1))
    return integral

def integrandM2(x,s,n) :
    """
    (second+third) integrands of the mass (c.f. Vitral & Mamon 2020a)

    """
    integral = np.exp(- b(n) * x**(1/n)) * (x**(1/n - 1)) * \
                   (np.arcsin(s/x) * x**2 - s*np.sqrt(x**2 - s**2))
    return integral

def getM(x,n) :
    """
    constructs the grid of mass values

    """
    # Checks if x = r/R_e is an array
    if (np.isscalar(x)) :
        x = np.asarray([x])
    # Checks if n is an array
    if (np.isscalar(n)) :
        n = np.asarray([n])
    M = np.zeros((len(x),len(n)))
    for i in range(0,len(x)) :
        for j in range(0,len(n)) :
            # computes X-critical (c.f. Vitral & Mamon 2020a)
            x_crit = (9*np.log(10)/b(n[j]))**n[j]
            fact   =  b(n[j])**(2*n[j]+1) / \
                    (gamma(2*n[j]) * n[j]**2)
            if (x_crit <= x[i]) :
                integral1 = 0.5 * si.quad(integrandM1, 0, x_crit, args=(n[j]),
                                       epsrel=1e-4,epsabs=0,limit=1000)[0] + \
                            0.5 * si.quad(integrandM1, x_crit, x[i], args=(n[j]),
                                       epsrel=1e-4,epsabs=0,limit=1000)[0]

                integral2 = (1/np.pi) * si.quad(integrandM2, x[i], np.inf,
                            args=(x[i],
                            n[j]), epsrel=1e-4,epsabs=0,limit=1000)[0]

                M[i,j] = fact * (integral1 + integral2)
            else :
                integral1 = 0.5 * si.quad(integrandM1, 0, x[i], args=(n[j]),
                              epsrel=1e-4,epsabs=0,limit=1000)[0]

                integral2 = (1/np.pi) * si.quad(integrandM2, x[i], x_crit,
                            args=(x[i], n[j]), epsrel=1e-4,epsabs=0,
                            limit=1000)[0] + \
                            (1/np.pi) * si.quad(integrandM2, x_crit, np.inf,
                            args=(x[i], n[j]), epsrel=1e-4,epsabs=0,
                            limit=1000)[0]

                M[i,j] = fact * (integral1 + integral2)

    return M

def pPS(n) :
    """
    Formula from Prugniel & Simien 1997, (PS97)

    """
    p = 1 - 1.188/(2*n) + 0.22/(4*n**2)
    return p

def pLN(n) :
    """
    Formula from Lima Neto, Gerbal & Marquez 1999, (LGM99)

    """
    p = 1 - 0.6097/n + 0.05463/(n**2)
    return p

def b(n) :
    """
    Formula from Ciotti & Bertin 1999, (CB99)

    """
    b = 2*n - 1/3 + 4/(405*n) + 46/(25515*n**2) + 131/(1148175*n**3) - \
        2194697/(30690717750*n**4)
    return b

def getNUm(x,n,model,*args) :
    """
    Constructs the density grid for a certain model

    """
    nu = np.zeros((len(x),len(n)))
    for i in range(0,len(x)) :
        for j in range(0,len(n)) :
            if (model == 'LN') :
                p = pLN(n[j])
            if (model == 'PS') :
                p = pPS(n[j])
            try:
                p
            except NameError:
                print("You did not give a valid model")
                return
            norm    = b(n[j])**(n[j]*(3-p)) / (n[j] * gamma(n[j]*(3-p)))
            nu[i,j] = norm * np.exp(- b(n[j]) * x[i]**(1/n[j])) * x[i]**(-p)

    return nu

def getMm(x,n,model,*args) :
    """
    Constructs the mass grid for a certain model

    """
    M = np.zeros((len(x),len(n)))
    for i in range(0,len(x)) :
        for j in range(0,len(n)) :
            if (model == 'LN') :
                p = pLN(n[j])
            if (model == 'PS') :
                p = pPS(n[j])
            try:
                p
            except NameError:
                print("You did not give a valid model")
                return

            M[i,j] = gammainc(n[j]*(3-p), b(n[j]) * x[i]**(1/n[j]))

    return M


def sersic2D(x, y, amplitude, r_eff, n, x_0, y_0, ellip, theta):
    r"""
    Two dimensional Sersic surface brightness profile.

    Parameters
    ----------
    amplitude : float
        Surface brightness at r_eff.
    r_eff : float
        Effective (half-light) radius
    n : float
        Sersic Index.
    x_0 : float, optional
        x position of the center.
    y_0 : float, optional
        y position of the center.
    ellip : float, optional
        Ellipticity.
    theta : float, optional
        Rotation angle in radians, counterclockwise from
        the positive x-axis.

    See Also
    --------
    Gaussian2D, Moffat2D

    Notes
    -----
    Model formula:

    .. math::

        I(x,y) = I(r) = I_e\exp\left\{-b_n\left[\left(\frac{r}{r_{e}}\right)^{(1/n)}-1\right]\right\}

    The constant :math:`b_n` is defined such that :math:`r_e` contains half the total
    luminosity, and can be solved for numerically.

    .. math::

        \Gamma(2n) = 2\gamma (b_n,2n)

    """
    #print (n)
    bn = gammaincinv(2. * n, 0.5)
    a, b = r_eff, (1 - ellip) * r_eff
    cos_theta, sin_theta = np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta))
    x_maj = (x - x_0) * cos_theta + (y - y_0) * sin_theta
    x_min = -(x - x_0) * sin_theta + (y - y_0) * cos_theta
    z = np.sqrt((x_maj / a) ** 2 + (x_min / b) ** 2)

    return amplitude * np.exp(-bn * (z ** (1 / n) - 1))


def exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d):
    r"""
    Two dimensional exponetial disk surface brightness profile.

    Parameters
    ----------
    amplitude : float
        Surface brightness at r_eff.
    r_s : float
        scale radius
    x_0 : float, optional
        x position of the center.
    y_0 : float, optional
        y position of the center.
    ellip : float, optional
        Ellipticity.
    theta : float, optional
        Rotation angle in radians, counterclockwise from
        the positive x-axis.

    See Also
    --------
    Sersic2D

    Notes
    -----
    Model formula:

    .. math::

        I(x,y) = I(r) = I_oexp\left[\left(\frac{r}{r_{s}\right)\right]
    """

    a, b = r_s, (1 - ellip_d) * r_s
    cos_theta, sin_theta = np.cos(np.deg2rad(theta_d)), np.sin(np.deg2rad(theta_d))
    x_maj = (x - x_0_d) * cos_theta + (y - y_0_d) * sin_theta
    x_min = -(x - x_0_d) * sin_theta + (y - y_0_d) * cos_theta
    z = np.sqrt((x_maj / a) ** 2 + (x_min / b) ** 2)

    return amplitude_d * np.exp(-1 * z)



def ferrer2D(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f,
             theta_f):
    r"""
    Two dimensional Rerrer surface brightness profile.

    Parameters
    ----------
    amplitude : float
        Surface brightness at r_eff.
    r_c : float
        cut radius
    x_0 : float, optional
        x position of the center.
    y_0 : float, optional
        y position of the center.
    ellip : float, optional
        Ellipticity.
    theta : float, optional
        Rotation angle in radians, counterclockwise from
        the positive x-axis.

    See Also
    --------
    Sersic2D

    Notes
    -----
    Model formula:

    .. math::

        I(x,y) = I(r) = I_oexp\left[\left(\frac{r}{r_{s}\right)\right]
    """

    a, b = r_c, (1 - ellip_f) * r_c
    cos_theta, sin_theta = np.cos(np.deg2rad(theta_f)), np.sin(np.deg2rad(theta_f))
    x_maj = (x - x_0_f) * cos_theta + (y - y_0_f) * sin_theta
    x_min = -(x - x_0_f) * sin_theta + (y - y_0_f) * cos_theta
    z = np.sqrt((x_maj / a) ** 2 + (x_min / b) ** 2)

    amp=amplitude_f * (1 - (z)**(2-beta) )**alpha

    amp[z>1] = 0
    amp[np.isnan(amp)] = 0
    return amp


def ferrer2D_g(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f,
             theta_f, Cf):
    """
    Two dimensional Ferrer surface brightness profile. The function supports generelized
    ellipses with Cf parameter.

    Parameters
    ----------
    amplitude : float
        Surface brightness at r_eff.
    r_c : float
        cut radius
    x_0 : float, optional
        x position of the center.
    y_0 : float, optional
        y position of the center.
    ellip : float, optional
        Ellipticity.
    theta : float, optional
        Rotation angle in radians, counterclockwise from
        the positive x-axis.
    Cf: controls the diskiness/boxiness. Decreasing C0 (C0 < 0)
        the shape becomes more disky of the isophote (diamond form).
        When C0 = 0 the isophotes are pure ellipses
        Increasing C0 ((C0 > 0) the isophotes are getting more boxy (rectangular form).

    See Also
    --------
    Sersic2D

    Notes
    -----
    Model formula:

    .. math::

        I(x,y) = I(r) = I_oexp\left[\left(\frac{r}{r_{s}\right)\right]
    """
    q = 1 -ellip_f
    a, b = r_c, q * r_c
    cos_theta, sin_theta = np.cos(np.deg2rad(theta_f)), np.sin(np.deg2rad(theta_f))
    x_maj = (x - x_0_f) * cos_theta + (y - y_0_f) * sin_theta
    x_min = -(x - x_0_f) * sin_theta + (y - y_0_f) * cos_theta
    N = Cf+2
    z = ( (abs(x_maj/a))**N + (abs(x_min/b))**N)**(1./N)

    amp=amplitude_f * (1 - (z)**(2-beta) )**alpha

    amp[z>1] = 0
    amp[np.isnan(amp)] = 0
    return amp



def Convolved_bulge_disc(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta,
                amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """
    z_sersic = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0,
                                ellip, theta)

    z_exp = exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d,
                                ellip_d, theta_d)

    z_tot = z_sersic + z_exp

    return sc.signal.fftconvolve(z_tot, psf, mode='same')

def Convolved_allmodels(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta,
                amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d,
                amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """

    z_sersic = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0,
                                ellip, theta)
    z_ferrer = ferrer2D(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f)

    z_exp = exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d,
                                ellip_d, theta_d)

    z_tot = z_sersic + z_ferrer + z_exp

    return sc.signal.fftconvolve(z_tot, psf, mode='same')



def Convolved_allmodels_g(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta,
                amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d,
                amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f, Cf):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """

    z_sersic = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0,
                                ellip, theta)
    z_ferrer = ferrer2D_g(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f, Cf)

    z_exp = exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d,
                                ellip_d, theta_d)

    z_tot = z_sersic + z_ferrer + z_exp

    return sc.signal.fftconvolve(z_tot, psf, mode='same')


def Convolved_disc(x, y, psf, amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d):
    """
    Two-dimensional Exponential disc surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.
    """
    z_tot = exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d)
    return sc.signal.fftconvolve(z_tot, psf, mode='same')

def Convolved_bulge(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.
    """
    z_tot = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0, ellip, theta)
    return sc.signal.fftconvolve(z_tot, psf, mode='same')

def Convolved_bar(x, y, psf, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                  ellip_f, theta_f):
    """
    Two-dimensional Ferrer surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.
    """
    z_tot = ferrer2D(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f)
    return sc.signal.fftconvolve(z_tot, psf, mode='same')


def Convolved_bar_g(x, y, psf, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                  ellip_f, theta_f, Cf):
    """
    Two-dimensional Ferrer surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.
    """
    z_tot = ferrer2D_g(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f, Cf)
    return sc.signal.fftconvolve(z_tot, psf, mode='same')



def Convolved_bar_disc(x, y, psf, amplitude_d, r_s, x_0_d, y_0_d, ellip_d,
                       theta_d, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                       ellip_f, theta_f):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """

    z_ferrer = ferrer2D(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f)

    z_exp = exp_disk2D(x, y, amplitude_d, r_s, x_0_d, y_0_d,
                                ellip_d, theta_d)

    z_tot = z_ferrer + z_exp

    return sc.signal.fftconvolve(z_tot, psf, mode='same')


def Convolved_bulge_bar(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta,
                        amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                        ellip_f, theta_f):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """
    z_sersic = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0,
                                ellip, theta)

    z_ferrer = ferrer2D(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f)

    z_tot = z_sersic + z_ferrer

    return sc.signal.fftconvolve(z_tot, psf, mode='same')

def Convolved_bulge_bar_g(x, y, psf, amplitude, r_eff, n, x_0, y_0, ellip, theta,
                        amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                        ellip_f, theta_f, Cf):
    """
    Two-dimensional Sersic surface brightness profile, convolved with
    a PSF provided by the user as a numpy array.

    See Also
    --------
    astropy.modeling.models.Sersic2D

    """
    z_sersic = sersic2D(x, y, amplitude, r_eff, n, x_0, y_0,
                                ellip, theta)

    z_ferrer = ferrer2D_g(x, y, amplitude_f, r_c, beta, alpha, x_0_f, y_0_f,
                                ellip_f, theta_f, Cf)

    z_tot = z_sersic + z_ferrer

    return sc.signal.fftconvolve(z_tot, psf, mode='same')


def fitmass(cubexy_obs, m200, c, vsys, cx, cy, nodpa, I0, ml_d, ml_b,
            f_b, f_d, scima, sckpc, psf, h=70, convolution=True):

    # Hubble constant in km/sec/Mpc units
    # Hubble constant (s)
    H = (h*1e3)/((1e6)*pc)
    # Critical density (kg/m^3)
    pho_0 = (3./(8.*np.pi))*(np.square(H)/g)

    # Definition M_200 (kg) and R_200 (m)
    m_200 = (10**m200)*1e12*masssun
    r_200 = ((m_200)*(3./4.)*(1./np.pi)*(1./200.)*(1./pho_0))**(1./3)

    # Characteristic overdensity  in   kg/m^3   (sun_mass/pc^3)
    pho_c = ( (200./3.)*(c**3)*pho_0 )/(np.log(1.+c)-c/(1.+c))

    # Core radius (m)
    r_c = r_200/abs(c)

    # Pa and i
    nod = np.deg2rad(nodpa)
    i = np.deg2rad(I0)

    cubexy_mod = np.copy(cubexy_obs)

    nx, ny = (cubexy_obs.shape[1], cubexy_obs.shape[0])
    x = np.arange(nx)
    y = np.arange(ny)
    xv, yv = np.meshgrid(x, y)

    x = xv+1 - cx
    y = yv+1 - cy
    r = np.hypot(y, x)
    pa = np.arctan2(y, x)

    pa[pa<0.0]+=2*np.pi
    phi = pa-nod


    f_r = np.sqrt( 1 + np.square(np.sin(phi))*np.square(np.tan(i)) )
    f_v = (np.sin(i)*np.cos(i)*np.cos(phi))/np.sqrt(1 -
         np.square(np.sin(i))*np.square(np.cos(phi)))

    # Rotation curves
    r = r*scima*sckpc*1000.*pc*f_r
    p = [pho_c,r_c]
    curve_halo  = nfw(p,r)[0]

    cubexy_mod=np.sqrt( f_b(r)*ml_b + f_d(r)*ml_d + curve_halo )*f_v + vsys

    if convolution:
       #cubexy_mod=fftconvolve(cubexy_mod, psf, mode='same')
       cubexy_mod=convolve(cubexy_mod, psf)

    cubexy_mod[np.isnan(cubexy_obs)] = np.nan

    return cubexy_mod

def err_bulge_bar_disc(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_allmodels(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model*segm - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    a, re, n, x0, y0, ep, pa, ad, rs, x0d, y0d, epd, pad, af, rc, bt, al, x0f, y0f, epf, paf= params

    if a>=0 and ad>=0 and af>=0 and re>=0 and rs>=0 and rc>=0 and n>=0.5 and bt>=0 and 5>al>=0 and ep<1:
    #if a>=0 and ad>=0 and af>=0 and re>=0 and rs>=0 and rc>=0 and n>=0.5 and bt>=0 and 5>al>=0 and ep<1 and re<(psf_i/sc_ima):
         return out
    else:
         return out*-np.inf



def err_bulge_disc(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_bulge_disc(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    a, re, n, x0, y0, ep, pa, ad, rs, x0d, y0d, epd, pad = params

    if a>=0 and ad>=0 and re>=0 and rs>=0 and n>=0.5  and rs>re  and ep>=0:
         return out
    else:
         return out*-np.inf


def err_bulge_bar(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_bulge_bar(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    a, re, n, x0, y0, ep, pa, af, rc, bt, al, x0f, y0f, epf, paf = params

    if a>=0 and af>=0 and re>=0 and rc>=0 and n>=0.5  and rc>re and bt>=0 and 5>al>=0:
         return out
    else:
         return out*-np.inf


def err_bar_disc(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_bar_disc(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model*segm - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    ad, rs, x0d, y0d, epd, pad, af, rc, bt, al, x0f, y0f, epf, paf= params

    if ad>=0 and af>=0 and rs>=0 and rc>=0 and bt>=0 and 5>al>=0 and 8>rc:
         return out
    else:
         return out*-np.inf

def err_disc(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_disc(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    ad, rs, x0d, y0d, epd, pad = params

    if ad>=0  and rs>=0:
         return out
    else:
         return out*-np.inf


def err_bulge(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_bulge(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    a, re, n, x0, y0, ep, pa = params

    if a>0 and re>0 and  n>=0.5 and ep>=0:
         return out
    else:
         return out*-np.inf


def err_bar(params, xdata, ydata, zdata, weights, psf, segm):

    model = Convolved_bar(xdata, ydata, psf, *params)*segm
    out= np.asarray(weights * (model - zdata*segm)).ravel()
    out[np.isnan(out)] = 0

    af, rc, bt, al, x0f, y0f, epf, paf= params

    if af>=0  and  rc>=0  and bt>=0 and 5>al>=0:
         return out
    else:
         return out*-np.inf


labels_bulge = np.array(["Ie", "Re", "n", "cx", "cy", "ellip", "PA"])
labels_disc = np.array(["Io", "Rs", "cx", "cy", "ellip", "PA"])
labels_bar = np.array(["Io", "Rout", "beta",  "alpha", "cx", "cy", "ellip", "PA"])

def fit2Dmodel(x, y, imagefit, imagefit_sig,  psf_f, segmapnan, imaref='8083-12704/m2.fits',
               comp_mod=np.array(['bulge','disc','bar']), R_cut_bar = 10, R_cut_bulge = 10,
    amplitude=1, r_eff=1, n=2, x_0=0, y_0= 0, ellip=0.1, theta=0,
    amplitude_d=1, r_s=1, x_0_d=0, y_0_d=0, ellip_d=0.1, theta_d=0,
    amplitude_f=1, r_c=1, beta=0.1, alpha=0.6, x_0_f=0, y_0_f=0, ellip_f=0.6, theta_f=0):

    import plot_functions as pfunc

    print ("Initial guess for Disc model")
    par0 = ([amplitude_d, r_s, x_0_d, y_0_d, ellip_d, theta_d])
    rests = op.leastsq(err_disc, par0, args=(x, y, imagefit, imagefit_sig, psf_f, segmapnan), full_output=1)
    #print (rests)

    pfound_disc = rests[0]
    pcov = rests[1]

    # Degrees of freedom
    degfree = np.copy(imagefit*segmapnan).ravel()
    degfree = len(degfree[degfree!=0]) - len(par0)

    # Chi square reduced
    s_sq = (err_disc(pfound_disc, x, y, imagefit, imagefit_sig, psf_f, segmapnan)**2).sum()/degfree
    print()
    print ("Chi^2_reduced: ", s_sq)

    pcov = pcov * s_sq
    perr_disc = np.sqrt(np.diag(pcov))


    print()

    labels =  labels_disc

    for i in np.arange(len(labels)):
        txt = "\mathrm{{{2}}} = {0:.2f}\pm{{{1:.2f}}}\,\,({3:.2f})"
        txt = txt.format(pfound_disc[i], perr_disc[i], labels[i], par0[i])
        display(Math(txt))

    if  len(comp_mod) == 1 and any(comp_mod=='disc'):
        print ('Only was fitted the disc!')
        return pfound_disc, perr_disc, s_sq



    modelgal_disc = Convolved_disc(x, y, psf_f, *pfound_disc)
    modelres= imagefit-modelgal_disc

    ima_xy, ima_array = pfunc.callf(imaref)

    if len(comp_mod) == 2:
        if any(comp_mod == 'bar'):

            print ("Initial guess for Bar model")

            poly_circ = pfunc.circ(int(x_0_f)-0.5,
                                   int(y_0_f)-0.5, R_cut_bar,plotr='no')

            mask_circ_inv = pfunc.maskpoly(poly_circ, ima_xy, imagefit*np.nan)
    #         poly_circ2 = pfunc.circ(int(x_0)-1, int(y_0)-1, R_cut_bulge*0.8,plotr='no')
    #         mask_circ_inv2 = pfunc.maskpoly(poly_circ2, ima_xy, imagefit*np.nan)
    #         mask_circ = pfunc.maskinv(mask_circ_inv2)


            # Bar
            par0 = ([amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f])
            rests = op.leastsq(err_bar, par0, args=(x, y,modelres +mask_circ_inv, imagefit_sig, psf_f, segmapnan), full_output=1)
            #print (rests)

            pfound_bar = rests[0]
            pcov = rests[1]

            # Degrees of freedom
            degfree = np.copy(imagefit*segmapnan+mask_circ_inv).ravel()
            degfree = len(degfree[degfree!=0]) - len(par0)

            # Chi square reduced
            s_sq = (err_bar(pfound_bar, x, y, imagefit, imagefit_sig, psf_f, segmapnan)**2).sum()/degfree
            print()
            print ("Chi^2_reduced: ", s_sq)

            try:

                pcov = pcov * s_sq
                perr_bar = np.sqrt(np.diag(pcov))


                labels =  labels_bar

                for i in np.arange(len(labels)):
                    txt = "\mathrm{{{2}}} = {0:.2f}\pm{{{1:.2f}}}\,\,({3:.2f})"
                    txt = txt.format(pfound_bar[i], perr_bar[i], labels[i], par0[i])
                    display(Math(txt))


                modelgal_bar = Convolved_bar(x, y, psf_f, *pfound_bar)
                modelres = modelres-modelgal_bar
            except:
                print ("The initial guess for the bar was not possible")
                pfound_bar = par0
                plt.imshow((-2.5*np.log10(modelres) + zp)*segmapnan+mask_circ_inv, origin='lower',
                           interpolation='nearest')

        if any(comp_mod == 'bulge'):
            print ("Initial guess for bulge  model")

            poly_circ2 = pfunc.circ(int(x_0)-0.5, int(y_0)-0.5, R_cut_bulge,plotr='no')

            mask_circ_inv2 = pfunc.maskpoly(poly_circ2, ima_xy, imagefit*np.nan)


            par0 = ([amplitude, r_eff, n, x_0, y_0, ellip, theta])

            rests = op.leastsq(err_bulge, par0, args=(x, y, modelres +mask_circ_inv2, imagefit_sig, psf_f,
                                                      segmapnan), full_output=1)
            #print (rests)

            pfound_bulge = rests[0]
            pcov = rests[1]

            # Degrees of freedom
            degfree = np.copy(imagefit*segmapnan+mask_circ_inv2).ravel()
            degfree = len(degfree[degfree!=0]) - len(par0)

            # Chi square reduced
            s_sq = (err_bulge(pfound_bulge, x, y, imagefit, imagefit_sig, psf_f, segmapnan)**2).sum()/degfree
            print()
            print ("Chi^2_reduced: ", s_sq)


            try:
                pcov = pcov * s_sq
                perr_bulge = np.sqrt(np.diag(pcov))


                labels =  labels_bulge

                kn_bulge = gammaincinv(2*pfound_all[2],0.5)
                amplitude_bulge=pfound_all[0]*np.exp(kn_bulge)
                txt = "\mathrm{{Ie_0}} = {:.2f}".format(amplitude_bulge)
                display(Math(txt))
                for i in np.arange(len(labels)):
                    txt = "\mathrm{{{2}}} = {0:.2f}\pm{{{1:.2f}}}\,\,({3:.2f})"
                    txt = txt.format(pfound_bulge[i], perr_bulge[i], labels[i], par0[i])
                    display(Math(txt))
            except:
                print ("An Initial guess for the bulge did not work")
                pfound_bulge = np.array([amplitude, r_eff, n, x_0, y_0, ellip, theta])
                plt.imshow((-2.5*np.log10(modelres) + zp)*segmapnan+mask_circ_inv2, origin='lower', interpolation='nearest')
    else:
        print ("Initial guess for Bulge + Bar model")

        poly_circ = pfunc.circ(int(x_0_f)-0.5,
                               int(y_0_f)-0.5, R_cut_bar,plotr='no')

        mask_circ_inv = pfunc.maskpoly(poly_circ, ima_xy, imagefit*np.nan)


        # Bulge + Bar
        par0 = ([amplitude, r_eff, n, x_0, y_0, ellip, theta,
                 amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f])
        rests = op.leastsq(err_bulge_bar, par0, args=(x, y,modelres +mask_circ_inv, imagefit_sig,
                                                      psf_f, segmapnan), full_output=1)
        #print (rests)

        pfound_bulge_bar = rests[0]
        pfound_bulge = rests[0][0:7]
        pfound_bar = rests[0][7::]

        pcov = rests[1]

        # Degrees of freedom
        degfree = np.copy(imagefit*segmapnan+mask_circ_inv).ravel()
        degfree = len(degfree[degfree!=0]) - len(par0)

        # Chi square reduced
        s_sq = (err_bulge_bar(pfound_bulge_bar, x, y, imagefit, imagefit_sig, psf_f, segmapnan)**2).sum()/degfree
        print()
        print ("Chi^2_reduced: ", s_sq)

        try:

            pcov = pcov * s_sq
            perr_bar = np.sqrt(np.diag(pcov))


            labels =  np.concatenate((labels_bulge,labels_bar))

            for i in np.arange(len(labels)):
                txt = "\mathrm{{{2}}} = {0:.2f}\pm{{{1:.2f}}}\,\,({3:.2f})"
                txt = txt.format(pfound_bulge_bar[i], perr_bar[i], labels[i], par0[i])
                display(Math(txt))
        except:
            print ("An Initial guess for the Bulge + Bar did not work")
            pfound_bulge = np.array([amplitude, r_eff, n, x_0, y_0, ellip, theta])
            pfound_bar = np.array([amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f])
            plt.imshow((-2.5*np.log10(modelres) + zp)*segmapnan+mask_circ_inv, origin='lower',
                       interpolation='nearest')

    ###############################
    # Fitting all component at once

    if any(comp_mod == 'bar') and any(comp_mod == 'bulge'):
        par0 = np.concatenate((pfound_bulge, pfound_disc, pfound_bar))
        rests = op.leastsq(err_bulge_bar_disc, par0, args=(x, y, imagefit, imagefit_sig,
                                                           psf_f, segmapnan), full_output=1)

    if len(comp_mod) == 2:
        if any(comp_mod == 'bulge'):
            par0 = np.concatenate((pfound_bulge,pfound_disc))
            rests = op.leastsq(err_bulge_disc, par0, args=(x, y, imagefit, imagefit_sig, psf_f,
                                                           segmapnan), full_output=1)
        else:
            par0 = np.concatenate((pfound_disc,pfound_bar))
            rests = op.leastsq(err_bar_disc, par0, args=(x, y, imagefit, imagefit_sig,
                                                               psf_f, segmapnan), full_output=1)

    pfound_all = rests[0]
    pcov = rests[1]

    # Degrees of freedom
    degfree = np.copy(imagefit*segmapnan).ravel()
    degfree = len(degfree[degfree!=0]) - len(par0)

    # Chi square reduced
    if any(comp_mod == 'bar') and any(comp_mod == 'bulge'):
        s_sq = (err_bulge_bar_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                                   segmapnan)**2).sum()/degfree
    if len(comp_mod) == 2:
        if any(comp_mod == 'bulge'):
            s_sq = (err_bulge_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                               segmapnan)**2).sum()/degfree
        else:
            s_sq = (err_bar_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                               segmapnan)**2).sum()/degfree
    print()
    print ("Chi^2_reduced: ", s_sq)

    try:
        pcov = pcov * s_sq
    except:
        print ('Try again...with the initial guess!')
        if any(comp_mod == 'bar') and any(comp_mod == 'bulge'):

            pfound_bulge = np.array([amplitude, r_eff, n, x_0, y_0, ellip, theta])
            pfound_bar = np.array([amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f])

            par0 = np.concatenate((pfound_bulge,pfound_disc,pfound_bar))
            rests = op.leastsq(err_bulge_bar_disc, par0, args=(x, y, imagefit, imagefit_sig,
                                                               psf_f, segmapnan), full_output=1)

        if len(comp_mod) == 2:
            if any(comp_mod == 'bulge'):
                pfound_bulge = np.array([amplitude, r_eff, n, x_0, y_0, ellip, theta])
                par0 = np.concatenate((pfound_bulge,pfound_disc))
                rests = op.leastsq(err_bulge_disc, par0, args=(x, y, imagefit, imagefit_sig, psf_f,
                                                               segmapnan), full_output=1)
            else:
                pfound_bar = np.array([amplitude_f, r_c, beta, alpha, x_0_f, y_0_f, ellip_f, theta_f])
                par0 = np.concatenate((pfound_disc,pfound_bar))
                rests = op.leastsq(err_bar_disc, par0, args=(x, y, imagefit, imagefit_sig, psf_f,
                                                               segmapnan), full_output=1)



        pfound_all = rests[0]
        pcov = rests[1]

        # Degrees of freedom
        degfree = np.copy(imagefit*segmapnan).ravel()
        degfree = len(degfree[degfree!=0]) - len(par0)

        if any(comp_mod == 'bar') and any(comp_mod == 'bulge'):
            s_sq = (err_bulge_bar_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                                   segmapnan)**2).sum()/degfree
        if len(comp_mod) == 2:
            if any(comp_mod == 'bulge'):
                s_sq = (err_bulge_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                                   segmapnan)**2).sum()/degfree
            else:
                s_sq = (err_bar_disc(pfound_all, x, y, imagefit, imagefit_sig, psf_f,
                                   segmapnan)**2).sum()/degfree
        print()
        print ("Chi^2_reduced: ", s_sq)
        pcov = pcov * s_sq


    perr_all = np.sqrt(np.diag(pcov))
    print()

    if any(comp_mod == 'bar') and any(comp_mod == 'bulge'):
        kn_bulge = gammaincinv(2*pfound_all[2],0.5)
        amplitude_bulge=pfound_all[0]*np.exp(kn_bulge)
        txt = "\mathrm{{Ie_0}} = {:.2f}".format(amplitude_bulge)
        display(Math(txt))

        labels = np.concatenate((labels_bulge, labels_disc, labels_bar))
    if len(comp_mod) == 2:
            if any(comp_mod == 'bulge'):
                kn_bulge = gammaincinv(2*pfound_all[2],0.5)
                amplitude_bulge=pfound_all[0]*np.exp(kn_bulge)
                txt = "\mathrm{{Ie_0}} = {:.2f}".format(amplitude_bulge)
                display(Math(txt))
                labels = np.concatenate((labels_bulge, labels_disc))
            else:
                labels = np.concatenate((labels_disc, labels_bar))
    for i in np.arange(len(labels)):
        txt = "\mathrm{{{2}}} = {0:.2f}\pm{{{1:.2f}}}\,\,({3:.2f})"
        txt = txt.format(pfound_all[i], perr_all[i], labels[i],par0[i])
        display(Math(txt))

    return pfound_all, perr_all, s_sq
