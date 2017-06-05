import csv
import numpy as np
import matplotlib.pyplot as plt
import date_dictionary

from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\Fonts\SimSun.ttc", size=12)


class RoadSection:
    file_name = None
    file_start_day = None
    file_end_day = None
    file_miss_day = []
    dict_entire = date_dictionary.get_dict_entire()
    flow_all = []

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        self.fix_header()
        with open('Fixed_' + self.file_name) as file:
            for row in csv.DictReader(file):
                if row['date'] in self.dict_entire:
                    self.dict_entire[row['date']] += int(row['flow31']) + int(row['flow32']) + int(row['flow41']) + int(
                        row['flow42']) + int(row['flow5'])

                if self.file_start_day is None:
                    self.file_start_day = row['date']
                    self.file_end_day = row['date']
                else:
                    self.file_end_day = row['date']

        for row in dict.items(self.dict_entire):
            if row[0] >= self.file_start_day and row[1] == 0:
                self.file_miss_day.append(row[0])
            print(row, type(row))
            self.flow_all.append(row[1])
        print(self.flow_all)

    def show_plot(self):
        self.flow_all = np.array(self.flow_all)
        plt.plot(self.flow_all)
        plt.title(self.file_name, fontproperties=font)
        plt.xlabel('day')
        plt.ylabel('flow')
        plt.show()

    def fix_header(self):
        with open('Fixed_' + self.file_name, 'w', newline='') as fixed_file:
            fixed = csv.writer(fixed_file)
            fixed.writerow(
                ['no', 'start', 'end', 'type31', 'travel31', 'flow31', 'type32', 'travel32', 'flow32', 'type41',
                 'travel41', 'flow41', 'type42', 'travel42', 'flow42', 'type5', 'travel5', 'flow5', 'avetime', 'date',
                 'time'])
            with open(self.file_name) as original_file:
                ori = csv.reader(original_file)
                for row in ori:
                    if ori.line_num == 1:
                        continue
                    fixed.writerow(row)

    def show_info(self):
        print('## Road Section Info.')
        print('File name:', self.file_name)
        print('File start day:', self.file_start_day)
        print('File end day:', self.file_end_day)
        print('File miss day:', self.file_miss_day)


if __name__ == '__main__':
    rs = RoadSection('01F2483N-03F2709S.csv')
    rs.load()
    rs.show_plot()
    rs.show_info()
