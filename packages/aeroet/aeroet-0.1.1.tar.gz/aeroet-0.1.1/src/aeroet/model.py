#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'MIT'
__date__ = 'Wed 24 Aug 22 13:39:37'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           model.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2022


"""


# IMPORTS
import numpy as np
import pandas as pd
import xarray as xr

from . import utils

# VARIABLES
KAPPA = 0.41        # von Karman constant [unitless]
G = 9.8             # acceleration due to gravity [m s-2]

flag_dict = {
    'NO_FLAG' : (0, 'All fluxes are good.'),
    'F_NEG_LE' : (1, 'Negative latent heat flux; forced to zero'),
    'F_NEG_H' : (2, 'Negative sensible heat flux; forced to zero.'),
    'F_ERROR' : (255, 'Arithmetic error; bad data; values should be discarded.')
}


class FluxModel:
    """
    _summary_
    """

    def __init__(self, airlayer, surface, radiation):
        """
        Parameters
        ----------
        airlayer : AirLayer
            air.AirLayer object for the model. Contains the following variables:
            z, u, T_a, p_a, e_a, c_p, h_r, 
        surface : Surface
            surface.Surface object for the model. Contains the following variables:
            h, d0, z_0m, z_0h, T_s
        radiation : Radiation
            radiation.Radiation object for the model. Contains the following variables:
            R_n, G, [SW_IN, SW_OUT, LW_IN, LW_OUT]
        """

        self.air = airlayer             # z, u, T_a, p_a, e_a, c_p, h_r, 
        self.surface = surface          # h, d0, z_0m, z_0h
        self.radiation = radiation      # R_n, G
        # self.theta_s = self.air.calc_theta(self.surface.T_s)
        # self._set_theta_s()

    def __repr__(self):
        class_name = type(self).__name__
        return '{}'.format(class_name)
    
    # def _set_theta_s(self):
    #     """
    #     Set potential surface temperature (self.surface.theta_s) for the model. 
    #     NOTE: Probably should go somewhere else?
    #     """
    #     # NOTE: It's probably worth forcing these to the same resolution regardless, 
    #     # but for now, only doing it when necessary bc resampling takes awhile.
    #     if self.radiation.R_n.shape != self.surface.T_s.shape:
    #         self.theta_s = self.air.calc_theta(
    #             self.surface.T_s.interp(x=self.radiation.R_n.x, y=self.radiation.R_n.y)
    #         )
    #     else:
    #         self.theta_s = self.air.calc_theta(self.surface.T_s)


    def get_var_stats(self, var):
        """
        Get summary statistics (min, max, mean, median, standard deviation) for 
        a variable.

        Parameters
        ----------
        var : xarray.DataArray | xarray.DataSet
            Pixel-wise variable for which to calculate summary statistics

        Returns
        -------
        stats_dict : dict
            Summary statistics for var as a dictionary.

        # NOTE: Probably will refactor.
        """
        
        stats_dict = {
            'MAX' : var.max().item(),
            'MIN' : var.min().item(),
            'MEAN' : var.mean().item(),
            'MEDIAN' : var.median().item(),
            'STD' : var.std().item()
        }

        return stats_dict

    def get_summary_stats(self, as_df=True, mask=None):
        """
        Get summary statistics for all flux-related variables (zeta, u_star, 
        Psi_M, Psi_H, r_aH, L, H, LE). Note that only array-like variables will
        return summary statistics; others will return the scalar values.

        Returns
        -------
        all_dict : dict
            Dictionary of dictionaries containing flux variables (keys) and their
            summary statistics (values : dict).
        
        # TODO: Change the way non-arrays are handled (this is sloppy--all should be the same type).
        # TODO: Refactor--this is temporary and will likely want to change.
        """
        # Get flux variables as dict
        var_dict = self.get_fluxes()
        # Initialize empty dictionary for variables
        all_dict = {}
        # Iterate through flux variables and return summary stats
        for key,val in var_dict.items():
            try:
                if mask is not None:
                    all_dict[key] = self.get_var_stats(val.where(mask))
                else:
                    all_dict[key] = self.get_var_stats(val)
            except:
                all_dict[key] = {'MEAN' : val}
        
        if as_df:
            return self.get_stats_df(all_dict)
        else:
            return all_dict

    def get_stats_df(self, stats_dict):

        # stats = self.get_summary_stats()

        df = pd.DataFrame(stats_dict).T.reset_index().rename(columns={'index':'Variable'})

        return df

    def get_fluxes(self):
        """
        Get flux-related variables created/output by the model.

        Returns
        -------
        dict
            Dictionary of flux variables calculated by the model run.
        """
        flux_dict =  {
            'zeta' : self.zeta,
            'u_star' : self.u_star,
            'Psi_M' : self.Psi_M,
            'Psi_H' : self.Psi_H,
            'r_aH' : self.r_aH,
            'r_bH' : self.r_bH,
            'r_H' : self.r_H,
            'L' : self.L,
            'H' : self.H,
            'LE' : self.LE,
            'ET' : self.calc_ET(self.LE),
            'EF' : self.calc_EF(self.LE)
            # 'n_iter' : len(self.Ls)
        }
        # TODO: Fix below
        for arr in flux_dict.values():
            try:
                utils.set_crs(arr, self.surface.theta_s)
            except:
                pass

        return flux_dict
    
    # def set_crs(self, arr):

    #     arr.rio.set_crs(self.surface.theta_s.rio.crs)

    def calc_ET(self, LE):

        self.ET = (LE / self.air.lambda_v) * 3600

        return self.ET
    
    def calc_EF(self, LE):
            
        self.EF = (LE / (self.radiation.R_n - self.radiation.G) )
        

        return self.EF

    def _run(self, L=np.inf, use_psi_0=True, allow_neg_flux=True):
        """
        Run model (defaults to neutral).

        Parameters
        ----------
        L : float, optional
            Initial Monin-Obukhov length [m]. The default is np.inf.
        use_psi_0 : bool, optional
            Whether to use the Psi_0 values (makes a minimal difference in r_aH).
            The default is False.
        allow_neg_flux : bool, optional
            Whether or not to allow negative values for H and LE. If False, negative
            values of both H and LE will be set to 0. The default is True (for now).
        
        Yields
        ------
        self.zeta : float
            Characteristic length scale.
        self.Psi_M : float
            Stability correction term for momentum transport.
        self.Psi_H : float
            Stability correction term for heat/vapor transport.
        self.u_star : float
            Friction velocity [m s-1]
        self.r_aH : float
            Aerodynamic resistance to heat/vapor transport.
        self.H : array-like
            Sensible heat flux [W m-2].
        self.LE : array-like
            Latent heat flux [W m-2].
        self.L : array-like
            Monin-Obukhov length [m].
        """
        # 1. Calculate zeta
        self.zeta = self.calc_zeta(L)
        # 2. Calculate Psi terms
        self.Psi_M = self.calc_Psi_M(self.zeta)
        self.Psi_H = self.calc_Psi_H(self.zeta)
        # Optionally calculate Psi_0 terms
        if use_psi_0:
            Psi_M0 = self.calc_Psi_M(self.surface.z_0m / L)
            Psi_H0 = self.calc_Psi_H(self.surface.z_0h / L)
        else:
            Psi_M0 = 0
            Psi_H0 = 0
        # 3. Calculate u_star
        self.u_star = self.calc_ustar(self.Psi_M, Psi_m0=Psi_M0)
        # 4. Calculate r_aH
        self.r_aH = self.calc_r_aH(self.Psi_M, self.Psi_H, Psi_M0=Psi_M0, Psi_H0=Psi_H0)
        # 5. Calculate r_bH
        self.r_bH = self.calc_r_bH(u_star=self.u_star, L=L, c=90.)
        # 6. Calculate total resistance, r_H
        self.r_H = self.calc_r_H(r_bH=self.r_bH)
        # 5. Calculate H
        self.H = self.calc_H(self.surface.theta_s, self.r_H)
        # Flag bad data
        if not allow_neg_flux:
            self.flag = np.where(self.H < 0, flag_dict.get('F_NEG_H')[0], self.flag)
            self.H = xr.where(self.H < 0.0, 0.0, self.H)
        # 6. Calculate LE
        self.LE = self.calc_LE(self.H)
        # Flag bad data
        # if not allow_neg_flux:
        #     self.flag = np.where(self.LE < 0, flag_dict.get('F_NEG_LE')[0], self.flag)
        #     self.LE = xr.where(self.LE < 0.0, 0.0, self.LE)
        self.flag = np.where(self.LE < 0, flag_dict.get('F_NEG_LE')[0], self.flag)
        self.LE = xr.where(self.LE < 0.0, 0.0, self.LE)
        # 7. Recalculate L
        H_v = self.calc_Hv(self.H, self.LE)
        # self.L = self.calc_L(self.u_star, H_v.where(H_v != 0.0, other=np.nan)) # change to calc_L on mean of H_v
        self.L = self.calc_L(self.u_star, np.nanmean(H_v))
        # Calculate difference in L
        #  L_diff = abs(np.nanmean(self.L.where(abs(self.L) < 1e6, other=np.nan)) - L)
        L_diff = abs(self.L - L)

        return L_diff



        
    # def run(self, L=np.inf, use_psi_0=True, allow_neg_flux=False, get_fluxes=False):
    def run(self, L=np.inf, use_psi_0=True, allow_neg_flux=False, max_i=15, L_thresh=0.001, get_fluxes=False):
        """
        Actually run the model and optionally return output variables.

        Parameters
        ----------
        L : float, optional
            Initial Monin-Obukhov length [m]. The default is np.inf.
        use_psi_0 : bool, optional
            Whether to use the Psi_0 values (makes a minimal difference in r_aH).
            The default is True.
        allow_neg_flux : bool, optional
            Whether or not to allow negative values for H and LE. If False, negative
            values of both H and LE will be set to 0. The default is True (for now).
        get_fluxes : bool, optional
            Whether or not to return flux variables as a dictionary. The default is False.

        Yields
        ------
        self.zeta : float
            Characteristic length scale.
        self.Psi_M : float
            Stability correction term for momentum transport.
        self.Psi_H : float
            Stability correction term for heat/vapor transport.
        self.u_star : float
            Friction velocity [m s-1]
        self.r_aH : float
            Aerodynamic resistance to heat/vapor transport.
        self.H : array-like
            Sensible heat flux [W m-2].
        self.LE : array-like
            Latent heat flux [W m-2].
        self.L : array-like
            Monin-Obukhov length [m].

        """
        self.flag = flag_dict.get('NO_FLAG')[0]
        # self._run(L=L, use_psi_0=use_psi_0, allow_neg_flux=allow_neg_flux)
        
        L_diff = np.inf
        self.L = L

        for i in range(max_i):
            L_diff = self._run(L=np.nanmean(self.L), use_psi_0=use_psi_0, allow_neg_flux=allow_neg_flux)
            if L_diff <= L_thresh:
                print(f"Finished {i+1} iterations with an L diff: {L_diff}")
                break
            elif i == 1:
                print(f"H : {np.nanmean(self.H)}, LE : {np.nanmean(self.LE)}")
            else:
                print(f"L diff (n = {i+1}): {L_diff}")
        self._n_iter = i + 1

        if get_fluxes:
            return self.get_fluxes()    

    


    def _run_pix(self, L=np.inf, use_psi_0=True, mask=None, allow_neg_flux=False):

        if mask is not None:
            self.zeta = xr.where(mask, self.calc_zeta(L), self.zeta)
        else:
            self.zeta = self.calc_zeta(L)

        self.Psi_M = self.calc_Psi_M(self.zeta)
        self.Psi_H = self.calc_Psi_H(self.zeta)

        if use_psi_0:
            Psi_M0 = self.calc_Psi_M(self.surface.z_0m / L)
            Psi_H0 = self.calc_Psi_H(self.surface.z_0h / L)
        else:
            Psi_M0 = 0
            Psi_H0 = 0

        # 3. Calculate u_star
        self.u_star = self.calc_ustar(self.Psi_M, Psi_m0=Psi_M0)
        # 4. Calculate r_aH
        self.r_aH = self.calc_r_aH(self.Psi_M, self.Psi_H, Psi_M0=Psi_M0, Psi_H0=Psi_H0)
        # 5. Calculate r_bH
        self.r_bH = self.calc_r_bH(u_star=self.u_star, L=self.L, c=90.)
        # 6. Calculate total resistance, r_H
        self.r_H = self.calc_r_H(r_bH=self.r_bH)
        # 5. Calculate H
        self.H = self.calc_H(self.surface.theta_s, self.r_aH)
        # Flag bad data
        if not allow_neg_flux:
            self.flag = np.where(self.H < 0, flag_dict.get('F_NEG_H')[0], self.flag)
            self.H = xr.where(self.H < 0.0, 0.0, self.H)
        # 6. Calculate LE
        self.LE = self.calc_LE(self.H)
        # Flag bad data
        if not allow_neg_flux:
            self.flag = np.where(self.LE < 0, flag_dict.get('F_NEG_LE')[0], self.flag)
            self.LE = xr.where(self.LE < 0.0, 0.0, self.LE)
        # 7. Recalculate L
        H_v = self.calc_Hv(self.H, self.LE)
        self.L = self.calc_L(self.u_star, H_v.where(H_v != 0.0))
        # Calculate difference in L
        L_diff = abs(self.L - L)

        return L_diff

    def run_pix(self, L=np.inf, use_psi_0=True, max_i=15, L_thresh=0.001, allow_neg_flux=False):

        L_diff = np.inf
        self.L = L
        self.zeta = self.calc_zeta(L)

        self.flag = flag_dict.get('NO_FLAG')[0]

        for i in range(max_i):
            # Create mask where L_diff > threshold = True, else False (i.e. don't re-calculate)
            mask = np.logical_and(L_diff >= L_thresh, self.flag != flag_dict.get('F_ERROR')[0])
            n_pix = mask.sum().item()
            print(f"Iteration {i}, non-converged pixels: {n_pix} . max L_diff : {np.nanmax(L_diff)}")
            # Run model again and get difference in L
            L_diff = self._run_pix(L=self.L, use_psi_0=use_psi_0, mask=mask, allow_neg_flux=allow_neg_flux)
            # If all values are lower than the threshold, stop iterating.
            if np.nanmax(L_diff) <= L_thresh:
                print(f"Finished iteration with a max L diff: {np.nanmax(L_diff)}")
                break
        # Set values outside image to NaN in zeta (they are 0 because of the first iteration)
        self.zeta = xr.where(self.surface.theta_s.notnull(), self.zeta, np.nan)
        self._n_iter = i + 1




    def calc_zeta(self, L : float):
    # def calc_zeta(z, d_0, L):
        """
        Calculate the characteristic length scale (zeta).

        Parameters
        ----------
        L : float
            Monin-Obukhov length [m].

        Returns
        -------
        zeta : float
            Characteristic length scale.
        """

        zeta = (self.air.z - self.surface.d_0) / L

        # try:
        #     zeta = zeta.item()
        # except:
        #     pass

        return zeta
    
    def calc_Psi_M(self, zeta):
        raise NotImplementedError
    
    def calc_Psi_H(self, zeta):
        raise NotImplementedError
    
    def calc_ustar(self, Psi_m, Psi_m0=0):
    # def calc_ustar(u, z, d_0, z_0m, Psi_m, Psi_m0=0):
        """
        Calculate friction velocity [m s-1].

        Parameters
        ----------
        Psi_m : float
            Stability correctoin function for momentum transport
        Psi_m0 : float, optional
            Additional stability correction term for momentum. The default is 0.
        
        Additional Variables
        --------------------
        u : float
            Wind speed [m s-1]
        z : float
            Height of wind speed measurement [m].
        h : float
            Canopy height [m].

        Returns
        -------
        u_star : float
            Friction velocity [m s-1].
        """

        u_star = (self.air.u * KAPPA) / ( np.log( (self.air.z - self.surface.d_0) / self.surface.z_0m ) - Psi_m + Psi_m0)

        return u_star

    def calc_r_aH(self, Psi_M, Psi_H, Psi_M0=0, Psi_H0=0):
    # def calc_r_a(u, z, d_0, z_0m, z_0h, Psi_M, Psi_H):
        """
        Calculate aerodynamic resistance according to MOST.

        Parameters
        ----------
        Psi_M : float
            Stability correction factor for momentum transport.
        Psi_H : float
            Stability correction factor for heat transport.
        Psi_M0 : float, optional
            Additional stability correction term for momentum. The default is 0.
        Psi_H0 : float, optional
            Additional stability correction term for heat. The default is 0.

        Additional Variables
        --------------------
        u : float
            Wind speed [m s-1].
        z : float
            Height of wind speed measurement.
        d_0 : float
            Zero-plane displacement height [m].
        z_0m : float
            Roughness length for momentum transport [m].
        z_0h : float
            Roughness length for heat transport [m].

        Returns
        -------
        r_a : float
            Aerodynamic resistance to heat transport [s m-1].
        """

        # Calculate aerodynamic resistance
        r_aH = ( 
            ( (np.log((self.air.z - self.surface.d_0) / self.surface.z_0m) - Psi_M + Psi_M0) * 
            (np.log((self.air.z - self.surface.d_0) / self.surface.z_0h) - Psi_H + Psi_H0) )
            / (KAPPA**2 * self.air.u) 
        )

        return r_aH


    def calc_r_bH(self, u_star, L, c=90.):
        """
        Calculate boundary layer resistance.
        """

        u_h = self.calc_u_z(z=self.surface.h, u_star=u_star, L=L)
        u_0m = self.calc_u0m(u_h = u_h)

        r_bH = (c / self.surface.lai) * ( (self.surface.w_l / u_0m) ** (1/2) )

        # TODO: Figure out a better way to do this. For now, just using a low-ish 
        # threshold of NDVI to avoid calculating r_bH where LAI is ~ 0 (which makes
        # r_bH –> infinity).
        # r_bH = xr.where(self.surface.ndvi < 0.25, np.nan, r_bH)
        r_bH = xr.where(self.surface.lai < 1., np.nan, r_bH)


        return r_bH

    def calc_u_z(self, z, u_star, L):

        Psi_m2 = self.calc_Psi_M( (z - self.surface.d_0) / L )
        Psi_m1 = self.calc_Psi_M( (self.air.z - self.surface.d_0) / L )

        u_z = ( ( 
            (u_star / KAPPA) * 
            ( np.log((z - self.surface.d_0) / (self.air.z - self.surface.d_0) ) 
             -  Psi_m2 + Psi_m1 ) 
            ) + self.air.u )

        return u_z

    def calc_u0m(self, u_h):

        a = ( 0.28 * 
             (self.surface.lai**(2/3)) * (self.surface.h**(1/3)) * 
             (self.surface.w_l**(-1/3)) 
        )
        
        u_0m = u_h * np.exp(
            -a * (1 - ( (self.surface.d_0 + self.surface.z_0m) / self.surface.h ) ) 
        )

        return u_0m


    def calc_r_H(self, r_bH=0.):
        r_H = self.r_aH + r_bH
        return r_H


    def calc_H(self, theta_s, r_aH):
    # def calc_H(self, rho_a, c_p, theta_s, theta_a, r_aH):
        """
        Calculate sensible heat flux using a temperature gradient and aerodynamic 
        resistance to heat transport.

        Parameters
        ----------
        theta_s : float or array-like
            Potential surface temperature [K]
        r_aH : float
            Aerodynamic resistance to heat transport [s m-1]

        Additional Variables
        --------------------
        rho_a : float
            Air density [kg m-3]
        c_p : float
            Heat capacity of air [J K-1 kg-1]
        theta_a : float
            Potential air temperature [K]

        Returns
        -------
        H : float or array-like
            Sensible heat flux [W m-2]
        """
        H = self.air.rho_a * self.air.c_p * ( (theta_s - self.air.theta_a) / r_aH )

        return H
    
    def calc_LE(self, H):
    # def calc_LE(R_n, G, H):
        """
        Calculate latent heat flux as the residual of the surface energy balance equation.

        Parameters
        ----------
        H : float or array
            Sensible heat flux [W m-2].
        
        Additional Variables
        --------------------
        R_n : float or array
            Net radiation [W m-2].
        G : float or array
            Soil heat flux [W m-2].

        Returns
        -------
        LE : float or array
            Latent heat flux [W m-2].
        """

        LE = xr.where(H < 0, self.radiation.R_n - self.radiation.G, self.radiation.R_n - self.radiation.G - H)
        
        # LE = self.radiation.R_n - self.radiation.G - H
        
        if LE.shape != H.shape:
            LE = LE.interp(x=H.x, y=H.y)

        return LE
    
    def calc_L(self, u_star, H_v):
    # def calc_L(self, u_star, theta_v, rho_a, c_p, H_v):
        """
        Calculate the Monin-Obukhov length, L [m].

        Parameters
        ----------
        u_star : float
            Friction velocity, by default None
        H_v : float
            Virtual sensible heat flux [W m-2], by default None
        
        Additional Variables
        --------------------
        theta_v : float
            Virtual potential temperature [K], by default None
        rho_a : float
            Air density [kg m-3], by default None
        c_p : float
            Heat capacity of air at constant pressure [J kg-1 K-1]

        Returns
        -------
        L : float
            Monin-Obukhov length [m].
        """

        # theta_v = met.calc_theta(T_a, p_a)

        L = - ( ( ( u_star**3 ) * self.air.theta_v ) / 
               ( KAPPA * G * ( H_v / ( self.air.rho_a * self.air.c_p ) ) ) )

        return L

    def calc_Hv(self, H, LE):
    # def calc_Hv(H, LE, T_a, p_a, e_a):
        """
        Calculate virtual sensible heat flux.

        Parameters
        ----------
        H : float | array-like
            Sensible heat flux [W m-2]
        LE : float | array-like
            Latent heat flux [W m-2]
        
        Additional Variables
        --------------------
        T_a : float
            Temperature [K]
        c_p : float
            Heat capacity of air at constant pressure [J kg-1 K-1]
        theta_a : float
            Potential temperature [K]

        Returns
        -------
        H_v : float
            Virtual sensible heat flux [W m-2]
        """
        # theta = met.calc_theta(T_a, p_a)
        E = LE / self.air.lambda_v
        # c_p = met.calc_cp(p_a, e_a)

        H_v = H + ( 0.61 * self.air.c_p * self.air.theta_a * E )

        return H_v




