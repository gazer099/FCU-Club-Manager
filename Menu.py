import DataManager
import GoogleTrend
import RoadSection


def logo():
    print('''  ______ ____   ______ _____             ___                   __              __ 
 /_  __// __ \\ / ____// ___/            /   |   ____   ____ _ / /__  __ _____ / /_
  / /  / / / // /     \\__ \\   ______   / /| |  / __ \\ / __ `// // / / // ___// __/
 / /  / /_/ // /___  ___/ /  /_____/  / ___ | / / / // /_/ // // /_/ /(__  )/ /_  
/_/  /_____/ \\____/ /____/           /_/  |_|/_/ /_/ \\__,_//_/ \\__, //____/ \\__/  
     Visualize the data of Traffic Data Collection System     /____/              ''')


def menu():
    print('選單：')
    print('(1) 檢閱與視覺化高速公路路段車流資料')
    print('(2) 檢閱與視覺化Google搜尋趨勢')
    print('(3) 將路段車流資料與Google搜尋趨勢做疊圖分析')
    print('(4) 列出高速公路路段資料清單')
    print('(5) 以關鍵字搜尋路段資料')
    print('(0) 離開')


if __name__ == '__main__':
    while True:
        logo()
        menu()
        option = input('>>> ')
        while option not in ['1', '2', '3', '4', '5', '0']:
            option = input('[Error] 選項輸入錯誤，請重新輸入\n>>> ')

        if option == '1':
            file_name = input('請輸入檔案名稱\n>>> ')
            if file_name[-4:] != '.csv':
                file_name += '.csv'
            # print(file_name)
            rs = RoadSection.RoadSection(file_name)
            if not rs.load():
                input('>>> 請按任意件繼續...')
                continue
            rs.normalize()
            rs.show_info()
            rs.show_plot()
            input('>>> 請按任意件繼續...')

        elif option == '2':
            file_name = input('請輸入檔案名稱\n>>> ')
            if file_name[-4:] != '.csv':
                file_name += '.csv'
            # print(file_name)
            gt = GoogleTrend.GoogleTrend(file_name)
            if not gt.load():
                input('>>> 請按任意件繼續...')
                continue
            gt.normalize()
            gt.show_info()
            gt.show_plot()
            input('>>> 請按任意件繼續...')

        elif option == '3':
            rs_file_name = input('請輸入"路段"檔案名稱\n>>> ')
            if rs_file_name[-4:] != '.csv':
                rs_file_name += '.csv'
            rs = RoadSection.RoadSection(rs_file_name)
            if not rs.load():
                input('>>> 請按任意件繼續...')
                continue
            rs.normalize()

            gt_file_name = input('請輸入"Google搜尋趨勢"檔案名稱\n>>> ')
            if gt_file_name[-4:] != '.csv':
                gt_file_name += '.csv'
            gt = GoogleTrend.GoogleTrend(gt_file_name)
            if not gt.load():
                input('>>> 請按任意件繼續...')
                continue
            gt.normalize()

            if rs.really_start_day_index != gt.trend_start_day_index:
                print('[warning] 兩檔案資料起始時間不一致')
            rs.show_plot_hold_on_google_trend(gt)
            input('>>> 請按任意件繼續...')

        elif option == '4':
            dm = DataManager.DataManager()
            dm.show_section_list()
            input('>>> 請按任意件繼續...')

        elif option == '5':
            keyword = input('請輸入關鍵字\n>>> ')
            dm = DataManager.DataManager()
            dm.search_section_list(keyword)
            input('>>> 請按任意件繼續...')

        elif option == '0':
            exit(0)
