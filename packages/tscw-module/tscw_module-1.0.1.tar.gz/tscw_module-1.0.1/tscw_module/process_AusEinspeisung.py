import matplotlib.pyplot as plt
from pathlib import Path
from scipy import interpolate
import numpy as np

font =  {'family' : 'arial',
            'size' : 20}
plt.rc('font', **font)
plt.rcParams['lines.linewidth'] = 2 

width  = 406 / 25.4 # inches
height = 229 / 25.4 # inches
dpi    = max([1536/width, 864/height])



def create_overviewTable(result_table, data_class, meta_data, filtered_df, df_index):
    
    result_table.append({
        'File': Path(data_class.path).name,
        'Zeit_ges': data_class.t_total[df_index],
        'Zeit [h]': data_class.t_etappe[df_index],
        'Rate [m³/h]': meta_data['rate'],
        'p RS (C) [bara]': meta_data['p_RS_C'] * 10, # MPa -> bara
        'T RS (C) [°C]': meta_data['T_RS_C'],
        'p Bezugspunkt (B) [bara]': meta_data['p_RS_B'] * 10, # MPa -> bara
        'T Bezugspunkt (B) [°C]': meta_data['T_RS_B'], 
        'P Kopf (A) [bara]': meta_data['p_RS_A'] * 10, # MPa -> bara
        'T Kopf (A) [°C]': meta_data['T_RS_A'],
        'T mittel (A+B)/2 [°C]'   : filtered_df.T_m,
        'p mittel (A+B)/2 [bara]'   : filtered_df.p_m * 10, # MPa -> bara,
        # 'delta_T': filtered_df.delta_T,
        # 'delta_p': filtered_df.Fz_t,
        # 'Fz_t': filtered_df.Fz_t,
        # 'Fz_p': filtered_df.Fz_p,
        'Fz Gesamt [kN]' : np.round(filtered_df.Fz_ges),
        # 'Fz_p_rr': filtered_df.Fz_p_rr,
        'Fz Gesamt [kN] mit RR': np.round(filtered_df.Fz_ges_rr) })
    
    return result_table

##########################################

def plot_pTcav_comparison(tswc_data, thermreg_data, name_bohrung, is_export:bool = False):
    fig, ax1 = plt.subplots(constrained_layout = True)
    ax2      = ax1.twinx()
    ax1.grid(which='major',linestyle='-')
    ax1.grid(which='minor',linestyle=':')   
    ax1.minorticks_on()

    lines = []
    lines += ax1.plot(tswc_data.t_total, tswc_data.vertT_df.iloc[:,-2], label = 'T_cav TSWC') # RS
    lines += ax1.plot(thermreg_data.t_total, thermreg_data.temp_array[:,-1], label = 'T_cav THERMREG', linewidth = 3) 
    lines += ax2.plot(tswc_data.t_total, tswc_data.vertP_df.iloc[:,-2], ':', label = 'p_cav TSWC') # RS
    lines += ax2.plot(thermreg_data.t_total, thermreg_data.press_array[:,-1], '-.', label = 'p_cav THERMREG', linewidth = 3) 

    ax1.set_xlabel('Time [h]')
    ax1.set_ylabel('Temperature [°C]')
    ax2.set_ylabel('Pressure [MPa]')
    fig.legend(handles=lines, loc='outside center right', ncol=1,
                fontsize= 10, labelspacing=0.5)
    plt.suptitle(name_bohrung)

    if is_export:
        fig.set_size_inches(width, height)
        save_path = Path(thermreg_data.path).parent.joinpath(Path(tswc_data.path).stem + '_cav_comparison.png')
        fig.savefig(save_path, dpi = dpi)
        print('Successfully exported %s\n' %(save_path) )

    return fig

##########################################

