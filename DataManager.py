import csv


class DataManager:
    section_list = []

    def __init__(self):
        with open('IntervalCodeName.csv') as file:
            for row in file:
                self.section_list.append(row)

    def show_section_list(self):
        for idx, row in enumerate(self.section_list):
            print(idx, row, end='')

    def search_section_list(self, keyword):
        count = 0
        print('對', keyword, '的搜尋結果:')
        for idx, row in enumerate(self.section_list):
            if keyword in row:
                print(idx, row, end='')
                count += 1
        print('共搜尋到', count, '筆資料')


if __name__ == '__main__':
    dm = DataManager()
    dm.show_section_list()
    dm.search_section_list('高公局')
