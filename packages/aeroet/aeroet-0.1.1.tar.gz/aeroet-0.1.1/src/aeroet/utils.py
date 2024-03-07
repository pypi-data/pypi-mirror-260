#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'MIT'
__date__ = 'Wed 17 Aug 22 10:21:05'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           utils.py
Compatibility:  Python 3.10.2
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


def quadratic_formula(a,b,c):
    """
    Return the roots of a quadratic equation, ax^2 + bx + c = 0.

    Parameters
    ----------
    a : float
        Quadratic term.

    b : float
        Linear term

    c : float
        Constant

    Returns
    -------
    root_pos : float
        The "positive" root (-b + sqrt(d)).

    root_neg : float
        The "negative" root (-b - sqrt(d)).
    """

    d = b**2 - 4*a*c
    root_pos = (- b + np.sqrt(d)) / 2*a
    root_neg = (- b - np.sqrt(d)) / 2*a

    return root_pos,root_neg


def calc_lhvap(T_K):
    """
    Calculates the latent heat of vaporization [J kg-1] of water at a given
    temperature.

    Parameters
    ----------
    T_K : float
        Temperature [K].

    Returns
    -------
    lambda_v : float
        Latent heat of vaporization [J kg-1]

    Reference: Allen et al. (1998), Eq. 3-1

    """
    # Calculate latent heat of vaporization at T
    lambda_v = (2.501 - (2.361e-3 * (T_K - 273.15))) * 1e6

    return lambda_v


def calc_gamma(c_p, T_K):

    gamma = c_p / calc_lhvap(T_K)

    return gamma

def set_crs(arr, ref_arr):

    arr.rio.set_crs(ref_arr.rio.crs)



# def calc_stefboltz(T_K):
#     """
#     Calculates the total energy radiated by a blackbody according to the
#     Stefan-Boltzmann Law.

#     Parameters
#     ----------
#     T_K : float
#         Temperature [K].

#     Returns
#     -------
#     M : float
#         Emitted blackbody radiance [W m-2]

#     """

#     M = SIGMA * T_K**4

#     return M


# def calc_emissivity(e_a,T_a):
#     """
#     Estimates the atmospheric emissivity for a clear sky.

#     Parameters
#     ----------
#     e_a : float
#         Vapor pressure of air [kPa].

#     T_a : float
#         Temperature of air [K]

#     Returns
#     -------
#     epsilon_a : float
#         Atmospheric emissivity [unitless]

#     Reference: Brutsaert (1975), Eq. 11
#     Brutsaert, W. (1975) On a derivable formula for long-wave radiation
#         from clear skies, Water Resour. Res., 11(5), 742-744,
#         htpp://dx.doi.org/10.1029/WR011i005p00742.

#     NOTE: Based on tower data, this formula is not great.
#     """

#     epsilon_a = 1.24 * ((e_a * 10) / T_a )**(1./7.)

#     return epsilon_a


