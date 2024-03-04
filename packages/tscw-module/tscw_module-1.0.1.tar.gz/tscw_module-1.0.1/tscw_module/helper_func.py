import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import mplcursors
from tkinter import *
from tkinter.ttk import *
from scipy import interpolate

width  = 406 / 25.4 # inches
height = 229 / 25.4 # inches
dpi    = max([1536/width, 864/height])


def filter_forces_fd(etappen, i_ettape, forces_df, mode:str, min_time:float):
    '''
    Extracts min or max Fz_ges for a selected Stage.
    INPUT:
    etappen: array [1 x n_Zeitschritte] mit jeweiliger etappennummer
    i_ettape: int -  welche Etappe untersucht werden soll
    forces_df : dataframe output from 'calculate_forces'
    mode: str - either 'min' or 'max'
    min_time: float - minimum time that has passed after the value is selected, put in +inf to select end of stage
    OUTPUT:
    filtered_df: pd.Dataframe containing relevant parameters
    df_index: int - index of total Dataframe df of respective class.
    '''

    s = pd.Series(etappen == i_ettape, name = 'bools')
    filtered_df = forces_df[s.values]

    match mode:
        case 'min':
            df_index = filtered_df.Fz_ges[filtered_df.t_STAGE > min_time].idxmin()
        case 'max':
            try:
                df_index = filtered_df.Fz_ges[filtered_df.t_STAGE > min_time].idxmax()
            except ValueError:
                df_index = filtered_df.index[-1]

    filtered_df = filtered_df.loc[df_index,:]

    return filtered_df, df_index


def plot_forces(forces_df, path, is_export:bool = False):
    '''
    Plots axial forces of forces_df.
    INPUT:
    forces_df : dataframe output from 'calculate_forces'
    path: str - Its filename will be displayed in title of figure
    is_export: bool - Export as png
    OUTPUT
    figure
    '''

    Fz_ges = forces_df.Fz_ges
    Fz_t   = forces_df.Fz_t
    Fz_p   = forces_df.Fz_p
    t_total = forces_df.t_TOTAL

    fig, ax = plt.subplots()

    ax.plot(t_total, Fz_ges, label ='Fz_ges')
    ax.plot(t_total, Fz_t,   label ='Fz_t (Temperatur)')
    ax.plot(t_total, Fz_p,   label ='Fz_p (Balloning)')

    ax.legend()

    ax.grid(which='major',linestyle='-')
    ax.grid(which='minor',linestyle=':')   
    ax.minorticks_on()
    ax.set_ylabel('[kN]')
    ax.set_xlabel('[h]')
    # ax.set_ylim([-70, 230])

    plt.title('%s'%(Path(path).name))
    plt.suptitle('Thermische Belastung nach WEG')

    # Cursor
    mplcursors.cursor(hover=2)

    if is_export:
        fig.set_size_inches(width, height)
        fig.savefig(Path(path).parent.joinpath(Path(path).stem + '_forces.png'), dpi = dpi)

    return fig


def interpolate_1d(x1:list, dataset:tuple):
    '''
    Performs a 1D linear interpolation.
    INPUT:
    x1: list/array of new x values
    dataset: tuple (x2, y2) consisting of default x,y values.
    OUTPUT:
    New y2 values that match x1.
    '''

    f = interpolate.interp1d(dataset[0], dataset[1], fill_value='extrapolate')

    y2 =  f(x1)

    return y2    


def calculate_relative_error(y1, y2):
    rel_error = np.abs((y1 - y2))  # 
    return rel_error


def calculate_forces(meta_data, t_vector, p_vector, t_total, t_etappe, T0:float = None, file_path:str = None):
    '''
    Bezogen auf 
    Daten und Formeln aus berechnungenbbg_rev2.xlsx.
    INPUT:
    meta_data: dict - mit meta daten, die eingelesen werden
    t_vector: temperature [1 x n] array in [K]
    p_vector: pressure [1 x n] array in [MPa]
    t_total: total time [1 x n] array in [h]
    t_etappe: stage time [1 x n] array in [h]
    T0: temperature for reference in delta_t [optional - float], else T = t_total[0] 
    file_path: absolute file path to export results, needs to end with '.csv' [optional - str]
    OUTPUT:
    df - Dataframe containing relevant parameters
    '''
    p_vector = p_vector*1e6    # convert MPa to Pa

    g             = 9.81 # [m/s]  

    mu            = meta_data['mu']              # Querdehnungszahl              
    alpha         = meta_data['alpha']           # [1/K]
    e_modul_stahl = meta_data['e_modul_stahl']   # [Pa]
    z_bezug       = meta_data['z_bezug']         # [m]
    rho_rrsf      = meta_data['rho_rrsf']        # [kg/m3]
    wd            = meta_data['wd']              # m
    d_a           = meta_data['d_a']             # Außendurchmesser [m]


    d_i           = d_a - 2*wd          # Innendurchmesser [m]
    R             = d_a / d_i           # Durchmesserverhältnis

    if T0 is None:
        T0 = t_vector[0]

    A = np.pi * ((d_a/2)**2 - (d_i/2)**2)

    p_vergleich = rho_rrsf * g * z_bezug * 0.5  

    ## Ohne Ringraum

    delta_T = T0 - t_vector
    delta_p = p_vector - p_vergleich

    Fz_t = alpha * delta_T * e_modul_stahl * A

    Fz_p = np.zeros_like(p_vector)
    tf   = delta_p < 0

    # mit Formel
    F_p_i = 2*mu*A*delta_p / (R**2 - 1)
    F_p_a = 2*mu*A*R**2*delta_p / (R**2 - 1)

    Fz_p[~tf]  = F_p_i[~tf]
    Fz_p[tf]   = F_p_a[tf]

    # mit Approximation
    # Fz_p[tf]     = 0.471 * delta_p[tf] * d_a**2
    # Fz_p[~tf]    = 0.471 * delta_p[~tf] * d_i**2

    Fz_ges = Fz_t + Fz_p

    ## Mit Ringraum
    delta_p_rr = delta_p - 3e6
    # mit Formel
    Fz_p_rr    = 2*mu*A*R**2*delta_p_rr / (R**2 - 1)    # kontraballoning
    Fz_ges_rr  = Fz_p_rr + Fz_t

    # mit Approximation
    # Fz_p_rr    = 0.471 * delta_p_rr * d_a**2

    df = pd.DataFrame(np.column_stack((t_total, t_etappe,
                    p_vector*1e-6 ,t_vector,
                    delta_T, delta_p*1e-6, Fz_t*1e-3, Fz_p*1e-3, Fz_ges*1e-3, Fz_p_rr*1e-3, Fz_ges_rr*1e-3)))

    df.columns = ['t_TOTAL','t_STAGE', 'p_m','T_m', 'delta_T', 'delta_p', 'Fz_t', 'Fz_p', 'Fz_ges', 'Fz_p_rr', 'Fz_ges_rr']

    if file_path is not None:
        file_path = Path(file_path)
        if file_path.parent.exists():
            df.to_excel(file_path, index=False, header=True)
            print('Sucessfully exported %s' %(file_path))
        else:
            print('No export, given directory %s does not exist.' %(file_path.parent))

    return df


def find_nearest(array, value):
    '''
    Find nearest element in an array for a given value.
    '''
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)



