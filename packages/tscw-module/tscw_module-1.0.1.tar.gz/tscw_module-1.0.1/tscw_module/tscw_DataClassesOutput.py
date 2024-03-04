import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
import mplcursors
from pathlib import Path
from .helper_func import *
import matplotlib.animation as animation
import pickle
from tqdm import tqdm

# FFMPEG Path for video export
ffmpeg_path = r".ffmpeg\bin\ffmpeg.exe"
matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path

class TSCW_Output():
    '''
    Super class for TSWC Output. Other instances are inheritances of it. Must not be called!
    '''
    def __init__(self,**kwargs):
        '''
        Define meta data.
        '''
        width  = 406 / 25.4 # inches
        height = 229 / 25.4 # inches

        self.plot_meta = {
            'fs' : 20,          # font size
            'lw' : 2,           # line width
            'family' : 'arial', # font style
            'subtitle_scale' : 0.8, # scaling for subtitle in plots
            'width'  : width, # inches
            'height' : height, # inches
            'dpi'    : max([1536/width, 864/height])
        }

        if kwargs:
            for key, value in kwargs.item():
                self.plot_meta[key] = value

        self.font =  {'family' : self.plot_meta['family'],
                        'size' : self.plot_meta['fs']}


    def create_data_array2plot(self, all_plot_points, all_data, mode = 'time'):
        """Extracts data to plot. Must no be called by user (for intern purposes)

        :param all_plot_points: which depths to plot [depth_t, depth_p] 
        :type all_plot_points: list
        :param all_data: [self.vertT_df,self.vertP_df] temperature and pressure data
        :type all_data: list
        :param mode: either 'depth' or 'time', defaults to 'time'
        :type mode: str, optional
        :return: _description_
        :rtype: _type_
        """ 

        data   = dict()
        n_data_counter = 0
        for k, dtype in enumerate(['temp', 'pressure']):
            plot_points = all_plot_points[k] # [depth_t, depth_p] 
            data_temp   = all_data[k]        # either time or depth
            for i, point in enumerate(plot_points):
                match mode:
                    case 'time':
                        idx = find_nearest(self.depth_array, point)
                        key_depth = '%.2f' %(self.depth_array[idx])
                    
                        data[n_data_counter] = {
                            'x' : self.t_total,
                            'y' : data_temp[key_depth],
                            'label' : '%.2fm - %s' %(self.depth_array[idx], dtype),
                            'dtype' : dtype,
                            'color' : None
                        }

                    case 'depth':
                        idx = find_nearest(self.t_total, point)

                        data[n_data_counter] = {
                            'x' : data_temp.iloc[idx, :],
                            'y' : self.depth_array,
                            'label' : '%.2fh - %s' %(self.t_total[idx], dtype),
                            'dtype' : dtype,
                            'color' : None
                        }

                n_data_counter += 1

        return data


    def create_pT_plot(self, data, meta:dict):
        """creates a temperture - pressure plot against time or depth.

        :param data: output from create_data_array2plot
        :type data: 
        :param meta: containing information for meta data in plot
        :type meta: dict
        :return: _description_
        :rtype: _type_
        """        

        plt.rc('font', **self.font)
        fig, ax1 = plt.subplots(constrained_layout = True)

        lines = []

        match meta['xlabel']:
            case 'time':
                ax2 = ax1.twinx()
                linestyle = ''
            case 'depth':
                ax2 = ax1.twiny()
                linestyle = 'o'

        for key in data.keys():
            sub_data = data[key]

            match sub_data['dtype']:
                case 'temp':
                    ln = ax1.plot(sub_data['x'],sub_data['y'], linestyle + '-' ,label = sub_data['label'], color = sub_data['color'],
                            linewidth = self.plot_meta['lw'])
                case 'pressure':
                    ln = ax2.plot(sub_data['x'],sub_data['y'], linestyle + ':',label = sub_data['label'], color = sub_data['color'],
                            linewidth = self.plot_meta['lw'])
            
            lines += ln

        labs = [l.get_label() for l in lines]

        ax1.grid(which='major',linestyle='-')
        ax1.grid(which='minor',linestyle=':')   
        ax1.minorticks_on()
        plt.suptitle(meta['title'])
        plt.title(meta['subtitle'], fontsize = self.plot_meta['subtitle_scale']*self.plot_meta['fs']*0.5)

        match meta['xlabel']:
            case 'time':

                ax1.set_xlabel('Time [h]')
                ax1.set_ylabel('Temperature [°C]')
                ax2.set_ylabel('Pressure [MPa]')

                for stage, i_stage in zip(self.stage_idx[0], self.stage_idx[1]):
                    plt.axvline(x = self.t_total[i_stage], label= 'Stage %d' %(stage) 
                                , linestyle='-.', color = 'black', linewidth = 0.3 * self.plot_meta['lw'])

            case 'depth':
                ax1.set_xlabel('Temperature [°C]')
                ax2.set_xlabel('Pressure [MPa]')
                ax1.set_ylabel('Depth [m]')
                ax1.invert_yaxis()

        fig.legend(handles=lines, loc='outside center right', ncol=1,
                   fontsize=self.plot_meta['subtitle_scale']*self.plot_meta['fs'], labelspacing=0.5)

        # Cursor
        mplcursors.cursor(hover=2)

        if meta['is_export']:
            fig.set_size_inches(self.plot_meta['width'], self.plot_meta['height'])
            save_path = Path(self.path).parent.joinpath(Path(self.path).stem + meta['suffix'] + '.png')
            i = 1
            while save_path.exists():
                name = save_path.stem
                path = save_path.parent
                save_path = path.joinpath(name + '_' + str(i) + '.png')
                i += 1
            fig.savefig(save_path, dpi = self.plot_meta['dpi'])
            print('Successfully exported %s\n' %(save_path) )

        return fig
        

    def calculate_axial_forces_super(self, meta_data, t_vector, p_vector, t_total,
                                     t_etappe, T0:float = None, export_dir:str = None):
        """  Berechnet Axialkraft bezogen auf Ansatz BB122 aus dem Jahr 2011.
        Daten und Formeln aus berechnungenbbg_rev2.xlsx.

        :param meta_data: _description_
        :type meta_data: _type_
        :param t_vector: temperature  in [K]
        :type t_vector: [1 x n] array
        :param p_vector: pressure in [MPa]
        :type p_vector: [1 x n] array
        :param t_total: total time  in [h]
        :type t_total: [1 x n] array
        :param t_etappe: stage time  in [h]
        :type t_etappe: [1 x n] array
        :param T0: temperature for reference in delta_t [optional - float], else T = t_total[0] 
        :type T0: float, optional
        :param export_dir: absolute file path to export results, needs to end with '.xlsx' , defaults to None
        :type export_dir: str, optional
        :return: pandas dataframe containing forces
        :rtype: pd.Dataframe
        """       

        df = calculate_forces(meta_data, t_vector, p_vector, t_total, t_etappe, T0, export_dir)

        return df


