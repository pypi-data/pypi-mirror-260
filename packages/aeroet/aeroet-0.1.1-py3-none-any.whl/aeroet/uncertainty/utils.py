#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Thu 16 Feb 23 14:21:07'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           utils_sensitivity.py
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


#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import itertools
import numpy as np
import pandas as pd


# import model
from .. import AirLayer, Surface, Radiation, radiation #, Atmosphere
from .atmosphere import Atmosphere

from . import partials 
# import resistance as res

#-------------------------------------------------------------------------------
#  VARIABLES
#-------------------------------------------------------------------------------
# CONSTANTS
KAPPA = 0.41
c_pd = 1005.7               # specific heat capacity of dry air at constant pressure [J kg-1 K-1]
c_pv = 1996.0               # specific heat of water vapour at constant pressure [J kg-1 K-1]
EPSILON = 0.622             # ratio of molar mass of water to molar mass of dry air [unitless]
R_D = 287.058	 	        # dry gas constant (J kg-1 K-1)
R = 8.314                   # ideal gas constant (J mol-1 K-1)
M_H2O = 0.01801528          # molar mass of water (kg mol-1)
SIGMA = 5.67036713e-08 		# Stefan-Boltzmann constant [W m-2 K-4]
G = 9.80665                 # gravitational acceleration [m s-1]
M_D = 0.0289635              # molar mass of dry air (kg mol-1)
gamma_d = G / c_pd

var_dict = {
    'T_s' : {
        'symbol' : r"$T_s$",
        'label' : r"$T_s$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTs',
        'tower_col' : 'T_s_CNR4',
    },
    'r_H': {
        'symbol' : r"$r_{H}$",
        'label' : r"$r_{H}$ (s m$^{-1}$)",
        'unit' : r"s m$^{-1}$",
        'der' : 'dLE_drH',
        'tower_col' : 'r_H_CNR4',
    },
    'T_a' : {
        'symbol' : r"$T_a$",
        'label' : r"$T_a$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa',
        'der_br' : ['dLE_dTa1', 'dLE_dTa2'],
    },
    'h_r' : {
        'symbol' : r"$h_r$",
        'label' : r"$h_r$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr',
        'der_br' : ['dLE_dhr1', 'dLE_dhr2'],
    },
    'SW_IN' : {
        'symbol' : r"$R_{\mathrm{SW}}^{\downarrow}$",
        'label' : r"$R_{\mathrm{SW}}^{\downarrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'der' : 'dLE_dRsw',
    },
    'p_a' : {
        'symbol' : r"$p_a$",
        'label' : r"$p_a$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa',
        'der_br' : ['dLE_dpa1', 'dLE_dpa2'],
    },    
    'p_s' : {
        'symbol' : r"$p_s$",
        'label' : r"$p_s$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dps',
    },    
    'T_a1' : {
        'symbol' : r"$T_{a1}$",
        'label' : r"$T_{a1}$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa1',
    },
    'T_a2' : {
        'symbol' : r"$T_{a2}$",
        'label' : r"$T_{a2}$ (°C)",
        'unit' : r"°C",
        'der' : 'dLE_dTa2',
    },
    'h_r1' : {
        'symbol' : r"$h_{r1}$",
        'label' : r"$h_{r1}$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr1',
    },
    'h_r2' : {
        'symbol' : r"$h_{r2}$",
        'label' : r"$h_{r2}$ (%)",
        'unit' : r"%",
        'der' : 'dLE_dhr2',
    },
    'p_a1' : {
        'symbol' : r"$p_{a1}$",
        'label' : r"$p_{a1}$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa1',
    },   
    'p_a2' : {
        'symbol' : r"$p_{a2}$",
        'label' : r"$p_{a2}$ (kPa)",
        'unit' : r"kPa",
        'der' : 'dLE_dpa2',
    },     
    'LE' : {
        'symbol' : r"$\lambda E$",
        'label' : r"$\lambda E$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
    },
    'H' : {
        'symbol' : r"$H$",
        'label' : r"$H$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
    },
    'dLE_dTs' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_s}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_s}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_drH' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial r_{H}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial r_{H}}$ (W m$^{-2}$ s$^{-1}$ m)"
    },
    'dLE_dTa' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_a}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_a}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dhr' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_r}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_r}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dRsw' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{SW}}^{\downarrow}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial R_{\mathrm{SW}}^{\downarrow}}$ (W m$^{-2}$ W$^{-1}$ m$^{2}$)"
    },
    'dLE_dpa' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_a}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_a}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dps' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_s}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_s}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dTa1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_{a1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_{a1}}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dTa2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial T_{a2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial T_{a2}}$ (W m$^{-2}$ °C$^{-1}$)"
    },
    'dLE_dhr1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_{r1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_{r1}}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dhr2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial h_{r2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial h_{r2}}$ (W m$^{-2}$ %$^{-1}$)"
    },
    'dLE_dpa1' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_{a1}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_{a1}}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'dLE_dpa2' : {
        'symbol' : r"$\frac{\partial \lambda E}{\partial p_{a2}}$",
        'label' : r"$\frac{\partial \lambda E}{\partial p_{a2}}$ (W m$^{-2}$ kPa$^{-1}$)"
    },
    'u' : {
        'symbol' : r"$u$",
        'label' : r"$u$ (m s$^{-1}$)",
        'unit' : r"m s$^{-1}$",
    },
    'LW_IN' : {
        'symbol' : r"$R_{\mathrm{LW}}^{\downarrow}$",
        'label' : r"$R_{\mathrm{LW}}^{\downarrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
        'der' : 'dLE_dRsw',
    },    
    'SW_OUT' : {
        'symbol' : r"$R_{\mathrm{SW}}^{\uparrow}$",
        'label' : r"$R_{\mathrm{SW}}^{\uparrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
    },    
    'LW_OUT' : {
        'symbol' : r"$R_{\mathrm{LW}}^{\uparrow}$",
        'label' : r"$R_{\mathrm{LW}}^{\uparrow}$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
    },    
    'R_n' : {
        'symbol' : r"$R_n$",
        'label' : r"$R_n$ (W m$^{-2}$)",
        'unit' : r"W m$^{-2}$",
    },  
    'u_star' : {
        'symbol' : r"$u_{*}$",
        'label' : r"$u_{*}$ (m s$^{-1}$)",
        'unit' : r"m s$^{-1}$",
        'tower_col' : 'ustar',
    },
}

