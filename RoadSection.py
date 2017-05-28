import csv
import numpy as np
import matplotlib.pyplot as plt
import date_dictionary

file_name = '01F2483N-03F2709S.csv'
dict_entire = date_dictionary.get_dict_entire()
flow_all = []


def fix_header():
    with open('Fixed_01F2483N-03F2709S.csv', 'w', newline='') as fixed_file:
        fixed = csv.writer(fixed_file)
        fixed.writerow(['no','start','end','type31','travel31','flow31','type32','travel32','flow32','type41','travel41','flow41','type42','travel42','flow42','type5','travel5','flow5','avetime','date','time'])
        with open('01F2483N-03F2709S.csv') as original_file:
            ori = csv.reader(original_file)
            for row in ori:
                if ori.line_num == 1:
                    continue
                fixed.writerow(row)

fix_header()

with open('Fixed_01F2483N-03F2709S.csv') as file:
    for row in csv.DictReader(file):
        if row['date'] in dict_entire:
            dict_entire[row['date']] += int(row['flow31'])+int(row['flow32'])+int(row['flow41'])+int(row['flow42'])+int(row['flow5'])

for row in dict.items(dict_entire):
    print(row, type(row))
    flow_all.append(row[1])
print(flow_all)

flow_all = np.array(flow_all)
plt.plot(flow_all)
plt.show()
