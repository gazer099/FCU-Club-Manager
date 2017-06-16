import pytest
from GoogleTrend import *


def test_load_fail():
    gt_load_fail_01 = GoogleTrend('00000.csv')
    gt_load_fail_02 = GoogleTrend('#####.csv')
    gt_load_fail_03 = GoogleTrend('00000.csv')
    gt_load_fail_04 = GoogleTrend('abcde.csv')
    assert gt_load_fail_01.load() is False
    assert gt_load_fail_02.load() is False
    assert gt_load_fail_03.load() is False
    assert gt_load_fail_04.load() is False


# 預先宣告,等下兩個test要共用
gt_00 = GoogleTrend('multiTimeline.csv')
gt_01 = GoogleTrend('multiTimeline-01.csv')
gt_02 = GoogleTrend('multiTimeline-02.csv')


def test_load_success():
    assert gt_00.load() is True
    assert gt_01.load() is True
    assert gt_02.load() is True


def test_load_info():
    gt_00.load()
    gt_01.load()
    gt_02.load()

    assert gt_00.category == '所有類別'
    assert gt_00.target == '劍湖山'
    assert gt_00.area == '(全球)\n'
    assert gt_00.trend_start_day == '2016/02/21'
    assert gt_00.trend_end_day == '2016/09/30'

    assert gt_01.category == '所有類別'
    assert gt_01.target == '童玩節'
    assert gt_01.area == '(全球)\n'
    assert gt_01.trend_start_day == '2015/01/04'
    assert gt_01.trend_end_day == '2016/09/25'

    assert gt_02.category == '所有類別'
    assert gt_02.target == '麗寶'
    assert gt_02.area == '(台灣)\n'
    assert gt_02.trend_start_day == '2015/01/04'
    assert gt_02.trend_end_day == '2016/09/25'


def test_load_data_flow_include_illegal_value():
    gt_include_illegal_value_01 = GoogleTrend('multiTimeline-ValueError-01.csv')
    assert gt_include_illegal_value_01.load() is False

    gt_include_illegal_value_02 = GoogleTrend('multiTimeline-ValueError-02.csv')
    assert gt_include_illegal_value_02.load() is False