#-------------------------------------------------------------------------------
# GENERAL UTILITY FUNCTIONS
#-------------------------------------------------------------------------------


def filter_df(df : pd.DataFrame, filt : dict) -> pd.DataFrame:

    filtered = df.loc[(df[list(filt)] == pd.Series(filt)).all(axis=1)]

    return filtered

def get_piv(df, x='T_s', y='r_H', c='LE', mask_vals={'T_a' : 20., 'h_r' : 50.}):

    piv = filter_df(df, mask_vals).pivot(index=y, columns=x, values=c)

    return piv

#-------------------------------------------------------------------------------
# MODEL CLASS HELPER FUNCTIONS
#-------------------------------------------------------------------------------

def create_surface(T_s, ndvi=0.95, h=1.0) -> Surface:

    surf = Surface(h=h, T_s=T_s, ndvi=ndvi, cover='homogeneous', veg='GRA')

    return surf

def correct_T_b(air : AirLayer, surf : Surface):

    surf.T_s = surf.correct_T_b(
        LW_IN = radiation.calc_LW(air.T_a, air.calc_emissivity()),
        T_a = air.T_a,
        tau = air.calc_tau(wvc=air.calc_wvc(), d=air.z - surf.h),
        epsilon_s = surf.epsilon_s
    )

def create_radiation(SW_IN, air : AirLayer, surf : Surface, G=None) -> Radiation:

    SW_OUT = radiation.calc_SW_out(SW_IN, surf.albedo)
    LW_IN = radiation.calc_LW(air.T_a, air.emissivity)
    LW_OUT = radiation.calc_LW(surf.T_s, surf.epsilon_s)
    # CREATE RADIATION OBJECT    
    rad = Radiation(SW_IN, SW_OUT, LW_IN, LW_OUT, G=G, allow_neg=True)
    # Optionally set components of radiation balance in Radiation object to be returned
    rad.set_components(SW_IN, SW_OUT, LW_IN, LW_OUT)

    return rad

def calc_H(air : AirLayer, surf : Surface, r_H, p_s = None):
    # def calc_H(self, rho_a, c_p, theta_s, theta_a, r_H):
        """
        Calculate sensible heat flux using a temperature gradient and aerodynamic 
        resistance to heat transport.
        """
        # theta_s = air.calc_theta(surf.T_s)
        if p_s is None:
            p_s = air.p_a

        theta_s = surf.T_s * (100. / p_s) ** (R_D / c_pd)

        H = air.rho_a * air.c_p * ( (theta_s - air.theta_a) / r_H )

        return H

