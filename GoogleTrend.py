import csv
import numpy as np
import matplotlib.pyplot as plt
import date_dictionary

from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\Fonts\SimSun.ttc", size=12)


class GoogleTrend:
    file_name = None
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

    def load(self):
        try:
            open(self.file_name)
        except FileNotFoundError as err:
            print(err)
            return False
        with open(self.file_name, encoding='utf8') as file:
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
            self.trend_percentage.append(int(row))
        # print(self.trend_percentage)
        # Determine the really start day and file miss day
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
        self.trend_percentage = np.array(self.trend_percentage)
        plt.plot(self.trend_percentage[self.trend_start_day_index:])
        plt.title(self.target + ' Google搜尋趨勢', fontproperties=font)
        plt.xlabel('day')
        plt.ylabel('percentage')
        plt.show()


if __name__ == '__main__':
    gt = GoogleTrend('multiTimeline.csv')
    gt.load()
    gt.show_info()
    # for i in gt.dict_entire.item():
    #     print(i)
    gt.show_plot()
