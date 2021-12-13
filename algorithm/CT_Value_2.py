import time
import datetime
from datetime import datetime, timedelta
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from openpyxl.worksheet.dimensions import ColumnDimension, RowDimension
import numpy as np
from heapq import nsmallest

from pandas.io.parsers import read_csv
#-----------------------------------------------------------------------------------------------------------------------------
global df_raw, df_ifc, df_normalization
now_output_time = str(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))+"output.xlsx"
print("-"*200)
df = pd.read_csv("2021_10_22_16_26_07pos VTM A.csv")
df_normalization = df.copy
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
# start_time = int(input("輸入時段1:    "))
# start_time_2 = int(input("輸入時段2:    "))
# print(start_time *2)
# print(start_time_2 *2)
# print(df_normalization)
def get_StdDev_and_Avg():
    for i in range(0,16,1):
        well_array.append([df.loc[data, 'well_' + str(i+1)] for data in range(len(df.index))])
        del well_array[i][0]
    stdDev = []
    Avg = []
    for j in range(0,16):
        # df_current_well = df[f'well_{j+1}']
        # std_value = float(df_current_well[10:32].mean())
        # print(std_value)
        well_catch = []
        for k in range(10,33):
            well_catch.append(int(well_array[j][k]))
        print('well_'+ str(j+1))
        sr = pd.Series(well_catch)
        print("pandas stdDev: " + str(sr.std()))
        stdDev.append(sr.std())
        print("pandas mean: " + str(sr.mean()))
        Avg.append(sr.mean())
        print('-'*50)
        #-------------------------------
        # print("numpy stdDev: " + str(np.std(well_catch)))
        # print("numpy mean: " + str(np.mean(well_catch)))
        stdDev.append(np.mean(well_catch))
        Avg.append(np.mean(well_catch)))
        print("-"*100)


    return stdDev, Avg
def normalize():
    baseline_array = []
    for i in range(0,16):
        df_current_well = df[f'well_{i+1}']
        baseline = df_current_well[10:32].mean()
        baseline_array.append(baseline)
    # print(baseline_array)

    
    # for k in range(0,16):
    #     df_current_well = df[f"well_{k+1}"]
        # print((df_current_well[10:32]))

        # stdDev.append(df_current_well[10:32].std())
        
# def normalize():
  



def main():
    get_StdDev_and_Avg()
    normalize()
    # df.to_excel('CT_Value_' + now_output_time, encoding="utf_8_sig")


if __name__ == '__main__':
    main()
        


