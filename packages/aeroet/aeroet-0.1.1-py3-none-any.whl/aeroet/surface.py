#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'MIT'
__date__ = 'Mon 22 Aug 22 15:15:04'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           air.py
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

# TODO: Add dictionary of params for a few veg types (h, w_l, x_lad)

#%% IMPORTS

import numpy as np
import xarray as xr
from . import utils

SIGMA = 5.67036713e-08 

class Surface:
    """
    
    Attributes
    ----------
    cover : str
        Land cover type

    veg : str
        Vegetation type.

    h : float | int
        Canopy height [m]

    T_s : array-like
        Temperature of the surface [K]
    
    Methods
    -------
    calc_d0()
        Calculate the zero-plane displacement height (height at which wind speed goes
        to 0), d_0 [m].
    
    calc_z0m()
        Calculate the aerodynamic roughness length for momemtum transport, z_0m [m].
    
    calc_z0h()
        Calculate the aerodynamic roughness length for heat transport, z_0h [m].

    """

    def __init__(
        self,
        h,
        T_s,
        w_l = 0.01,
        ndvi = None,
        x_lad = 1.,
        b = 10.,
        theta_sun = 60.,
        cover : str = None,     # TODO: Figure out how to force cover and veg to be in a list of options
        veg : str = None,
    ):
        """
        Parameters
        ----------
        h : float
            Height of the canopy [m]
        T_s : float | array-like
            Temperature of the surface [K]
        w_l : float
            Leaf width [m]
        ndvi : float | array-like
            NDVI
        x_lad : float | array-like
            Ratio of horizontal to vertical projected leaf area
        b : float 
            Ratio of z_0m to z_0h. The default is 10.
        theta_sun : float
            Solar zenith angle at time of data collection.
        cover : str
            Land cover type
        veg : str
            Vegetation type
        """

        self.h = h
        self.w_l = w_l
        self.T_s = T_s
        self.ndvi = ndvi
        self.cover = cover
        self.veg = veg

        self.theta_s = self.calc_theta_s()

        self.d_0 = self.calc_d0()
        self.z_0m = self.calc_z0m()
        self.z_0h = self.calc_z0h(b=b)

        if ndvi is not None:
            self.albedo = self.calc_albedo(ndvi)
            self.epsilon_s = self.calc_surf_emissivity(ndvi)
            self.lai = self.calc_lai( k_be = self.calc_k_be(theta_sun=theta_sun, x=x_lad) )
        else:
            self.albedo = 0.28
            self.epsilon_s = 0.98
            self.lai = 1.0

    def describe(self):
        raw = self.__dict__.copy()
        # raw['T_s'] = self.T_s.mean().item()
        raw.update({k : v.mean().item() for k,v in raw.items() if v is not None and not isinstance(v,(float,int,str))})
        return raw

    def calc_theta_s(self):
        return self.T_s


    def calc_d0(self):
        """
        Calculate the zero-plane displacement height (height at which wind speed goes
        to 0), d_0 [m].

        Parameters
        ----------
        h : float
            Canopy height [m].

        Returns
        -------
        d_0 : float
            Zero-plane displacement height [m].

        Reference: Norman et al. (1995).
        """
        d_0 = 0.65 * self.h

        return d_0

    def calc_z0m(self):
        """
        Calculate the aerodynamic roughness length for momemtum transport, z_0m [m].

        Parameters
        ----------
        h : float
            Canopy height [m]

        Returns
        -------
        z_0m : float
            Roughness length for momentum transport [m].

        Reference: Norman et al. (1995).
        """
        z_0m = 0.125 * self.h

        return z_0m


    def calc_z0h(self, b=10.):
        """
        Calculate the aerodynamic roughness length for heat (and vapour) transport,
        z_0h [m].

        Parameters
        ----------
        z_0m : float
            Roughness length for momentum transport [m].

        Returns
        -------
        z_0h : float
            Roughness length for heat transport [m].

        Reference: Bonan (2016), p. 213.
        """
        # TODO: This only applies to vegetation. Should change this?
        z_0h = self.z_0m / b

        return z_0h

    def calc_albedo(self, ndvi):
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


    def calc_surf_emissivity(self, ndvi):

        # For 0.131 <= NDVI < 0.608, epsilon_s = 1.0094 + 0.047 * ln(ndvi); else, ndvi = 0.986
        epsilon_s = xr.where( 
            ( (ndvi < 0.608) & (ndvi >= 0.131) ), 
            1.0094 + 0.047 * np.log(ndvi), 
            0.986
        )
        # for NDVI < 0.131, epsilon_s = 0.914 (else leave as calculated above)
        epsilon_s = xr.where( ndvi < 0.131, 0.914, epsilon_s )
        # Set nans
        if not isinstance(ndvi,(float,int)):
            epsilon_s = xr.where( ndvi.isnull(), np.nan, epsilon_s )

        if isinstance(epsilon_s,xr.DataArray):
            utils.set_crs(epsilon_s, self.T_s)

        return epsilon_s


    def correct_T_b(self, LW_IN, T_a, tau, epsilon_s=None):

        if epsilon_s is None:
            epsilon_s = self.epsilon_s

        LW_sens = SIGMA * self.T_s**4
        LW_refl = (1 - epsilon_s) * LW_IN       # Incoming LW radiation reflected by surface
        LW_atm = (1 - tau) * SIGMA * (T_a**4)   # LW radiation emitted by atmosphere btw surface and sensor

        # tes = tau * epsilon_s * SIGMA

        # T_s = ( ( LW_OUT / (tau * epsilon_s * SIGMA) ) - \
        #         ( ((1 - epsilon_s) / (epsilon_s * SIGMA)) * LW_IN ) - \
        #         ( LW_atm / (tau * epsilon_s) ) 
        #     ) ** (1/4)

        if self.T_s.shape != epsilon_s.shape:
            LW_refl = LW_refl.interp(x = self.T_s.x, y = self.T_s.y)


        T_s = ( ( LW_sens - tau * LW_refl - LW_atm ) / (tau * epsilon_s * SIGMA) ) ** (1/4)
        
        self.theta_s = T_s.copy()

        return T_s

    def calc_k_be(self, theta_sun, x=1.):
        """
        Calculate the beam extinction coefficient base on an ellipsoidal leaf 
        inclination distribution function. For spherical LAD, x = 1. For vertical,
        x = 0.

        Parameters
        ----------
        theta_sun : float or array-like
            Solar zenith angle [degrees].
        x : float, optional
            Ratio of horizontal to vertical projected area (i.e. leaf angle distribution, 
            LAD). For spherical LAD, x = 1. For vertical, x = 0.
        
        Returns
        -------
        k_be : float or array-like
            Beam extinction coefficient
        
        Reference: Campbell + Norman, 1998, eq. 15.4
        """

        theta_rad = np.radians(theta_sun)

        k_be = ( np.sqrt( x**2 + np.tan(theta_rad)**2 ) /
                (x + 1.774 * (x + 1.182)**-0.733 ) )

        return k_be

    def calc_vi_scaled(self):
        """
        Calculate scaled vegetation index.

        Parameters
        ----------
        vi : array-like
            Vegetation index

        Returns
        -------
        vi_star : array-like
            Scaled vegetation index.
        
        Reference: Jones and Vaughan, Eq. 7.6
        """
        if isinstance(self.ndvi, (float,int)):
            return self.ndvi
        
        vi_veg = self.ndvi.where(self.ndvi < 1.0).max()
        vi_soil = self.ndvi.where(self.ndvi > 0.0).min()

        vi_star = (self.ndvi - vi_soil) / (vi_veg - vi_soil)

        vi_star = xr.where(vi_star == 1.0, vi_veg, vi_star)
        vi_star = xr.where(vi_star < 0.0, 0.0, vi_star)

        return vi_star
    

    def calc_lai(self, k_be):
        """
        Calculate LAI from scaled vegetation index (typically NDVI).

        Parameters
        ----------
        k_be : float or array-like
            Beam extinction coefficient
        vi_star : float or array-like
            Scaled vegetation index

        Returns
        -------
        lai : float or array-like
            Leaf area index [m m-2]
        
        Reference: Jones and Vaughan, Eq. 7.6

        TODO: Consider moving calc_lai() (and related functions) to ecoflydro.ortho.
        Doesn't make sense for epsilon_s and albedo, but LAI could be useful more
        generally (like NDVI).
        """
        vi_star = self.calc_vi_scaled()

        lai = - (1 / k_be) * np.log(1 - vi_star)

        if isinstance(lai,xr.DataArray):
            utils.set_crs(lai, self.T_s)

        return lai