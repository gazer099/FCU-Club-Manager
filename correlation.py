import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn
import dynamic_bpnn
import time
import os
import scipy as sp

# Load Data-----------------------------------------------------
gt = GoogleTrend.GoogleTrend('multiTimeline.csv')
gt.load()
gt.normalize()

rs = RoadSection.RoadSection('03F2614S-03F2709S.csv')
rs.load()
rs.normalize()

print(len(rs.flow_all))
print(len(gt.trend_percentage))
assert rs.really_start_day_index == gt.trend_start_day_index  # 416

gt2_trend_percentage = []
with open('GoogleTrendData/1_北港朝天宮.csv', 'r', encoding='utf8') as file:
    for line in file:
        if line[0:4] == '2016':
            data = line.split(',')
            gt2_trend_percentage.append(int(data[1]) / 100)
            # print(int(data[1]))
print(len(gt2_trend_percentage))

gt3_trend_percentage = []
with open('GoogleTrendData/7_雲林故事館.csv', 'r', encoding='utf8') as file:
    for line in file:
        if line[0:4] == '2016':
            data = line.split(',')
            gt3_trend_percentage.append(int(data[1]) / 100)
            # print(int(data[1]))
print(len(gt3_trend_percentage))

t1 = []
t2 = []
t3 = []
with open('GoogleTrendData/top3.csv', 'r', encoding='utf8') as file:
    for line in file:
        if line[0:4] == '2016':
            data = line.split(',')
            t1.append(int(data[1]) / 100)
            t2.append(int(data[2]) / 100)
            t3.append(int(data[3]) / 100)
# exit()
# Store to Pandas DataFrame Type-------------------------------------------
# dates = pd.date_range('20150101', periods=639)
df = pd.DataFrame({
    '0flow': rs.flow_all[416:],
    # 'trend': gt.trend_percentage[416:],
    # 'trend2': gt2_trend_percentage,
    # 'trend3': gt3_trend_percentage
    '1': t1,
    '2': t2,
    '3': t3,
},
    # index=dates
)

print(df)
plt.plot(df[:125])
plt.show()
print(sp.stats.pearsonr(rs.flow_all[416:], gt.trend_percentage[416:]))
# del gt
# gt_temple = GoogleTrend.GoogleTrend('北港朝天宮.csv')
# gt_temple.load()
# gt_temple.normalize()
# plt.plot(gt_temple.trend_percentage)
# plt.show()
# # print(sp.stats.pearsonr(rs.flow_all[416:], gt_temple.trend_percentage[416:]))