####################################################################################

class TSCW_TBHC(TSCW_Output):
    """    Reads data from Projektname_i_pTBHC.txt
    Important attributes:
    self.sr_df: - meta data
    self.vertT_df: - temperature data
    self.vertP_df: - pressure data
    """   
    def __init__(self, path):
        super().__init__()

        self.path = path

        fid  = open(self.path,'r')
        line = fid.readlines()[4].split('\t')
        line = [item.replace('\n', '') for item in line]
        idx  = [index for index, item in enumerate(line) if item == '***']

        df = pd.read_csv(self.path, skiprows=4,
                         sep=r'\t*\*\*\*\t*\s*|\s*\t\*\*\*\s*|\t\s*',
                         engine='python') 

        # lines2drop = [0,1,2]            # drop the first three lines due to the three asterics *** in txt file, TODO: read it in as fid open to also read the first three lines.
        # df = df.drop(lines2drop)
        # df = df.reset_index(drop=True)
        self.df = df

        print('Succesfully loaded %s' %(os.path.basename(path)))

        idx = [index for index, item in enumerate(df.columns.to_list()) if item == '0.00' or item == '0.00.1' or item == '0.0' or item == '0.0.1']  # zwei gleiche Schlüssel

        self.sr_df       = self.df.iloc[:,:idx[0]]

        vertT_df    = self.df.iloc[:,idx[0]:idx[1]]
        data_column = []
        for m in vertT_df.columns:
            if m.count('.') > 1:
                idx_string = [i for i, letter in enumerate(m) if letter == '.']
                data_column.append(m[:idx_string[1]] + '1')
            else:
                data_column.append('%.2f' %(float(m)))


        vertT_df    = vertT_df.rename(columns={key:value for key,value in zip(vertT_df.columns, data_column)}) # give same column names to T and p
        self.vertT_df = vertT_df

        vertP_df    = self.df.iloc[:,idx[1]:]
        vertP_df    = vertP_df.rename(columns={key:value for key,value in zip(vertP_df.columns, data_column)}) # give same column names to T and p
        self.vertP_df = vertP_df

        self.depth_array = np.array(data_column, dtype = np.float32)
        self.t_total  = np.array(self.sr_df['t_TOTAL'])
        self.t_etappe = np.array(self.sr_df['t_STAGE'])

        self.stage_idx = np.unique(self.sr_df.STAGE, return_index=True)

    def plot_cavern_pt_development(self, is_export:bool = False):
        """Plots cavern pressure - temperature development over time.

        :param is_export: defaults to False
        :type is_export: bool, optional
        """        
        data = dict()

        data[0] = {
                    'x' : self.t_total,
                    'y' : self.sr_df['T_CAVERN'],
                    'label' : 'T_CAVERN',
                    'dtype' : 'temp',
                    'color' : 'red'
                }

        data[1] = {
                    'x' : self.t_total,
                    'y' : self.sr_df['T_WH'],
                    'label' : 'T_WH',
                    'dtype' : 'temp',
                    'color' : 'orange'
                }

        data[2] = {
                    'x' : self.t_total,
                    'y' : self.sr_df['p_CAVERN'],
                    'label' : 'p_CAVERN',
                    'dtype' : 'pressure',
                    'color' : 'red'
                }

        data[3] = {
                    'x' : self.t_total,
                    'y' : self.sr_df['p_WH'],
                    'label' : 'p_WH',
                    'dtype' : 'pressure',
                    'color' : 'orange'
                }

        meta = {
            'title' : 'Cavern p-T Distribution',
            'subtitle' : os.path.basename(self.path),
            'is_export': is_export,
            'suffix': 'pt_cav_development',
            'xlabel': 'time'
        }

        self.create_pT_plot(data, meta)

    def plot_tp_vs_time(self,depth_t = None,depth_p = None, is_export = False):
        """_summary_

        :param depth_t:  which depth intervals for Temperature, by default all
        :type depth_t: _type_, optional
        :param depth_p: _description_, defaults to None
        :type depth_p: which depth intervals for Pressure, by default all
        :param is_export: defaults to False
        :type is_export: bool, optional
        """        

        if depth_t is None:
            depth_t = self.depth_array
        
        if depth_p is None:
            depth_p = self.depth_array

        all_plot_points = [depth_t, depth_p]
        all_data        = [self.vertT_df,self.vertP_df]

        data = self.create_data_array2plot(all_plot_points, all_data)

        meta = {
            'title'       : 'p-T Distribution',
            'subtitle'    : os.path.basename(self.path),
            'is_export'   : is_export,
            'suffix'      : 'tp_vs_time',
            'xlabel'      : 'time'
        }

        fig = self.create_pT_plot(data, meta)

        return fig

    def plot_tp_vs_depth(self,depth_t = None,depth_p = None, is_export = False):
        """Plots borehole temperature - pressure development over depth.

        :param depth_t: which time intervals for Temperature, by default all
        :type depth_t: _type_, optional
        :param depth_p: which time intervals for Pressure, by default all
        :type depth_p: _type_, optional
        :param is_export: defaults to False
        :type is_export: bool, optional
        """        
        
        if depth_t is None:
            depth_t = self.t_total
        
        if depth_p is None:
            depth_p = self.depth_array

        all_plot_points = [depth_t, depth_p]
        all_data        = [self.vertT_df,self.vertP_df]

        data = self.create_data_array2plot(all_plot_points, all_data, 'depth')

        meta = {
            'title': 'p-T Distribution',
            'subtitle' : os.path.basename(self.path),
            'is_export'   : is_export,
            'suffix': 'tp_vs_depth',
            'xlabel'   : 'depth'
        }

        self.create_pT_plot(data, meta)

    def export_csv(self, depths):
        """ Exports data to a xlsx- file.

        :param depths:  which depths to export (alogrithm looks for closest match)
        :type depths: list
        """        
        depth_keys = []
        for depth in depths:
            depth_keys.append(self.depth_array[find_nearest(self.depth_array,depth)])


        dir_path = Path(self.path).parent
        file_name = Path(self.path).stem
        new_path = dir_path.joinpath(file_name + '_export.xlsx')
        headers = ['t_TOTAL [h]'] + ['t_Etappe [h]'] + ['T_(z = %.2fm) [deg]' % (i) for i in depth_keys] + ['p_(z = %.2fm) [MPa]' % (i) for i in depth_keys] 
        
        data_array = np.column_stack((self.sr_df.t_TOTAL, self.sr_df.t_STAGE))
        for depth in depth_keys:
            data_array = np.column_stack((data_array, self.vertT_df['%.2f' %(depth)]))
        for depth in depth_keys:
            data_array = np.column_stack((data_array, self.vertP_df['%.2f' %(depth)]))
        
        df = pd.DataFrame(data_array)
        df.columns = headers
        df.to_excel(new_path, index=False, header=True)

        print('Succesfully exported Regtherm data to %s\n' %(new_path))

    def calculate_axial_forces(self, meta_data, z_ref, T0:float = None, is_export:bool = False):
        """Calculates resulting axial forces

        :param meta_data:  dictionary containing meta data.
        :type meta_data: dict
        :param z_ref: reference depth, temperature and pressure array will be calculated by the mean at z_ref and z0 = 0m.
        :type z_ref: _type_
        :param T0:  Initial temperature for reference in delta_T, if None it will be the first element of the temperature array.
        :type T0: float, optional
        :param is_export: _description_, defaults to False
        :type is_export: bool, optional
        :return: pandas dataframe containing forces
        :rtype: pd.Dataframe
        """    
        
 
        i_z0 = np.where(self.depth_array < z_ref)[0][-1]
        i_z1 = np.where(self.depth_array >= z_ref)[0][0]

        z0 = self.depth_array[i_z0]
        z1 = self.depth_array[i_z1]

        t_vector = np.zeros_like(self.t_total)
        p_vector = np.zeros_like(t_vector)

        # for i_time in range(len(self.t_total)):
        #     f_t = interpolate.interp1d([z0, z1],
        #                                 [self.vertT_df['%.2f'%(z0)].iloc[i_time],
        #                                 self.vertT_df['%.2f'%(z1)].iloc[i_time]]) 

        #     f_p = interpolate.interp1d([z0, z1],
        #                             [self.vertP_df['%.2f'%(z0)].iloc[i_time],
        #                             self.vertP_df['%.2f'%(z1)].iloc[i_time]]) 

            # t_vector[i_time] = f_t(z_ref)
            # p_vector[i_time] = f_p(z_ref)

        #TODO: Take mean temperature between z_ref and 0
        z_ref = self.depth_array[find_nearest(self.depth_array, z_ref)]

        t_vector = np.mean((self.vertT_df['%.2f'%(z_ref)].to_numpy(), self.vertT_df.iloc[:,0].to_numpy()), axis = 0)
        p_vector = np.mean((self.vertP_df['%.2f'%(z_ref)].to_numpy(), self.vertP_df.iloc[:,0].to_numpy()), axis = 0)


        if T0 is None:
            T0 = t_vector[0]

        if is_export:
            path = Path(self.path)
            export_dir = path.parent.joinpath(path.stem + '_forces.xlsx')
        else:
            export_dir = None


        df = self.calculate_axial_forces_super(meta_data, t_vector, p_vector,
                                          self.t_total, self.sr_df.t_STAGE,
                                          T0, export_dir)

        self.forces_df = df

        return df

    def extract_max_force(self, i_etappe:int, mode:str, min_time:float = 0):
        """ Extracts min or max Fz_ges for a selected Stage.

        :param i_etappe: Stage number
        :type i_etappe: int
        :param mode: either 'min' or 'max'
        :type mode: str
        :param min_time: float - minimum time that has passed after the value is selected, put in +inf to select end of stage, 0 by default, defaults to 0
        :type min_time: float, optional
        :return: pd.Dataframe containing relevant parameters, respective index in self.df
        :rtype: _type_
        """       
        assert mode in ['max', 'min'], 'Rechtschreibfehler!'

        filtered_df, df_index = filter_forces_fd(self.sr_df.STAGE, i_etappe, self.forces_df, mode, min_time)

        return filtered_df, df_index


    def plot_axial_forces(self, is_export:bool = False):
        """Plots axial forces of forces_df.

        :param is_export: Export as png, defaults to False
        :type is_export: bool, optional
        :rtype: figure
        """       
        fig = plot_forces(self.forces_df, self.path, is_export)
        return fig
    
    def plot_forces_difference(self, *args):
        """Plot difference between calculated forces. Pass other TSWC_TBHC instances as input (comma separated).
        :param args: Other instances of TSWC_TBHC.
        :rtype: figure
        """        
        labels = ['Fz_ges','Fz_t (Temperatur)','Fz_p (Ballooning)']
        forces = ['Fz_ges','Fz_t','Fz_p']

        Fz            = np.zeros(( len(args), len(forces), len(self.t_total)))
        Fz_difference = np.zeros_like(Fz)

        paths = []
        for idx, arg in enumerate(args):
            if np.array_equal(arg.t_total, self.t_total):
                Fz[idx,0,:] = arg.forces_df.Fz_ges
                Fz[idx,1,:] = arg.forces_df.Fz_t
                Fz[idx,2,:] = arg.forces_df.Fz_p
            else:
                for i_force in range(len(forces)):
                    f = interpolate.interp1d(arg.t_total, arg.forces_df[forces[i_force]], fill_value='extrapolate')
                    interpolated_force = f(self.t_total)
                    Fz[idx,i_force,:]  = interpolated_force

            paths.append(arg.path)
            Fz_difference[idx,0,:] = np.abs(self.forces_df.Fz_ges - Fz[idx,0,:])
            Fz_difference[idx,1,:] = np.abs(self.forces_df.Fz_t - Fz[idx,1,:])
            Fz_difference[idx,2,:] = np.abs(self.forces_df.Fz_p - Fz[idx,2,:])

        Fz = np.vstack([Fz, np.array([self.forces_df['Fz_ges'], self.forces_df['Fz_t'], self.forces_df['Fz_p']])[None,:,:] ] )
        paths.append(self.path)

        colors =  matplotlib.cm.Set1(range(Fz.shape[0]))
        fig, axes = plt.subplots(nrows=2, constrained_layout=True)
        for idx_arg, color in enumerate(colors):
                 temp_path = Path(paths[idx_arg])
                 axes[0].plot(self.t_total, Fz[idx_arg,0,:], color=color,
                                label='%s - Fz_ges' %(temp_path.stem) ,linestyle='-')
                 axes[0].plot(self.t_total, Fz[idx_arg,1,:], color=color,
                                label='%s - Fz_t' %(temp_path.stem) ,linestyle='--')
                 axes[0].plot(self.t_total, Fz[idx_arg,2,:], color=color,
                                label='%s - Fz_p' %(temp_path.stem) ,linestyle=':')

        for idx_arg, color in enumerate(colors[:-1]):
                 axes[1].plot(self.t_total, Fz_difference[idx_arg,0,:], color=color, linestyle='-')
                 axes[1].plot(self.t_total, Fz_difference[idx_arg,1,:], color=color, linestyle='--')
                 axes[1].plot(self.t_total, Fz_difference[idx_arg,2,:], color=color, linestyle=':')

        for ax in axes:
            ax.grid(which='major',linestyle='-')
            ax.grid(which='minor',linestyle=':')   
            ax.minorticks_on()

        fig.legend(loc='outside upper center', ncols=2, fontsize = 10)
        axes[0].set(ylabel='[kN]', title='Axial Forces')
        axes[1].set(xlabel='time [h]', ylabel='[kN]', title='Absolute Difference')

        return fig


    def plot_pt_difference(self, depths, *args):
        
        depths_keys = []
        for depth in depths:
            depths_keys.append('%.2f' %(self.depth_array[find_nearest(self.depth_array, depth)]))

        pT_data            = np.zeros(( len(args), 2, len(depths_keys), len(self.t_total)))
        pT_data_difference = np.zeros_like(pT_data)

        paths = []
        for idx, arg in enumerate(args):
            if np.array_equal(arg.t_total, self.t_total):
                pT_data[idx,0,:,:] = arg.vertT_df[depths_keys]
                pT_data[idx,1,:,:] = arg.vertP_df[depths_keys]
            else:
                for i, depth in enumerate(depths_keys):
                    f_t = interpolate.interp1d(arg.t_total, arg.vertT_df[depth], fill_value='extrapolate')
                    f_p = interpolate.interp1d(arg.t_total, arg.vertP_df[depth], fill_value='extrapolate')

                    pT_data[idx,0,i,:] = f_t(self.t_total)
                    pT_data[idx,1,i,:] = f_p(self.t_total)

            paths.append(arg.path)
            pT_data_difference[idx, 0, :, :] = pT_data[idx, 0, :, :] - self.vertT_df[depths_keys] 
            pT_data_difference[idx, 1, :, :] = pT_data[idx, 1, :, :] - self.vertP_df[depths_keys] 

