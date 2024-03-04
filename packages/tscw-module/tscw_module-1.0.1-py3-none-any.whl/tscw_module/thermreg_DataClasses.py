import numpy as np
import re
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import mplcursors
from tkinter import *
from tkinter.ttk import *
from .helper_func import *

class ThermregData():
    '''
    Read in and process Thermreg output data.
    '''
    def __init__(self, path:str, n_depths:int = None):
        '''
        path: absolute path of Regtherm file (*.txt).
        n_dephts: how many vertical depth points (including z0 = 0m)
        '''
        self.path     = path
        self.n_depths = n_depths

        if n_depths is not None:
            temp_array  = np.empty((0,n_depths), float)
            press_array = np.empty((0,n_depths), float)
        else:
            temp_array  = None
            press_array = None

        t_total     = np.array([])
        t_etappe    = np.array([])
        t_neueEtappe = np.array([])
        temp_field   = None

        temp_split = 'T,GRD C:'
        pres_split = 'P,MPA  :'
        temp_field_split = 'TEMPERATURFELD'

        is_readNextRow = 0
        with open(path) as fid:
            for row in fid:

                if temp_split in row:
                    row_val = re.split(temp_split, row)[-1].split()
                    row_val = np.array([row_val], dtype=float)

                    if temp_array is None:
                        self.n_depths = row_val.shape[1]
                        temp_array = np.empty((0,self.n_depths), float)
                        press_array = np.empty((0,self.n_depths), float)

                    temp_array = np.append(temp_array, row_val, axis=0)
                    
                    row_val = prev_row.split()[0]
                    t_total = np.append(t_total,float(row_val))
                    
                    row_val = prev_row.split()[1]
                    t_etappe = np.append(t_etappe,float(row_val))

                if pres_split in row:
                    row_val = re.split(pres_split, row)[-1].split()
                    row_val = np.array([row_val], dtype=float)
                    press_array = np.append(press_array, row_val, axis=0)

                if temp_field_split in row:
                    is_readNextRow = self.n_depths - 1
                    continue

                if is_readNextRow > 0 and len(row) > 3: #avoid next line \n 
                    row_val     = np.array([row.split()], dtype=float)

                    if temp_field is None:
                        temp_field = np.empty((0,row_val.shape[1]), float)

                    temp_field  = np.append(temp_field, row_val, axis=0)
                    is_readNextRow -= 1

                prev_row = row

                if 'ETAPPE' in row:
                    try:
                        t_neueEtappe = np.append(t_neueEtappe, t_total[-1])
                    except:
                        pass

        self.t_neueEtappe = t_neueEtappe

        t_neueEtappe = np.append(t_neueEtappe, t_total[-1])

        i_etappen = np.zeros_like(t_total)
        idx1 = find_nearest(t_total, t_neueEtappe[0]) + 1
        i_etappen[:idx1] = 1
        etappen_counter = 2
        for i_etappe in range(len(t_neueEtappe[:-2])):
            idx1 = find_nearest(t_total, t_neueEtappe[i_etappe]) + 1
            idx2 = find_nearest(t_total, t_neueEtappe[i_etappe + 1]) + 1
            i_etappen[idx1:idx2] = etappen_counter
            etappen_counter += 1

        i_etappen[idx2:] = etappen_counter

        self.t_total = t_total
        self.temp_array = temp_array
        self.press_array = press_array
        self.i_etappen = i_etappen
        self.t_etappe = t_etappe
        self.temp_field = temp_field

        headers = ['STAGE'] + ['t_TOTAL [h]'] + ['t_Etappe [h]'] + ['T_z%d [deg]' % (i) for i in range(self.n_depths)] + ['p_z%d [MPa]' % (i) for i in range(self.n_depths)] 
        df = pd.DataFrame(np.column_stack((self.i_etappen,self.t_total,self.t_etappe,self.temp_array,self.press_array)))
        df.columns = headers

        self.df = df

        print('Succesfully inported Thermreg data %s\n' %(path))

    def export_csv(self):
        '''
        Export Thermreg p-T data into a xlsx file.
        '''
        dir_path = Path(self.path).parent
        file_name = Path(self.path).stem
        new_path = dir_path.joinpath(file_name + '_export.xlsx')
        self.df.to_excel(new_path, index=False, header=True)
        print('Succesfully exported Regtherm data to %s\n' %(new_path))

    def plot_tp_vs_depth(self, depths, times, is_export:bool = False):

        font =  {'family' : 'arial',
            'size' : 20}
        plt.rc('font', **font)
        plt.rcParams['lines.linewidth'] = 2 

        indices = []
        for time in times:
            indices.append(find_nearest(self.t_total, time))

        fig, ax1 = plt.subplots(constrained_layout = True)
        ax2 = ax1.twiny()

        ln = []
        for idx in indices:
            ln += ax1.plot(self.temp_array[idx,:],depths, 'o-',
                           label = '%.2fh [°C]' %(self.t_total[idx]) )
            ln += ax2.plot(self.press_array[idx,:],depths, 'o:',
                           label = '%.2fh [MPa]' %(self.t_total[idx]) )
            
        ax1.grid(which='major',linestyle='-')
        ax1.grid(which='minor',linestyle=':')   
        ax1.minorticks_on()

        plt.suptitle('') #p-T Distribution')
        plt.title(Path(self.path).name, fontsize = 10)
        ax1.set_xlabel('Temperature [°C]')
        ax2.set_xlabel('Pressure [MPa]')
        ax1.set_ylabel('Depth [m]')
        ax1.invert_yaxis()

        fig.legend(handles=ln, loc='outside upper center', ncol=3, labelspacing=0.5)

        if is_export:
            fig.set_size_inches(406 / 25.4, 229 / 25.4  )
            path = Path(self.path)
            save_path = path.parent.joinpath(path.stem + 'pt_vs_depth_thermreg.png')
            fig.savefig(save_path, dpi = 300)
            print('Saved\n%s' %(save_path))

    def plot_tp_vs_time(self, depths, is_export:bool = False):
        '''
        Plots a temperature - pressure diagram vs Time.
        INPUT:
        depths: array of depths (must match n_depths)
        is_export: true or false [optional]
        OUTPUT:
        figure
        '''
        font =  {'family' : 'arial',
            'size' : 20}
        plt.rc('font', **font)
        plt.rcParams['lines.linewidth'] = 2 

        assert len(depths) == self.n_depths 

        fig, ax1 = plt.subplots(constrained_layout = True)
        ax2      = ax1.twinx()
        ax1.grid(which='major',linestyle='-')
        ax1.grid(which='minor',linestyle=':')   
        ax1.minorticks_on()

        lines = []
        for i, depth in enumerate(depths):
            lines += ax1.plot(self.t_total, self.temp_array[:,i], label = '%.2fm - temp' %(depth)) 
        for i, depth in enumerate(depths): 
            lines += ax2.plot(self.t_total, self.press_array[:,i], ':', label = '%.2fm - pressure' %(depth)) 

        for t in self.t_neueEtappe:
            plt.axvline(x=t, linestyle= '--', linewidth = 1, color = 'black')

        ax1.set_xlabel('Time [h]')
        ax1.set_ylabel('Temperature [°C]')
        ax2.set_ylabel('Pressure [MPa]')
        fig.legend(handles=lines, loc='outside center right', ncol=1,
                    fontsize= 16, labelspacing=0.5)
        plt.suptitle('p-T Distribution')
        plt.title('%s' %(Path(self.path).name), fontsize = 16)

        # Cursor
        mplcursors.cursor(hover=2)

        if is_export:
            fig.set_size_inches(406 / 25.4, 229 / 25.4  )
            path = Path(self.path)
            save_path = path.parent.joinpath(path.stem + 'pt_vs_time_thermreg.png')
            fig.savefig(save_path, dpi = 300)
            print('Saved\n%s' %(save_path))

        return fig
    

    def calculate_axial_forces(self, meta_data:dict, T0:float = None, vectors=tuple, is_export:bool = False):
        '''
        Calculates resulting axial forces
        INPUT:
        meta_data: dictionary containing meta data.
        T0: Initial temperature for reference in delta_T
        vectors: tuple - (temperature, pressure) [K, MPa]
        is_export: true or false - as a xlsx file
        OUTPUT
        Dataframe
        '''

        t_vector = vectors[0]
        p_vector = vectors[1]

        if is_export:
            path = Path(self.path)
            file_path = path.parent.joinpath(path.stem + '_forces.xlsx')
        else:
            file_path = None

        if T0 is None:
            T0 = t_vector[0]

        df = calculate_forces(meta_data, t_vector, p_vector, self.t_total, self.t_etappe, T0 , file_path)

        self.forces_df = df

        return df
    

    def extract_max_force(self, i_etappe, mode, min_time:float = 0):
        '''
        Extracts min or max Fz_ges for a selected Stage.
        INPUT:
        i_etappe: int - Stage number
        mode: either 'min' or 'max'
        min_time: float - minimum time that has passed after the value is selected, put in +inf to select end of stage, 0 by default
        OUTPUT:
        filtered_df: pd.Dataframe containing relevant parameters
        df_index: int - index of total Dataframe df of respective class.
        '''

        assert mode in ['max', 'min'], 'Rechtschreibfehler!'

        filtered_df, df_index = filter_forces_fd(self.i_etappen, i_etappe, self.forces_df, mode, min_time)

        return filtered_df, df_index
    
    def plot_axial_forces(self, is_export:bool = False):
        '''
        Plots axial forces of forces_df.
        INPUT:
        is_export: bool - Export as png [optional]
        OUTPUT
        figure
        '''
        fig = plot_forces(self.forces_df, self.path, is_export)
        return fig
    

    def interpolate_pt(self, time_array):
        '''
        Interpolates pressure and temperature for a new time_array
        INPUT:
        time_array: list - new time array
        OUTPUT
        thermreg_temp_inter - interpolated temperature array
        thermreg_pres_inter - interpolated pressure array
        '''

        thermreg_temp_inter = np.zeros((time_array.shape[0], self.n_depths))
        thermreg_pres_inter = np.zeros_like(thermreg_temp_inter)

        for i in range(self.n_depths):

            f_temp = interpolate.interp1d(self.t_total,
                                        self.temp_array[:,i], fill_value='extrapolate' )
            f_press = interpolate.interp1d(self.t_total,
                                        self.press_array[:,i], fill_value='extrapolate' )
            
            thermreg_temp_inter[:,i] =  f_temp(time_array)
            thermreg_pres_inter[:,i] =  f_press(time_array)

        self.temp_array_inter  =  thermreg_temp_inter
        self.press_array_inter =  thermreg_pres_inter

        return thermreg_temp_inter, thermreg_pres_inter
    

    def plot_all_tempfields(self, depths = None, radial_vector = None, x2_limit:float = None, is_export:bool = False):

        n_field_dephts = self.n_depths - 1

        n_field = int(self.temp_field.shape[0] / n_field_dephts)

        if depths is not None:
            assert len(depths) == n_field_dephts
        else:
            depths = np.linspace(0,1,n_field_dephts)

        if radial_vector is not None:
            radial_vector[0] = 0
            assert len(radial_vector) == self.temp_field.shape[1] 
            self.radial_vector = radial_vector
        else:
            radial_vector = np.linspace(0,1,self.temp_field.shape[1])

        if x2_limit is None:
            x2_limit = np.max(radial_vector)

        min_val = np.min(self.temp_field + 273.15)
        max_val = np.max(self.temp_field + 273.15)
        for iField in range(n_field):
            fig, ax = plt.subplots()
            fig.canvas.manager.set_window_title('Figure %d' %(iField)) 
            temp_data = self.temp_field[iField*n_field_dephts:(iField+1)*n_field_dephts,:] + 273.15

            X,Y = np.meshgrid(radial_vector, depths)
            # Z   = temp_data[:-1, :-1]
            Z = temp_data
            cm = ax.contourf(X,Y,Z, levels = 100, cmap = 'jet', vmin = min_val, vmax = max_val)
            ax.set(ylabel = 'z [m]' , xlim = [0, x2_limit])
            ax.invert_yaxis()
            cbar = plt.colorbar(cm, ax = ax) #, format = '%.1f K', label = 'Temperature')
            cbar.ax.set_title('T [°C]', loc='center')

            if is_export:
                save_path = Path(self.path).parent.joinpath(Path(self.path).stem + 'Tempfield%d.png' %(iField))
                fig.savefig(save_path)
                print('Exported %s\n' %(save_path))