class NeutralModel(FluxModel):
    """
    Calculate turbulent fluxes assuming neutral conditions.
    """

    def __init__(self, airlayer, surface, radiation):

        super().__init__(airlayer, surface, radiation)

        self.L = np.inf

    # def run(self, n_iter=1):
    #     self._run(n_iter=n_iter)
    def run(self, L=np.inf, use_psi_0=False, allow_neg_flux=False, get_fluxes=False):
        self.flag = flag_dict.get('NO_FLAG')[0]
        self._run(L=L, use_psi_0=use_psi_0, allow_neg_flux=allow_neg_flux)
        if get_fluxes:
            return self.get_fluxes()    


    def run_pix(self, L=np.inf, use_psi_0=False, max_i=1, L_thresh=0.001, allow_neg_flux=False):
        return super().run_pix(L, use_psi_0, max_i, L_thresh, allow_neg_flux)

    def calc_Psi_M(self, zeta):
        return 0
    
    def calc_Psi_H(self, zeta):
        return 0




class DyerModel(FluxModel):
    """
    Calculate turbulent fluxes using the equations for stability correction terms
    found in Bonan (2016). NOTE: Not original source.
    """

    def __init__(self, airlayer, surface, radiation):

        super().__init__(airlayer, surface, radiation)
    
    # def run(self, L=np.inf):
    #     # Run first time to get neutral L
    #     self._run(L=L)
    #     # Run again to get actual fluxes
    #     self._run(L=self.L.mean())


    def calc_Psi_M(self, zeta):
        """
        Calculates the stability correction function for momentum transport.

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        psi_m : float
            Stability correction function for momentum transport.

        Reference: ???? Bonan (but not original source)
        """

        Psi_m = xr.where(zeta < 0, self._calc_Psi_M_unstable(zeta), self._calc_Psi_stable(zeta))

        return Psi_m

    def calc_Psi_H(self, zeta):
        """
        Calculates the stability correction function for heat (and vapour) transport.

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        psi_h : float
            Stability correction function for heat (or vapor) transport.

        Reference: ??? Bonan (but not original source)
        """

        Psi_h = xr.where(zeta < 0, self._calc_Psi_H_unstable(zeta), self._calc_Psi_stable(zeta))

        return Psi_h

    def _calc_Psi_stable(self, zeta):
        """
        Calculate Psi for stable conditions (zeta >= 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        psi : float
            Stability correction term for momentum and heat (or vapor) transport
            under stable conditions.
        """

        Psi_m = -5 * zeta

        return Psi_m
    
    def _calc_Psi_M_unstable(self, zeta):
        """
        Calculate Psi_M for unstable conditions (zeta < 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        Psi_m : float
            Stability correction term for momentum transport under unstable conditions.
        """
        x = (1 - 16 * zeta)**(1/4)

        Psi_m = 2 * np.log((1 + x) / 2) + np.log( (1 + x**2) / 2) - 2 * np.arctan(x) + np.pi/2

        return Psi_m
    
    def _calc_Psi_H_unstable(self, zeta):
        """
        Calculate Psi_H for unstable conditions (zeta < 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        Psi_m : float
            Stability correction term for heat transport under unstable conditions.
        """
        x = (1 - 16*zeta)**(1/4)
        Psi_h = 2 * np.log((1 + x**2)/2)
        
        return Psi_h



