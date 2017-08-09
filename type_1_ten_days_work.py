import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn
import dynamic_bpnn
import time
import os

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
total_start_time = time.time()

ten_days_mse_all = []
for input_day_size in range(1, 11):
    point = rs.really_start_day_index + 10  # 先跳過有問題那幾筆
    cases = []
    labels = []
    for i in range(0, 100):
        size_days = list(df.iloc[point:point + input_day_size, 0]) + list(df.iloc[point:point + input_day_size, 1])
        cases.append(size_days)
        labels.append([df.iloc[point + input_day_size, 0]])
        point += 1

    cases_test = []
    labels_test = []
    for j in range(0, 100):
        size_days = list(df.iloc[point:point + input_day_size, 0]) + list(df.iloc[point:point + input_day_size, 1])
        cases_test.append(size_days)
        labels_test.append([df.iloc[point + input_day_size, 0]])
        point += 1

    # TensorFlow version
    nn = dynamic_bpnn.BPNeuralNetwork()
    nn.setup(input_day_size * 2, [2], 1)
    input_day_mse_all = []
    for _ in range(1):
        start = time.time()
        nn.train(cases, labels)
        predict_all = nn.test(cases_test, labels_test)
        end = time.time()
        elapsed = end - start
        print("Time taken: ", elapsed, "seconds.")
        input_day_mse_all.append(nn.mse)
        if nn.mse == np.array(input_day_mse_all).min():
            if not os.path.isdir(os.getcwd() + '\\type_1_ten_days_work'):
                os.mkdir(os.getcwd() + '\\type_1_ten_days_work')
            if not os.path.isdir(os.getcwd() + '\\type_1_ten_days_work' + '\\' + str(input_day_size)):
                os.mkdir(os.getcwd() + '\\type_1_ten_days_work' + '\\' + str(input_day_size))
            nn.save_model('type_1_ten_days_work\\' + str(input_day_size) + '\\' + str(input_day_size) + '.ckpt')
    # plt.plot(labels_test, 'b')
    # plt.plot(predict_all, 'r')
    # plt.show()
    ten_days_mse_all.append(input_day_mse_all)
    del nn

total_end_time = time.time()
print("Total time taken: ", total_end_time - total_start_time, "seconds.")

for i in ten_days_mse_all:
    print(np.array(i).min())

# start = time.time()
# # Basic version
# nn = bpnn.BPNeuralNetwork()
# nn.setup(10, 2, 1)
# nn.train(cases, labels)
# predict_all = nn.test(cases_test, labels_test)
# end = time.time()
# elapsed = end - start
# print("Time taken: ", elapsed, "seconds.")
