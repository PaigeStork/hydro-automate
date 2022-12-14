# name=CC_ExportTimeSeries_ExperimentalCNs
# description=Export time series data of each HMS reach, which corresponds to a RAS key river station, to .txt files after running CC HMS models
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.io import TimeSeriesContainer
from hec.io import PairedDataContainer
from hec.hecmath import TimeSeriesMath
from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname, HecTimeSeries
import java
from hec.heclib.dss import *
import sys

#syntax and guidance to develop this script found in DSS Programmers Guide for Java and HEC-DSSVue Users Manual
#https://www.hec.usace.army.mil/confluence/dssjavaprogrammer/dss-progammers-guide-for-java
#https://www.hec.usace.army.mil/software/hec-dssvue/documentation/User'sManual_2.0/HEC-DSSVue_20_Users_Manual.pdf

reaches = ['MCC A - MCC B',
 'MCC B MCC C',
 'MCC C - MCC D',
 'MCC D - MCC E',
 'CC 17 - JUNCTION',
 'CC16 - JUNCTION',
 'TC B REACH 1',
 'CC15 - JUNCTION',
 'TC B REACH 2',
 'CC 41 - JUNCTION',
 'TC B REACH 3',
 'CC 14 - JUNCTION',
 'TC B REACH 4',
 'CC23 - JUNCTION',
 'CC24 - JUNCTION',
 'JUNCTION - JUNCTION TC A',
 'CC25 - JUNCTION',
 'JUNCTION - TC A',
 'CC21 - TC A',
 'TC A - TC C',
 'TC B - D',
 'JUNCTION - TC F',
 'CC53 - TC E',
 'JUNCTION - TC G',
 'CC31 - CC29',
 'CC29 - UCC A',
 'CC33 - UCC A',
 'UCC A - B',
 'UCC B - C',
 'UCC C - JUNCTION',
 'CC35 - JUNCTION',
 'JUNCTION - UCC D',
 'UCC & TC - JUNCTION',
 'MCC H REACH 1',
 'MCC E - MCC F',
 'MCC H REACH 2',
 'MCC H REACH 3',
 'MCC I & H - MCC K',
 'MCC O UPPER',
 'Junction - MCC O',
 'MCC N - MCC P',
 'JUNCTION - LCC B',
 'LCC B - D',
 'LCC C - JUNCTION',
 'JUNCTION - LCC F',
 'JUNCTION - LCC G',
 'LCC G - LCC H',
 'LCC H - JUNCTION',
 'Lower CC I INTO J',
 'JUNCTION - LCC J',
 'LCC A - LCC C']


#2yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_2yrStorm/MSE4_No_Dams.dss" # specify the DSS file
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 2yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/2yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#5yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_5yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 5yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/5yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#10yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_10yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 10yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/10yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#25yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_25yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 25yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/25yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#50yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_50yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 50yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/50yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#100yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CoonCreek_100yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 100yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/100yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#200yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_200yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 200yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/200yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#500yr
file = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/CC_500yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 500yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_CC_Final/TimeSeriesData/500yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 
