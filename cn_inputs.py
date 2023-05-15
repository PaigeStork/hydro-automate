import re

#usage: manipulate and output CN values from CC or WFK, from a baseline of current conditions. To be applied in XX_cn_adjustments.py
#enter subbasins as strings and updated CN values as floats
#cn_inputs.CN_Inputs('XX').replaceCN('reach',float) replaces desired CN, does not output anything
#or cn_inputs.CN_Inputs('XX').get_basin_CN_input() outputs new basin:CN dictionary


#CC
#grab CNs from No Dams basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()

subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
cn_no_dams = [float(x) for x in cn_no_dams]

CC_basin_CN_input = {}
for basin in range(len(subbasins_no_dams)):
    CC_basin_CN_input[f'{subbasins_no_dams[basin]}'] = cn_no_dams[basin]
    
#WFK
#grab CNs from No Dams basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()

subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
cn_no_dams = [float(x) for x in cn_no_dams]

WFK_basin_CN_input = {}
for basin in range(len(subbasins_no_dams)):
    WFK_basin_CN_input[f'{subbasins_no_dams[basin]}'] = cn_no_dams[basin]

    
class CN_Inputs:
    def __init__(self,watershed):
        self.watershed = watershed
    def reset(self):
        if self.watershed == 'CC':
            #CC
            with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
                fdata = f.read()
            subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
            cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
            cn_no_dams = [float(x) for x in cn_no_dams]
            CC_basin_CN_input = {}
            for basin in range(len(subbasins_no_dams)):
                CC_basin_CN_input[f'{subbasins_no_dams[basin]}'] = cn_no_dams[basin]

        elif self.watershed == 'WFK':
            #WFK
            with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
                fdata = f.read()
            subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
            cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
            cn_no_dams = [float(x) for x in cn_no_dams]
            WFK_basin_CN_input = {}
            for basin in range(len(subbasins_no_dams)):
                WFK_basin_CN_input[f'{subbasins_no_dams[basin]}'] = cn_no_dams[basin]

    def replaceCN(self,basin,newCN):
        if self.watershed == 'CC':
            CC_basin_CN_input[basin] = newCN
        elif self.watershed =='WFK':
            WFK_basin_CN_input[basin] = newCN
    def get_basin_CN_input(self):
        if self.watershed == 'CC':
            return CC_basin_CN_input
        elif self.watershed == 'WFK':
            return WFK_basin_CN_input


        