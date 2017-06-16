import numpy as np
import matplotlib.pyplot as plt
import date_dictionary
import os

from matplotlib.font_manager import FontProperties

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
        print('## Road Section Info.')
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

# # For debug
# if __name__ == '__main__':
#     # gt = GoogleTrend('multiTimeline.csv')
#     # gt.load()
#     # gt.show_info()
#     # # for i in gt.dict_entire.item():
#     # #     print(i)
#     # gt.show_plot()
#
#     rs_00 = GoogleTrend('multiTimeline.csv')
#     rs_01 = GoogleTrend('multiTimeline-01.csv')
#     rs_02 = GoogleTrend('multiTimeline-ValueError.csv')
#     rs_02.load()
#     rs_02.show_info()
