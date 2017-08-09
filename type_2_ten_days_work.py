import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn
import dynamic_bpnn
import time
from sklearn.metrics import mean_squared_error
import os


def normalize(series, x):
    return 2 / (series.max() - series.min()) * (x - series.min()) - 1


def normalize_all(series):
    series_max = series.max()
    series_min = series.min()
    return pd.Series([(lambda x: 2 / (series_max - series_min) * (x - series_min) - 1)(x) for x in series])


def anti_normalize_all(src_series, target_series):
    src_series_max = src_series.max()
    src_series_min = src_series.min()
    return pd.Series(
        [(lambda y: (y + 1) * ((src_series_max - src_series_min) / 2) + src_series_min)(y) for y in target_series])


# Load Data-----------------------------------------------------
rs = RoadSection.RoadSection('03F2614S-03F2709S.csv')
rs.load()
# rs.normalize()

gt = GoogleTrend.GoogleTrend('multiTimeline.csv')
gt.load()
# gt.normalize()

print(len(rs.flow_all))
print(len(gt.trend_percentage))
assert rs.really_start_day_index == gt.trend_start_day_index  # 416

# Store to Pandas DataFrame Type-------------------------------------------
# dates = pd.date_range('20150101', periods=639)
df = pd.DataFrame({
    'flow': rs.flow_all,  # df[:, 0]
    'trend': gt.trend_percentage  # df[:, 1]
},
    # index=dates
)

flow_week_dict = {
    '0': rs.flow_all[rs.really_start_day_index::7],
    '1': rs.flow_all[rs.really_start_day_index + 1::7],
    '2': rs.flow_all[rs.really_start_day_index + 2::7],
    '3': rs.flow_all[rs.really_start_day_index + 3::7],
    '4': rs.flow_all[rs.really_start_day_index + 4::7],
    '5': rs.flow_all[rs.really_start_day_index + 5::7],
    '6': rs.flow_all[rs.really_start_day_index + 6::7]
}
trend_week_dict = {
    '0': gt.trend_percentage[rs.really_start_day_index::7],
    '1': gt.trend_percentage[rs.really_start_day_index + 1::7],
    '2': gt.trend_percentage[rs.really_start_day_index + 2::7],
    '3': gt.trend_percentage[rs.really_start_day_index + 3::7],
    '4': gt.trend_percentage[rs.really_start_day_index + 4::7],
    '5': gt.trend_percentage[rs.really_start_day_index + 5::7],
    '6': gt.trend_percentage[rs.really_start_day_index + 6::7]
}
df_flow_week = pd.DataFrame.from_dict(flow_week_dict, orient='index').T
df_trend_week = pd.DataFrame.from_dict(trend_week_dict, orient='index').T
print(df)
print(df_flow_week)
print(df_trend_week)
# exit()

# Type 2 Neural Network---------------------------------------------------------------
df_flow_week_sub_mean = df_flow_week.copy()
df_trend_week_sub_mean = df_trend_week.copy()
assert df_flow_week_sub_mean.shape == df_trend_week_sub_mean.shape

# subtract mean
for col in range(df_flow_week_sub_mean.shape[1]):
    df_flow_week_sub_mean.iloc[:, col] -= df_flow_week.iloc[:, col].mean()
    df_trend_week_sub_mean.iloc[:, col] -= df_trend_week.iloc[:, col].mean()
print(df_flow_week_sub_mean)
print(df_trend_week_sub_mean)

# transform to series
series_flow_week_sub_mean = pd.Series(pd.concat(
    [(lambda row: df_flow_week_sub_mean.iloc[row, :])(row) for row in range(df_flow_week_sub_mean.shape[0])], axis=0,
    ignore_index=True))
print(series_flow_week_sub_mean)
series_trend_week_sub_mean = pd.concat(
    [(lambda row: df_trend_week_sub_mean.iloc[row, :])(row) for row in range(df_trend_week_sub_mean.shape[0])], axis=0,
    ignore_index=True)
print(series_trend_week_sub_mean)

# normalization
point = 10  # 先跳過有問題那幾筆
series_flow_week_sub_mean_normalization = normalize_all(series_flow_week_sub_mean[point:])
series_trend_week_sub_mean_normalization = normalize_all(series_trend_week_sub_mean[point:])
print('***', len(series_flow_week_sub_mean_normalization), point)
df_FnT_week_sub_mean_normalization = pd.DataFrame({
    'f_sn': series_flow_week_sub_mean_normalization,
    't_sn': series_trend_week_sub_mean_normalization
})
print(df_FnT_week_sub_mean_normalization)
# plt.plot(df_FnT_week_sub_mean_normalization)
# plt.show()
# exit()

