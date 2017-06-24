import csv
import numpy as np
import matplotlib.pyplot as plt
import date_dictionary
import DataManager
import os

from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\Fonts\SimSun.ttc", size=12)


class RoadSection:
    file_name = None
    file_path = None
    road_section_name = None
    file_start_day = None
    file_end_day = None
    file_miss_day = []
    really_start_day = None
    really_start_day_index = None
    dict_entire = date_dictionary.get_dict_entire()
    flow_all = []

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = str(os.path.join(os.getcwd(), 'RoadSectionData', self.file_name))
        # 清空不明原因 self.dict_entire 內的殘值
        for day in self.dict_entire:
            self.dict_entire[day] = 0

    def load(self):
        try:
            open(self.file_path)
        except FileNotFoundError as err:
            print(err)
            return False
        # Get road section name
        dm = DataManager.DataManager()
        self.road_section_name = dm.get_road_section_name(self.file_name)
        # Fix original file header
        self.revise_header()
        # 清空不明原因 self.dict_entire 內的殘值
        for day in self.dict_entire:
            self.dict_entire[day] = 0
        # Load data of flow
        with open(str(os.path.join(os.getcwd(), 'RoadSectionData', 'Revised', 'Revised_' + self.file_name))) as file:
            for row in csv.DictReader(file):
                if row['date'] in self.dict_entire:
                    try:
                        self.dict_entire[row['date']] += int(row['flow31']) + int(row['flow32']) + int(
                            row['flow41']) + int(row['flow42']) + int(row['flow5'])
                    except ValueError as err:
                        print(err)
                        return False
                # Determine the file start day and end day
                if self.file_start_day is None:
                    self.file_start_day = row['date']
                    self.file_end_day = row['date']
                else:
                    self.file_end_day = row['date']
        # Determine the really start day and file miss day
        for idx, row in enumerate(dict.items(self.dict_entire)):
            if row[0] >= self.file_start_day and row[1] != 0 and self.really_start_day is None:
                self.really_start_day = row[0]
                self.really_start_day_index = idx
            elif row[0] >= self.file_start_day and row[1] == 0 and self.really_start_day is not None:
                self.file_miss_day.append(row[0])  # since really_start_day
            # print(row, type(row))
            self.flow_all.append(row[1])
            # print(self.flow_all)
        return True

    def show_plot(self):
        flow_really_all = np.array(self.flow_all[self.really_start_day_index:])
        plt.plot(flow_really_all)
        plt.title(self.road_section_name, fontproperties=font)
        plt.xlabel('day')
        plt.ylabel('flow')
        plt.show()

    def show_plot_hold_on_google_trend(self, google_trend):
        flow_really_all = np.array(self.flow_all[self.really_start_day_index:])
        plt.plot(flow_really_all, label='Traffic flow')
        plt.plot(np.array(google_trend.trend_percentage[self.really_start_day_index:]), label='Google Trend')
        plt.title(self.road_section_name + '\n' + google_trend.target + ' Google搜尋趨勢', fontproperties=font)
        plt.xlabel('day')
        plt.ylabel('flow')
        plt.legend()
        plt.show()

    def revise_header(self):
        with open(str(os.path.join(os.getcwd(), 'RoadSectionData', 'Revised', 'Revised_' + self.file_name)), 'w',
                  newline='') as fixed_file:
            fixed = csv.writer(fixed_file)
            fixed.writerow(
                ['no', 'start', 'end', 'type31', 'travel31', 'flow31', 'type32', 'travel32', 'flow32', 'type41',
                 'travel41', 'flow41', 'type42', 'travel42', 'flow42', 'type5', 'travel5', 'flow5', 'avetime', 'date',
                 'time'])
            with open(self.file_path) as original_file:
                ori = csv.reader(original_file)
                for row in ori:
                    if ori.line_num == 1:
                        continue
                    fixed.writerow(row)

    def show_info(self):
        print('## Road Section Info.')
        print('Road Section Name:', self.road_section_name, end='')
        print('File name        :', self.file_name)
        print('File start day   :', self.file_start_day)
        print('File end day     :', self.file_end_day)
        print('Really start day :', self.really_start_day)
        print('File miss day    :', self.file_miss_day)

    def normalize(self):
        norm = [float(i) / sum(self.flow_all) for i in self.flow_all]
        norm = [float(i) / max(self.flow_all) for i in self.flow_all]
        self.flow_all = norm


# For debug
if __name__ == '__main__':
    import GoogleTrend

    rs = RoadSection('03F2614S-03F2709S.csv')
    rs.load()
    rs.normalize()
    rs.show_info()
    # rs.show_plot()

    gt = GoogleTrend.GoogleTrend('multiTimeline.csv')
    gt.load()
    gt.normalize()
    gt.show_info()
    # print(gt.get_peak_info())

    peak_flow_all = []
    for section in gt.get_peak_info():
        print(section)
        peak_flow = []
        for day in range(section[0], section[1] + 1):
            peak_flow.append(rs.flow_all[day])
        peak_flow_all.append(peak_flow)

    for i in peak_flow_all:
        print(len(i))
        print(i)
