import numpy as np
# import xarray as xr

KAPPA = 0.41
c_pd = 1005.7               # specific heat capacity of dry air at constant pressure [J kg-1 K-1]
R_D = 287.058	 	        # dry gas constant (J kg-1 K-1)
G = 9.8

def calc_r_H(rho_a, c_p, p_a, T_s, T_a, H):
    """
    Calculate total resistance by inverting the sensible heat flux equation.
    """

    theta_coeff = ( (100 / p_a) ** (R_D/c_pd) )
    r_H = rho_a * c_p * ((theta_coeff * (T_s - T_a) ) / H)

    return r_H

def calc_r_aH(surf, u, Psi_M, Psi_H, Psi_M0=0, Psi_H0=0, z=3.8735):
# def calc_r_a(u, z, d_0, z_0m, z_0h, Psi_M, Psi_H):
    """
    Calculate aerodynamic resistance according to MOST.
    """

    # Calculate aerodynamic resistance
    r_a = ( (np.log((z - surf.d_0) / surf.z_0m) - Psi_M + Psi_M0) * \
            (np.log((z - surf.d_0) / surf.z_0h) - Psi_H + Psi_H0) ) / \
                (KAPPA**2 * u)

    return r_a

def calc_r_bH(u_0m, w_l, lai, c):
    """
    Calculate boundary layer resistance.
    """

    r_bH = (c / lai) * ( (w_l / u_0m) ** (1/2) )

    return r_bH

def calc_r_aM(u, u_star):

    r_aM = u / (u_star**2)

    return r_aM

# def calc_u(z, u_star, h, Psi_M, Psi_M0=0):
#     """
#     Calculate wind speed according to the logarithmic wind profile.
#     """
#     d_0 = calc_d0(h)
#     z_0m = calc_z0m(h)
    
#     u = (u_star / KAPPA) * (np.log((z - d_0) / z_0m) - Psi_M + Psi_M0)

#     return u

# def calc_ustar(u, h, Psi_M, Psi_M0=0, z=3.8735):
#     """
#     Calculate friction velocity according to MOST.
#     """
#     d_0 = calc_d0(h)
#     z_0m = calc_z0m(h)

#     u_star = ( u * KAPPA) /  (np.log((z - d_0) / z_0m) - Psi_M + Psi_M0)

#     return u_star


def calc_Psi_M(zeta):
    """
    Calculates the stability correction function for momentum transport.

    Reference: Brutsaert, W. (2005). Hydrology: An Introduction. Cambridge University Press.
    """

    Psi_m = np.real_if_close(np.where(zeta < 0, _calc_Psi_M_unstable(zeta), _calc_Psi_stable(zeta)))

    return Psi_m

def calc_Psi_H(zeta):
    """
    Calculates the stability correction function for heat (and vapour) transport.

    Reference: Brutsaert, W. (2005). Hydrology: An Introduction. Cambridge University Press.
    """
    Psi_h = np.real_if_close(np.where(zeta < 0, _calc_Psi_H_unstable(zeta), _calc_Psi_stable(zeta)))

    return Psi_h

def _calc_Psi_stable(zeta):
    """

    """
    a = 6.1
    b = 2.5
    Psi_m = -a * np.log(zeta + (1.0 + zeta**b)**(1.0/b))    # Eq. (2.59)

    return Psi_m

def _calc_Psi_M_unstable(zeta):
    """
    Calculate Psi_M for unstable conditions (zeta < 0).
    """
    a = 0.33
    b = 0.41
    y = -1 * zeta
    x = (y / a)**(1/3)

    Psi_0 = -np.log(a) + np.sqrt(3) * b * a**(1/3) * (np.pi/6.0)
    # y = min(y, b**(-1/3))
    y = np.where(y < b**(-1/3), y, b**(-1/3))

    Psi_m = np.log(a+y) - 3 * b * y**(1/3) + \
                ((b*a**(1/3)) / 2 ) * np.log( (1+x)**2 / (1 - x + x**2)) + \
                np.sqrt(3) * b * a**(1/3) * np.arctan((2*x - 1) / np.sqrt(3) ) + \
                Psi_0                       # Eq. (2.63)

    return Psi_m

def _calc_Psi_H_unstable(zeta):
    """
    Calculate Psi_H for unstable conditions (zeta < 0).
    """
    c = 0.33
    d = 0.057
    n = 0.78
    y = -1 * zeta

    Psi_h = ((1 - d) / n) * np.log((c + y**n) / c )     # Eq. (2.64)

    return Psi_h  


def calc_Hv(air, H, LE):
# def calc_Hv(H, LE, T_a, p_a, e_a):
    """
    Calculate virtual sensible heat flux.
    """
    # theta = met.calc_theta(T_a, p_a)
    E = LE / air.lambda_v
    # c_p = met.calc_cp(p_a, e_a)

    H_v = H + ( 0.61 * air.c_p * air.theta_a * E )

    return H_v

def calc_L(air, u_star, H, LE):
# def calc_L(self, u_star, theta_v, rho_a, c_p, H_v):
    """
    Calculate the Monin-Obukhov length, L [m].
    """

    H_v = calc_Hv(air, H, LE)
    # theta_v = met.calc_theta(T_a, p_a)

    L = - ( ( u_star**3 ) * air.theta_v ) / ( KAPPA * G * ( H_v / ( air.rho_a * air.c_p ) ) )

    return L

def calc_zeta(z, d_0, L):

    return (z - d_0) / L

def calc_u(z, u_star, d_0, z_0m, Psi_M, Psi_M0=0):
    """
    Calculate wind speed according to the logarithmic wind profile.
    """    
    u = (u_star / KAPPA) * (np.log((z - d_0) / z_0m) - Psi_M + Psi_M0)

    u = np.where(u < 0., 1e-6, u)

    return u

def calc_ustar(u, d_0, z_0m, Psi_M, Psi_M0=0, z=3.8735):
    """
    Calculate friction velocity according to MOST.
    """
    u_star = ( u * KAPPA) /  (np.log((z - d_0) / z_0m) - Psi_M + Psi_M0)

    return u_star


def calc_u0m(u_h, lai, h, d_0, z_0m, w_l):
    """
    Calculate wind speed at the source height for momentum transfer
    """

    a = 0.28 * (lai**(2/3)) * (h**(1/3)) * (w_l**(-1/3))
    # d_0 = res.calc_d0(h)
    # z_0m = res.calc_z0m(h)

    u_0m = u_h * np.exp(-a * (1 - ( (d_0 + z_0m) / h ) ) )

    return u_0m