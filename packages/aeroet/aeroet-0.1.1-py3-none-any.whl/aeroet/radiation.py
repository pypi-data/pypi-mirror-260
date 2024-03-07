#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'MIT'
__date__ = 'Wed 24 Aug 22 16:04:30'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           radiation.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2022


"""


# IMPORTS
import numpy as np
import xarray as xr

# CONSTANTS
SIGMA = 5.67036713e-08 		# Stefan-Boltzmann constant [W m-2 K-4]


def calc_SW_in(SW_in_mean, cos_i):
    """
    Calculate pixel-wise incoming shortwave radiation.

    Parameters
    ----------
    SW_in_mean : float
        Mean shortwave incoming radiation over the flight [W m-2].
        NOTE: May want a different value?--how to make use of the wealth of SW data?
    cos_i : float
        Cosine of the incidence angle of solar radiation.

    Returns
    -------
    SW_in : ndarray
        Incoming shortwave radiation raster [W m-2].
    """

    SW_in = SW_in_mean * cos_i

    return SW_in


def calc_cos_i(slope, aspect, theta_sun, psi_sun):
    """
    Calculate the cosine of the solar incidence angle.

    Parameters
    ----------
    slope : ndarray
        Slope of the surface [radians].
    aspect : ndarray
        Aspect of the surface (orientation of the slope from N) [radians].
    theta_sun : float
        Solar zenith angle [radians].
    psi_sun : float
        Solar azimuth angle [radians].

    Returns
    -------
    [type]
        [description]
    """

    cos_i = ( np.cos(slope) * np.cos(theta_sun) ) + ( 
        np.sin(slope) * np.sin(theta_sun) * np.cos(psi_sun - aspect) 
    )

    return cos_i


def calc_SW_out(SW_in, alpha):

    SW_out = SW_in * alpha

    return SW_out


def calc_albedo(ndvi):
    """
    Estimate albedo from NDVI.

    Parameters
    ----------
    ndvi : float or array-like
        Normalized-difference vegetation index.

    Returns
    -------
    alpha : float or array-like
        Surface albedo.
    
    Source: GAO, 1995; Mo et al., 2014 in Wang et al. (2019), p. 20, eqs. 13-14.
    (NOTE: There may be a better source out there...)
    """

    # Calculate NDVI reflectance
    sr = (1 + ndvi) / (1 - ndvi)
    # Calculate albedo
    alpha = 0.28 - 0.14 * np.e**( -6.08 / (sr**2) )

    return alpha


def calc_emissivity(e_a,T_a, c=0):
    """
    Estimates the atmospheric emissivity for a clear sky.

    Parameters
    ----------
    e_a : float
        Vapor pressure of air [kPa].

    T_a : float
        Temperature of air [K]

    c : float, optional
        Cloud cover fraction [--]. The default is 0 (clear sky).
        
    Returns
    -------
    epsilon_a : float
        Atmospheric emissivity [unitless]

    Reference: Brutsaert (1975), Eq. 11
    Brutsaert, W. (1975) On a derivable formula for long-wave radiation
        from clear skies, Water Resour. Res., 11(5), 742-744,
        htpp://dx.doi.org/10.1029/WR011i005p00742.

    NOTE: Based on tower data, this formula is not great.
    """

    epsilon_ac = 1.24 * ((e_a * 10) / T_a )**(1./7.)

    epsilon_a = calc_cloudy_emissivity(epsilon_ac, c)

    return epsilon_a

def calc_cloudy_emissivity(eps_ac, c):
    """
    Calculates the atmospheric emissivity for a cloudy sky. Note that if c = 0, 
    then eps_a = eps_ac.

    Parameters
    ----------
    eps_ac : float
        Clear-sky atmospheric emissivity [-].
    c : float
        Cloud cover fraction [--].

    Returns
    -------
    eps_a : float
        Cloudy-sky atmospheric emissivity [-].

    Reference: Campbell and Norman (1998), Eq. 10.12
    Campbell, G. S. and J. M. Norman (1998), An Introduction to Environmental
        Biophysics, 2nd Ed., Springer, New York, 286 pp.

    NOTE: Based on tower data, this formula is not great.
    """

    eps_a = ( (1 - 0.84 * c) * eps_ac ) + (0.84 * c)

    return eps_a


def calc_surf_emissivity(ndvi):

    # For 0.131 <= NDVI < 0.608, epsilon_s = 1.0094 + 0.047 * ln(ndvi); else, ndvi = 0.986
    epsilon_s = xr.where( 
        ( (ndvi < 0.608) & (ndvi >= 0.131) ), 
        1.0094 + 0.047 * np.log(ndvi), 
        0.986
    )
    # for NDVI < 0.131, epsilon_s = 0.914 (else leave as calculated above)
    epsilon_s = xr.where( ndvi < 0.131, 0.914, epsilon_s)
    # Set nans
    epsilon_s = xr.where(ndvi.isnull(), np.nan, epsilon_s)
    epsilon_s

    return epsilon_s


def calc_stefboltz(T_K):
    """
    Calculates the total energy radiated by a blackbody according to the
    Stefan-Boltzmann Law.

    Parameters
    ----------
    T_K : float
        Temperature [K].

    Returns
    -------
    M : float
        Emitted blackbody radiance [W m-2]

    """

    M = SIGMA * T_K**4

    return M


def calc_LW(T, epsilon=1):
    """ Add doc strings



    """
    return epsilon * calc_stefboltz(T)


def calc_Rn(SW_IN, SW_OUT, LW_IN, LW_OUT):
    """
    Calculates net radiation from the four components of the surface energy balance.

    Parameters
    ----------
    SW_in : float or array-like
        Incoming shortwave radiation [W m-2].

    SW_out : float or array-like
        Outgoing shortwave radiation [W m-2].
    
    LW_in : float or array-like
        Incoming longwave radiation [W m-2].

    LW_out : float or array-like
        Outgoing longwave radiation [W m-2].

    Returns
    -------
    R_n : float or array-like
        Net radiation [W m-2].
    """
    R_n = SW_IN - SW_OUT + LW_IN - LW_OUT

    return R_n


#-------------------------------------------------------------------------------
#       RADATION
#-------------------------------------------------------------------------------

class Radiation:
    """
    
    Attributes
    ----------
    R_n : array-like
        Net radiation [W m-2]
    
    G : float | array-like
        Ground heat flux [W m-2]
    
    SW_IN : float | array-like
        Shortwave incoming radiation [W m-2]
    
    SW_OUT : float or array-like
        Outgoing shortwave radiation [W m-2].
    
    LW_IN : float or array-like
        Incoming longwave radiation [W m-2].

    LW_OUT : float or array-like
        Outgoing longwave radiation [W m-2].

    Methods
    -------
    calc_Rn()
        Calculates net radiation from the four components of the surface energy balance.
    
    calc_G()
        Calculate ground heat flux.
    
    set_components()
        Set radiation components as attributes.
    """
    def __init__(self, SW_IN, SW_OUT, LW_IN, LW_OUT, R_n = None, G = None, G_params=None, allow_neg=False):
        """

        Parameters
        ----------
        SW_IN : float | array-like
            Shortwave incoming radiation [W m-2]
        SW_OUT : float or array-like
            Outgoing shortwave radiation [W m-2].
        LW_IN : float or array-like
            Incoming longwave radiation [W m-2].
        LW_OUT : float or array-like
            Outgoing longwave radiation [W m-2].
        R_n : float | array-like, optional
            Net radiation [W m-2]. The default is to calculate from components.
        G : float | array-like, optional
            Ground heat flux. The default is to calculate.
        """


        # self.SW_IN = np.array(SW_IN)
        # self.SW_OUT = np.array(SW_OUT)
        # self.LW_IN = np.array(LW_IN)
        # self.LW_OUT = np.array(LW_OUT)

        if R_n is not None:
            self.R_n = R_n
        else:
            self.R_n = self.calc_Rn(SW_IN, SW_OUT, LW_IN, LW_OUT, allow_neg=allow_neg)
        
        if G is not None:
            self.G = G
        elif G_params is not None:
            self.G = self.calc_G(**G_params)
        else:
            self.G = 0.0

        self.set_component_avgs(SW_IN, SW_OUT, LW_IN, LW_OUT)
    

    def describe(self, means=True):
        raw = self.__dict__.copy()
        # raw['R_n'] = np.mean(self.R_n)
        if means:
            raw.update({k : v.mean().item() for k,v in raw.items() if not isinstance(v,(float,int))})

        return raw
            


    @staticmethod
    def calc_Rn(SW_IN, SW_OUT, LW_IN, LW_OUT, allow_neg=False):
        """
        Calculates net radiation from the four components of the surface energy balance.

        Parameters
        ----------
        SW_in : float or array-like
            Incoming shortwave radiation [W m-2].

        SW_out : float or array-like
            Outgoing shortwave radiation [W m-2].
        
        LW_in : float or array-like
            Incoming longwave radiation [W m-2].

        LW_out : float or array-like
            Outgoing longwave radiation [W m-2].

        Returns
        -------
        R_n : float or array-like
            Net radiation [W m-2].
        """
        R_n = SW_IN - SW_OUT + LW_IN - LW_OUT

        # Force negative values to be 0.
        if not isinstance(R_n, float) and not allow_neg:
            R_n = xr.where(R_n < 0, 0.0, R_n)

        return R_n

    def calc_G_ratio(self, t, A=0.2, c=-4.0, B=24.0):
        """
        Calculate the ratio of G / R_n.

        Parameters
        ----------
        t : float or array-like
            Time of day [h].
        A : float, optional
            Amplitude of diurnal fluctuation in G/R_n (max diurnal G/R_n). The 
            default is 0.2.
        c : float, optional
            Phase shift relative to noon [h]. Negative values are in the afternoon. 
            The default is -4.0 (16:00).
        B : float, optional
            Period [h]. The default is 24.

        Returns
        -------
        G_ratio : float or array-like
            Ratio of soil heat flux to net radiation.
        
        Reference
        ---------
        Santanello, J. A., & Friedl, M. A. (2003). Diurnal Covariation in Soil 
        Heat Flux and Net Radiation. Journal of Applied Meteorology and Climatology, 
        42(6), 851–862. https://doi.org/10.1175/1520-0450(2003)042<0851:DCISHF>2.0.CO;2
            
        """
        t = t - 12.0
        G_ratio = A * np.cos(2.0 * np.pi * (t + c) / B)

        return G_ratio


    def calc_G(self, t, A=0.2, c=-4.0, B=24.0):
        """
        Calculate ground heat flux.

        Parameters
        ----------
        t : float or array-like
            Time of day [h].
        A : float, optional
            Amplitude of diurnal fluctuation in G/R_n (max diurnal G/R_n). The 
            default is 0.2.
        c : float, optional
            Phase shift relative to noon [h]. Negative values are in the afternoon. 
            The default is -4.0 (16:00).
        B : float, optional
            Period [h]. The default is 24.

        Returns
        -------
        G : float or array-like
            Ground heat flux [W m-2].

        """
        G_ratio = self.calc_G_ratio(t, A=A, c=c, B=B)
        G = G_ratio * self.R_n

        return G


    def set_components(self, SW_IN, SW_OUT, LW_IN, LW_OUT):

        self.SW_IN = SW_IN
        self.SW_OUT = SW_OUT
        self.LW_IN = LW_IN
        self.LW_OUT = LW_OUT

    def set_component_avgs(self, SW_IN, SW_OUT, LW_IN, LW_OUT):
        
        self.SW_IN_mean = np.mean(SW_IN)
        self.SW_OUT_mean = np.mean(SW_OUT)
        self.LW_IN_mean = np.mean(LW_IN)
        self.LW_OUT_mean = np.mean(LW_OUT)

