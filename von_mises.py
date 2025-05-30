"""
@author: Jack Charles   jack@jackcharlesconsulting.com
"""






import math
import json
import numpy as np
import matplotlib.pyplot as plt
import wellengcalc as wec

class VonMisesEnvelope():
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

    def calc_VME_API_curves(self, Yp, outer_diameter, inner_diameter, radius, eccentricity, temperature, Youngs_modulus, Poissons_raio):
        self.VME_pressure, self.VME_tension = wec.calc_VM_envelope(Yp, outer_diameter, inner_diameter, radius, eccentricity, temperature, self.DF_burst_triaxial, self.DF_tension_triaxial)
        self.API_collapse_pressure = wec.calc_API_collapse(Yp, outer_diameter, inner_diameter, Youngs_modulus, Poissons_raio) / self.DF_collapse
        self.API_burst_pressure = wec.calc_API_burst(Yp, outer_diameter, inner_diameter) / self.DF_burst
        self.API_tension = wec.calc_API_tension(Yp, outer_diameter, inner_diameter) / self.DF_tension /1000

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
    ax1.legend(loc="best", fontsize=8)
    ax1.grid(True)

    plt.show()  


VME_data = []
load_data = []
menu_loop = True

while menu_loop != False:
    print(f"\nCurrent Units are psi and inches")
    menu_selection = int(input(f"Please type the number of selection\n"
                        "1: Input Pipe Data\n"
                        "2: Add Data Points\n"
                        "3: Plot VME Graphs\n"
                        "0: Quit\n"
                        "Selection: "))
    
    if menu_selection == 1:
        name = input("Name/Description of VME Plot: ")
        OD = float(input("Pipe OD: "))
        ID = float(input("Pipe ID: "))
        eccen = float(input("Wall thickness or eccentricity (fraction): "))
        Yp = float(input("Minimum Yield Stress: "))
        YM = float(input("Young's Modulus: "))
        poisson = float(input("Poisson's Ratio: "))
        temperature = float(input("Temperature: "))
        radial_stress_query = input("Include radial stresses? (Y/N): ")
        
        DF_burst_triaxial = float(input("Design Factor Triaxial Burst: "))
        DF_tension_triaxial = float(input("Design Factor Triaxial Tension: "))
        DF_burst = float(input("Design Factor Burst: "))
        DF_collapse = float(input("Design Factor Collapse: "))
        DF_tension = float(input("Design Factor Tension: "))
        
        if radial_stress_query == "Y":
            radius = ID/2
        else:
            radius = OD/2
        
        VME_data.append(VonMisesEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
              
    elif menu_selection == 2:
        load_name = input("Name of load case: ")
        stress_data_filename = input("Path to Stress Results: ")
        try:
            load_data.append(read_stress_data_file(load_name, stress_data_filename))
        except FileNotFoundError:
            print("File not found")      
    
    elif menu_selection == 3:
        plot_VME_graphs(VME_data, load_data)
      
    elif menu_selection == 0:
        print("Thank you")
        menu_loop = False

#Demo mode 1 for testing
    elif menu_selection == 10:
        name = "w/o Radial Stress"
        OD = 9.625
        ID = 8.535
        eccen = 0.875
        Yp = 95000.0
        YM = 30.0*10**6
        poisson = 0.25
        temperature = 75.0
        radial_stress_query = "N"
        
        DF_burst_triaxial = 1.0
        DF_tension_triaxial = 1.0
        DF_burst = 1.0
        DF_collapse = 1.0
        DF_tension = 1.0

        if radial_stress_query == "Y":
            radius = ID/2
        else:
            radius = OD/2

        VME_data.append(VonMisesEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        plot_VME_graphs(VME_data, load_data)

    #Demo mode 2 for testing   
    elif menu_selection == 20:
        name = "w/ Radial Stress"
        OD = 9.625
        ID = 8.535
        eccen = 0.875
        Yp = 95000.0
        YM = 30.0*10**6
        poisson = 0.25
        temperature = 75.0
        radial_stress_query = "Y"
        DF_burst_triaxial = 1.0
        DF_tension_triaxial = 1.0
        DF_burst = 1.0
        DF_collapse = 1.0
        DF_tension = 1.0

        if radial_stress_query == "Y":
            radius = ID/2
        else:
            radius = OD/2

        VME_data.append(VonMisesEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        plot_VME_graphs(VME_data, load_data)

    #Demo mode 3 for testing
    elif menu_selection == 30:
        name = "w/ Radial Stress & DF"
        OD = 9.625
        ID = 8.535
        eccen = 0.875
        Yp = 95000.0
        YM = 30.0*10**6
        poisson = 0.25
        temperature = 75.0
        radial_stress_query = "Y"
        DF_burst_triaxial = 1.25
        DF_tension_triaxial = 1.15
        DF_burst = 1.25
        DF_collapse = 1.0
        DF_tension = 1.15
         

        if radial_stress_query == "Y":
            radius = ID/2
        else:
            radius = OD/2

        VME_data.append(VonMisesEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        plot_VME_graphs(VME_data, load_data)