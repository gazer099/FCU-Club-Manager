import pytest

from RoadSection import *


def test_load_file():
    rs_01 = RoadSection('00000-00000.csv')
    rs_02 = RoadSection('#####-00000.csv')
    rs_03 = RoadSection('00000------.csv')
    rs_04 = RoadSection('00222222222.csv')
    rs_05 = RoadSection('098898989as.csv')
    assert rs_01.load() is False
    assert rs_02.load() is False
    assert rs_03.load() is False
    assert rs_04.load() is False
    assert rs_05.load() is False


# 預先宣告,等下兩個test要共用
rs_01 = RoadSection('01F0005S-01F0017S.csv')
rs_02 = RoadSection('01F0509S-03F0559S.csv')
rs_03 = RoadSection('01F1389N-01F1292N.csv')
rs_04 = RoadSection('01F2425S-01F2483S.csv')
rs_05 = RoadSection('01F3185N-03F3496S.csv')


@pytest.mark.skip(reason="no way of currently testing this")
def test_load_success():
    assert rs_01.load() is True
    assert rs_02.load() is True
    assert rs_03.load() is True
    assert rs_04.load() is True
    assert rs_05.load() is True


@pytest.mark.skip(reason="no way of currently testing this")
def test_load_data_info():
    assert rs_01.road_section_name == '01F0005S,(基隆端-基隆),01F0017S,(基隆-八堵),1,S\n'
    assert rs_01.file_start_day == '2015/01/01'
    assert rs_01.file_end_day == '2016/09/30'
    assert rs_01.really_start_day == '2015/01/01'
    assert rs_01.file_miss_day == []

    assert rs_02.road_section_name == '01F0509S,(桃園-機場系統),03F0559S,(鶯歌系統-大溪),1,S\n'
    assert rs_02.file_start_day == '2015/01/01'
    assert rs_02.file_end_day == '2016/09/30'
    assert rs_02.really_start_day == '2015/01/01'
    assert rs_02.file_miss_day == []

    assert rs_03.road_section_name == '01F1389N,(銅鑼-苗栗),01F1292N,(苗栗-頭屋),1,N\n'
    assert rs_03.file_start_day == '2015/01/01'
    assert rs_03.file_end_day == '2016/09/30'
    assert rs_03.really_start_day == '2015/01/01'
    assert rs_03.file_miss_day == []


def test_load_data_info_special():
    rs = RoadSection('test_file-01.csv')
    rs.load()
    assert rs.file_start_day == '2015/01/01'
    assert rs.file_end_day == '2015/01/10'
    assert rs.really_start_day == '2015/01/04'
    assert '2015/01/05' in rs.file_miss_day
    assert '2015/01/08' in rs.file_miss_day
    assert '2015/01/10' in rs.file_miss_day
