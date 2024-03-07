#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Fri 03 Mar 23 18:49:59'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           atmosphere.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       Add docstrings for all functions
                Clean up code

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2023


"""

#-------------------------------------------------------------------------------
# IMPORTS 
#-------------------------------------------------------------------------------
import numpy as np

# Local imports
from ..air import AirLayer
from . import resistance as res

#-------------------------------------------------------------------------------
#  CONSTANTS
#-------------------------------------------------------------------------------
KAPPA = 0.41
c_pd = 1005.7               # specific heat capacity of dry air at constant pressure [J kg-1 K-1]
c_pv = 1996.0               # specific heat of water vapour at constant pressure [J kg-1 K-1]
EPSILON = 0.622             # ratio of molar mass of water to molar mass of dry air [unitless]
R_D = 287.058	 	        # dry gas constant (J kg-1 K-1)
R = 8.314                   # ideal gas constant (J mol-1 K-1)
# M_H2O = 0.01801528          # molar mass of water (kg mol-1)
G = 9.80665                 # gravitational acceleration [m s-1]
M_D = 0.0289635              # molar mass of dry air (kg mol-1)
gamma_d = G / c_pd


class Atmosphere():
    """
    

    Attributes
    ----------
    z0 : float | array-like
        Height of reference level [m]
    
    u0 : float | array-like
        Wind speed at reference level |[m s-1]|
    
    T_a0 : float | array-like
        Air temperature at reference level [K]
    
    p_a0 : float | array-like
        Air pressure at reference level [Pa]
    
    h_r0 : float | array-like
        Relative humidity at reference level [%]
    
    u_star : float | array-like
        Friction velocity |[m s-1]|
    
    T_star : float | array-like
        Temperature scale [K]
    
    L : float | array-like
        Obukhov length [m]
    
    LE : float | array-like
        Latent heat flux |[W m-2]|
    
    d_0 : float | array-like
        Zero-plane displacement height [m]
    
    Methods
    -------

    

    .. |[m s-1]| replace:: :math: [m s\ :sup:`-1`]
    .. |[W m-2]| replace:: :math: [W m\ :sup:`-2`]

    """
    def __init__(        
        self,
        z0,
        u0,
        T_a0,
        p_a0,
        h_r0,
        u_star,
        T_star,
        L,
        LE,
        d_0,
    ):

        # Create reference air layer
        self.air0 = AirLayer(z=z0, u=u0, T_a=T_a0, p_a=p_a0, h_r=h_r0)
        
        # Zero-plane displacement height, [m]
        self.d_0 = d_0
        # Obukhov length, L [m]
        self.L = L
        # Friction velocity, u_star [m s-1]
        self.u_star = u_star
        # Temperature scale, T_star [K]
        self.T_star = T_star
        # Humidity scale, q_star [kg kg-1]
        self.q_star = self.calc_q_star(LE, u_star)

        # Potential temperature at reference height (standardized to surface)
        self.theta_a = self.calc_theta_a(T_a=self.air0.T_a, z=z0, z_0=0., gamma=gamma_d)
        # Surface air pressure
        self.p_0 = self.calc_p_z(z=0, gamma=None)
        # Air pressure at z
        # self.p_az = self.calc_p_z(z=z, gamma=gamma_d)
    
    def describe(self):
        self_dict = {
            **{k+'0' : v for k,v in self.air0.describe().items()}, 
            **self.__dict__.copy()
        }
        return self_dict

    def calc_q_star(self, LE, u_star):
        """
        Calculate the humidity scale, q_star |[kg kg-1]|.

        Parameters
        ----------
        LE : float | array-like
            Latent heat flux |[W m-2]|.
        
        u_star : float | array-like
            Friction velocity |[m s-1]|.

        Returns
        -------
        q_star : float | array-like
            Humidity scale |[kg kg-1]|.
        
        Notes
        -----
        The humidity scale, |q_star| |[kg kg-1]|, is defined as:

        .. math::
            q_star = - \\frac{LE}{\\rho_a \\lambda_v u_star}
        
        where |rho_a| is the air density, |lambda_v| is the latent heat of 
        vaporization, and |u_star| is the friction velocity.
        
        .. |[kg kg-1]| replace:: :math: [kg kg\ :sup:`-1`]
        .. |[W m-2]| replace:: :math: [W m\ :sup:`-2`]
        .. |[m s-1]| replace:: :math: [m s\ :sup:`-1`]
        .. |rho_a| replace:: :math: `\\rho_a` [kg m\ :sup:`-3`]
        .. |lambda_v| replace:: :math:`\\lambda_v` [J kg\ :sup:`-1`]
        .. |u_star| replace:: :math: `u_*` [m s\ :sup:`-1`]

        """
        q_star = - LE / (self.air0.rho_a * self.air0.lambda_v * u_star)
        
        return q_star
    
    def calc_theta_a(self, T_a, z, z_0=0, gamma=gamma_d):
        if gamma is None:
            gamma = self.air0.calc_lapse_rate()

        theta_a = T_a + (z - z_0) * gamma
        
        return theta_a

    def calc_p_z(self, z, gamma=gamma_d):

        if gamma is None:
            gamma = self.air0.calc_lapse_rate()
        
        a = (-G * M_D) / (R * gamma)
        p_z = self.air0.p_a * ( 
            ( (self.air0.T_a + gamma * (z - self.air0.z) ) / self.air0.T_a ) **a
        )
        
        return p_z
    
    def calc_var_z(self, var, z, x_1, z1, x_star, L, d_0):

        if var == 'u':
            f = res.calc_Psi_M
        else:
            f = res.calc_Psi_H

        Psi_2 = f( (z - d_0) / L )
        Psi_1 = f( (z1 - d_0) / L )

        x_z = ( (x_star / KAPPA) * (np.log((z - d_0) / (z1 - d_0) ) -  Psi_2 + Psi_1) ) + x_1

        return x_z
    
    def calc_theta_az(self, z):

        theta_az = self.calc_var_z(
            var='theta_a', z=z, x_1=self.theta_a, z1=self.air0.z, 
            x_star=self.T_star, L=self.L, d_0=self.d_0
        )

        return theta_az
    
    def calc_u_z(self, z):

        u_z = self.calc_var_z(
            var='u', z=z, x_1=self.air0.u, z1=self.air0.z, x_star=self.u_star, L=self.L, d_0=self.d_0
        )
        return u_z
    
    def calc_q_z(self, z):

        q_az = self.calc_var_z(
            var='q', z=z, x_1=self.air0.q, z1=self.air0.z, x_star=self.q_star, L=self.L, d_0=self.d_0
        )
        return q_az
    
    
    def calc_T_az(self, z, theta_az=None, p_az=None):

        if theta_az is None:
            theta_az = self.calc_theta_az(z)
        if p_az is None:
            p_az = self.calc_p_z(z)

        T_a = theta_az * ((p_az / self.p_0)**(R_D/c_pd))
        
        return T_a
    
    def calc_h_rz(self, z, T_a=None, q=None, p_a=None):
        if T_a is None:
            T_a = self.calc_T_az(z)
        if p_a is None:
            p_a = self.calc_p_z(z)
        if q is None:
            q = self.calc_q_z(z)
        
        e_a = self.calc_e_a(q, p_a)
        e_star = self.calc_svp(T_a)

        h_rz = (e_a / e_star) * 100

        return h_rz

    def calc_e_a(self, q, p_a):
        e_a = (q * p_a) / ( EPSILON + (q * (1 - EPSILON)) )
        return e_a


    def calc_svp(self, T_a):
        T_C = T_a - 273.15
        e_star = 0.611 * np.exp((17.502 * T_C) / (T_C + 240.97))
        return e_star
    
    def calc_z_vals(self, z):

        theta_az = self.calc_theta_az(z)
        q_z = self.calc_q_z(z)
        p_az = self.calc_p_z(z=z, gamma=gamma_d)
        T_az = self.calc_T_az(z, theta_az=theta_az, p_az=p_az)


        z_dict = {
            'z' : z,
            'theta_a' : theta_az,
            'u' : self.calc_u_z(z),
            'q' : q_z,
            'p_a' : p_az,
            'T_a' : T_az,
            'e_a' : self.calc_e_a(q_z, p_az),
            'e_star' : self.calc_svp(T_az),
            'h_r' : self.calc_h_rz(z, T_az, q_z, p_az)
        }

        return z_dict