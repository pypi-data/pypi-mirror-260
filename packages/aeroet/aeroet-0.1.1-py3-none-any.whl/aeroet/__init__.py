# Load Main Classes into Module here.
# These can be accessed externally (e.g. from tests) using "from model import AirLayer". etc...
from .surface import Surface
from .air import AirLayer
from .radiation import Radiation
from . import radiation
from . import model


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
