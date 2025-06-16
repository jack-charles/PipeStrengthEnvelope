"""
@author: Jack Charles   jack@jackcharlesconsulting.com
"""






import math
import json
import numpy as np
import matplotlib.pyplot as plt
import wellengcalc as wec

class PipeStrengthEnvelope():
    def __init__(self, env_name, VME_tension, VME_pressure, API_burst, API_collapse, API_tension, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension):
        self.env_name = env_name
        self.VME_tension = VME_tension
        self.VME_pressure = VME_pressure
        self.API_burst = API_burst
        self.API_collapse = API_collapse
        self.API_tension = API_tension
        self.DF_burst_triaxial = DF_burst_triaxial
        self.DF_tension_triaxial = DF_tension_triaxial
        self.DF_burst = DF_burst
        self.DF_tension = DF_tension
        self.DF_collapse = DF_collapse

    def calc_VME_API_curves(self, Yp, tubing_OD, tubing_ID, radius, eccentricity, temperature, Youngs_modulus, poissons_raio):
        self.VME_pressure, self.VME_tension = wec.calc_VM_envelope(Yp, tubing_OD, tubing_ID, radius, eccentricity, temperature, self.DF_burst_triaxial, self.DF_tension_triaxial)
        self.API_collapse_pressure = wec.calc_API_collapse(Yp, tubing_OD, tubing_ID, Youngs_modulus, poissons_raio) / self.DF_collapse
        self.API_burst_pressure = wec.calc_API_burst(Yp, tubing_OD, tubing_ID) * wec.calc_pipe_temperature_derating(temperature) / self.DF_burst
        self.API_tension = wec.calc_API_tensile(Yp, tubing_OD, tubing_ID) * wec.calc_pipe_temperature_derating(temperature)  / self.DF_tension /1000

class CaTStressAnalysisResults():
    def __init__(self, load_name, tension, pressure):
        self.load_name = load_name
        self.tension = tension
        self.pressure = pressure

def read_stress_data_file(load_name, data_filename="default_stress_data.txt"):
    data_ndarray = np.genfromtxt(data_filename, delimiter=',', dtype=float, skip_header=1)  
    data_class, _x, _tens, _press = [], [], [], []
    for data_content in data_ndarray:
        _x = data_content.tolist()
        _tens.append(_x[0])
        _press.append(_x[1])
    data_class = CaTStressAnalysisResults(load_name, _tens, _press)
    print(data_class.tension, data_class.pressure)
    return data_class

def plot_VME_graphs(VME_data, load_data):
    fig = plt.figure()
    fig.suptitle('VME Plot')
    fig.tight_layout()

    ax1 = fig.add_subplot(111)
    
    for _x in range(len(VME_data)):
        ax1.plot(VME_data[_x].VME_tension, VME_data[_x].VME_pressure, label = VME_data[_x].env_name)
        API_x = [VME_data[_x].API_tension, VME_data[_x].API_tension, 0, -VME_data[_x].API_tension, -VME_data[_x].API_tension, VME_data[_x].API_tension]
        API_y = [VME_data[_x].API_burst_pressure, 0, -VME_data[_x].API_collapse_pressure, -VME_data[_x].API_collapse_pressure, VME_data[_x].API_burst_pressure, VME_data[_x].API_burst_pressure]
        ax1.plot(API_x, API_y, color='black')
        
        ax1.annotate(xy = (0,max(VME_data[_x].VME_pressure)), text = f"Triaxial DF={VME_data[_x].DF_burst_triaxial}", horizontalalignment = 'center', verticalalignment = 'bottom', fontsize = 6)
        ax1.annotate(xy = (-VME_data[_x].API_tension,VME_data[_x].API_burst_pressure), text = f"Burst DF={VME_data[_x].DF_burst}", horizontalalignment = 'left', verticalalignment = 'bottom', fontsize = 6)
        ax1.annotate(xy = (VME_data[_x].API_tension,0), text = f"Tension DF={VME_data[_x].DF_tension}", horizontalalignment = 'right', verticalalignment = 'bottom', fontsize = 6)
        ax1.annotate(xy = (0,-VME_data[_x].API_collapse_pressure), text = f"Collapse DF={VME_data[_x].DF_collapse}", horizontalalignment = 'right', verticalalignment = 'bottom', fontsize = 6)

    for _x in range(len(load_data)):
        ax1.plot(load_data[_x].tension, load_data[_x].pressure, label = load_data[_x].load_name)
    ax1.set_xlabel("Tension")
    ax1.set_ylabel("Pressure")
    ax1.legend(loc='best', fontsize=8)
    ax1.grid(True)

    plt.show()  