class BrutsaertModel(FluxModel):
    """
    Calculate turbulent fluxes using the stability correction terms found in 
    Brutsaert (2005). 
    """
    def __init__(self, airlayer, surface, radiation):

        super().__init__(airlayer, surface, radiation)

    # def run(self, L=np.inf):
    #     # Run first time to get neutral L
    #     self._run(L=L)
    #     # Run again to get actual fluxes
    #     self._run(L=self.L.mean())


    def calc_Psi_M(self, zeta):
        """
        Calculates the stability correction function for momentum transport.

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        psi_m : float
            Stability correction function for momentum transport.

        Reference: Brutsaert, W. (2005). Hydrology: An Introduction. Cambridge University Press.
        """
        # # Stable conditions, zeta >= 0
        # if zeta >= 0:
        #     a = 6.1
        #     b = 2.5
        #     Psi_m = -a * np.log(zeta + (1.0 + zeta**b)**(1.0/b))    # Eq. (2.59)

        # # Unstable conditions, zeta < 0
        # else:
        #     a = 0.33
        #     b = 0.41
        #     y = -1 * zeta
        #     x = (y / a)**(1/3)

        #     Psi_0 = -np.log(a) + np.sqrt(3) * b * a**(1/3) * np.pi/6.0
        #     y = min(y, b**(-1/3))

        #     Psi_m = np.log(a+y) - 3 * b * y**(1/3) + \
        #                 ((b*a**(1/3)) / 2 ) * np.log( (1+x)**2 / (1 - x + x**2)) + \
        #                 np.sqrt(3) * b * a**(1/3) * np.arctan((2*x - 1) / np.sqrt(3) ) + \
        #                 Psi_0                       # Eq. (2.63)

        Psi_m = xr.where(zeta < 0, self._calc_Psi_M_unstable(zeta), self._calc_Psi_stable(zeta))

        # if Psi_m.ndim == 1:
        #     return Psi_m
        # else:
        #     return Psi_m.item()
        return Psi_m
    
    def calc_Psi_H(self, zeta):
        """
        Calculates the stability correction function for heat (and vapour) transport.

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        psi_h : float
            Stability correction function for heat (or vapor) transport.

        Reference: Brutsaert, W. (2005). Hydrology: An Introduction. Cambridge University Press.
        """
        # # Stable conditions, zeta >=0
        # if zeta >= 0:
        #     Psi_h = self.calc_Psi_M(zeta)

        # # Unstable conditions, zeta < 0
        # else:
        #     c = 0.33
        #     d = 0.057
        #     n = 0.78
        #     y = -1 * zeta

        #     Psi_h = ((1 - d) / n) * np.log((c + y**n) / c )     # Eq. (2.64)

        Psi_h = xr.where(zeta < 0, self._calc_Psi_H_unstable(zeta), self._calc_Psi_stable(zeta))

        # if Psi_h.ndim == 1:
        #     return Psi_h
        # else:
        #     return Psi_h.item()
        return Psi_h
    
    def _calc_Psi_stable(self, zeta):
        """
        Calculate Psi for stable conditions (zeta >= 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        Psi : float
            Stability correction term for momentum or heat transport under stable 
            conditions.
        """
        a = 6.1
        b = 2.5
        Psi_m = -a * np.log(zeta + (1.0 + zeta**b)**(1.0/b))    # Eq. (2.59)

        return Psi_m
    
    def _calc_Psi_M_unstable(self, zeta):
        """
        Calculate Psi_M for unstable conditions (zeta < 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        Psi_m : float
            Stability correction term for momentum transport under unstable conditions.
        """
        a = 0.33
        b = 0.41
        y = -1 * zeta
        x = (y / a)**(1/3)

        Psi_0 = -np.log(a) + np.sqrt(3) * b * a**(1/3) * np.pi/6.0
        # y = min(y, b**(-1/3))
        y = np.where(y < b**(-1/3), y, b**(-1/3))

        Psi_m = np.log(a+y) - 3 * b * y**(1/3) + \
                    ((b*a**(1/3)) / 2 ) * np.log( (1+x)**2 / (1 - x + x**2)) + \
                    np.sqrt(3) * b * a**(1/3) * np.arctan((2*x - 1) / np.sqrt(3) ) + \
                    Psi_0                       # Eq. (2.63)

        return Psi_m
    
    def _calc_Psi_H_unstable(self, zeta):
        """
        Calculate Psi_H for unstable conditions (zeta < 0).

        Parameters
        ----------
        zeta : float
            Dimensionless length parameter

        Returns
        -------
        Psi_h : float
            Stability correction term for heat transport under unstable conditions.
        """
        c = 0.33
        d = 0.057
        n = 0.78
        y = -1 * zeta

        Psi_h = ((1 - d) / n) * np.log((c + y**n) / c )     # Eq. (2.64)

        return Psi_h        


