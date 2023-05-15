import subprocess
import os
import time
import sa_cn_inputs
import sys
import fileinput
import textwrap
import re
import shutil
import numpy as np
import cn_inputs
import pandas as pd
import matplotlib.pyplot as plt
import re
import json
from collections import OrderedDict
from datetime import datetime
import reach_station_lookup
import json

#subbasins_no_dams = sa_cn_inputs.CC_subbasins_no_dams #define list of subbasin names by pulling work from sa_cn_inputs
#for ramping up purposes, may instead want to take workflow a few subbasins at a time, hash out the rest

subbasins_no_dams = ['Harrison Creek D',
 'Harrison Creek A',
 'Harrison Creek B',
 'Harrison Creek C',
 'Harrison Creek E',
 'Bishop A',
 'West _Fork Kickapoo 17',
 'Bishop B',
 'Bishop C',
 'West Fork Kickapoo F',
 'West Fork Kickapoo C',
 'West Fork Kickapoo D',
 'West Fork Kickapoo A',
 'West _Fork Kickapoo 4',
 'West Fork Kickapoo 5',
 'Knapp Creek - WFK M',
 'Knapp Creek - WFK J',
 'Knapp Creek - WFK L',
 'West Fork Kickapoo 12',
 'Knapp Creek - WFK F',
 'WEST FORK KICKAPOO 3',
 'MLSNA',
 'KLINKNER',
 'Knapp Creek - WFK A',
 'Knapp Creek - WFK B',
 'Knapp Creek - WFK C',
 'WEST FORK KICKAPOO 1',
 'Knapp Creek - WFK D',
 'West Fork Kickapoo 16',
 'Knapp Creek - WFK E',
 'Knapp Creek - WFK G',
 'Knapp Creek - WFK I',
 'Knapp Creek - WFK H',
 'Seas Branch',
 'Knapp Creek - WFK K',
 'West Fork Kickapoo B',
 'West Fork Kickapoo E',
 'West Fork Kickapoo G',
 'Bishop D',
 'West Fork Kickapoo I',
 'West Fork Kickapoo H',
 'West Fork Kickapoo J']

WFK = sa_cn_inputs.SA_CN_Inputs('WFK')

