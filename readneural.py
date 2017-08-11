"""
load neural
readneural.py
Created on 2017/07/02
@author ken83715
"""

import csv
import math
import matplotlib.pyplot as plt
import pickle


def verifying(bestneu, datalist, rangelist):
    """
    testing the best neural
    """
    vermse = 0
    count = 0
    result = []

    # maxofdata = 0
    minofdata = 0
    datarange = 0

    # maxofdata = rangelist[0]
    minofdata = rangelist[1]
    datarange = rangelist[2]

    # pick a day
    starttestindex = 288 * 0

    for i in range(283):

        inputlist = []
        expect = 0

        for j in range(bestneu.inputnumber):
            inputlist.append(datalist[starttestindex + i + j])
        expect = datalist[starttestindex + i + bestneu.inputnumber]

        output = bestneu.forward(inputlist)
        result.append(output[0])
        # print('output: ', output)
        vermse = vermse + (expect - output[0]) * (expect - output[0])
        count = count + 1

    vermse = math.sqrt(vermse / count)
    print('verifying mse: ', vermse)

    predictxaxis = [0, 1, 2, 3, 4]
    origyaxis = []
    predictyaxis = []

    for i in range(5):
        origyaxis.append((datalist[starttestindex + i] + 1) / 2 * datarange + minofdata)
        predictyaxis.append((datalist[starttestindex + i] + 1) / 2 * datarange + minofdata)

    for i in range(283):
        predictxaxis.append(i + bestneu.inputnumber)
        origyaxis.append((datalist[starttestindex + i + bestneu.inputnumber] + 1) / 2 * datarange + minofdata)

    for res in result:
        predictyaxis.append((res + 1) / 2 * datarange + minofdata)

    with open('out.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for i in range(len(origyaxis)):
            spamwriter.writerow([origyaxis[i]] + [predictyaxis[i]])
    csvfile.close()

    fig1 = plt.figure('fig1')
    plt.plot(predictxaxis, origyaxis)
    plt.plot(predictxaxis, predictyaxis)

    plt.xlabel("time")
    plt.ylabel("travel time")
    plt.title("predict result")

    plt.show()

    return vermse


def readdata(seg):
    """
    read train data from file
    """
    listoriginal = []
    datalist1 = []
    trainfile = open('E:/PYTHON/project/ETC/cleandata/' + seg + '.csv', 'r')
    for everyrow in csv.DictReader(trainfile):
        listoriginal.append(int(everyrow['avetime']))
    trainfile.close()

    datamax = max(listoriginal)
    datamin = min(listoriginal)
    datarange = datamax - datamin

    for i in listoriginal:
        datalist1.append((i - datamin) / datarange * 2 - 1)

    return datalist1


def maxminrange(seg):
    """
    find range of data
    """
    listoriginal = []
    trainfile = open('E:/PYTHON/project/ETC/cleandata/' + seg + '.csv', 'r')
    for everyrow in csv.DictReader(trainfile):
        listoriginal.append(int(everyrow['avetime']))
    trainfile.close()

    datamax = max(listoriginal)
    datamin = min(listoriginal)
    datarange = datamax - datamin

    maxminandrange = [datamax, datamin, datarange]
    return maxminandrange


def readneu(seg):
    """
    read neu
    """
    fpath = 'E:/PYTHON/project/ETC/NEUDATA/' + seg + '.data'
    fopen = open(fpath, 'rb')
    neutest = pickle.load(fopen)  # load the object from the file
    print(neutest.segment)

    return neutest


seg = '01F3126N-01F3083N-2'

neur = readneu(seg)
data = readdata(seg)
datarange = maxminrange(seg)

vermse = verifying(neur, data, datarange)
