#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'MIT'
__date__ = 'Thu 13 Oct 22 15:45:11'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           temp.py
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

# FUNCTIONS


SIGMA = 5.67036713e-08 



def calc_wvc(h_r, T_a):
    """
    Calculate the water vapour content of air [mm Hg]

    Parameters
    ----------
    h_r : float | array-like
        Relative humidity [%]
    T_a : float | array-like
        Air temperature [K]

    Returns
    -------
    wvc : float | array-like
         Water vapour concentration [mm Hg]
        
    SOURCE: 
    """
    h1 = 6.8455e-7
    h2 = -2.7816e-4
    h3 = 6.939e-2
    h4 = 1.5587

    T_aC = T_a - 273.15

    wvc = (h_r/100) * np.exp( 
        h1 * T_aC**3 + h2 * T_aC**2 + h3 * T_aC + h4
    )

    return wvc


def calc_tau(wvc, d):
    """
    Calculate atmospheric transmissivity 

    Parameters
    ----------
    wvc : float | array-like
        Water vapour concentration [mm Hg]
    d : float | array-like
        Distance between surface and sensor [m]

    Returns
    -------
    tau : float | array-like
        Atmospheric transmissivity.
    
    SOURCE: 
    """

    K_atm = 1.9
    a1 = 6.569e-3
    a2 = 0.01262
    b1 = -2.276e-3
    b2 = -6.67e-3

    tau = K_atm * np.exp( -(d**(1/2)) * (a1 + b1 * wvc**(1/2)) ) + \
         (1 - K_atm) * np.exp( -(d**(1/2)) * (a2 + b2 * wvc**(1/2)) )

    return tau




def calc_LW_atm(T_a, tau):
    """
    Calculate the longwave radiation emitted by the atmosphere between the surface and a sensor.

    Parameters
    ----------
    T_a : float | array-like
        Air temperature [K]
    tau : float | array-like
        Atmospheric transmissivity

    Returns
    -------
    LW_atm : float | array-like
        Longwave radiation emitted by the atmosphere between the surface and a sensor [W m-2].
    """

    LW_atm = (1 - tau) * SIGMA * (T_a**4)

    return LW_atm

def calc_LW_refl(LW_IN, epsilon_s):
    """
    Calculate the incoming longwave radiation reflected by a surface.

    Parameters
    ----------
    LW_IN : float | array-like
        Incoming longwave radiation [W m-2]
    epsilon_s : float | array-like
        Surface emissivity

    Returns
    -------
    LW_refl : float | array-like
        Incoming longwave radiation reflected by a surface [W m-2].
    """
    LW_refl = (1 - epsilon_s) * LW_IN

    return LW_refl


def calc_T_s_LW(T_b, LW_IN, T_a, tau, epsilon_s):

    LW_sens = SIGMA * T_b**4
    LW_atm = calc_LW_atm(T_a, tau)              # LW radiation emitted by atmosphere btw surface and sensor
    LW_refl = calc_LW_refl(LW_IN, epsilon_s)    # Incoming LW radiation reflected by surface

    # tes = tau * epsilon_s * SIGMA

    # T_s = ( ( LW_OUT / (tau * epsilon_s * SIGMA) ) - \
    #         ( ((1 - epsilon_s) / (epsilon_s * SIGMA)) * LW_IN ) - \
    #         ( LW_atm / (tau * epsilon_s) ) 
    #     ) ** (1/4)


    T_s = ( ( LW_sens - tau * LW_refl - LW_atm ) / (tau * epsilon_s * SIGMA) ) ** (1/4)
    
    return T_s



def calc_T_s_EMP(T_b, slope, intercept):

    T_s = slope * T_b + intercept

    return T_s


def correct_T_s(T_s, method=None, **kwargs):

    if method == 'LW':
        T_s_corr = calc_T_s_LW(T_b = T_s, **kwargs)
    elif method == 'empirical':
        T_s_corr = calc_T_s_EMP(T_b = T_s, **kwargs)
    else:
        return T_s
    
    return T_s_corr