def plot_pT_Overlap(thermreg_data, tswc_data, depths, is_export:bool = False):

    fig_thermreg = thermreg_data.plot_tp_vs_time(depths)
    fig_tswc = tswc_data.plot_tp_vs_time(depths,depths)

    lines = []
    lines += fig_thermreg.get_axes()[0].get_lines()
    lines += fig_thermreg.get_axes()[1].get_lines()

    for i in range(thermreg_data.n_depths):

        fig_thermreg.get_axes()[0].plot(tswc_data.t_total, thermreg_data.temp_array_inter[:,i], linestyle = '--', color = 'black', linewidth = 1)
        fig_thermreg.get_axes()[1].plot(tswc_data.t_total, thermreg_data.press_array_inter[:,i], linestyle = ':', color = 'black', linewidth = 1)

        ln_t = fig_tswc.get_axes()[0].plot(thermreg_data.t_total, thermreg_data.temp_array[:,i],
                                    label = 'Equivalent Thermreg Temperature Data',
                                    linestyle = '--', color = 'black', linewidth = 1)
        ln_p = fig_tswc.get_axes()[1].plot(thermreg_data.t_total, thermreg_data.press_array[:,i],
                                    label = 'Equivalent Thermreg Pressure Data' , linestyle = ':', color = 'black', linewidth = 1)

    lines += ln_t
    lines += ln_p

    fig_tswc.legends[0] = fig_tswc.legend(handles=lines, loc='outside center right', ncol=1,
                                            fontsize = 12, labelspacing = 0.5)

    if is_export:
        fig_tswc.set_size_inches(width, height)
        fig_thermreg.set_size_inches(width, height)
        fig_tswc.savefig(Path(thermreg_data.path).parent.joinpath(Path(tswc_data.path).stem + '_pt_development_tswc.png'), dpi = dpi)
        fig_thermreg.savefig(Path(thermreg_data.path).parent.joinpath(Path(thermreg_data.path).stem + '_pt_development_thermreg.png'),
                             dpi = dpi)
        print('Successfully exported %s\n' %(Path(thermreg_data.path).parent.joinpath(Path(tswc_data.path).stem + '_pt_development_tswc.png')) )
        print('Successfully exported %s\n' %(Path(thermreg_data.path).parent.joinpath(Path(thermreg_data.path).stem + '_pt_development_thermreg.png')) )


    return fig_tswc, fig_thermreg

##########################################

def plot_pt_Difference(tswc_data, thermreg_data, depths, is_export:bool = False):

    fig, ax1 = plt.subplots(constrained_layout = True)
    ax1.grid(which='major',linestyle='-')
    ax1.grid(which='minor',linestyle=':')   
    ax1.minorticks_on()

    lines = []
    for i, depth in enumerate(depths):  # Temperature
        y_tswc = tswc_data.vertT_df['%.2f' %(depth)]
        error = np.abs( (y_tswc - thermreg_data.temp_array_inter[:,i]) / y_tswc )*100
        lines += ax1.plot(tswc_data.t_total, error, label = '%.2f m - temp' %(depth)) 

    plt.gca().set_prop_cycle(None)
    for i, depth in enumerate(depths):  # Pressure
        y_tswc = tswc_data.vertP_df['%.2f' %(depth)]
        error = np.abs( (y_tswc - thermreg_data.press_array_inter[:,i]) / y_tswc )*100
        lines += ax1.plot(tswc_data.t_total, error, label = '%.2f m - press' %(depth), linestyle = ':') 

    ax1.set_xlabel('Time [h]')
    ax1.set_ylabel('[%]')

    fig.legend(handles=lines, loc='outside center right', ncol=1,
                fontsize= 10, labelspacing=0.5)
    plt.suptitle('%s - Rel. Error (TSWC - THERMREG)/TSWC' %(Path(tswc_data.path).name))

    if is_export:
        fig.set_size_inches(width, height)
        save_path = Path(thermreg_data.path).parent.joinpath(Path(tswc_data.path).stem + '_pt_Error.png')
        fig.savefig(save_path, dpi = dpi)
        print('Successfully exported %s\n' %(save_path) )

    return fig

##########################################

def plot_forces_difference(tswc_data, thermreg_data, is_export:bool = False):

    fig, ax = plt.subplots()
    labels = ['Fz_ges','Fz_t (Temperatur)','Fz_p (Ballooning)', 'Fz_p_rr (Ballooning)','Fz_ges_rr']
    for i, force in enumerate(['Fz_ges','Fz_t', 'Fz_p', 'Fz_p_rr', 'Fz_ges_rr']):
        f           = interpolate.interp1d(thermreg_data.t_total, thermreg_data.forces_df[force], fill_value='extrapolate')
        temp_force  = f(tswc_data.t_total)

        rel_error   = np.abs((tswc_data.forces_df[force] - temp_force))
        ax.plot(tswc_data.t_total, rel_error, label = labels[i])


    ax.grid(which='major',linestyle='-')
    ax.grid(which='minor',linestyle=':')   
    ax.minorticks_on()
    ax.set_ylabel('Differenz absolut')
    ax.set_xlabel('[h]')
    plt.title('%s\n%s' %(Path(tswc_data.path).name, Path(thermreg_data.path).name))
    plt.suptitle('Thermische Belastung nach WEG')
    ax.legend()

    if is_export:
        fig.set_size_inches(width, height)
        save_path = Path(thermreg_data.path).parent.joinpath(Path(tswc_data.path).stem + '_forces_Error.png')
        fig.savefig(save_path, dpi = dpi)
        print('Successfully exported %s\n' %(save_path) )

    return fig