####################################################################################

class TSCW_TFBH(TSCW_Output):
    """Reads data from /*_TFBH.TXT (Radial temperature along depth in borehole).
    Stores data in
    self.data: - data
    """   
    def __init__(self, path:str):
        super().__init__()

        self.path = path
        data      = pd.read_csv(self.path, sep=r'\s*\t\s*', engine='python')
        self.df   = data

        idx = [index for index, item in enumerate(data.columns.to_list()) if '0.0' in item]  # zwei gleiche Schlüssel
        
        self.meta = data.iloc[:,:idx[0]]
        self.data = data.iloc[:,idx[0]:]

        self.t_total = np.unique(self.meta.t_TOTAL)

        self.depth_vector = np.unique(self.meta.Depth)

        data_column = []
        for m in self.data.columns:
            if m.count('.') > 1:
                idx = [i for i, letter in enumerate(m) if letter == '.']
                data_column.append(m[:idx[1]] + '1')
            else:
                data_column.append(m)

        self.radial_vector = np.array(data_column, dtype=float)


    def plot_temp_distribution(self, times:list, depths:list = None, range_radial: list = None, is_colormap:bool = True,  n_levels: int = 150):
        """The values given in all input lists do not need to match exactly with the simulation result.
        The algorithm automatically finds the nearest neighbor.

        :param times: which time points 
        :type times: list
        :param depths:  which depth points, defaults to None
        :type depths: list, optional
        :param range_radial:  [x0, x1] beginning and end of radial range, defaults to None
        :type range_radial: list, optional
        :param is_colormap: plot as a colormap or line plot, defaults to True
        :type is_colormap: bool, optional
        :param n_levels: how many levels in pcolormesh plot, defaults to 150
        :type n_levels: int, optional
        :rtype: figure
        """      

        # Find radial indices to plot
        if range_radial is not None:
            idx1 = find_nearest(self.radial_vector, range_radial[0])
            idx2 = find_nearest(self.radial_vector, range_radial[1])
        else:
            idx1 = 0
            idx2 = self.radial_vector.shape[1]

        # Find total time indices to plot
        indices_t = []
        for time in times:
            indices_t.append(find_nearest(self.t_total, time))

        # Find depths to plot 
        if depths is None:
            indices_d = list(range(len(self.depth_vector)))
        else:
            indices_d = []
            for depth in depths:
                indices_d.append(find_nearest(self.depth_vector, depth))

        # Find respective depth indices to plot
        indices_depth = []
        for idx_t in indices_t:
            tf_time = self.meta.t_TOTAL == self.t_total[idx_t] 
            for idx_d in indices_d:
                tf_depth = (self.meta.Depth == self.depth_vector[idx_d])
                tf_depth = [tf_d and tf_t for tf_d, tf_t in zip(tf_time, tf_depth)]
                tf_depth = np.nonzero(np.array(tf_depth))[0]    # should be a scalar
                try:
                    indices_depth.append(int(tf_depth))
                except TypeError:
                    indices_depth.append(int(tf_depth[0]))
        
        data = self.data.iloc[indices_depth, :] #+ 273.15   # convert °C -> K
        meta = self.meta.iloc[indices_depth, :]

        print(data)
        print(meta)

        plt.rc('font', **self.font)

        max_val = np.max(data)
        min_val = np.min(data)
        if is_colormap:
            fig, axes = plt.subplots(ncols=len(times), constrained_layout = True, sharey=True)
            if len(times) < 2:
                axes = [axes]
            for ax, i_time in zip(axes, indices_t):
                temp_data = data[meta.t_TOTAL == self.t_total[i_time]]
                cur_stage = np.unique(meta.STAGE[meta.t_TOTAL == self.t_total[i_time]])[0]
                X,Y = np.meshgrid(self.radial_vector[idx1:idx2+1],self.depth_vector[indices_d])
                Z = temp_data.iloc[:,idx1:idx2+1] 
                cm = ax.contourf(X,Y,Z, levels = n_levels, cmap = 'jet', vmin = min_val, vmax = max_val)
                # ticklabs = cbar.ax.get_yticklabels()
                # cbar.ax.set_yticklabels(ticklabs, fontsize=10)
                # ax.set_clim(min_val, max_val)
                ax.set_title('t = %.2fh (Ett. %d)' %(self.t_total[i_time], cur_stage))
                ax.set_xlabel('x [m]')

            axes[0].set_ylabel('z [m]')
            axes[0].invert_yaxis()
            cbar = plt.colorbar(cm, ax = axes[-1]) #, format = '%.1f K', label = 'Temperature')
            cbar.ax.set_title('T [°C]', loc='center')

        else:
            fig, axs = plt.subplots(len(indices_d), 1, sharex=True, sharey=True, constrained_layout=True)

            for i_depth, ax in enumerate(axs):
                temp_depth = meta.Depth.iloc[i_depth]
                temp_data  = data.loc[meta.Depth == temp_depth]
                temp_meta  = meta.loc[meta.Depth == temp_depth]
                for i_row in range(len(temp_data)):

                    ax.plot(self.radial_vector[idx1:idx2+1], temp_data.iloc[i_row,idx1:idx2+1],'o-',
                            label = '%.2f h (Stage %d)' %(temp_meta.t_TOTAL.iloc[i_row], temp_meta.STAGE.iloc[i_row]) if i_depth == 0 else '',
                            linewidth = self.plot_meta['lw'])         # only save legend for first entry
                    ax.title.set_text('z = %.2f m' %(temp_depth))
                    ax.grid(which='major',linestyle='-')
                    ax.grid(which='minor',linestyle=':')   
                    ax.minorticks_on()
                    ax.set_ylabel('[°C]')

            fig.legend(loc='outside center right')
            ax.set_xlabel('x [m]')

        fig.suptitle('%s' %(os.path.basename(self.path)))

        return fig
    

    def create_movie(self, range_radial:list = None, 
                     is_export:bool = False, n_levels: int = 100,
                     field_data_picklePath:str = None):
        """Generates a time lapse of the simulated temperature.

        :param range_radial: [x0, x1] range of radial start and end point (no exact match needed), defaults to None
        :type range_radial: list, optional
        :param is_export: export movie as .mp4 into the same folder of current instance, defaults to False
        :type is_export: bool, optional
        :param n_levels: how many levels for plt.contourf, defaults to 150
        :type n_levels: int, optional
        :param field_data_picklePath: path to (/*.pickle) of FieldData class (if it has been exported). If loaded, the geometry will be displayed in the background., defaults to None
        :type field_data_picklePath: str, optional
        :return: animation
        :rtype: animation.FuncAnimation
        """        # Find radial indices to plot

        font =  {'family' : 'arial',
                    'size' : 15}
        alpha = 1
        plt.rc('font', **font)

        n_depths = len(self.depth_vector)

        max_val = np.max(self.data)
        min_val = np.min(self.data)

        Z = self.data.iloc[:n_depths ,:] 
        im_ratio = Z.shape[0]/Z.shape[1]
        fig, (ax,cax) = plt.subplots(1,2, gridspec_kw={"width_ratios":[1,0.02*im_ratio]}, constrained_layout = True)

        delta_z = 0
        is_antialiased = False
        if field_data_picklePath is not None:
            try:
                with open(field_data_picklePath, 'rb') as f:
                    field_data = pickle.load(f)
                    alpha      = 0.6
                    x_geom = field_data.radial_vector_borehole
                    y_geom = field_data.bottom_edge_vertical - field_data.delta_z
                    y_geom[-1] = field_data.bottom_edge_vertical[-1]
                    X_geom,Y_geom = np.meshgrid(np.insert(x_geom[:-1], 0, 0), y_geom)
                    Z_geom     = field_data.heat_capacity
                    Z_geom     = Z_geom[:-1, :-1]
                    ax.pcolormesh(X_geom, Y_geom, Z_geom, cmap = 'binary')
                    delta_z = field_data.delta_z
                    is_antialiased = True
            except:
                print('Failed to load %s' %(field_data_picklePath))

        x,y = self.radial_vector, self.depth_vector  + delta_z /2
        y[0] = 0 
        X,Y = np.meshgrid(x, y)

        contour_gid = 'contourf'
        cm      = ax.contourf(X,Y,Z, levels = n_levels, cmap = 'jet',
                              vmin = min_val, vmax = max_val, linewidths = 0)
        cm.set_gid(gid=contour_gid)     
        ax.set(xlabel='x [m]', ylabel='y [m]', xlim = [range_radial[0], range_radial[1]]) #, ylim = [y[0], y[-1]])
        ax.invert_yaxis()

        def animationUpdate(i):
            ax.findobj(lambda x: x.get_gid() == contour_gid)[0].remove()
            Z   	        = self.data.iloc[n_depths*i:n_depths*(i+1),:]
            cm              = ax.contourf(X,Y,Z, levels=n_levels, cmap = 'jet',
                                       vmin = min_val, vmax = max_val,
                                       alpha=alpha, antialiased=is_antialiased)
            cm.set_gid(gid=contour_gid)
            temp_time    = np.unique(self.meta.t_TOTAL[n_depths*i:n_depths*(i+1)])[0]
            temp_stage   = np.unique(self.meta.STAGE[n_depths*i:n_depths*(i+1)])[0]
            ax.set_title('Time: %.3fh (Stage %d)' %(temp_time, temp_stage))
            return cm

        ani = animation.FuncAnimation(fig, animationUpdate, frames=range(int(self.data.shape[0] / n_depths - 1) ),
                                blit=False, interval=100)
        
        cmap = matplotlib.cm.jet
        norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap,
                                norm=norm,
                                orientation='vertical')
        cbar.ax.set_title('T [°C]', loc='center')
        plt.suptitle('%s' %(Path(self.path).stem))

        if is_export:
            save_path = Path(self.path).parent.joinpath(Path(self.path).stem + '.mp4')
            print('Saving %s\n' %(save_path))
            t = tqdm(total=ani.save_count)
            def export_progress(current_frame: int, total_frames: int):
                t.update(1)
            
            writervideo = animation.FFMpegWriter(fps=20)
            ani.save(save_path, writer=writervideo, progress_callback =  lambda i, n: export_progress(i, n)) 
        else:
            plt.show()

        return ani

