"""
@author: Jack Charles   jack@jackcharlesconsulting.com
"""






import math
import json
import numpy as np
import matplotlib.pyplot as plt
import wellengcalc as wec
import pipe_envelope as penv

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
        tubing_OD = float(input("Pipe OD: "))
        tubing_ID = float(input("Pipe ID: "))
        eccen = float(input("Wall thickness or eccentricity (fraction): "))
        Yp = float(input("Minimum Yield Stress: "))
        YM = float(input("Young's Modulus: "))
        poissons_ratio = float(input("Poisson's Ratio: "))
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
        
        VME_data.append(penv.PipeStrengthEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, tubing_OD, tubing_ID, radius, eccen, temperature, YM, poissons_ratio)
              
    elif menu_selection == 2:
        load_name = input("Name of load case: ")
        stress_data_filename = input("Path to Stress Results: ")
        try:
            load_data.append(penv.read_stress_data_file(load_name, stress_data_filename))
        except FileNotFoundError:
            print("File not found")      
    
    elif menu_selection == 3:
        penv.plot_VME_graphs(VME_data, load_data)
      
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

        VME_data.append(penv.PipeStrengthEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        penv.plot_VME_graphs(VME_data, load_data)

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

        VME_data.append(penv.PipeStrengthEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        penv.plot_VME_graphs(VME_data, load_data)

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

        VME_data.append(penv.PipeStrengthEnvelope(name, [], [],0,0,0, DF_burst_triaxial, DF_tension_triaxial, DF_burst, DF_collapse, DF_tension))
        VME_data[-1].calc_VME_API_curves(Yp, OD, ID, radius, eccen, temperature, YM, poisson)
        
        penv.plot_VME_graphs(VME_data, load_data)