# import matplotlib相關套件

import matplotlib.pyplot as plt

# import字型管理套件

from matplotlib.font_manager import FontProperties

 

# 指定使用字型和大小

myfont = FontProperties(fname='D:/Programs/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/msjh.ttc', size=40)

 

# 使用月份當做X軸資料

month = [1,2,3,4,5,6,7,8,9,10,11,12]

# 使用台G電的某年每月收盤價當第一條線的資料

stock_tsmcc = [255,246,247.5,227,224,216.5,246,256,262.5,234,225.5,225.5]

# 使用紅海的某年每月收盤價當第二條線的資料

stock_foxconnn = [92.2,88.1,88.5,82.9,85.7,83.2,83.8,80.5,79.2,78.8,71.9,70.8]

 

# 設定圖片大小為長15、寬10

plt.figure(figsize=(15,10),dpi=100,linewidth = 2)

# 把資料放進來並指定對應的X軸、Y軸的資料，用方形做標記(s-)，並指定線條顏色為紅色，使用label標記線條含意

plt.plot(month,stock_tsmcc,'s-',color = 'r', label="TSMC")

# 把資料放進來並指定對應的X軸、Y軸的資料 用圓形做標記(o-)，並指定線條顏色為綠色、使用label標記線條含意

plt.plot(month,stock_foxconnn,'o-',color = 'g', label="FOXCONN")

 

# 設定圖片標題，以及指定字型設定，x代表與圖案最左側的距離，y代表與圖片的距離

plt.title("Python 畫折線圖(Line chart)範例", fontproperties=myfont, x=0.5, y=1.03)

# 设置刻度字体大小

plt.xticks(fontsize=20)

plt.yticks(fontsize=20)

# 標示x軸(labelpad代表與圖片的距離)

plt.xlabel("month", fontsize=30, labelpad = 15)

# 標示y軸(labelpad代表與圖片的距離)

plt.ylabel("price", fontsize=30, labelpad = 20)

# 顯示出線條標記位置

plt.legend(loc = "best", fontsize=20)

# 畫出圖片

plt.show()