# # anti-normalization
# series_flow_week_sub_mean_anti_normalization = anti_normalize_all(series_flow_week_sub_mean[point:],
#                                                                   series_flow_week_sub_mean_normalization)
# series_trend_week_sub_mean_anti_normalization = anti_normalize_all(series_trend_week_sub_mean[point:],
#                                                                    series_trend_week_sub_mean_normalization)
# print('anti!!!!!!!!!!!!!!!!!!!!!!!')
# cp_series_flow_week_sub_mean = series_flow_week_sub_mean[point:].copy()
# cp_series_trend_week_sub_mean = series_trend_week_sub_mean[point:].copy()
# print(type(series_flow_week_sub_mean), type(series_trend_week_sub_mean))
# df_FnT_week_sub_mean_normalization = pd.DataFrame({
#     'f': cp_series_flow_week_sub_mean,
#     't': cp_series_trend_week_sub_mean,
#     'f_san': series_flow_week_sub_mean_anti_normalization,
#     't_san': series_trend_week_sub_mean_anti_normalization
# })
# print(df_FnT_week_sub_mean_normalization)
# # exit()

total_start_time = time.time()

ten_days_mse_all = []
for input_day_size in range(1, 11):
    cases = []
    labels = []
    for i in range(0, 100):
        size_days = list(series_flow_week_sub_mean_normalization[i:i + input_day_size]) + list(
            series_trend_week_sub_mean_normalization[i:i + input_day_size])
        cases.append(size_days)
        # print(i, i + 5, [series_flow_week_sub_mean_normalization[i + input_day_size]])
        labels.append([series_flow_week_sub_mean_normalization[i + input_day_size]])

    cases_test = []
    labels_test = []
    for i in range(100, 200):
        size_days = list(series_flow_week_sub_mean_normalization[i:i + input_day_size]) + list(
            series_trend_week_sub_mean_normalization[i:i + input_day_size])
        cases_test.append(size_days)
        # print(i, i + 5, [series_flow_week_sub_mean_normalization[i + input_day_size]])
        labels_test.append([series_flow_week_sub_mean_normalization[i + input_day_size]])

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
            if not os.path.isdir(os.getcwd() + '\\type_2_ten_days_work'):
                os.mkdir(os.getcwd() + '\\type_2_ten_days_work')
            if not os.path.isdir(os.getcwd() + '\\type_2_ten_days_work' + '\\' + str(input_day_size)):
                os.mkdir(os.getcwd() + '\\type_2_ten_days_work' + '\\' + str(input_day_size))
            nn.save_model('type_2_ten_days_work\\' + str(input_day_size) + '\\' + str(input_day_size) + '.ckpt')
    # plt.plot(labels_test, 'b')
    # plt.plot(predict_all, 'r')
    # plt.show()
    ten_days_mse_all.append(input_day_mse_all)
    del nn

total_end_time = time.time()
print("Total time taken: ", total_end_time - total_start_time, "seconds.")

for i in ten_days_mse_all:
    print(np.array(i).min())

# # Basic version
# nn = bpnn.BPNeuralNetwork()
# nn.setup(10, 2, 1)
# while True:
#     start = time.time()
#     nn.train(cases_test, labels_test)
#     predict_all = nn.test(cases, labels)
#     end = time.time()
#     elapsed = end - start
#     print("Time taken: ", elapsed, "seconds.")
#     if nn.mse < 0.21:
#         break

# # TensorFlow version
# nn = dynamic_bpnn.BPNeuralNetwork()
# nn.setup(10, [2], 1)
# while True:
#     start = time.time()
#     nn.train(cases, labels)
#     predict_all = nn.test(cases_test, labels_test)
#     end = time.time()
#     elapsed = end - start
#     print("Time taken: ", elapsed, "seconds.")
#     if nn.mse < 0.020:
#         break
# nn.save_model('tf_model\save_net.ckpt')

# Load
# nn = dynamic_bpnn.BPNeuralNetwork()
# nn.setup(10, [2], 1)
# nn.load_model('tf_model\save_net.ckpt')
# predict_all = nn.test(cases_test, labels_test)
#
# plt.plot(labels_test, 'b')
# plt.plot(predict_all, 'r')
# # plt.plot(google)
# plt.show()
