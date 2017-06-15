import RoadSection
import GoogleTrend
import DataManager
import date_dictionary


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
    print('(2) 視覺化Google搜尋趨勢')
    print('(3) 將路段車流資料與Google搜尋趨勢做疊圖分析')
    print('(4) 以關鍵字搜尋路段資料')
    print('(0) 離開')


if __name__ == '__main__':
    logo()
    menu()
    option = input('>>> ')
    while option not in ['1', '2', '3', '4', '0']:
        option = input('[Error]選項輸入錯誤，請重新輸入\n>>> ')
    if option == '1':
        file_name = input('請輸入檔案名稱\n>>> ')
        if file_name[-4:] != '.csv':
            file_name += '.csv'
        # print(file_name)
        rs = RoadSection.RoadSection(file_name)
        rs.load()
        rs.show_info()
        rs.show_plot()
        pass
    elif option == '2':
        pass
    elif option == '3':
        pass
    elif option == '4':
        pass
    elif option == '0':
        exit(0)