def calc_LE(H, rad):

    LE = rad.R_n - rad.G - H

    return LE


#-------------------------------------------------------------------------------
# PARTIAL DERIVATIVE HELPER FUNCTIONS
#-------------------------------------------------------------------------------

def calc_partials(air : AirLayer, surf : Surface, r_H, p_s=None) -> dict:

    if p_s is None:
        p_s = air.p_a

    # theta_s = surf.T_s * (100. / p_s) ** (R_D / c_pd)

    dLE_dTs = partials.calc_dLE_dTs(air, r_H, surf.epsilon_s, surf.T_s, p_s)
    dLE_drH = partials.calc_dLE_dra(air, r_H, surf.theta_s)
    dLE_dTa = partials.calc_dLE_dTa(air, r_H, surf.theta_s)
    dLE_dhr = partials.calc_dLE_dhr(air, r_H, surf.theta_s)
    # dLE_dpa = partials.calc_dLE_dpa(air, r_H, surf.T_s)
    dLE_dRsw = partials.calc_dLE_dRsw(surf.albedo)
    dLE_dpa = partials.calc_dLE_dpa(air, r_H, surf.theta_s, p_s)
    # dLE_dps = partials.calc_dLE_dps(air, r_H, theta_s, p_s)

    partial_dict = {
        'dLE_dTs' : dLE_dTs,
        'dLE_drH' : dLE_drH,
        'dLE_dTa' : dLE_dTa,
        'dLE_dhr' : dLE_dhr,
        'dLE_dpa' : dLE_dpa,
        'dLE_dRsw' : dLE_dRsw,
        # 'dLE_dpa' : dLE_dpa,
        # 'dLE_dps' : dLE_dps
    }

    return partial_dict

def generate_partials(
    T_s = np.arange(0., 61., 1),
    r_H = np.arange(1.0, 101., 1),
    T_a = np.arange(0., 46., 1),
    h_r = np.arange(0., 101., 10.),
    SW_IN = 650.,
    u = 3.0,
    p_a = 99.6,
    h = 0.3,
    ndvi = 0.98,
    z = 3.8735
) -> pd.DataFrame:
    # Create surface + air layers
    surf_list = [create_surface(t_s+273.15, ndvi, h) for t_s in T_s]
    air_list = [AirLayer(z, u, a[0]+273.15, p_a, a[1]) for a in itertools.product(T_a,h_r)]
    # Calculate sensible heat flux
    H_list = [calc_H(*a) for a in itertools.product(air_list, surf_list, r_H)]
    # Create radiation layer
    # rad = [create_radiation(SW_IN, a[0], a[1]) for a in itertools.product(air_list, surf_list, r_H_list)]
    rad_list = list(np.repeat([create_radiation(SW_IN, a[0], a[1]) for a in itertools.product(air_list, surf_list)], len(r_H)))

    # Calculate LE
    LE = [calc_LE(H,r) for H,r in zip(H_list, rad_list)]
    # Calculate partial derivatives
    dLEs = [calc_partials(*a) for a in itertools.product(air_list, surf_list, r_H)]


    params = [{**a[0].describe(), **a[1].describe(), **{'r_H' : a[2]}} for a in itertools.product(air_list, surf_list, r_H)]
    rad_dicts = [r.describe() for r in rad_list]

    df = pd.concat([pd.DataFrame(params), pd.DataFrame(rad_dicts), pd.DataFrame(dLEs)], axis=1) 

    df['H'] = H_list
    df['LE'] = LE
    df.T_a = df.T_a - 273.15
    df.T_s = df.T_s - 273.15
    df['dT'] = df.T_s - df.T_a
    df['EF'] = df.LE / df.R_n

    return df


