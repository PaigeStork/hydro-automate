import sys
import fileinput
import textwrap
import re
import shutil
import numpy as np
import cn_inputs

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

#bring in dictionary of subbasin experimental CNs
WFK_CNs_input = cn_inputs.CN_Inputs('WFK') #bring in module
WFK_CNs_input.reset() #ensure values are reset, otherwise past replacements perpetuate
#WFK_CNs_input.replaceCN('Harrison Creek D', 66.66) #if we wanted to change any CN values
WFK_CNs = WFK_CNs_input.get_basin_CN_input() #this is a subbasin:CN dictionary

#define function to calculate lag (as referenced in part 630.1502a Hydrology National Engineering Handbook; see above)
def calcL(subbasin):
    S = (1000/WFK_CNs[subbasin]) - 10
    L = ((WFK_params[subbasin][0]**0.8)*(S+1)**0.7)/(1900*WFK_params[subbasin][1]**0.5)*60
    return round(L,2)

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
    
    