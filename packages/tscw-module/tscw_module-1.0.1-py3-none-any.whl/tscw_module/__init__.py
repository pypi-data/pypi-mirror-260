from .helper_func import calculate_forces, calculate_relative_error, interpolate_1d
from .thermreg_DataClasses import ThermregData
from .tscw_DataClassesInput import GacaFieldData, GacaProcessData
from .tscw_DataClassesOutput import TSCW_TBHC, TSCW_TFBH, TSCW_TFC
from .process_AusEinspeisung import create_overviewTable, plot_pTcav_comparison, \
                                 plot_pT_Overlap, plot_pt_Difference, plot_forces_difference

from .material_data import MaterialProperties

__name__ = 'tscw_module'
__version__ = "0.1.0"
__author__ = 'Thomas Simader'
__credits__ = 'UGS GmbH'