def run_LE(T_s, r_H, T_a, h_r, SW_IN, u, p_a, p_s=None, G=None, h=0.3, ndvi=0.98, z=3.8735, partials=True) -> dict:


    surf = create_surface(T_s+273.15, ndvi, h)
    air = AirLayer(z, u, T_a+273.15, p_a, h_r)

    if p_s is None:
        p_s = air.p_a
    
    H = calc_H(air, surf, r_H, p_s)
    rad = create_radiation(SW_IN, air, surf, G=G)
    LE = calc_LE(H, rad)

    if partials:
        dLEs = calc_partials(air, surf, r_H, p_s=p_s)
    else:
        dLEs = {}

    params = {
        **air.describe(), 
        **surf.describe(), 
        **{'r_H' : r_H}, 
        **rad.describe(means=False),
        **{'H' : H, 'LE' : LE},
        **dLEs
    }

    params['T_a'] = params['T_a'] - 273.15
    params['T_s'] = T_s
    params['SW_IN'] = SW_IN
    params['dT'] = params['T_s'] - params['T_a']
    params['EF'] = params['LE'] / params['R_n']

    return params


def run_le_tower(df, var_list=['T_s', 'r_H', 'T_a', 'h_r', 'SW_IN'], G=None, h=0.3, ndvi=0.98, z=3.8735, ):
    # Get names of tower variables
    tow_var_list = [var_dict[var].get('tower_col', var) for var in var_list] + ['u', 'p_a']
    tow_var_list = list(set(tow_var_list))

    tower_params = df[tow_var_list].copy()
    
    # NOTE: update below to get from var_dict--list comprehension with zip(var_list,tow_var_list) if var != tow_var
    tower_params.rename(columns={'T_s_CNR4' : 'T_s', 'r_H_CNR4' : 'r_H'}, inplace=True)
    tower_params['T_s'] = tower_params['T_s'] - 273.15
    tower_params['T_a'] = tower_params['T_a'] - 273.15

    num_dict = run_LE(**{k:np.array(v) for k,v in tower_params.to_dict('list').items()}, G=G, h=h, ndvi=ndvi, z=z)
    keys = [var_dict.get(var)['der'] for var in var_list] + ['H', 'LE']

    num_df = pd.DataFrame(dict(zip(keys,map(num_dict.get, keys))))
    # num_df.rename(columns={'H' : 'H_num', 'LE' : 'LE_num'}, inplace=True)
    num_df.set_index(tower_params.index, inplace=True)

    out_df = pd.concat([tower_params, num_df], axis=1)

    return out_df




#-------------------------------------------------------------------------------
# CANOPY SUBCLASS
#-------------------------------------------------------------------------------

class Canopy(Surface):
    def __init__(
        self, h, lai, w_l, b, T_s, ndvi, cover : str = 'homogeneous', veg : str = 'GRA'
    ):
        super().__init__(cover=cover, veg=veg, h=h, T_s=T_s, ndvi=ndvi, b=b)

        self.lai = lai
        self.w_l = w_l

    def describe(self):
        return self.__dict__.copy()





#-------------------------------------------------------------------------------
# BOWEN RATIO HELPER FUNCTIONS
#-------------------------------------------------------------------------------
def calc_beta(air1, air2, gamma_i=2):
    air_dict = {1 : air1, 2 : air2}

    c_p = air_dict.get(gamma_i).c_p 
    lambda_v = air_dict.get(gamma_i).lambda_v

    beta = (c_p / lambda_v) * ( (air2.theta_a - air1.theta_a) / (air2.q - air1.q) )

    return beta

def calc_Qav(rad : Radiation):
    Q_av = rad.R_n - rad.G
    return Q_av

def calc_LE_hat(beta, Q_av):
    LE_hat = Q_av /(1 + beta)
    return LE_hat

def calc_H_hat(beta, LE_hat):
    H_hat = beta * LE_hat
    return H_hat


