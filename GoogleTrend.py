import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

import date_dictionary

font = FontProperties(fname=r"c:\windows\Fonts\SimSun.ttc", size=12)


class GoogleTrend:
    file_name = None
    file_path = None
    target = None
    trend_start_day = None
    trend_end_day = None
    category = None
    area = None
    trend_percentage = []
    trend_start_day_index = None

    dict_entire = date_dictionary.get_dict_entire()

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = str(os.path.join(os.getcwd(), 'GoogleTrendData', self.file_name))

    def load(self):
        try:
            open(self.file_path)
        except FileNotFoundError as err:
            print(err)
            return False
        with open(self.file_path, encoding='utf8') as file:
            for idx, line in enumerate(file):
                if idx == 0:
                    self.category = line[3:-1]
                if idx == 2:
                    self.target = line.split(':')[0][2:]  # 天,劍湖山: (全球)
                    self.area = line.split(':')[1][1:]
                if idx >= 3 and line != '':
                    line = line.split(',')
                    line[0] = line[0].replace('-', '/')
                    self.dict_entire[line[0]] = line[1]
                    if self.trend_start_day is None:
                        self.trend_start_day = line[0]
                    else:
                        self.trend_end_day = line[0]
        for row in self.dict_entire.values():
            try:
                self.trend_percentage.append(int(row))
            except ValueError as err:
                print(err)
                return False
        # print(self.trend_percentage)
        # Determine the trend start day index
        for idx, row in enumerate(dict.items(self.dict_entire)):
            # print(idx, row)
            if int(row[1]) != 0:
                self.trend_start_day_index = idx
                break
        return True

    def show_info(self):
        print('## Google Trend Info.')
        print('File name:', self.file_name)
        print('Category:', self.category)
        print('Target:', self.target)
        print('Area:', self.area[:-1])
        print('Trend start day:', self.trend_start_day)
        print('Trend end day:', self.trend_end_day)

    def show_plot(self):
        self.trend_percentage = np.array(self.trend_percentage[self.trend_start_day_index:])
        plt.plot(self.trend_percentage)
        plt.title(self.target + ' Google搜尋趨勢', fontproperties=font)
        plt.xlabel('day')
        plt.ylabel('percentage')
        plt.show()

    def normalize(self):
        norm = [float(i) / sum(self.trend_percentage) for i in self.trend_percentage]
        norm = [float(i) / max(self.trend_percentage) for i in self.trend_percentage]
        self.trend_percentage = norm

    def get_peak_info(self):
        datum = 0.2
        peak_info_all = []
        peak_info = []
        # max_temp = 0
        # print(self.trend_percentage)
        for idx, percent in enumerate(self.trend_percentage):
            if percent >= datum:
                if not peak_info:
                    peak_info.append(idx)
                    # if percent > max_temp:
                    #     max_temp = percent
            elif len(peak_info) == 1:
                peak_info.append(idx)
                # peak_info.append(max_temp)
                peak_info_all.append(peak_info)
                peak_info = []
                # max_temp = 0
        return peak_info_all


# For debug
if __name__ == '__main__':
    # gt = GoogleTrend('multiTimeline.csv')
    # gt.load()
    # gt.show_info()
    # # for i in gt.dict_entire.item():
    # #     print(i)
    # gt.show_plot()

    # rs_00 = GoogleTrend('multiTimeline.csv')
    # rs_01 = GoogleTrend('multiTimeline-01.csv')
    # rs_02 = GoogleTrend('multiTimeline-ValueError.csv')
    # rs_02.load()
    # rs_02.show_info()

    gt = GoogleTrend('multiTimeline.csv')
    gt.load()
    gt.normalize()
    gt.show_info()
    for i in gt.get_peak_info():
        print(i)
    # gt.show_plot()
    pi = gt.get_peak_info()
    for section in pi:
        eigenvalues = []
        data = np.array(gt.trend_percentage[section[0]:section[1] + 1])
        eigenvalues.append(data.max())
        eigenvalues.append(data.min())
        eigenvalues.append(data.mean())
        eigenvalues.append(data.std())
        eigenvalues.append(data.var())
        eng = 0
        for i in data:
            eng += i ** 2
        eigenvalues.append(eng)
        eigenvalues.append(len(data))
        section += eigenvalues

    for i in pi:
        print(i)
