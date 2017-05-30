import csv
import numpy as np
import matplotlib.pyplot as plt
import date_dictionary


class GoogleTrend:
    file_name = None
    target = None
    trend_start_day = None
    trend_end_day = None
    category = None
    # area = None

    dict_entire = date_dictionary.get_dict_entire()

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        with open(self.file_name) as file:
            line_list = []
            for line in file:
                line_list.append(line)
            print(line_list)
            # for idx, line in enumerate(line_list):
            #     if idx == 0:
            #         self.category = line[3:]
            #     if idx == 2:
            #         # todo solve split problem
            #         self.target = line[2:]
            #     if idx >= 3 and line != '':
            #         line = line.split(',')
            #         line[0] = line[0].replace('-', '/')
            #         self.dict_entire[line[0]] = line[1]
            #         if self.trend_start_day is None:
            #             self.trend_start_day = line[0]
            #         else:
            #             self.trend_end_day = line[0]

    def show_info(self):
        print('## Road Section Info.')
        print('File name:', self.file_name)
        print('Category', self.category)
        print('Target:', self.target)
        print('Trend start day:', self.trend_start_day)
        print('Trend end day:', self.trend_end_day)


if __name__ == '__main__':
    gt = GoogleTrend('multiTimeline.csv')
    gt.load()
    # gt.show_info()
    # for i in gt.dict_entire:
    #     print(i)
