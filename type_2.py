import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GoogleTrend
import RoadSection
import bpnn


def normalize(series, x):
    return 2 / (series.max() - series.min()) * (x - series.min()) - 1


def normalize_all(series):
    series_max = series.max()
    series_min = series.min()
    return pd.Series([(lambda x: 2 / (series_max - series_min) * (x - series_min) - 1)(x) for x in series])


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

for col in range(df_flow_week_sub_mean.shape[1]):
    df_flow_week_sub_mean.iloc[:, col] -= df_flow_week_sub_mean.iloc[:, col].mean()
    df_trend_week_sub_mean.iloc[:, col] -= df_trend_week_sub_mean.iloc[:, col].mean()
print(df_flow_week_sub_mean)
print(df_trend_week_sub_mean)

series_flow_week_sub_mean = pd.Series(pd.concat(
    [(lambda row: df_flow_week_sub_mean.iloc[row, :])(row) for row in range(df_flow_week_sub_mean.shape[0])], axis=0,
    ignore_index=True))
print(series_flow_week_sub_mean)
series_trend_week_sub_mean = pd.concat(
    [(lambda row: df_trend_week_sub_mean.iloc[row, :])(row) for row in range(df_trend_week_sub_mean.shape[0])], axis=0,
    ignore_index=True)
print(series_trend_week_sub_mean)

point = 10  # 先跳過有問題那幾筆
cases = []
labels = []
series_flow_week_sub_mean_normalization = normalize_all(series_flow_week_sub_mean[point:])
series_trend_week_sub_mean_normalization = normalize_all(series_trend_week_sub_mean[point:])
print('***', len(series_flow_week_sub_mean_normalization), point)
df_sub_mean_normalization = pd.DataFrame({
    'f_sn': series_flow_week_sub_mean_normalization,
    't_sn': series_trend_week_sub_mean_normalization
})
print(df_sub_mean_normalization)
plt.plot(df_sub_mean_normalization)
plt.show()
exit()

for i in range(0, 100):
    five_days = list(series_flow_week_sub_mean_normalization[i:i + 5]) + list(
        series_trend_week_sub_mean_normalization[i:i + 5])
    cases.append(five_days)
    print(i, i + 5, [series_flow_week_sub_mean_normalization[i + 5]])
    labels.append([series_flow_week_sub_mean_normalization[i + 5]])

cases_test = []
labels_test = []
google = []
for i in range(100, 200):
    five_days = list(series_flow_week_sub_mean_normalization[i:i + 5]) + list(
        series_trend_week_sub_mean_normalization[i:i + 5])
    cases_test.append(five_days)
    print(i, i + 5, [series_flow_week_sub_mean_normalization[i + 5]])
    labels_test.append([series_flow_week_sub_mean_normalization[i + 5]])
    google.append([series_trend_week_sub_mean_normalization[i + 5]])

# exit()
nn = bpnn.BPNeuralNetwork()
nn.setup(10, 2, 1)
nn.train(cases_test, labels_test)
predict_all = nn.test(cases, labels)

plt.plot(labels_test, 'b')
plt.plot(predict_all, 'r')
# plt.plot(google)
plt.show()
