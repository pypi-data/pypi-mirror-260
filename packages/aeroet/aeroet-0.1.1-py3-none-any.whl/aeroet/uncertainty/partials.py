#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Wed 11 Jan 23 15:51:50'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           partials.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2023


"""


# CONSTANTS
c_pd = 1005.7               # specific heat capacity of dry air at constant pressure [J kg-1 K-1]
c_pv = 1996.0               # specific heat of water vapour at constant pressure [J kg-1 K-1]
EPSILON = 0.622             # ratio of molar mass of water to molar mass of dry air [unitless]
R_D = 287.058	 	        # dry gas constant (J kg-1 K-1)
R = 8.314                   # ideal gas constant (J mol-1 K-1)
M_H2O = 0.01801528          # molar mass of water (kg mol-1)
SIGMA = 5.67036713e-08 		# Stefan-Boltzmann constant [W m-2 K-4]

# FUNCTIONS

'''
PROPERTIES OF AN AIR LAYER
z : float
    Height of the air layer (and met data measurements) [m]
u : float | array-like
    Wind speed [m s-1]
T_a : float | array-like
    Air temperature [K]
p_a : float | array-like
    Air pressure [kPa]
RH : float | array-like
    Relative humidity [%]
e_a : float | array-like, optional
    Vapor pressure of air [kPa]
c_p : float | array-like, optional
    Heat capacity of air [J kg-1 K-1], by default None
rho_a : float | array-like, optional
    Density of air [kg m-3], by default None
q
theta_a
theta_v
vpd

Can calculate svp, epsilon_a

'''

def calc_dea_dTa(airlayer):
    """
    Calculate the derivative of vapor pressure with respect to air temperature.

    Returns
    -------
    dea_dTa : float
        Derivative of vapor pressure with respect to air temperature |[kPa K-1]|.

    Notes
    -----
    The derivative of vapor pressure (|e_a|) with respect to air temperature (|T_a|)
    is:

    .. math::

        \\frac{\partial e_a}{\partial T_a} = \\frac{17.502 \\cdot 240.97 \\cdot e_a}{(T_a - 273.15 + 240.97)^2}

    .. |[kPa K-1]| replace:: :math: [kPa K\ :sup:`-1`]
    .. |dea_dTa| replace:: :math:`\\frac{\partial e_a}{\partial T_a}` [kPa/K]
    .. |e_a| replace:: :math:`e_a` [kPa]
    .. |T_a| replace:: :math:`T_a` [K]

    See Also
    --------
    calc_dea_dhr
        The derivative of vapor pressure with respect to relative humidity.

    """
    dea_dTa = (17.502 * 240.97 * airlayer.e_a) / ((airlayer.T_a - 273.15 + 240.97) ** 2)
    return dea_dTa

def calc_dea_dhr(airlayer):
    """
    Calculate the derivative of vapor pressure with respect to relative humidity.

    Returns
    -------
    dea_dhr : float
        Derivative of vapor pressure with respect to relative humidity |[kPa %]|.

    Notes
    -----
    This function computes the derivative of vapor pressure (e_a) with respect to relative humidity (hr)
    as a constant value (1/100):

    .. math::

        \\frac{\partial e_a}{\partial h_r} = \\frac{1}{100}

    .. |[kPa %]| replace:: :math: [kPa %\ :sup:`-1`]
    .. |dea_dhr| replace:: :math:`\\frac{\partial e_a}{\partial h_r}` [kPa/%]
    .. |e_a| replace:: :math:`e_a` [kPa]

    See Also
    --------
    calc_dea_dTa
        The derivative of vapor pressure with respect to air temperature.
    """
    dea_dhr = airlayer.calc_svp() / 100.0
    return dea_dhr

def calc_deps_a_dTa(airlayer):
    """
    Calculate the derivative of emissivity of air with respect to air temperature.

    Returns
    -------
    deps_a_dTa : float
        Derivative of emissivity of air with respect to air temperature [-].

    Notes
    -----
    The derivative of the emissivity of air (|eps_a|) with 
    respect to air temperature (|T_a|) is:

    .. math::

        \\frac{{d(\\varepsilon_a)}}{{dT_a}} = \\frac{1}{7} \\varepsilon_a \\left(\\frac{{17.502 \\cdot 240.97}}{{(T_a - 273.15 + 240.97)^2}} - \\frac{1}{{T_a}}\\right)

    .. |deps_a_dTa| replace:: :math:`\\frac{{d(\\varepsilon_a)}}{{dT_a}}` [-]
    .. |eps_a| replace:: :math:`\\varepsilon_a` [-]
    .. |T_a| replace:: :math:`T_a` [K]

    See Also
    --------
    calc_deps_a_dhr
        The derivative of emissivity of air with respect to relative humidity.
    """
    eps_a = airlayer.calc_emissivity()
    deps_a_dTa = (1.0 / 7.0) * eps_a * (
        ((17.502 * 240.97) / ((airlayer.T_a - 273.15 + 240.97) ** 2))
        - (1 / airlayer.T_a)
    )
    return deps_a_dTa

def calc_deps_a_dhr(airlayer):
    """
    Calculate the derivative of emissivity of air with respect to relative humidity.

    Returns
    -------
    deps_a_dhr : float
        Derivative of emissivity of air with respect to relative humidity [-].

    Notes
    -----
    This function computes the derivative of the emissivity of air (|eps_a|) with 
    respect to relative humidity (|h_r|) using the simplified relation:

    .. math::

        \\frac{\\partial \\varepsilon_a}{\\partial dhr}} = \\frac{1.24}{7} \\left(\\frac{{10 \\cdot e_a}}{{T_a}}\\right)^{-6/7} \\frac{{e^*}}{{10 \\cdot T_a}}

    .. |deps_a_dhr| replace:: :math:`\\frac{\\partial \\varepsilon_a }{{d h_r}}` [-]
    .. |eps_a| replace:: :math:`\\varepsilon_a` [-]
    .. |h_r| replace:: :math:`h_r` [%]
    .. |e_a| replace:: :math:`e_a` [kPa]
    .. |T_a| replace:: :math:`T_a` [K]
    .. |e^*| replace:: :math:`e^*` [kPa]
    """
    e_star = airlayer.calc_svp()
    deps_a_dhr = (1.24 / 7.0) * ((10.0 * airlayer.e_a / airlayer.T_a) ** (-6.0 / 7.0)) * (
        e_star / (10.0 * airlayer.T_a)
    )
    return deps_a_dhr




# # VAPOUR PRESSURE
# def calc_dea_dTa(airlayer):

#     dea_dTa = (17.502 * 240.97 * airlayer.e_a) / ((airlayer.T_a - 273.15 + 240.97)**2) 

#     return dea_dTa

# def calc_dea_dhr(airlayer):

#     dea_dhr = airlayer.calc_svp() / 100.

#     return dea_dhr


# # EMISSIVITY OF AIR
# def calc_deps_a_dTa(airlayer):

#     eps_a = airlayer.calc_emissivity()

#     deps_a_dTa = ( (1. / 7.) * eps_a * (
#         ((17.502 * 240.97) / ((airlayer.T_a - 273.15 + 240.97)**2)  ) 
#         - (1 / airlayer.T_a) 
#     ) )

#     return deps_a_dTa

# def calc_deps_a_dhr(airlayer):

#     e_star = airlayer.calc_svp()

#     deps_a_dhr = ( (1.24 / 7.) * 
#         ((10. * airlayer.e_a / airlayer.T_a)**(-6./7.)) * 
#         ( e_star / (10. * airlayer.T_a) ) 
#     )

#     return deps_a_dhr


# SPECIFIC HUMIDITY
def calc_dq_dTa(airlayer):
    
    dea_dTa = calc_dea_dTa(airlayer)
    dq_dTa = ( (EPSILON * airlayer.p_a) / ( (airlayer.p_a - ( airlayer.e_a * (1 - EPSILON) ) )**2 ) ) * dea_dTa

    return dq_dTa

def calc_dq_dhr(airlayer):

    dea_dhr = calc_dea_dhr(airlayer)
    dq_dhr = ( (EPSILON * airlayer.p_a) / ( (airlayer.p_a - ( airlayer.e_a * (1 - EPSILON) ) )**2 ) ) * dea_dhr

    return dq_dhr

def calc_dq_dpa(airlayer):

    dq_dpa =  (-EPSILON * airlayer.e_a) / ( (airlayer.p_a - airlayer.e_a * (1 - EPSILON))**2 )

    return dq_dpa


# HEAT CAPACITY
def calc_dcp_dTa(airlayer):

    dq_dTa = calc_dq_dTa(airlayer)

    dcp_dTa = (c_pv - c_pd) * dq_dTa

    return dcp_dTa

def calc_dcp_dhr(airlayer):

    dq_dhr = calc_dq_dhr(airlayer)

    dcp_dhr = (c_pv - c_pd) * dq_dhr

    return dcp_dhr

def calc_dcp_dpa(airlayer):

    dq_dpa = calc_dq_dpa(airlayer)

    dcp_dpa = (c_pv - c_pd) * dq_dpa

    return dcp_dpa



# AIR DENSITY
def calc_drho_dTa(airlayer):

    dea_dTa = calc_dea_dTa(airlayer)
    
    drho_dTa = - (1 / airlayer.T_a) * ( ((1 - EPSILON) / R_D) * dea_dTa + airlayer.rho_a )

    return drho_dTa

def calc_drho_dhr(airlayer):

    drho_dhr = - ((1 - EPSILON) / (R_D * airlayer.T_a)) * calc_dea_dhr(airlayer)
    
    return drho_dhr

def calc_drho_dpa(airlayer):

    drho_dpa = 1000 / (R_D * airlayer.T_a)

    return drho_dpa


# POTENTIAL TEMPERATURE
def calc_dtheta_dTa(airlayer):
    
    # dtheta_dTa = (100. / airlayer.p_a )**(R_D / c_pd)
    dtheta_dTa = 1

    return dtheta_dTa

def calc_dtheta_dpa(airlayer):

    # dtheta_dpa = - (R_D / c_pd) * (airlayer.theta_a / airlayer.p_a)
    dtheta_dpa = 0.

    return dtheta_dpa

# LATENT HEAT OF VAPORIZATION
def calc_dlhvap_dTa(airlayer=None):
    return -2.361e3

#-------------------------------------------------------------------------------
# RADIATION COMPONENTS
#-------------------------------------------------------------------------------
# LONGWAVE IN
def calc_dLWin_dTa(airlayer, epsilon_s=0.98):

    deps_a_dTa = calc_deps_a_dTa(airlayer)

    dLWin_dTa = (
        SIGMA * epsilon_s * (airlayer.T_a**3) * 
        (4 * airlayer.calc_emissivity() + airlayer.T_a * deps_a_dTa)
    )

    return dLWin_dTa

def calc_dLWin_dhr(airlayer, epsilon_s=0.98):

    deps_a_dhr = calc_deps_a_dhr(airlayer)

    dLWin_dhr = ( SIGMA * epsilon_s * (airlayer.T_a**4) * deps_a_dhr )

    return dLWin_dhr


# LONGWAVE OUT
def calc_dLWout_dTs(T_s, epsilon_s):

    dLWout_dTs = (-4 * SIGMA * epsilon_s * (T_s**3))

    return dLWout_dTs

#-------------------------------------------------------------------------------
# NET RADIATION
#-------------------------------------------------------------------------------

# def calc_dRn_dRsw(albedo):

#     dRn_dRsw = 1 - albedo

#     return dRn_dRsw


#-------------------------------------------------------------------------------
# SENSIBLE HEAT FLUX
#-------------------------------------------------------------------------------
def calc_dH_dTs(airlayer, r_H, p_s=100.):

    # theta_coeff = (100. / p_s) ** (R_D / c_pd)
    dtheta_dTa = calc_dtheta_dTa(airlayer)

    dH_dTs = airlayer.rho_a * airlayer.c_p * dtheta_dTa / r_H

    return dH_dTs

def calc_dH_drH(airlayer, r_H, theta_s):
    
    dH_drH = - airlayer.rho_a * airlayer.c_p * ((theta_s - airlayer.theta_a) / (r_H**2))

    return dH_drH


def calc_dH_dTa(airlayer, r_H, theta_s):

    # theta_coeff = airlayer.theta_a / airlayer.T_a
    dtheta_dTa = calc_dtheta_dTa(airlayer)
    # theta_s = T_s * theta_coeff

    drho_dTa = calc_drho_dTa(airlayer)
    dcp_dTa = calc_dcp_dTa(airlayer)

    dH_dTa = (1 / r_H) * (
        ( ( drho_dTa * airlayer.c_p + dcp_dTa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) ) 
        - airlayer.rho_a * airlayer.c_p * dtheta_dTa
    )

    return dH_dTa


def calc_dH_dhr(airlayer, r_H, theta_s):
    
    # theta_s = T_s * (airlayer.theta_a / airlayer.T_a)

    drho_dhr = calc_drho_dhr(airlayer)
    dcp_dhr = calc_dcp_dhr(airlayer)

    dH_dhr = ((theta_s - airlayer.theta_a) / r_H) * (drho_dhr * airlayer.c_p + dcp_dhr * airlayer.rho_a)

    return dH_dhr


# NOTE: dH_dpa derivatives might change/should change (at the least need to be 
# cleaned up) due to different theta_a calcs


# def calc_dH_dpa(airlayer, r_H, theta_s, p_s):

#     # theta_s = T_s * (airlayer.theta_a / airlayer.T_a)

#     drho_dpa = calc_drho_dpa(airlayer)
#     dcp_dpa = calc_dcp_dpa(airlayer)

#     dtheta_dpa = calc_dtheta_dpa(airlayer)

#     if isinstance(p_s, float):
#         if p_s == airlayer.p_a:
#             dH_dpa = (1 / r_H) * ( 
#                 ( ( drho_dpa * airlayer.c_p + dcp_dpa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) )
#                 + airlayer.rho_a * airlayer.c_p * dtheta_dpa
#             )
#         else:
#             dH_dpa = (1 / r_H) * ( 
#                 ( ( drho_dpa * airlayer.c_p + dcp_dpa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) )
#                 - airlayer.rho_a * airlayer.c_p * dtheta_dpa
#             )
#     else:
#         if (p_s == airlayer.p_a).sum() == len(airlayer.p_a):
#             dH_dpa = (1 / r_H) * ( 
#                 ( ( drho_dpa * airlayer.c_p + dcp_dpa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) )
#                 + airlayer.rho_a * airlayer.c_p * dtheta_dpa
#             )
#         else:
#             dH_dpa = (1 / r_H) * ( 
#                 ( ( drho_dpa * airlayer.c_p + dcp_dpa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) )
#                 - airlayer.rho_a * airlayer.c_p * dtheta_dpa
#             )    

#     return dH_dpa

def calc_dH_dpa(airlayer, r_H, theta_s, p_s=None):

    # theta_s = T_s * (airlayer.theta_a / airlayer.T_a)

    drho_dpa = calc_drho_dpa(airlayer)
    dcp_dpa = calc_dcp_dpa(airlayer)

    dtheta_dpa = calc_dtheta_dpa(airlayer)

    dH_dpa = (1 / r_H) * ( 
        ( ( drho_dpa * airlayer.c_p + dcp_dpa * airlayer.rho_a ) * (theta_s - airlayer.theta_a) )
        - airlayer.rho_a * airlayer.c_p * dtheta_dpa
    ) 

    return dH_dpa

def calc_dH_dps(airlayer, r_H, theta_s, p_s):


    if isinstance(p_s, float):
        if p_s == airlayer.p_a:
            dH_dps = calc_dH_dpa(airlayer, r_H, theta_s, p_s)
        else:
            dH_dps = ((airlayer.rho_a * airlayer.c_p) / r_H ) * (- (R_D / c_pd) * (theta_s / p_s))
    else:
        if (p_s == airlayer.p_a).sum() == len(airlayer.p_a):
            dH_dps = calc_dH_dpa(airlayer, r_H, theta_s, p_s)
        else:
            dH_dps = ((airlayer.rho_a * airlayer.c_p) / r_H ) * (- (R_D / c_pd) * (theta_s / p_s))

    return dH_dps



#-------------------------------------------------------------------------------
# LATENT HEAT FLUX PARTIAL DERIVATIVES
#-------------------------------------------------------------------------------

# SURFACE TEMPERATURE
def calc_dLE_dTs(airlayer, r_H, epsilon_s, T_s, p_s):

    # theta_coeff = airlayer.theta_a/airlayer.T_a
    # theta_coeff = (100. / p_s) ** (R_D / c_pd)
    dtheta_dTa = calc_dtheta_dTa(airlayer)
    dLWout_dTs = calc_dLWout_dTs(T_s, epsilon_s)

    dLE_dTs = dLWout_dTs - (airlayer.rho_a * airlayer.c_p * dtheta_dTa / r_H)

    return dLE_dTs

# RESISTANCE TO HEAT TRANSFER
def calc_dLE_dra(airlayer, r_H, theta_s):

    # theta_coeff = airlayer.theta_a/airlayer.T_a
    # theta_s = theta_coeff * T_s

    dLE_drH = airlayer.rho_a * airlayer.c_p * ((theta_s - airlayer.theta_a) / (r_H **2))

    return dLE_drH

# SHORTWAVE IN
def calc_dLE_dRsw(albedo):
    
    dLE_dRsw = 1 - albedo

    return dLE_dRsw

# AIR TEMPERATURE
def calc_dLE_dTa(airlayer, r_H, theta_s):

    dLWin_dTa = calc_dLWin_dTa(airlayer)
    dH_dTa = calc_dH_dTa(airlayer, r_H, theta_s)

    dLE_dTa = dLWin_dTa - dH_dTa

    return dLE_dTa

# RELATIVE HUMIDITY
def calc_dLE_dhr(airlayer, r_H, theta_s):

    dLWin_dhr = calc_dLWin_dhr(airlayer)
    dH_dhr = calc_dH_dhr(airlayer, r_H, theta_s)

    dLE_dhr = dLWin_dhr - dH_dhr

    return dLE_dhr

# AIR PRESSURE
def calc_dLE_dpa(airlayer, r_H, theta_s, p_s):

    dLE_dpa = - calc_dH_dpa(airlayer, r_H, theta_s, p_s)

    return dLE_dpa

# SURFACE PRESSURE
def calc_dLE_dps(airlayer, r_H, theta_s, p_s):

    dLE_dps = - calc_dH_dps(airlayer, r_H, theta_s, p_s)

    return dLE_dps



# WIND SPEED
def calc_dLE_du(airlayer, r_aH, theta_s):

    # theta_s = T_s * (airlayer.theta_a / airlayer.T_a)
    dLE_du = - airlayer.rho_a * airlayer.c_p * ((theta_s - airlayer.theta_a) / (airlayer.u * r_aH))

    return dLE_du

# SOIL HEAT FLUX
def calc_dLE_dG(G=0.):
    return -1.

#-------------------------------------------------------------------------------
# BOWEN RATIO
#-------------------------------------------------------------------------------

def calc_dbeta_dTa(air1, air2, d_i, gamma_i=2):

    air_dict = {1 : air1, 2 : air2}

    c_p = air_dict.get(gamma_i).c_p 
    lambda_v = air_dict.get(gamma_i).lambda_v


    dtheta_dTa = calc_dtheta_dTa( air_dict.get(d_i) )
    dq_dTa = calc_dq_dTa( air_dict.get(d_i) )

    dbeta_dT = (
        (c_p / lambda_v) *
        ( 1 / ( (air2.q - air1.q)**2 ) ) *
        ( ( (air2.q - air1.q) * dtheta_dTa ) - ( (air2.theta_a - air1.theta_a) * dq_dTa ) )
    )

    if d_i == 1:
        dbeta_dT = dbeta_dT * -1

    if d_i == gamma_i:

        dcp_dTa = calc_dcp_dTa( air_dict.get(d_i) )
        dlv_dTa = calc_dlhvap_dTa( air_dict.get(d_i) )
        
        ex = ( 
            ( (air2.theta_a - air1.theta_a) / (air2.q - air1.q) ) *
            ( lambda_v * dcp_dTa - c_p * dlv_dTa) *
            ( 1 / (lambda_v**2) ) 
        )
    
        dbeta_dT = dbeta_dT + ex

    return dbeta_dT

def calc_dbeta_dhr(air1, air2, d_i, gamma_i=2):
    air_dict = {1 : air1, 2 : air2}
    
    c_p = air_dict.get(gamma_i).c_p 
    lambda_v = air_dict.get(gamma_i).lambda_v

    dq_dhr = calc_dq_dhr( air_dict.get(d_i) )

    dbeta_dhr = (
        (c_p / lambda_v) *
        ( 1 / ( (air2.q - air1.q)**2 ) ) *
        ( (air2.theta_a - air1.theta_a) * dq_dhr )
    )

    if d_i == 2:
        dbeta_dhr = dbeta_dhr * -1
    
    if d_i == gamma_i:
        dcp_dhr = calc_dcp_dhr(air_dict.get(d_i))
        
        ex = ( 
            ( (air2.theta_a - air1.theta_a) / (air2.q - air1.q) ) *
            ( (1 / lambda_v) * dcp_dhr)
        )
    
        dbeta_dhr = dbeta_dhr + ex
    
    return dbeta_dhr

def calc_dbeta_dpa(air1, air2, d_i, gamma_i=2):
    air_dict = {1 : air1, 2 : air2}
    
    c_p = air_dict.get(gamma_i).c_p 
    lambda_v = air_dict.get(gamma_i).lambda_v

    dtheta_dpa = calc_dtheta_dpa( air_dict.get(d_i) )
    dq_dpa = calc_dq_dpa( air_dict.get(d_i) )

    dbeta_dpa = (
        (c_p / lambda_v) *
        ( 1 / ( (air2.q - air1.q)**2 ) ) *
        ( ((air2.q - air1.q) * dtheta_dpa) - ((air2.theta_a - air1.theta_a) * dq_dpa) )
    )

    if d_i == 1:
        dbeta_dpa = dbeta_dpa * -1

    if d_i == gamma_i:

        dcp_dpa = calc_dcp_dpa( air_dict.get(d_i) )
        
        ex = ( 
            ( (air2.theta_a - air1.theta_a) / (air2.q - air1.q) ) *
            ( (1 / lambda_v) * dcp_dpa)
        )
    
        dbeta_dpa = dbeta_dpa + ex

    return dbeta_dpa

def calc_dbeta_dG(G=0.):
    return 0.

#-------------------------------------------------------------------------------
# AVAILABLE ENERGY
#-------------------------------------------------------------------------------

def calc_dQav_dTs(T_s, epsilon_s=0.98):

    dQav_dTs = (-4 * SIGMA * epsilon_s * (T_s**3))

    return dQav_dTs

def calc_dQav_dTa(airlayer):

    dQav_dTa = calc_dLWin_dTa(airlayer)

    return dQav_dTa

def calc_dQav_dhr(airlayer):

    dQav_dhr = calc_dLWin_dhr(airlayer)

    return dQav_dhr

def calc_dQav_dG(G=0.):
    return -1.

#-------------------------------------------------------------------------------
# LE FROM BOWEN RATIO
#-------------------------------------------------------------------------------

def calc_dLEbr_dQav(beta):

    dLEbr_dQav = 1 / (1 + beta)

    return dLEbr_dQav

def calc_dLEbr_dbeta(beta, Q_av):
    
    dLEbr_dbeta = - ( Q_av) / ( (1 + beta)**2 )

    return dLEbr_dbeta

dbeta_dict = {
    'T_a' : calc_dbeta_dTa,
    'h_r' : calc_dbeta_dhr,
    'p_a' : calc_dbeta_dpa,
    'G' : calc_dbeta_dG
}

dQav_dict = {
    'T_s' : calc_dQav_dTs,
    'T_a' : calc_dQav_dTa,
    'h_r' : calc_dQav_dhr,
    'G' : calc_dQav_dG
}

def calc_dLEbr_dx(var, beta, Q_av, air1, air2, d_i, gamma_i):

    if d_i == 1:
        dQav_dx = dQav_dict.get(var, lambda _ : 0)(air1)
    else:
        dQav_dx = 0

    dbeta_dx = dbeta_dict.get(var)(air1, air2, d_i, gamma_i)

    dLEbr_dx = ( ((1 + beta) * dQav_dx) - (Q_av * dbeta_dx) ) / ( (1 + beta)**2 )

    return dLEbr_dx

def calc_dLEbr_dTs(beta, T_s, epsilon_s=0.98):

    dLEbr_dTs = calc_dQav_dTs(T_s, epsilon_s) / (1 + beta)

    return dLEbr_dTs

def calc_dLEbr_dRsw(albedo, beta):

    dLEbr_dRsw = (1 - albedo) / (1 + beta)
    
    return dLEbr_dRsw