class TSCW_TFC(TSCW_Output):
    """Reads data from /*_TFC.TXT (cavern temperature over time)
    Stores data in
    self.data: - data
    """    
    def __init__(self, path:str):
        super().__init__()

        self.path = path
        data      = pd.read_csv(self.path, sep=r'\s*\t\s*', engine='python')
        self.df   = data

        idx = [index for index, item in enumerate(data.columns.to_list()) if '0.0' in item]  # zwei gleiche Schlüssel
        
        self.meta = data.iloc[:,:idx[0]]
        self.data = data.iloc[:,idx[0]:]

        self.t_total = np.unique(self.meta.t_TOTAL)

        data_column = []
        for m in self.data.columns:
            if m.count('.') > 1:
                idx = [i for i, letter in enumerate(m) if letter == '.']
                data_column.append(m[:idx[1]] + '1')
            else:
                data_column.append(m)

        self.radial_vector = np.array([data_column], dtype=float)



    def plot_temp_distribution(self, times:list, range_radial:list = None):
        """Plot radial temperature development in cavern over time.

        :param times: which time points 
        :type times: list
        :param range_radial:  [x0, x1] beginning and end of radial range, defaults to None
        :type range_radial: list, optional
        """        
        if range_radial is not None:
            idx1 = find_nearest(self.radial_vector, range_radial[0])
            idx2 = find_nearest(self.radial_vector, range_radial[1])
        else:
            idx1 = 0
            idx2 = self.radial_vector.shape[1]

        times_indices = []
        for time in times:
            times_indices.append(find_nearest(self.t_total, time))

        fig, ax = plt.subplots(constrained_layout=True)

        for i, i_time in enumerate(times_indices):
            ax.plot(self.radial_vector[0,idx1:idx2+1], self.data.iloc[i_time,idx1:idx2+1],
                    'o-', label = '%.2fh' %(self.t_total[i_time]),
                    linewidth = self.plot_meta['lw'])

        plt.suptitle('Cavern temperature development')
        plt.title('%s' %(os.path.basename(self.path)),
                  fontsize = self.plot_meta['subtitle_scale']*self.plot_meta['fs'])

        ax.grid(which='major',linestyle='-')
        ax.grid(which='minor',linestyle=':')   
        ax.minorticks_on()
        ax.set_ylabel('[°C]')
        ax.set_xlabel('[m]')

        fig.legend(loc='outside center right', ncol=1,
                   fontsize=self.plot_meta['subtitle_scale']*self.plot_meta['fs'], labelspacing=0.5)
