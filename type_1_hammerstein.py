import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn
import dynamic_bpnn
import time
import csv
import math
from multiprocessing import Pool
import neural
from sklearn.metrics import mean_squared_error

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

# Store to Pandas DataFrame Type-------------------------------------------
# dates = pd.date_range('20150101', periods=639)
df = pd.DataFrame({
    'flow': rs.flow_all,
    'trend': gt.trend_percentage
},
    # index=dates
)

# Type 1 Neural Network---------------------------------------------------------------
point = rs.really_start_day_index + 10  # 先跳過有問題那幾筆
cases = []
labels = []
for i in range(0, 100):
    five_days = list(df.iloc[point:point + 5, 0]) + list(df.iloc[point:point + 5, 1])
    cases.append(five_days)
    labels.append([df.iloc[point + 5, 0]])
    point += 1

cases_test = []
labels_test = []
for j in range(0, 100):
    five_days = list(df.iloc[point:point + 5, 0]) + list(df.iloc[point:point + 5, 1])
    cases_test.append(five_days)
    labels_test.append([df.iloc[point + 5, 0]])
    point += 1
# ---------------------------------------------------------------------------------------
# for c, l in zip(cases, labels):
#     print(c, l)
neutest = neural.Neu('03F2614S-03F2709S')

trainfinished = False
while trainfinished != True:
    try:
        for i in range(neutest.epoch):
            # print(i + 1)
            # count = 0
            for c, l in zip(cases, labels):
                inputlist = c
                expect = l

                # print('input: ', inputlist)
                # print('expect: ', expect)

                result = neutest.forward(inputlist)
                # print('result: ', result)
                neutest.backward(expect)
                # print(count)
                # count = count + 1
                # if count == 288:
                #     count = 0
            neutest.cleartemporalepoch()
    except OverflowError:
        neutest = neural.Neu('03F2614S-03F2709S')
        print('math error')
    else:
        trainfinished = True

predict_all = []
for test1 in cases_test:
    result = neutest.forward(test1)
    predict_all.append(result)
mse = mean_squared_error(labels_test, predict_all)
print('MSE :', mse)

plt.plot(labels_test, 'b')
plt.plot(predict_all, 'r')
plt.show()