#Master Loop
#WFK
for basin in range(len(subbasins_no_dams)):
    WFK = sa_cn_inputs.SA_CN_Inputs('WFK')
    WFK_CNs = WFK.get_SA_CN(f'{subbasins_no_dams[basin]}') #this updated definition of CC_CNs will be applied to the object by the same name in step 1
    JSON_name_ext = f'{subbasins_no_dams[basin]}' #this updated definition of JSON_name_ext will be applied to the object by the same name in step 4
    print(subbasins_no_dams[basin])
    
    #STEP 1----------------------------------------------------------------------------------------------------------------------
    #script functionality: using original No Dams .basin file, swap FloodScape-user defined CNs within .basin file, recalculate Lag accordingly

    #TODO: current CN values may be fine-tuned according to SmartScape data, current CN conditions are, as of now, pulled from NRCS contractor's .basin files 
    #TODO: according to how data will be packaged from FloodScape, how input is read needs adjustment


    # grab original .basin file from safe folder and copy to where HMS will pull from it. these copied .basin files stored in their respective filepaths will edited below

    #2yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm")
    #5yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm")
    #10yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm")
    #25yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm")
    #50yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm")
    #100yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm")
    #200yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm")
    #500yr
    shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
                 r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm")


    #basin parameters built into basin models are saved to a BasinParams.csv file, adapted from data provided by NRCS contractors
    #these values are needed to recalculate lag (L) according to the watershed lag method (part 630.1502a Hydrology National Engineering Handbook)
    #L = ((l**0.8)(S+1)**0.7)/(1900*Y**0.5) where S = (1000/CN) - 10

    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_BasinParams.csv",'r') as f:
        fdata = f.read()
    #create dictionary of subbasin constant parameters
    WFK_params_subbasins = re.findall(r"\n(.*?)\,", fdata)

    WFK_params_l = re.findall(r"\n.*?,(.*?)\,", fdata)
    WFK_params_l = [float(l) for l in WFK_params_l]

    WFK_params_Y = re.findall(r"\n.*?,.*?,(\d*.\d*)", fdata)
    WFK_params_Y = [float(Y) for Y in WFK_params_Y]

    WFK_params = {}
    for subbasin in range(len(WFK_params_subbasins)): #42 instances
        WFK_params[f'{WFK_params_subbasins[subbasin]}'] = np.array(([float(f'{WFK_params_l[subbasin]}'),float(f'{WFK_params_Y[subbasin]}')]))

    #how input is read may need adjustment, see TODO section-------------------------------------------------------------------------------
    #bring in dictionary of subbasin experimental CNs
    # WFK_CNs_input = cn_inputs.CN_Inputs('WFK') #bring in module
    # WFK_CNs_input.reset() #ensure values are reset, otherwise past replacements perpetuate
    # #WFK_CNs_input.replaceCN('reach', float) #if we wanted to change any CN values
    # WFK_CNs = WFK_CNs_input.get_basin_CN_input() #this is a subbasin:CN dictionary

    #Bring in current dictionary of subbasin:CN values based on which iteration master loop is on
    #from WFK_SA_Master_WorkflowTrigger import WFK_CNs
    #------------------------------------------------------------------------------------------------------------------------------------

    #define function to calculate lag (as referenced in part 630.1502a Hydrology National Engineering Handbook; see above)
    def calcL(subbasin):
        S = (1000/WFK_CNs[subbasin]) - 10
        L = (((WFK_params[subbasin][0]**0.8)*(S+1)**0.7)/(1900*WFK_params[subbasin][1]**0.5))*60
        return L

    #create dictionary of subbasins' calculated lag
    WFK_Ls = {}
    for subbasin in range(len(WFK_params_subbasins)): #42 instances
        WFK_Ls[f'{WFK_params_subbasins[subbasin]}'] = calcL(f'{WFK_params_subbasins[subbasin]}')


    #order the CN and L lists so that they can be eaten by re.sub; create template from which to regenerate ordered lists for each storm, as list.pop() consumes list
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
    ordered_Ls_template = []
    for ordered_subbasin in range(len(ordered_subbasins)):
        ordered_Ls_template.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])


    ordered_CNs_template = []
    for ordered_subbasin in range(len(ordered_subbasins)):
        ordered_CNs_template.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])



    #-----------------------------------------------------------------------------------------------------------        
    #define replacement functions
    def replace_CN(m):
        if not ordered_CNs: 
            raise Exception("length of replacements does not match length of Curve Number instances in file")

        return f"Curve Number: {ordered_CNs.pop(0)}"

    def replace_L(m):
        if not ordered_Ls: 
            raise Exception("length of replacements does not match length of Lag instances in file")

        return f"Lag: {ordered_Ls.pop(0)}"


    #2yr-----------------------------------------------------------------------------------------------------------
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #5yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #10yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #25yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #50yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #100yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to the .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)

    #-----------------------------------------------------------------------------------------------------------        
    #200yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    #for loop; create a lookup between .basin file subbasin and above dictionaries
    #OR, reorder and pop from end with each function... this seems way easier, less robust
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)


    #-----------------------------------------------------------------------------------------------------------        
    #500yr
    ordered_Ls = ordered_Ls_template.copy()
    ordered_CNs = ordered_CNs_template.copy()
    #replace values in .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
        fdata = f.read()
    fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
    fdata = re.sub(r"Lag: (\d\d*.\d\d*)", replace_L, fdata)
    #write to .basin file
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
        f.write(fdata)
        
    time.sleep(2)
    #if list_files.returncode == 0:
    #STEP2: run all storm scenarios--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #must cd to installation folder of HEC
    t = r"C:\Program Files\HEC\HEC-HMS\4.6"
    os.chdir(t)
    list_files = subprocess.run([r"hec-hms.cmd", "-s", r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_HMSRun.script"],executable=r"C:\Program Files\HEC\HEC-HMS\4.6\hec-hms.cmd")
    print("The exit code to run STEP2 was %d" %list_files.returncode)

    time.sleep(2)
    if list_files.returncode == 0:
        #STEP 3: extract each HMS reach time series data from output .dss file, save to .txt files
        list_files = subprocess.run("python WFK_dss_output.py",cwd=r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final")
        print("The exit code to run STEP3 was %d" %list_files.returncode)

        time.sleep(2)
        if list_files.returncode == 0:
            #STEP 4: compile time series, peak Q, peak WSE data to JSON file------------------------------------------------------------
            #usage: pull together all pertinent data from .dss files (time series, Qmax, calculated WSE) with the support of Qmax~WSE correlations compiled from RAS, and HMS reach~RAS station correlations compiled manually
            #SET UP DICTIONARY OF ARRAYS HOLDING QMAX, WSE, SLOPE & INTERCEPT /STATION /STORM

            #bring in compiled .csv (UTF-8) file of Peak Flow ~ WSE correlations, exported from RAS summary table and keep only 
            #reach, river station, profile, Q Total and W.S. Elev columns;
            #.csv should have no extra spaces, keep headings
            with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\PeakFlow_WSE_Correlations_RiverStations_WFK_090722.csv",'r') as f:
                    fdata = f.read()
            stations = re.findall(r"\n.*?,(.*?),.*?,.*?,\d*.\d*",fdata) #regex structured this way to toss the culvert
            stations = list(OrderedDict.fromkeys(stations)) #to remove duplicates and maintain order
            q_max = re.findall(r"\n.*?,.*?,.*?,(\d*.\d*)\,",fdata)
            q_max = [float(x) for x in q_max]
            wse = re.findall(r"\n.*?,.*?,.*?,.*?,(\d*.\d*)",fdata)
            wse = [float(x) for x in wse]

            #define slope and intercept functions
            def slope(x0,x1,y0,y1):
                return((y1-y0)/(x1-x0)) if x1-x0 else None
            def intercept(x0,x1,y0,y1):
                return y0-(((y1-y0)/(x1-x0))*x0) if x1-x0 else None

            #compile info for each river station
            qmax_wse = {}
            i = 0
            for station in range(len(stations)):
                qmax_wse[f'{stations[station]}'] = np.array(([q_max[i],wse[i],99,999],
                               [q_max[i+1],wse[i+1],slope(q_max[i],q_max[i+1],wse[i],wse[i+1]),intercept(q_max[i],q_max[i+1],wse[i],wse[i+1])],
                               [q_max[i+2],wse[i+2],slope(q_max[i+1],q_max[i+2],wse[i+1],wse[i+2]),intercept(q_max[i+1],q_max[i+2],wse[i+1],wse[i+2])],
                               [q_max[i+3],wse[i+3],slope(q_max[i+2],q_max[i+3],wse[i+2],wse[i+3]),intercept(q_max[i+2],q_max[i+3],wse[i+2],wse[i+3])],
                               [q_max[i+4],wse[i+4],slope(q_max[i+3],q_max[i+4],wse[i+3],wse[i+4]),intercept(q_max[i+3],q_max[i+4],wse[i+3],wse[i+4])],
                               [q_max[i+5],wse[i+5],slope(q_max[i+4],q_max[i+5],wse[i+4],wse[i+5]),intercept(q_max[i+4],q_max[i+5],wse[i+4],wse[i+5])],
                               [q_max[i+6],wse[i+6],slope(q_max[i+5],q_max[i+6],wse[i+5],wse[i+6]),intercept(q_max[i+5],q_max[i+6],wse[i+5],wse[i+6])],
                              [q_max[i+7],wse[i+7],slope(q_max[i+6],q_max[i+7],wse[i+6],wse[i+7]),intercept(q_max[i+6],q_max[i+7],wse[i+6],wse[i+7])]))
                i = i+8

            #DEFINE HMS REACHES TO PULL TIME SERIES DATA FROM DSS VUE (pulled from hms_reach from proof. 
            #naming is case insensitive. requires some manual adjustments because HMS cuts off names)

            # #KEY STATION ~ HMS REACH LOOKUP
            # #proofs for development of following lists are in proofs.ipynb
            with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\HMS_RAS_NetworkCorrelation_WFK_090722.csv",'r') as f:
                    fdata = f.read()        
            reaches = re.findall(r"\n.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
            key_station = re.findall(r"\n.*?,.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
            key_station = [float(x) for x in key_station]

            #KEY STATION ~ HMS REACH LOOKUP
            WFK = reach_station_lookup.Watershed('WFK') #usage: WFK.get_reach(station) or WFK.get_station('reach')

            #PULL EXPERIMENTAL DATA FROM DSS VUE; SWAP HMS REACH FOR RAS STATION IDENTIFIER
            # Opening JSON file
            f = open(r'C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\CompiledDataFromDSS_overwrite.json')

            # returns JSON object as a dictionary
            CompiledDataFromDSS = json.load(f)

            #WSE CALCULATION
            #create some useful elements to make looping easier
            storms = ['2', '5', '10','25', '50', '100', '200', '500']

            calc_wse = {'2':{}, '5':{}, '10':{}, '25':{}, '50':{},'100':{}, '200':{}, '500':{}}
            for storm in range(len(storms)): #8 instances
                for station in range(len(key_station)): #42 instances
                    #under 2yr Qmax
                    if CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][0,0]:
                        statement = 'Warning: Max flow is under model parameters'
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = 99
                    #between 2yr & 5yr Qmax
                    if qmax_wse[f'{key_station[station]}'][0,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][1,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][1,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][1,3] # y=mx+b
                    #between 5yr & 10yr Qmax
                    if qmax_wse[f'{key_station[station]}'][1,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][2,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][2,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][2,3] # y=mx+b
                    #between 10yr and 25yr Qmax
                    if qmax_wse[f'{key_station[station]}'][2,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][3,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][3,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][3,3] # y=mx+b
                    #between 25yr and 50yr Qmax
                    if qmax_wse[f'{key_station[station]}'][3,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][4,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][4,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][4,3] # y=mx+b
                    #between 50yr and 100yr Qmax
                    if qmax_wse[f'{key_station[station]}'][4,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][5,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][5,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][5,3] # y=mx+b
                    #between 100yr and 200yr Qmax
                    if qmax_wse[f'{key_station[station]}'][5,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][6,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][6,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][6,3] # y=mx+b
                    #between 200yr and 500yr Qmax
                    if qmax_wse[f'{key_station[station]}'][6,0] < CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] <= qmax_wse[f'{key_station[station]}'][7,0]:
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][7,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][7,3] # y=mx+b
                    #above 500yr Qmax
                    if CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] > qmax_wse[f'{key_station[station]}'][7,0]:
                        statement = 'Warning: Max flow is above model parameters; 200yr to 500yr rating curve applied to flow'
                        calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][7,2] * CompiledDataFromDSS[f'{storms[storm]}'][WFK.get_reach(f'{key_station[station]}')]['max_q'] + qmax_wse[f'{key_station[station]}'][7,3] # y=mx+b


            #COMPILE ALL INFO TO JSON
            #set up dictionary to be populated
            CompiledRiverStationData = {'2yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'5yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'10yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'25yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'50yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'100yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'200yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}},'500yr':{'5075.74':{},
             '4688.81':{},
             '21459.97':{},
             '18520.11':{},
             '9044.28':{},
             '4683.66':{},
             '1299.05':{},
             '6131.81':{},
             '2722.88':{},
             '2945.19':{},
             '5429.81':{},
             '1689.83':{},
             '12749.08':{},
             '5350.41':{},
             '10798.11':{},
             '6346.46':{},
             '2417.83':{},
             '6721.04':{},
             '1933.21':{},
             '6000.33':{},
             '3277.91':{},
             '4687.52':{},
             '3751.15':{},
             '5128.21':{},
             '4660.94':{},
             '2048.78':{},
             '11827.62':{},
             '1446.65':{},
             '5600.6':{},
             '15905.06':{},
             '1052.29':{},
             '3338.29':{},
             '5313.02':{},
             '5325.85':{},
             '3737.3':{},
             '13383.6':{},
             '2334.44':{},
             '1020.65':{},
             '29422.32':{},
             '23916.11':{},
             '15699.21':{},
             '3134.44':{},
             '2179.29':{},
             '23321.9':{},
             '16392.48':{},
             '20307.34':{},
             '11361.86':{},
             '1690.2':{},
             '2432.4':{},
             '10964.2':{},
             '9033.32':{},
             '4276.96':{}}}

            #for storm in range(len(dict_of_stations_max_names)): #8 instances
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['2yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['2'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['2yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['2'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['2yr'][f'{key_station[station]}']['WSE'] = calc_wse['2'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['5yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['5'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['5yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['5'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['5yr'][f'{key_station[station]}']['WSE'] = calc_wse['5'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['10yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['10'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['10yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['10'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['10yr'][f'{key_station[station]}']['WSE'] = calc_wse['10'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['25yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['25'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['25yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['25'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['25yr'][f'{key_station[station]}']['WSE'] = calc_wse['25'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['50yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['50'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['50yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['50'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['50yr'][f'{key_station[station]}']['WSE'] = calc_wse['50'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['100yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['100'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['100yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['100'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['100yr'][f'{key_station[station]}']['WSE'] = calc_wse['100'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['200yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['200'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['200yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['200'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['200yr'][f'{key_station[station]}']['WSE'] = calc_wse['200'][f'{key_station[station]}']
            for station in range(len(key_station)): #42 instances
                CompiledRiverStationData['500yr'][f'{key_station[station]}']['time series'] = CompiledDataFromDSS['500'][WFK.get_reach(f'{key_station[station]}')]['q']
                CompiledRiverStationData['500yr'][f'{key_station[station]}']['Qmax'] = CompiledDataFromDSS['500'][WFK.get_reach(f'{key_station[station]}')]['max_q']
                CompiledRiverStationData['500yr'][f'{key_station[station]}']['WSE'] = calc_wse['500'][f'{key_station[station]}']

            # Serializing json
            json_object = json.dumps(CompiledRiverStationData, indent=4)
            date = datetime.today()
            date = date.strftime("%d%m%Y_%H%M%S")

            # Writing to sample.json
            with open(r'C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\{}_CompiledRiverStationData.json'.format(JSON_name_ext), "w") as outfile:
                outfile.write(json_object)

            print(f'WORKFLOW FOR {basin} FULLY EXECUTED')
