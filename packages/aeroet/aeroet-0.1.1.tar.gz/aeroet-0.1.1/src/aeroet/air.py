#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'brynmorgan@ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2022'

__license__ = 'GNU General Public License v3.0'
__date__ = 'Wed 24 Aug 22 10:54:04'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = 'https://github.com/brynemorgan/aeroet/blob/main/src/aeroet/air.py'

"""

Name:           air.py
Compatibility:  Python 3.10.0
Description:    Description of what program does

URL:            https://

Requires:       numpy

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        brynmorgan@ucsb.edu
Copyright:      (c) Bryn Morgan 2022

"""


# IMPORTS
import numpy as np

# from model.radiation import calc_emissivity

# CONSTANTS
c_pd = 1005.7               # specific heat capacity of dry air at constant pressure [J kg-1 K-1]
c_pv = 1996.0               # specific heat of water vapour at constant pressure [J kg-1 K-1]
EPSILON = 0.622             # ratio of molar mass of water to molar mass of dry air [unitless]
R_D = 287.058	 	        # dry gas constant (J kg-1 K-1)
R = 8.314                   # ideal gas constant (J mol-1 K-1)
R_v = 461.                  # gas constant for water vapor (J kg-1 K-1)
M_H2O = 0.01801528          # molar mass of water (kg mol-1)
# SIGMA = 5.67036713e-08 		# Stefan-Boltzmann constant [W m-2 K-4]
G = 9.80665                 # gravitational acceleration [m s-2]
M_D = 0.0289635              # molar mass of dry air (kg mol-1)
gamma_d = G / c_pd


