import pandas as pd
import numpy as np
import sys
import fileinput
import textwrap
import re
import csv

#usage: reach_station_lookup.Watershed('XX').get_reach(XXXXX.XX) to return HMS reach corresponding to entered key RAS station
#or reach_station_lookup.Watershed('XX').get_key_station('reach') to return key RAS station corresponding to entered HMS reach
#or reach_station_lookup.Watershed('XX').get_station('reach') to return list of all RAS stations corresponding to entered HMS reach

#HMS reach to key RAS station dictionary development
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\HMS_RAS_NetworkCorrelation_CC_08232022.csv",'r') as f:
        fdata = f.read()        
hms_reach = re.findall(r"\n.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
ras_station = re.findall(r"\n.*?,.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
#ras_station = [float(x) for x in ras_station] #with the implementation of a lookup tool for all minor stations, some of which include a *, stations must now be strings
CC_reach_station_lookup = {}
for reach in range(len(hms_reach)):
    CC_reach_station_lookup[f'{hms_reach[reach]}'] = ras_station[reach]
    
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\HMS_RAS_NetworkCorrelation_WFK_090722.csv",'r') as f:
        fdata = f.read()        
hms_reach = re.findall(r"\n.*?,.*?,.*?,.*?(.*?)\,",fdata)
ras_station = re.findall(r"\n.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
#ras_station = [float(x) for x in ras_station]
WFK_reach_station_lookup = {}
for reach in range(len(hms_reach)):
    WFK_reach_station_lookup[f'{hms_reach[reach]}'] = ras_station[reach]

#HMS reach to all corresponding RAS reaches dictionary development
#crawl row by row, setting first element (HMS reach) as key, following elements (all corresponding RAS reaches) as values
#CC
CC_HMSreach_to_RASstations = {}
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_KeyStation_MinorStation_230119.csv") as file_obj:
    heading = next(file_obj)
    reader_obj = csv.reader(file_obj)
    for column in reader_obj:
        CC_HMSreach_to_RASstations[column[0]] = column[1:]

#algorithm for removing blanks inspired by: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
for key in CC_HMSreach_to_RASstations:
    while('' in CC_HMSreach_to_RASstations[key]):
        CC_HMSreach_to_RASstations[key].remove('')


#WFK
WFK_HMSreach_to_RASstations = {}
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_KeyStation_MinorStation_230119.csv") as file_obj:
    heading = next(file_obj)
    reader_obj = csv.reader(file_obj)
    for column in reader_obj:
        WFK_HMSreach_to_RASstations[column[0]] = column[1:]

#algorithm for removing blanks inspired by: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
for key in WFK_HMSreach_to_RASstations:
    while('' in WFK_HMSreach_to_RASstations[key]):
        WFK_HMSreach_to_RASstations[key].remove('')
    
class Watershed:
    def __init__(self,watershed):
        self.watershed = watershed
    def get_key_station(self,reach):
        self.reach = reach
        if self.watershed == 'CC':
            return CC_reach_station_lookup[self.reach]
        elif self.watershed == 'WFK':
            return WFK_reach_station_lookup[self.reach]
    def get_station(self,reach):#returns list of all RAS stations corresponding to entered HMS reach
        self.reach = reach
        if self.watershed == 'CC':
            return CC_HMSreach_to_RASstations[self.reach]
        elif self.watershed == 'WFK':
            return WFK_HMSreach_to_RASstations[self.reach]
    def get_reach(self,station):
            self.station = station
            if self.watershed == 'CC':
                #inspired by: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
                return list(CC_reach_station_lookup.keys()) [list(CC_reach_station_lookup.values()).index(self.station)]
            elif self.watershed == 'WFK':
                return list(WFK_reach_station_lookup.keys()) [list(WFK_reach_station_lookup.values()).index(self.station)]

