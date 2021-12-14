import time
import datetime
from datetime import datetime, timedelta
from numpy.core.fromnumeric import std
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from openpyxl.worksheet.dimensions import ColumnDimension, RowDimension
import numpy as np
from heapq import nsmallest

from pandas.io.parsers import read_csv


global df,df_ifc,df_normalization
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))+"output.xlsx"

raw_file_path = "2021_10_22_16_26_07pos VTM A.csv"
ifc_file_path = "cali_factor.csv"
df = pd.read_csv(raw_file_path)
ifc= pd.read_csv(ifc_file_path)
df_normalization = df.copy()
df.columns = ['time','temp_lid', 'temp_well', 'well_1', 'well_2', 'well_3', 'well_4', 'well_5', 'well_6', 'well_7', 'well_8','well_9', 'well_10', 'well_11', 'well_12', 'well_13', 'well_14', 'well_15', 'well_16']

well_array = []
ifc_array  = []
for i in range(0,16,1):
    well_array.append([df.loc[data, 'well_' + str(i+1)] for data in range(len(df.index))])
    del well_array[i][0]
    ifc_array.append([ifc.loc[data, 'well' + str(i+1)] for data in range(len(ifc.index))])
print(ifc_array[0][0])

StdDev = []
Avg = []
for i in range(0, 16):
    # df_current_well = df_normalization[f'well_{i+1}']
    well_catch = []
    for j in range(10,33):
        well_catch.append(int(well_array[i][j]))
    StdDev.append(np.std(well_catch))
    Avg.append(np.mean(well_catch))
print(Avg[0])

for j in range(0,16):
    test = []
    baseline = Avg[j]
    for k in range(0,len(df.index)-1,1):
        test.append(int(well_array[j][k]) - baseline / int(ifc_array[j][0])) 
    print(test)
threshold_value = []


    
        
    





    # StdDev.append(df_current_well[8:30].std())
    # Avg.append(df_current_well[8:30].mean())








        