class AirLayer:
    """
    
    Parameters
    ----------
    z : float
        Height of the air layer (and met data measurements) [m]
    
    u : float | array-like
        Wind speed [m s-1]
    
    T_a : float | array-like
        Air temperature [K]

    p_a : float | array-like
        Air pressure [kPa]
    
    h_r : float | array-like
        Relative humidity [%]
    
    e_a : float | array-like
        Vapor pressure of air [kPa]
    
    q : float | array-like
        Specific humidity of air [kg kg-1]
    
    rho_a : float | array-like
        Density of air [kg m-3]
    
    c_p : float | array-like
        Heat capacity of air at constant pressure [J kg-1 K-1]
    
    theta_a : float | array-like
        Potential temperature of air [K]
    
    theta_v : float | array-like
        Virtual potential temperature of air [K]


    Methods
    -------
    calc_vp()
        Calculates the vapour pressure of air based on relative humidity and the
        Tetens equation for saturation vapour pressure.

    calc_rho()
        Calculates the density of air based on the ideal gas law.
    
    calc_c_p()
        Calculates heat capacity of (moist) air at constant pressure.

    calc_q()
        Calculate the specific humidity.
    
    calc_theta()
        Calculate the potential temperature of a parcel of air.
    
    calc_Tv()
        Calculate the virtual temperature.

    calc_r_v(self):
        Calculate the mixing ratio of a parcel of air.
    
    calc_slope_svp(self):
        Calculates the slope of the saturation vapour pressure line.
    
    calc_svp()
        Calculates the saturation vapour pressure using the Tetens equation.

    calc_theta_v()
        Calculate virtual potential temperature.

    calc_emissivity()
        Estimates the atmospheric emissivity for a clear sky.

    """

    def __init__(
        self,
        z,
        u,
        T_a,
        p_a,
        h_r,
        c = 0.,
        z_0 = 0.,
        e_a = None,
        c_p = None,
        rho_a = None
    ):
        """
        Parameters
        ----------
        z : float
            Height of the `AirLayer` (and met data measurements) [m]
        u : float | array-like
            Wind speed [m s-1]
        T_a : float | array-like
            Air temperature [K]
        p_a : float | array-like
            Air pressure [kPa]
        h_r : float | array-like
            Relative humidity [%]
        e_a : float | array-like, optional
            Vapor pressure of air [kPa]
        c_p : float | array-like, optional
            Heat capacity of air [J kg-1 K-1], by default None
        rho_a : float | array-like, optional
            Density of air [kg m-3], by default None
        """

        self.z = z
        self.u = u
        self.T_a = T_a
        self.p_a = p_a
        self.h_r = h_r

        # self.z = np.array(z)
        # self.u = np.array(u)
        # self.T_a = np.array(T_a)
        # self.p_a = np.array(p_a)
        # self.h_r = np.array(RH)

        # Vapour pressure, e_a [kPa]
        if e_a is not None:
            self.e_a = e_a
        else:
            self.e_a = self.calc_vp()

        # Specific humidity, q [kg kg-1]
        self.q = self.calc_q()

        # Air density, rho_a [kg m-3]
        if rho_a is not None:
            self.rho_a = rho_a
        else:
            self.rho_a = self.calc_rho()
        
        # Heat capacity, c_p [J kg-1 K-1]
        if c_p is not None:
            self.c_p = c_p
        else:
            self.c_p = self.calc_cp()

        # Latent heat of vaporization, lambda_v [J kg-1]
        self.lambda_v = self.calc_lhvap()

        # Potential temperature, theta_a [K]
        self.theta_a = self.calc_theta(T_a=self.T_a, z_0=z_0, gamma=gamma_d)

        # Virtual potential temperature, theta_v [K]
        self.theta_v = self.calc_theta_v()

        # VPD [kPa]
        self.vpd = self.calc_vpd()

        # Emissivity
        self._cloud_fraction = c
        self.emissivity = self.calc_emissivity()

    def describe(self):
        return self.__dict__.copy()



    def calc_vp(self):
        """
        Calculates the vapour pressure of air based on relative humidity and the
        saturation vapour pressure.

        Parameters
        ----------
        h_r : float
            Relative humidity [%].
        
        e_star : float
            Saturation vapour pressure [kPa].

        Returns
        -------
        e_a : float
            Vapour pressure of air [kPa]

        Notes
        -----
        The vapour pressure of air, |e_a|, is the product of relative 
        humidity, |h_r|, and saturation vapour pressure, |e_star|.
        
        .. math:: 
        
            e_a = \\frac{h_r}{100} e_a^*
        
        .. |e_a| replace:: :math:`e_a` [kPa]
        .. |h_r| replace:: :math:`h_r` [%]
        .. |e_star| replace:: :math:`e_a^*` [kPa]

        """

        e_a = (self.h_r/100) * self.calc_svp()

        return e_a
    
    def calc_rho(self):
        """
        Calculates the density of air based on the ideal gas law.

        Parameters
        ----------
        p_a : float
            Total pressure of air [kPa].
        
        e_a : float
            Vapor pressure of air [kPa].
        
        T_a : float
            Temperature of air [K]

        Returns
        -------
        rho : float
            Density of air [kg m-3]
        
        Notes
        -----
        The density of air, |rho_a|, varies with temperature, 
        pressure, and humidity, and can be calculated from the ideal gas law:

        .. math::
            
            \\rho_a = \\frac{1000 \\, p_a}{R_d T_a} \left( 1 - \\frac{(1 - \epsilon) e_a}{1000 \\, p_a} \\right)
        
        where |R_d [J mol-1 K-1]| is the gas constant for dry air, |T_a [K]| is 
        the temperature of air, |p_a [kPa]| is the total pressure of air, |e_a [kPa]|
        is the vapor pressure of air, and |epsilon| is the ratio of the molar mass
        of water to that of dry air.

        .. |rho_a| replace:: :math:`\\rho_a`  [kg m\ :sup:`-3`]
        .. |R_d [J mol-1 K-1]| replace:: :math:`R_d = 287.058`  J mol\ :sup:`-1` K\ :sup:`-1`
        .. |T_a [K]| replace:: :math:`T_a`  [K]
        .. |p_a [kPa]| replace:: :math:`p_a`  [kPa]
        .. |e_a [kPa]| replace:: :math:`e_a`  [kPa]
        .. |epsilon| replace:: :math:`\epsilon = 0.622`

        """

        rho = ((self.p_a*1000)/(R_D*self.T_a))*(1-(((1-EPSILON)*self.e_a)/(self.p_a*1000)))

        return rho

    def calc_cp(self):
        """
        Calculates heat capacity of (moist) air at constant pressure.

        Parameters
        ----------
        p_a : float
            Total pressure of air. Units must match `e_a`.
        e_a : float
            Vapor pressure of air. Units must match `p_a`.

        Returns
        -------
        c_p : float
            Heat capacity of air at constant pressure |[J kg-1 K-1]|.
        
        Notes
        -----
        The heat capacity of air at constant pressure, |c_p|, is calculated as 
        the sum of the heat capacities of dry air, |c_pd|, and water vapour,
        |c_pv|, at constant pressure, weighted by the specific humidity, |q|:

        .. math::

            c_p = (1 - q) c_{pd} + q c_{pv}
        
        where |c_pd = 1005.7| and |c_pv = 1996.0|.

        .. |[J kg-1 K-1]| replace:: [J kg\ :sup:`-1` K\ :sup:`-1`
        .. |c_p| replace:: :math:`c_p` [J kg\ :sup:`-1` K\ :sup:`-1`]
        .. |c_pd| replace:: :math:`c_{pd}` [J kg\ :sup:`-1` K\ :sup:`-1`]
        .. |c_pv| replace:: :math:`c_{pv}` [J kg\ :sup:`-1` K\ :sup:`-1`]
        .. |q| replace:: :math:`q` [kg kg\ :sup:`-1`]
        .. |c_pd = 1005.7| replace:: :math:`c_{pd} = 1005.7` J kg\ :sup:`-1` K\ :sup:`-1`
        .. |c_pv = 1996.0| replace:: :math:`c_{pv} = 1996.0` J kg\ :sup:`-1` K\ :sup:`-1`
        """
        # Calculate specific humidity
        # q = self.calc_q(self.p_a, self.e_a)w

        # Calculate heat capacity of moist air
        c_p = (1 -self.q) * c_pd + self.q * c_pv

        return c_p

    def calc_lhvap(self):
        """
        Calculates the latent heat of vaporization |[J kg-1]| of water at a given
        temperature.

        Parameters
        ----------
        T_K : float
            Temperature [K].

        Returns
        -------
        lambda_v : float
            Latent heat of vaporization |[J kg-1]|

        Notes
        -----
        The latent heat of vaporization, |lambda_v|, is calculated
        as a function of temperature, |T|, using the following equation [1]_:
       
        .. math::
            
            \lambda_v = (2.501 - 2.361 \\times 10^{-3} T) \\times 10^6    
        
        .. |[J kg-1]| replace:: [J kg\ :sup:`-1`]
        .. |lambda_v| replace:: :math:`\lambda_v` [J kg-1]    
        .. |T| replace:: :math:`T` [K]
        
        References
        ----------
        .. [1] Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). Crop 
            evapotranspiration: Guidelines for computing crop water requirements 
            (FAO Irrigation and Drainage Paper 56). Food and Agriculture Organization 
            of the United Nations. https://www.fao.org/3/x0490e/x0490e00.htm. (Eq. 3-1).
        """
        # Calculate latent heat of vaporization at T
        lambda_v = (2.501 - (2.361e-3 * (self.T_a - 273.15))) * 1e6

        return lambda_v
    
    def calc_q(self):
        """
        Calculate the specific humidity of air.

        Parameters
        ----------
        p_a : float
            Total pressure of air. Units must match `e_a`.
        e_a : float
            Vapor pressure of air. Units must match `p_a`.

        Returns
        -------
        q : float
            Specific humidity |[kg kg-1]|.

        Notes
        -----
        The specific humidity, |q|, is calculated from the vapour pressure |e_a| 
        and air pressure |p_a| according to Cambell and Norman (1998), Eq. 3.19 [1]_:

        .. math::

            q = \\frac{\epsilon \\, e_a}{(p_a - e_a (1 - \epsilon))}
        
        where |epsilon| is the ratio of the molecular weight of water vapour to
        that of dry air.
        
        
        .. |[kg kg-1]| replace:: [kg kg\ :sup:`-1`]
        .. |q| replace:: :math:`q` [kg kg\ :sup:`-1`]
        .. |e_a| replace:: :math:`e_a` [kPa]
        .. |p_a| replace:: :math:`p_a` [kPa]
        .. |epsilon| replace:: :math:`\epsilon = 0.622`
        

        References
        ----------
        .. [1] Campbell, G. S., & Norman, J. (1998). An Introduction to Environmental 
            Biophysics. Springer Science & Business Media.
        """
        q = (EPSILON * self.e_a) / (self.p_a - (1-EPSILON) * self.e_a)

        return q


    def calc_theta(self, T_a, z_0=0.0, gamma=gamma_d, p_0=100.):
        """
        Calculate the potential temperature of a parcel of air.

        Parameters
        ----------
        T_a : float
            Air temperature [K]
        p_a : float
            Air pressure [kPa]
        p_0 : float
            Reference air pressure [kPa]. The default is 100.0.

        Returns
        -------
        theta : float
            Potential temperature [K].
        
        Notes
        -----
        The potential temperature, |theta|, of air at some reference height |z| 
        above the surface, |z_0|, is given by the equation [1]_:

        .. math::

            \\theta_a = T_a + (z - z_0) \Gamma_d
        
        where |Gamma_d| is the dry adiabatic lapse rate,  which is a function of 
        the gravitational constant, |g|, and the heat capacity of dry air at 
        constant pressure, |c_pd|.

        .. |theta| replace:: :math:`\\theta_a` [K]
        .. |z| replace:: :math:`z` [m]
        .. |z_0| replace:: :math:`z_0` [m]
        .. |Gamma_d| replace:: :math:`\Gamma_d` [K m\ :sup:`-1`]
        .. |g| replace:: :math:`g = 9.8` m s\ :sup:`-2`
        .. |c_pd| replace:: :math:`c_{pd} = 1005.7` J kg\ :sup:`-1` K\ :sup:`-1`

        References
        ----------
        .. [1] Bonan, G. B. (2016). Ecological Climatology: Concepts and Applications. 
            Cambridge University Press.
        """
        # NOTE: This is going to be a problem for taller canopies... See Notes 
        # from Wed, 10 May 2023.
        # https://glossary.ametsoc.org/wiki/Potential_temperature
        # theta = T_a * ( (p_0 / self.p_a) ** (R_D/c_pd) )
        theta = T_a + (self.z - z_0) * gamma

        return theta

    def calc_vpd(self):
        """
        Calculate the vapour pressure deficit.

        Returns
        -------
        vpd : float
            Vapour pressure deficit of air [kPa].
        
        Notes
        -----
        The vapour pressure deficit, |VPD|, is defined as the difference
        between the saturation vapour pressure, |e_star|, and the actual
        vapour pressure, |e_a|:

        .. math::

            \\text{VPD} = e_a^* - e_a.
        
        .. |VPD| replace:: :math:`\\text{VPD}` [kPa]
        .. |e_a| replace:: :math:`e_a` [kPa]
        .. |e_star| replace:: :math:`e_a^*` [kPa]
        """

        vpd = self.calc_svp() - self.e_a

        return vpd

    def calc_lapse_rate(self):
        """
        Calculate the lapse rate of air.

        Returns
        -------
        gamma : float
            Lapse rate of air |[K m-1]|
        
        Notes
        -----
        The lapse rate, |gamma|, is defined as the rate of change of temperature 
        with height, |z|:

        .. math::

            \Gamma = - \\frac{dT_a}{dz}
        
        .. |[K m-1]| replace:: [K m\ :sup:`-1`]
        .. |gamma| replace:: :math:`\Gamma` [K m\ :sup:`-1`]
        .. |z| replace:: :math:`z` [m]
        """
        
        r_v = self.calc_r_v()

        gamma = G * ( 
            (1 + (self.lambda_v * r_v) / (R_D * self.T_a)) / 
            ( c_pd + ((self.lambda_v**2 * r_v) / (R_v * self.T_a**2)) ) 
        )
        return gamma


    def calc_svp(self):
        """
        Calculates the saturation vapour pressure using the Tetens equation.

        Parameters
        ----------
        T_a : float
            Temperature [K]

        Returns
        -------
        e_star : float
            Saturation vapour pressure [kPa]

        Notes
        -----
        The saturation vapour pressure, |e_star|, is calculated using the Tetens
        equation [1]_:

        .. math::

            e_a^* = a \exp \left( \\frac{b (T_a+273.15)}{c + T_a + 273.15} \\right)
        
        where |a = 0.611|, |b = 17.502|, and |c = 240.97| are 
        constants.

        .. |e_star| replace:: :math:`e_a^*` [kPa]
        .. |a = 0.611| replace:: :math:`a = 0.611`
        .. |b = 17.502| replace:: :math:`b = 17.502`
        .. |c = 240.97| replace:: :math:`c = 240.97`

        References
        ----------
        .. [1] Buck, A. L. (1981). New Equations for Computing Vapor Pressure and 
           Enhancement Factor. Journal of Applied Meteorology and Climatology, 
           20(12). https://doi.org/10.1175/1520-0450(1981)020%3C1527:NEFCVP%3E2.0.CO;2


        """
        # TODO: Raise a warning if T_a is not in range for Teten's equation.
        T_C = self.T_a - 273.15

        e_star = 0.611 * np.exp((17.502 * T_C) / (T_C + 240.97))

        return e_star


    def calc_slope_svp(self):
        """
        Calculates the slope of the saturation vapour pressure line.

        Parameters
        ----------
        T_a : float
            Temperature [K]

        Returns
        -------
        delta : float
            Slope of the saturation vapour pressure curve [unitless]

        Notes
        -----
        The slope of the saturation vapour pressure curve, |delta|, is calculated as [1]_:

        .. math::

            \delta = \\frac{b \cdot c \cdot e_a^*}{(c + T_a + 273.15)^2}
        
        where |e_star| is the saturation vapour pressure, |T_a| is the air temperature,
        |a = 0.611|, |b = 17.502|, and |c = 240.97|.

        .. |delta| replace:: :math:`\delta`
        .. |e_star| replace:: :math:`e_a^*` [kPa]
        .. |T_a| replace:: :math:`T_a` [K]
        .. |a = 0.611| replace:: :math:`a = 0.611`
        .. |b = 17.502| replace:: :math:`b = 17.502`
        .. |c = 240.97| replace:: :math:`c = 240.97`

        References
        ----------
        .. [1] Campbell, G. S., & Norman, J. (1998). An Introduction to Environmental 
            Biophysics. Springer Science & Business Media. (Eq. 3.9).
        """
        T_C = self.T_a - 273.15
        e_star = self.calc_svp()

        delta = (17.502 * 240.97 * e_star) / ((240.97 + T_C)**2)

        return delta
    


    def calc_Tv(self):
        """
        Calculate the virtual temperature.

        Parameters
        ----------
        T_a : float
            Air temperature [K]
        
        p_a : float
            Air pressure [kPa]
        
        e_a : float
            Vapour pressure [kPa]

        Returns
        -------
        T_v : float
            Virtual air temperature [K]
        
        Notes
        -----
        The virtual temperature, |T_v|, is calculated as [4]_:

        .. math::

            T_v = T_a \left( \\frac{1 + r_v}{\epsilon (1 + r_v)} \\right)
        
        where |r_v| is the mixing ratio, |T_a| is the air temperature, and |epsilon| 
        is the ratio of the gas constants for dry air and water vapour.

        .. |T_v| replace:: :math:`T_v` [K]
        .. |r_v| replace:: :math:`r_v` [--]
        .. |T_a| replace:: :math:`T_a` [K]

        References
        ----------
        .. [4] https://glossary.ametsoc.org/wiki/Virtual_temperature
        """

        r_v = self.calc_r_v()

        T_v = self.T_a * ( (1 + r_v) / (EPSILON * (1 + r_v)) )

        return T_v
    

    def calc_r_v(self):
        """
        Calculate the mixing ratio of a parcel of air.

        Parameters
        ----------
        p_a : float
            Total pressure of air. Units must match `e_a`.
        
        e_a : float
            Vapour pressure of air. Units must match `p_a`.
        
        Returns
        -------
        r_v : float
            Mixing ratio (unitless)
        
        Notes
        -----
        The mixing ratio, |r_v|, is calculated as:

        .. math::

            r_v = \\frac{\epsilon e_a}{p_a - e_a}
        
        where |e_a| is the vapour pressure of air, |p_a| is the total pressure of air,
        and |epsilon| is the ratio of the gas constants for dry air and water vapour.

        .. |r_v| replace:: :math:`r_v` [unitless]
        .. |e_a| replace:: :math:`e_a` [kPa]
        .. |p_a| replace:: :math:`p_a` [kPa]
        .. |epsilon| replace:: :math:`\epsilon = 0.622`
            
        """

        r_v = (EPSILON * self.e_a) / (self.p_a - self.e_a)

        return r_v
    

    def calc_theta_v(self):
        """
        Calculate virtual potential temperature.

        Parameters
        ----------
        theta : float
            Potential temperature [K].

        q : float
            Specific humidity [kg kg-1].

        Returns
        -------
        theta_v : float
            Virtual potential temperature [K]
        
        Notes
        -----
        The virtual potential temperature, |theta_v|, is calculated as:

        .. math::

            \\theta_v = \\theta_a (1 + 0.61 q)
        
        where |theta| is the potential temperature, and |q| is the specific humidity [1]_.

        .. |theta_v| replace:: :math:`\\theta_v` [K]
        .. |theta| replace:: :math:`\\theta_a` [K]
        .. |q| replace:: :math:`q` [kg kg\ :sup:`-1`]

        References 
        ----------
        .. [1] https://glossary.ametsoc.org/wiki/Virtual_potential_temperature
        """
        theta_v = self.theta_a * (1 + 0.61*self.q)

        return theta_v

    def calc_psychrometric(self):
        """
        Calculate the psychrometric constant.

        Parameters
        ----------
        c_p : float
            Specific heat of air at constant pressure [J kg-1 K-1]
        
        p_a : float
            Air pressure [kPa]
        
        lambda_v : float
            Latent heat of vaporization [J kg-1]
        
        Returns
        -------
        gamma : float
            Psychrometric constant [kPa K-1]
        
        Notes
        -----
        The psychrometric constant, |gamma|, is calculated as [1]_:

        .. math::

            \gamma = \\frac{c_p p_a}{\\lambda_v \\epsilon}
        
        where |c_p| is the specific heat of air at constant pressure, |p_a| is the air
        pressure, |lambda_v| is the latent heat of vaporization, and |epsilon| is the
        ratio of the gas constants for dry air and water vapour (0.622).
        
        .. |gamma| replace:: :math:`\gamma` [kPa K\ :sup:`-1`]
        .. |c_p| replace:: :math:`c_p` [J kg\ :sup:`-1` K\ :sup:`-1`]
        .. |p_a| replace:: :math:`p_a` [kPa]
        .. |lambda_v| replace:: :math:`\lambda_v` [J kg\ :sup:`-1`]
        .. |epsilon| replace:: :math:`\epsilon` [--]

        References
        ----------

    
        """
        gamma = (self.c_p * self.p_a) / (self.lambda_v * EPSILON)

        return gamma


    
    def calc_emissivity(self):
    # def calc_emissivity(e_a,T_a):
        """
        Estimates the atmospheric emissivity for a clear sky.

        Parameters
        ----------
        e_a : float
            Vapor pressure of air [kPa].

        T_a : float
            Temperature of air [K]
        
        c : float, optional
            Cloud cover fraction [--].

        Returns
        -------
        epsilon_a : float
            Atmospheric emissivity [--]
        
        Notes
        -----
        Atmospheric emissivity, |epsilon_a|, is calculated from the vapor 
        pressure, |e_a|, and temperature of air, |T_a|, as [1]_:

        .. math::

            \epsilon_a = 1.24 \left( \\frac{e_a}{T_a} \\right)^{1/7}
        
        .. |epsilon_a| replace:: :math:`\epsilon_a` [--]
        .. |e_a| replace:: :math:`e_a` [kPa]
        .. |T_a| replace:: :math:`T_a` [K]

        References
        ----------
        .. [1] Brutsaert, W. (1975) On a derivable formula for long-wave radiation
            from clear skies, Water Resour. Res., 11(5), 742-744,
            htpp://dx.doi.org/10.1029/WR011i005p00742.
        """

        epsilon_ac = 1.24 * ((self.e_a * 10) / self.T_a )**(1./7.)

        epsilon_a = self._calc_cloudy_emissivity(epsilon_ac, self._cloud_fraction)

        return epsilon_a



    def _calc_cloudy_emissivity(self, eps_ac, c=0):
        """
        Calculates the atmospheric emissivity for a cloudy sky. Note that if c = 0, 
        then eps_a = eps_ac.

        Parameters
        ----------
        eps_ac : float
            Clear-sky atmospheric emissivity [-].
        
        c : float
            Cloud cover fraction [--]. The default is 0 (clear sky).

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




    def calc_wvc(self):
        """
        Calculate the water vapour content of air [mm Hg]

        Parameters
        ----------
        h_r : float | array-like
            Relative humidity [%]
        
        T_a : float | array_like
            Air temperature [K]

        Returns
        -------
        wvc : float | array-like
            Water vapour concentration [mm Hg]
        
        Notes
        -----
        The water vapour content of air, |wvc [mm Hg]|, is calculated as [1]_, [2]_:

        .. math::

            \omega = \\frac{h_r}{100} \cdot e^{( h_1 T_a^3 + h_2 T_a^2 + h_3 T_a + h_4 )}
        
        where |h_r| is the relative humidity, |T_a| is the air temperature, and
        |h_1|, |h_2|, |h_3|, and |h_4| are constants.

        .. |wvc [mm Hg]| replace:: :math:`\omega` [mm Hg]
        .. |h_r| replace:: :math:`h_r` [\%]
        .. |T_a| replace:: :math:`T_a` [K]
        .. |h_1| replace:: :math:`h_1 = 6.4385 \\times 10^{-7}`
        .. |h_2| replace:: :math:`h_2 = -2.7816 \\times 10^{-4}`
        .. |h_3| replace:: :math:`h_3 = 6.939 \\times 10^{-2}`
        .. |h_4| replace:: :math:`h_4 = 1.5587`

        References
        ----------
        .. [1] Tran, Q. H., Han, D., Kang, C., Haldar, A., & Huh, J. (2017). 
            Effects of Ambient Temperature and Relative Humidity on Subsurface 
            Defect Detection in Concrete Structures by Active Thermal Imaging. 
            Sensors, 17(8), Article 8. https://doi.org/10.3390/s17081718

        .. [2] Minkina, W., & Dudzik, S. (2009). Infrared Thermography: 
            Errors and Uncertainties. John Wiley & Sons.
        """
        h1 = 6.8455e-7
        h2 = -2.7816e-4
        h3 = 6.939e-2
        h4 = 1.5587

        T_aC = self.T_a - 273.15

        wvc = (self.h_r/100) * np.exp( 
            h1 * T_aC**3 + h2 * T_aC**2 + h3 * T_aC + h4
        )

        return wvc


    def calc_tau(self, wvc, d):
        """
        Calculate atmospheric transmissivity 

        Parameters
        ----------
        wvc : float | array_like
            Water vapour concentration [mm Hg]
        d : float | array-like
            Distance between surface and sensor [m]

        Returns
        -------
        tau : float | array_like
            Atmospheric transmissivity.

        Notes
        -----
        The atmospheric transmissivity, |tau|, is calculated as [1]_, [2]_:

        .. math::

            \\tau = K_{\\text{atm}} \cdot e^{-d^{1/2} (\\alpha_1 + \\beta_1 \omega ^{1/2}) } + ( 1 -K_{\\text{atm}}) \cdot e^{-d^{1/2} ( x_2 + \\beta_2 \omega ^{1/2} ) }

        where |K_atm| is the atmospheric transmissivity constant, |d| is the
        distance between the surface and the sensor, |alpha_1|, |beta_1|,
        |alpha_2|, and |beta_2| are constants, and |omega| is the water vapour
        concentration.

        .. |tau| replace:: :math:`\tau`
        .. |K_atm| replace:: :math:`K_{\\text{atm}} = 1.9`
        .. |d| replace:: :math:`d` [m]
        .. |alpha_1| replace:: :math:`\\alpha_1 = 6.569 \\times 10^{-3}`
        .. |beta_1| replace:: :math:`\\beta_1 = -2.276 \\times 10^{-3}`
        .. |alpha_2| replace:: :math:`\\alpha_2 = 0.01262`
        .. |beta_2| replace:: :math:`\\beta_2 = -6.67 \\times 10^{-3}`
        .. |omega| replace:: :math:`\omega` [mm Hg]

        References
        ----------
        .. [1] Tran, Q. H., Han, D., Kang, C., Haldar, A., & Huh, J. (2017). 
            Effects of Ambient Temperature and Relative Humidity on Subsurface 
            Defect Detection in Concrete Structures by Active Thermal Imaging. 
            Sensors, 17(8), Article 8. https://doi.org/10.3390/s17081718

        .. [2] Minkina, W., & Klecha, D. (2015). Modeling of Atmospheric Transmission 
            Coefficient in Infrared for Thermovision Measurements. Sensors and IRS² 2015, 
            903–907. https://doi.org/10.5162/irs2015/1.4
        """

        K_atm = 1.9
        a1 = 6.569e-3
        a2 = 0.01262
        b1 = -2.276e-3
        b2 = -6.67e-3

        tau = K_atm * np.exp( -(d**(1/2)) * (a1 + b1 * wvc**(1/2)) ) + \
            (1 - K_atm) * np.exp( -(d**(1/2)) * (a2 + b2 * wvc**(1/2)) )

        return tau