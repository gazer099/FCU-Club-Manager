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

    def get_road_section_name(self, file_name):
        file_name = file_name.split('-')
        file_name[1] = file_name[1][:-4]
        # print(file_name)
        road_section_name = None
        for row in self.section_list:
            if file_name[0] in row and file_name[1] in row:
                # print(row)
                road_section_name = row
                break
        if road_section_name is not None:
            # print(road_section_name)
            return road_section_name
        else:
            return False

if __name__ == '__main__':
    dm = DataManager()
    dm.show_section_list()
    # dm.search_section_list('高公局')
    dm.get_road_section_name('01F2483N-03F2709S.csv')
