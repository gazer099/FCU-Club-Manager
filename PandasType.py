import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn

gt = GoogleTrend.GoogleTrend('multiTimeline.csv')
gt.load()
gt.normalize()

rs = RoadSection.RoadSection('03F2614S-03F2709S.csv')
rs.load()
rs.normalize()

print(len(gt.trend_percentage))
print(len(rs.flow_all))
print(rs.really_start_day_index)

dates = pd.date_range('20150101', periods=639)
df = pd.DataFrame({
    'trend': gt.trend_percentage,
    'flow': rs.flow_all
},
    # index=dates
)

print(df)

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

nn = bpnn.BPNeuralNetwork()
nn.setup(10, 22, 1)
nn.train(cases, labels)
nn.test(cases_test, labels_test)
