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
# Normalize data 1 to -1
def normalize_all(series):
    series_max = series.max()
    series_min = series.min()
    return pd.Series([(lambda x: 2 / (series_max - series_min) * (x - series_min) - 1)(x) for x in series])
df = pd.DataFrame({
    'flow': normalize_all(np.array(rs.flow_all[rs.really_start_day_index:])),
    'trend': normalize_all(np.array(gt.trend_percentage[rs.really_start_day_index:]))
},
    # index=dates
)

# Type 1 Neural Network---------------------------------------------------------------
point = 10  # 先跳過有問題那幾筆
cases = []
labels = []
for i in range(0, 100):
    one_day = list(df.iloc[point:point + 1, 0]) + list(df.iloc[point:point + 1, 1])
    cases.append(one_day)
    labels.append([df.iloc[point + 1, 0]])
    point += 1

cases_test = []
labels_test = []
for j in range(0, 100):
    one_day = list(df.iloc[point:point + 1, 0]) + list(df.iloc[point:point + 1, 1])
    cases_test.append(one_day)
    labels_test.append([df.iloc[point + 1, 0]])
    point += 1
# ---------------------------------------------------------------------------------------
mse_all = []
total_start_time = time.time()
for r in range(100):
    start = time.time()
    neutest = neural.Neu('03F2614S-03F2709S' + ' #' + str(r))
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
            neutest = neural.Neu('03F2614S-03F2709S' + ' #' + str(r))
            print('math error')
        else:
            trainfinished = True
    end = time.time()
    elapsed = end - start
    print("Time taken: ", elapsed, "seconds.")
    # test
    predict_all = []
    for test1 in cases_test:
        result = neutest.forward(test1)
        predict_all.append(result)
    mse = mean_squared_error(labels_test[50:], predict_all[50:])
    print('MSE :', mse)
    mse_all.append(mse)

total_end_time = time.time()
print("Total time taken: ", total_end_time - total_start_time, "seconds.")

print(mse_all)
print(np.array(mse_all).min())


# plt.plot(labels_test, 'b')
# plt.plot(predict_all, 'r')
# plt.show()
