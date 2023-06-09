import pandas as pd
import os
from datetime import datetime


# global variable
raw_file_path = "./result/detection.csv"
ifc_file_path = "./para/cali_factor.csv"

def get_accumulation_time():
    df_time = df_normalization['time']
    time_ori = datetime.strptime(df_time[0], "%H:%M:%S")
    time_delta = []
    for time in df_time:
        time_now = datetime.strptime(time, "%H:%M:%S")
        time_delta.append((time_now - time_ori).seconds/60)
    df_normalization.insert(1, column="accumulation", value=time_delta)

def get_StdDev_and_Avg():
    StdDev = []
    Avg = []
    for i in range(0, 16):
        df_current_well = df_normalization[f'well{i+1}']
        StdDev.append(df_current_well[8:30].std())
        Avg.append(df_current_well[8:30].mean())
    return StdDev, Avg

def normalize(baseline_begin, baseline_end):
    for i in range(0, 16):
        df_current_well = df_raw[f'well{i+1}']
        df_current_ifc = df_ifc[f'well{i+1}']
        baseline = df_current_well[baseline_begin:baseline_end].mean()
        df_normalization[f'well{i+1}'] = (df_raw[f'well{i+1}']-baseline)/df_current_ifc[0] # normalized = (IF(t)-IF(b))/IFc

def get_ct_threshold():
    threshold_value = []
    StdDev, Avg = get_StdDev_and_Avg()
    for i in range(0, 16):
        threshold_value.append(10*StdDev[i] + Avg[i])
        print(f"Well {i+1}: StdDev is {StdDev[i]}, Avg is {Avg[i]}")
    return threshold_value

def get_ct_value(threshold_value):
    Ct_value = []
    for i in range(0, 16):
        df_current_well = df_normalization[f'well{i+1}']
        df_accumulation = df_normalization['accumulation']
        print("\n")
        print(df_current_well)
        print(f"Threshold value: {threshold_value[i]}")
        try:
            for j, row in enumerate(df_current_well):
                if row >= threshold_value[i]:
                    print(f"row: {row}")
                    thres_lower = df_current_well[j-1]
                    thres_upper = df_current_well[j]                
                    acc_time_lower = df_accumulation[j-1]
                    acc_time_upper = df_accumulation[j+1]
                    
                    # linear regression
                    x2 = acc_time_upper
                    y2 = thres_upper
                    x1 = acc_time_lower
                    y1 = thres_lower
                    y = threshold_value[i]
                    x = (x2-x1)*(y-y1)/(y2-y1)+x1

                    Ct_value.append(round(x, 2))
                    print(f"Ct of well{i+1} is {round(x, 2)}")
                    break

                # if there is no Ct_value availible
                elif j == len(df_current_well)-1:
                    Ct_value.append(99.99)
                    print("Ct value is not available")
        except Exception as e:
            print(e)
            Ct_value.append(99.99)
            print("Ct value is not available")

    return Ct_value

def ct_calculation(baseline_begin, baseline_end):
    global df_raw, df_ifc, df_normalization
    df_raw = pd.read_csv(raw_file_path)
    df_ifc = pd.read_csv(ifc_file_path)
    df_normalization = df_raw.copy()

    get_accumulation_time()
    normalize(baseline_begin, baseline_end)
    # df_normalization.to_csv("./result/normalization.csv", index=False)
    threshold_value = get_ct_threshold()
    Ct_value = get_ct_value(threshold_value)
    return Ct_value
