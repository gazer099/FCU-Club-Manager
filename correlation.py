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
gt = GoogleTrend.GoogleTrend('雲林.csv')
gt.load()
gt.normalize()

rs = RoadSection.RoadSection('03F2614S-03F2709S.csv')
rs.load()
rs.normalize()

print(len(rs.flow_all))
print(len(gt.trend_percentage))
assert rs.really_start_day_index == gt.trend_start_day_index  # 416

# Store to Pandas DataFrame Type-------------------------------------------
# dates = pd.date_range('20150101', periods=639)
df = pd.DataFrame({
    'flow': rs.flow_all,
    'trend': gt.trend_percentage
},
    # index=dates
)

print(df)
# plt.plot(df[416:])
# plt.show()
print(sp.stats.pearsonr(rs.flow_all[416:], gt.trend_percentage[416:]))
# del gt
# gt_temple = GoogleTrend.GoogleTrend('北港朝天宮.csv')
# gt_temple.load()
# gt_temple.normalize()
# plt.plot(gt_temple.trend_percentage)
# plt.show()
# # print(sp.stats.pearsonr(rs.flow_all[416:], gt_temple.trend_percentage[416:]))
