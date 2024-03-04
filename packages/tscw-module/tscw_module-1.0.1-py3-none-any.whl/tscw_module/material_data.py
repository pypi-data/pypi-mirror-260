material_data = {
    'cement': {'rho': 3100, 'cp': 750,'lambda': 1.55},
    'steel':  {'rho': 7900, 'cp': 500,'lambda': 50},
    'rrsf':  {'rho': 1000, 'cp': 4170,'lambda': 0.6},
    'quartar':  {'rho': 1800, 'cp': 950,'lambda': 2.3},
    'unt_buntsandstein':  {'rho': 2500, 'cp': 760,'lambda': 2.6},
    'hauptanhydrit':  {'rho': 2900, 'cp': 864,'lambda': 4.0},
    'stasfurt':  {'rho': 2150, 'cp': 860,'lambda': 5.91},
    'anhydrit':  {'rho': 3000, 'cp': 860,'lambda': 4.2},
}


class MaterialProperties():
    def __init__(self):
        
        for key in material_data.keys():
            material_data[key]['rhocp'] = material_data[key]['rho'] * material_data[key]['cp'] * 1e-6

            self.material_data = material_data
