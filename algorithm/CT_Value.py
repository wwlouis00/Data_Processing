import time
import datetime
from datetime import datetime, timedelta
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from openpyxl.worksheet.dimensions import ColumnDimension, RowDimension
import numpy as np
from openpyxl import load_workbook
from heapq import nsmallest
#-----------------------------------------------------------------------------------------------------------------------------
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))+"output.xlsx"
print("-"*200)
df = pd.read_csv("2021_10_22_16_26_07pos VTM A.csv")
#插入首行
df.drop(df.index[0])
df.columns = ['Time','temp_lid', 'temp_well', 'well_1', 'well_2', 'well_3', 'well_4', 'well_5', 'well_6', 'well_7', 'well_8','well_9', 'well_10', 'well_11', 'well_12', 'well_13', 'well_14', 'well_15', 'well_16']
print("-"*200)
print("橫列數"+str(len(df.columns)))
print("直列數"+str(len(df.index)-1))
time_1 = datetime.strptime(df.loc[1, 'Time'],"%H:%M:%S")
time_2 = datetime.strptime(df.loc[len(df.index)-1, 'Time'],"%H:%M:%S")
time_interval = time_2 - time_1
print("測試分鐘: "+str(time_interval))
print("-"*100)
#-----------------------------------------------------------------------------------------------------------------------------
time_array = []
for i in range(0, len(df.index), 1):
    time_array.append(i)
well_array = []
well_var = []
well_threshold =[]
start_time = int(input("輸入時段1:    "))
start_time_2 = int(input("輸入時段2:    "))
print(start_time *2)
print(start_time_2 *2)
for i in range(1,17,1):
    print("well_"+str(i))
    well_array.append([df.loc[data, 'well_' + str(i)] for data in range(len(df.index))])
    del well_array[i-1][0]
    #平均
    sum = 0
    for j in range(7,30,1):
        sum = sum + int(well_array[i-1][j])
    avg_well = sum/23
    print("平均:"+ str(avg_well))
    var = 0
    for k in range(7,30,1):
        var = abs((int(well_array[i-1][k]) - avg_well) / avg_well)
        well_var.append(var)
    print(np.std(well_var))
    threshold= var*10 + avg_well
    well_threshold.append(threshold)
    well_cut = []
    for m in range(0,len(df.index)-1,1):
        if threshold <= int(well_array[i-1][m]) and  m >= 31:
            if len(well_cut) == 0:
                well_cut.append(m)
                print(well_array[i-1][m])
                print(m)
            if len(well_cut) >= 1:
                break
    print(well_cut)   


df.to_excel('CT_Value_' + now_output_time, encoding="utf_8_sig")
