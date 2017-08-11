"""
Hammerstein Recurrent Neural Network
main.py
Created on 2017/04/23
@author ken83715
"""

import csv
import math
from multiprocessing import Pool
import matplotlib.pyplot as plt

import neural

SEGLIST = []


def testing(neutest, datalist):
    """
    testing the trained neural
    """
    mse = 0
    count = 0
    for i in range(len(datalist) - neutest.inputnumber):

        inputlist = []
        expect = 0

        for j in range(neutest.inputnumber):
            inputlist.append(datalist[i + j])
        expect = datalist[i + neutest.inputnumber]

        result = neutest.forward(inputlist)
        # print(result)
        mse = mse + (expect - result[0]) * (expect - result[0])
        count = count + 1

    mse = math.sqrt(mse / count)
    neutest.mse = mse
    print('mse: ', mse)
    return mse


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
    print('best mse: ', bestneu.mse)
    print('verifying mse: ', vermse)

    msexaxis = []
    mseyaxis = []
    for i in range(bestneu.count):
        msexaxis.append(i)
    for j in range(len(bestneu.training_MSE[0])):
        mseyaxis.append(bestneu.training_MSE[0][j])

    fig1 = plt.figure('fig1')
    plt.plot(msexaxis, mseyaxis)

    plt.xlabel("train count")
    plt.ylabel("MSE")
    plt.title("MSE")

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

    fig2 = plt.figure('fig2')
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
    trainfile = open('E:/大型資料/TDCS/M04A/TDCSDIVIDEBYSEGSMOOTHDAY/' + seg + '.csv', 'r')
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
    trainfile = open('E:/大型資料/TDCS/M04A/TDCSDIVIDEBYSEGSMOOTHDAY/' + seg + '.csv', 'r')
    for everyrow in csv.DictReader(trainfile):
        listoriginal.append(int(everyrow['avetime']))
    trainfile.close()

    datamax = max(listoriginal)
    datamin = min(listoriginal)
    datarange = datamax - datamin

    maxminandrange = [datamax, datamin, datarange]
    return maxminandrange


def multitraining(seg, daynum, datalist):
    """
    multi-core training
    """
    neutest = neural.Neu(seg, daynum)

    trainfinished = False
    while trainfinished != True:
        try:
            for i in range(neutest.epoch):
                # print(i + 1)
                # count = 0
                for j in range(len(datalist) - neutest.inputnumber):
                    # print('j: ', j)
                    inputlist = []
                    expect = []

                    for k in range(neutest.inputnumber):
                        inputlist.append(datalist[j + k])

                    expect.append(datalist[j + neutest.inputnumber])

                    # print('input: ', inputlist)
                    # print('expect: ', expect)

                    result = neutest.forward(inputlist)
                    # print('result: ', result)
                    neutest.backward(expect)
                    # print(count)
                    # count = count + 1
                    # if count == 288:
                    #     count = 0
                neutest.cleartemporalepoch()
        except OverflowError:
            neutest = neural.Neu(seg, daynum)
            print('math error')
        else:
            trainfinished = True

    return neutest


def neutraining(seg, daynum):
    """
    training the neural, fordward & backward
    """
    datalist = readdata(seg + '-' + daynum)
    rangelist = maxminrange(seg + '-' + daynum)

    bestneu = neural.Neu(seg, daynum)
    bestmse = 1000000000000000
    trainingtime = 10

    templist = []
    results = []
    proc = Pool(5)

    for train in range(trainingtime):
        print('neural: ', train + 1)
        templist.append(proc.apply_async(multitraining, (seg, daynum, datalist)))

    for res in templist:
        results.append(res.get())

    proc.close()

    for neutest in results:
        mse = testing(neutest, datalist)
        if mse < bestmse:
            bestmse = mse
            bestneu = neutest

    # bestneu.saveneu()
    verifymse = verifying(bestneu, datalist, rangelist)


def segtraining(seg):
    """
    training this segment, generate 7 neural for 7 day
    """
    neutraining(seg, '0')
    # neutraining(seg, '1')
    # neutraining(seg, '2')
    # neutraining(seg, '3')
    # neutraining(seg, '4')
    # neutraining(seg, '5')
    # neutraining(seg, '6')


FILEOPEN = open('E:/大型資料/TDCS/IntervalCodeName.csv', 'r')
for row in csv.DictReader(FILEOPEN):
    SEGLIST.append(row['start'] + '-' + row['end'])
FILEOPEN.close()

if __name__ == '__main__':
    # for i in range(len(SEGLIST)):
    #     segtraining(SEGLIST[i])

    segtraining('01F1664N-01F1621N')