class BowenModel(FluxModel):
    """
    Calculate turbulent fluxes according to the Bowen Ratio using a profile approach.
    """

    def __init__(self, airlayer_2, airlayer_1, surface, radiation):
        """
        Parameters
        ----------
        airlayer2 : AirLayer
            air.AirLayer object at height z2. Contains the following variables:
            z, u, T_a, p_a, e_a, c_p, h_r, 
        airlayer1 : AirLayer
            air.AirLayer object at height z1. Contains the following variables:
            z, u, T_a, p_a, e_a, c_p, h_r, 
        surface : Surface
            surface.Surface object for the model. Contains the following variables:
            h, d0, z_0m, z_0h, T_s
        radiation : Radiation
            radiation.Radiation object for the model. Contains the following variables:
            R_n, G, [SW_IN, SW_OUT, LW_IN, LW_OUT]
        """
        super().__init__(airlayer_2, surface, radiation)

        self.air2 = airlayer_2
        self.air1 = airlayer_1


    def run(self, allow_neg_flux=True):
        """
        Calculate turbulent fluxes according to the Bowen Ratio.

        Yields
        ------
        self.LE_hat : float
            Landscape-level average latent heat flux [W m-2]
        self.H_hat : float
            Landscape-level average sensible heat flux [W m-2]
        self.r_aH : float
            Aerodynamic resistance to heat/vapor transport [s m-2]
        self.H : array-like
            Sensible heat flux [W m-2].
        self.LE : array-like
            Latent heat flux [W m-2].
        """
        # Set flag
        self.flag = flag_dict.get('NO_FLAG')[0]
        # 1. Calculate Bowen Ratio from profile data
        beta = self.calc_beta()
        # 2. Calculate landscape-level LE from Bowen Ratio
        # self.LE_hat = self.calc_LE_bowen(beta)
        self.LE = self.calc_LE_bowen(beta)
        # 3. Calculate landscape-level H from Bowen Ratio
        # self.H_hat = self.calc_H_bowen(self.LE_hat, beta)
        self.H = self.calc_H_bowen(self.LE, beta)
        # 4. Calculate aerodynamic resistance
        self.r_H = self.calc_r_H(self.H)
        # 5. Calculate pixel-wise H
        # self.H = self.calc_H(self.surface.theta_s, self.r_H)
        # Flag bad data
        if not allow_neg_flux:
            self.flag = np.where(self.H < 0, flag_dict.get('F_NEG_H')[0], self.flag)
            self.H = xr.where(self.H < 0.0, 0.0, self.H)
        # 6. Calculate pixel-wise LE
        self.LE = self.calc_LE(self.H)
        # Flag bad data
        if not allow_neg_flux:
            self.flag = np.where(self.LE < 0, flag_dict.get('F_NEG_LE')[0], self.flag)
            self.LE = xr.where(self.LE < 0.0, 0.0, self.LE)
        # 7. Calculate L
        # H_v = self.calc_Hv(self.H, self.LE)
        # self.L = self.calc_L(self.u_star, H_v)
        # # 8. Calculate zeta
        # self.zeta = self.calc_zeta(self.L)
        self.zeta = None
        self.u_star = None
        self.Psi_M = None
        self.Psi_H = None
        self.L = None
        self.r_aH = None
        self.r_bH = None


    def calc_beta(self):
    # def calc_bowen(T_2, p_2, rh_2, T_1, p_1, rh_1):
        """
        Calculates the Bowen Ratio given the temperature and humidity of air at
        height z2 and the temperature and humidity of air at height z1.

        Parameters
        ----------
        T_2 : float
            Air temperature at height z_2 [K].
    
        p_2 : float
            Air pressure at height z_2 [kPa].

        rh_2 : float
            Relative humidity at height z_2 [%].

        T_1 : float
            Air temperature at height z_1 [K].

        p_1 : float
            Air pressure at height z_1 [kPa].
        
        rh_1 : float
            Relative humidity at height z_1 [%].

        Returns
        -------
        beta : float
            Bowen Ratio
        """

        # Calculate Bowen Ratio 
        beta = (self.air1.c_p / self.air1.lambda_v) * ( 
            (self.air2.theta_a - self.air1.theta_a) / (self.air2.q - self.air1.q ) 
        )

        return beta


    def calc_LE_bowen(self, beta):
    # def calc_LE_bowen(R_n, G, beta):
        """
        Calculates LE using the Bowen Ratio.

        Parameters
        ----------
        R_n : float
            Net radiation [W m-2]

        G : float
            Soil heat flux [W m-2]

        beta : float
            Bowen Ratio

        Returns
        -------
        LE : float
            Latent heat flux [W m-2]

        NOTE: I'm taking the mean R_n and G here. I think this makes more sense
        physically. It's worth noting, though, that slightly different values result
        in the final calculations if these are calculated pixel-wise (and then
        if r_aH is calculated pixel-wise vs. from average H, theta_s).
        """
        # LE = (np.mean(self.radiation.R_n) - np.mean(self.radiation.G)) / (1 + beta)
        LE = (self.radiation.R_n - self.radiation.G) / (1 + beta)

        return LE


    def calc_H_bowen(self, LE, beta):
    # def calc_H_bowen(LE, beta):
        """
        Calculate H using the LE from the Bowen Ratio

        Parameters
        ----------
        LE : float
            Latent heat flux [W m-2]
        
        beta : flaot
            Bowen ratio

        Returns
        -------
        H : float
            Sensible heat flux [W m-2]
        """
        H = beta * LE

        return H
    
    def calc_r_H(self, H_hat):
        """
        Calculate total resistance to heat transfer from sensible heat flux.

        Parameters
        ----------
        H_hat : float
            Landscape-level average sensible heat flux [W m-2].

        Returns
        -------
        r_H : float
            Total resistance to heat transport [s m-1].
        """

        # Calculate aerodynamic resistance
        r_H = self.air2.rho_a * self.air2.c_p * ( (self.surface.theta_s - self.air2.theta_a) / H_hat)

        return r_H


