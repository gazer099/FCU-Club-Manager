import datetime as dt

start_day = dt.datetime(2015, 1, 1)
end_day = dt.datetime(2016, 9, 30)

def get_dict_entire():
    dic = {}
    current_day = start_day
    while current_day <= end_day:
        dic[current_day.strftime('%Y/%m/%d')] = 0
        current_day += dt.timedelta(days=1)
    return dic

# print(get_dict_entire())
