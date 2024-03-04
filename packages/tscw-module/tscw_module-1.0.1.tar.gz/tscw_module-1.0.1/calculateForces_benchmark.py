from tscw_module import calculate_forces
import numpy as np
from pathlib import Path
import pandas as pd
import unittest

'''
Unit Test for calculating axial forces.
Benchmark data from BB122 - Ausspeisung
"L:\Projekte\SG-UBT\40_Thermodynamik\Berichte\berechnungenbbg_rev2_2011.xls"
'''

def check_list(list1, list2):
    tolerance_digits = 3
    for val1, val2 in zip(list1, list2):
        if np.round(val1, tolerance_digits) != np.round(val2, tolerance_digits):
            return False
        break
    return True

class ForcesBenchmark(unittest.TestCase):
    def test_axial_forces(self):
        # Validation with Excel from 2011 - BB122
        T0 = 15 #
        t_vector = np.array([15.0, 18.3, 18.1, 17.8, 17.2,]) # T
        p_vector = np.array([91.000, 90.850, 90.250, 89.350, 88.200])/10 # MPa
        t_total  = t_stage = np.array([ 0, 1, 2, 4, 7 ]) # h

        # caclulate axial forces
        meta_data_path = r"L:\\Projekte\\SG-UBT\\40_Thermodynamik\\TSWC_GACA_Bernburg\\VergleichRegthermTswc\\metaDataForces.xlsx"
        meta_data = pd.read_excel(meta_data_path, header=None, dtype={'Name': str, 'Value': float}, sheet_name='BB122')
        meta_data = dict(zip(meta_data.iloc[:,0], meta_data.iloc[:,1]))
        df = calculate_forces(meta_data, t_vector, p_vector, t_total, t_stage, T0, None)
        expected_Fz_ges = [123.626504,   68.822167,   71.002468,   74.272920,   82.031644]
        self.assertTrue(check_list(df.Fz_ges, expected_Fz_ges))


if __name__ == '__main__':
    unittest.main()
