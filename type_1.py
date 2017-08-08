import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn
import dynamic_bpnn
import time

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

# start = time.time()
# # Basic version
# nn = bpnn.BPNeuralNetwork()
# nn.setup(10, 2, 1)
# nn.train(cases, labels)
# predict_all = nn.test(cases_test, labels_test)
# end = time.time()
# elapsed = end - start
# print("Time taken: ", elapsed, "seconds.")

# TensorFlow version
nn = dynamic_bpnn.BPNeuralNetwork()
nn.setup(10, [2], 1)
while True:
    start = time.time()
    nn.train(cases, labels)
    predict_all = nn.test(cases_test, labels_test)
    end = time.time()
    elapsed = end - start
    print("Time taken: ", elapsed, "seconds.")
    if nn.mse < 0.012:
        break


plt.plot(labels_test, 'b')
plt.plot(predict_all, 'r')
plt.show()