class QuadraticModel(FluxModel):

    def __init__(self, airlayer, surface, radiation):

        super().__init__(airlayer, surface, radiation)


    def run(self, H_0):

        # 1. Calculate Psi terms
        self.Psi_M = self.calc_Psi_M(H_0)
        self.Psi_H = self.calc_Psi_H(H_0)
        # 2. Calculate u_star
        self.u_star = self.calc_ustar(self.Psi_M)
        # 3. Calculate r_aH
        self.r_aH = self.calc_r_aH(self.Psi_M, self.Psi_H)
        # 4. Calculate H
        self.H = self.calc_H(self.surface.theta_s, self.r_aH)
        # 5. Calculate LE
        self.LE = self.calc_LE(self.H)
        # 6. Calculate L
        H_v = self.calc_Hv(self.H, self.LE)
        self.L = self.calc_L(self.u_star, H_v)
        # 7. Calculate zeta
        self.zeta = self.calc_zeta(self.L)


        
    def calc_Psi_M(self, H_hat):
    # def calc_Psi_M_quadratic(u, z, h, rho_a, c_p, theta_a, theta_s, H_hat):
        """
        Calculates the stability correction function for momentum transport based on
        a quadratic solution.

        Parameters
        ----------
        u : float
            Wind speed [m s-1].
        z : float
            Height of wind speed measurement [m].
        h : float
            Canopy height [m].
        rho_a : float
            Air density [kg m-3].
        c_p : float
            Heat capacity of air at constant pressure [J kg-1 K-1].
        theta_a : float
            Potential temperature of air [K].
        theta_s : float
            Potential temperature of the surface [K].
        H_hat : float
            Landscape-level average sensible heat flux [W m-2].

        Returns
        -------
        _type_
            _description_
        """

        # Coefficients
        a = 1
        b = -1 * ( 
            np.log((self.air.z - self.surface.d_0) / self.surface.z_0m) + \
            np.log( (self.air.z - self.surface.d_0) / self.surface.z_0h ) 
        )
        c = ( 
            np.log( (self.air.z - self.surface.d_0) / self.surface.z_0m ) * \
            np.log( (self.air.z - self.surface.d_0) / self.surface.z_0h ) 
        ) - ( (KAPPA ** 2 * self.air.u * self.air.rho_a * self.air.c_p * (self.surface.theta_s - self.air.theta_a) ) / H_hat )

        # Calculate Psi_M
        psi_1,psi_2 = utils.quadratic_formula(a, b, c)

        return psi_2

    def calc_Psi_H(self, H_hat):
        return self.calc_Psi_M(H_hat)



# TODO: Model outputs (self.get_fluxes()) are not consistent. Need to reconfigure 
# functions so that variables are more consistent types.