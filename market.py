############################################
# 資料來源: 工業產銷存動態調查
# 王維澤
############################################
import pandas as pd
from datetime import datetime, time
from matplotlib.axis import XAxis
import plotly.graph_objs as go
import os

data = []

m_csv = pd.read_excel("./InquireAdvance.xlsx")
print(m_csv)

# m_csv.to_excel("test.xlsx")

for i in range(0,len(m_csv.index),1):
    data.append(m_csv.loc[i,'生產值 (千元)'])
print(data)