def calc_br_partials(air1 : AirLayer, air2 : AirLayer, surf : Surface, beta, Q_av, gamma_i=2) -> dict:

    partial_dict = {
        'dLE_dTs' : partials.calc_dLEbr_dTs(beta, surf.T_s, surf.epsilon_s),
        'dLE_dTa1' : partials.calc_dLEbr_dx(
            var='T_a', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dLE_dTa2' : partials.calc_dLEbr_dx(
            var='T_a', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
        'dLE_dhr1' : partials.calc_dLEbr_dx(
            var='h_r', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dLE_dhr2' : partials.calc_dLEbr_dx(
            var='h_r', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
        'dLE_dpa1' : partials.calc_dLEbr_dx(
            var='p_a', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dLE_dpa2' : partials.calc_dLEbr_dx(
            var='p_a', beta=beta, Q_av=Q_av, air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
        'dLE_dRsw' : partials.calc_dLEbr_dRsw(surf.albedo, beta),
        'dLE_dQav' : partials.calc_dLEbr_dQav(beta),
        'dLE_dbeta' : partials.calc_dLEbr_dbeta(beta, Q_av),
        **calc_beta_partials(air1=air1, air2=air2, gamma_i=gamma_i),
        **calc_Qav_partials(air=air1)
    }

    return partial_dict

def calc_beta_partials(air1 : AirLayer, air2 : AirLayer, gamma_i=2) -> dict:

    partial_dict = {
        'dbeta_dTa1' : partials.calc_dbeta_dTa(
            air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dbeta_dTa2' : partials.calc_dbeta_dTa(
            air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
        'dbeta_dhr1' : partials.calc_dbeta_dhr(
            air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dbeta_dhr2' : partials.calc_dbeta_dhr(
            air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
        'dbeta_dpa1' : partials.calc_dbeta_dpa(
            air1=air1, air2=air2, d_i=1, gamma_i=gamma_i
        ),
        'dbeta_dpa2' : partials.calc_dbeta_dpa(
            air1=air1, air2=air2, d_i=2, gamma_i=gamma_i
        ),
    }
    return partial_dict

def calc_Qav_partials(air : AirLayer) -> dict :

    partial_dict = {
        'dQav_dTa1' : partials.calc_dQav_dTa(air),
        'dQav_dhr1' : partials.calc_dQav_dhr(air),
    }

    return partial_dict

def run_LE_hat(T_s, air1, air2, SW_IN, G=None, gamma_i=2, ndvi=0.98, h=0.3, partials=True) -> dict :
    
    surf = create_surface(T_s, ndvi, h)
    rad = create_radiation(SW_IN, air1, surf, G=G)

    beta = calc_beta(air1, air2, gamma_i=gamma_i)
    # if Q_av is None:
    Q_av = calc_Qav(rad)

    LE = calc_LE_hat(beta, Q_av)
    H = calc_H_hat(beta, LE)

    if partials:
        dLEs = calc_br_partials(air1, air2, surf, beta, Q_av, gamma_i)
    else:
        dLEs = {}
    
    params = {
        **{k+'1' : v for k,v in air1.describe().items()}, 
        **{k+'2' : v for k,v in air2.describe().items()}, 
        **surf.describe(), 
        **rad.describe(means=False),
        **{'beta' : beta, 'Q_av' : Q_av, 'H' : H, 'LE' : LE},
        **dLEs
    }

    params['T_a1'] = params['T_a1'] - 273.15
    params['T_a2'] = params['T_a2'] - 273.15
    params['T_s'] = T_s
    params['SW_IN'] = SW_IN
    # params['dT'] = params['T_s'] - params['T_a']
    params['EF'] = params['LE'] / params['R_n']

    return params


def create_atmosphere(df, d_0=0.65*0.3, z=3.8735, le_col='LE', calc_L=True):

    if calc_L:
        L = ((z - d_0) / df.zeta).to_numpy()
    else:
        L = df.L.to_numpy()

    atmos = Atmosphere(
        z0=3.8735, u0=df.u.to_numpy(), T_a0=df.T_a.to_numpy(), p_a0=df.p_a.to_numpy(), 
        h_r0=df.h_r.to_numpy(), u_star=df.ustar.to_numpy(), T_star=df['T*'].to_numpy(), 
        L=L, LE=df[le_col].to_numpy(), d_0=d_0
    )
    return atmos


def create_air_z(z, atmos):

    z_vals = atmos.calc_z_vals(z)
    air = AirLayer(
        z=z, u=z_vals.get('u'), T_a=z_vals.get('T_a'), p_a=z_vals.get('p_a'), h_r=z_vals.get('h_r')
    )

    return air


def run_le_br_tower(df, z1=1.5, z2=60.5, h=0.3, d_0=0.65*0.3, G=0.0, ndvi=0.98, gamma_i=2):

    atmos = create_atmosphere(df, d_0)

    air1 = create_air_z(z1, atmos)
    air2 = create_air_z(z2, atmos)

    T_s = df['T_s_CNR4'].to_numpy()
    SW_IN = df['SW_IN'].to_numpy()

    # G = df['G'].to_numpy()
    # G = 0.0

    params = run_LE_hat(T_s, air1, air2, SW_IN, G=G, ndvi=ndvi, h=h, gamma_i=gamma_i)

    return params