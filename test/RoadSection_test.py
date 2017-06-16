import pytest

from RoadSection import *


def test_load_fail():
    rs_load_fail_01 = RoadSection('00000-00000.csv')
    rs_load_fail_02 = RoadSection('#####-00000.csv')
    rs_load_fail_03 = RoadSection('00000------.csv')
    rs_load_fail_04 = RoadSection('abcdefghijk.csv')
    assert rs_load_fail_01.load() is False
    assert rs_load_fail_02.load() is False
    assert rs_load_fail_03.load() is False
    assert rs_load_fail_04.load() is False


# 預先宣告,等下兩個test要共用
rs_01 = RoadSection('01F0005S-01F0017S.csv')
rs_02 = RoadSection('01F0509S-03F0559S.csv')
rs_03 = RoadSection('01F1389N-01F1292N.csv')
rs_04 = RoadSection('01F2483N-03F2709S.csv')


# @pytest.mark.skip(reason="this test will take much time")
def test_load_success():
    assert rs_01.load() is True
    assert rs_02.load() is True
    assert rs_03.load() is True
    assert rs_04.load() is True


# @pytest.mark.skip(reason="this test will take much time")
def test_load_data_info():
    rs_01.load()
    rs_02.load()
    rs_03.load()
    rs_04.load()

    assert rs_01.road_section_name == '01F0005S,(基隆端-基隆),01F0017S,(基隆-八堵),1,S\n'
    assert rs_01.file_start_day == '2015/01/01'
    assert rs_01.file_end_day == '2016/09/30'
    assert rs_01.really_start_day == '2015/01/01'

    assert rs_02.road_section_name == '01F0509S,(桃園-機場系統),03F0559S,(鶯歌系統-大溪),1,S\n'
    assert rs_02.file_start_day == '2015/01/01'
    assert rs_02.file_end_day == '2016/09/30'
    assert rs_02.really_start_day == '2015/01/01'

    assert rs_03.road_section_name == '01F1389N,(銅鑼-苗栗),01F1292N,(苗栗-頭屋),1,N\n'
    assert rs_03.file_start_day == '2015/01/01'
    assert rs_03.file_end_day == '2016/09/30'
    assert rs_03.really_start_day == '2015/01/01'

    assert rs_04.road_section_name == '01F2483N,(大林-雲林系統),03F2709S,(古坑系統-古坑),1,N\n'
    assert rs_04.file_start_day == '2015/05/31'
    assert rs_04.file_end_day == '2016/09/30'
    assert rs_04.really_start_day == '2016/02/21'


def test_load_data_info_self_assumed():
    rs_self_assumed_01 = RoadSection('test_file-01.csv')
    rs_self_assumed_01.load()
    assert rs_self_assumed_01.file_start_day == '2015/01/01'
    assert rs_self_assumed_01.file_end_day == '2015/01/10'
    assert rs_self_assumed_01.really_start_day == '2015/01/04'
    assert '2015/01/05' in rs_self_assumed_01.file_miss_day
    assert '2015/01/08' in rs_self_assumed_01.file_miss_day
    assert '2015/01/10' in rs_self_assumed_01.file_miss_day

    rs_self_assumed_02 = RoadSection('test_file-02.csv')
    rs_self_assumed_02.load()
    assert rs_self_assumed_02.file_start_day == '2016/09/15'
    assert rs_self_assumed_02.file_end_day == '2016/09/24'
    assert rs_self_assumed_02.really_start_day == '2016/09/18'
    assert '2016/09/22' in rs_self_assumed_02.file_miss_day
    assert '2016/09/24' in rs_self_assumed_02.file_miss_day


def test_load_data_flow_include_illegal_value():
    rs_include_illegal_value_01 = RoadSection('test_file-03.csv')
    assert rs_include_illegal_value_01.load() is False

    rs_include_illegal_value_02 = RoadSection('test_file-04.csv')
    assert rs_include_illegal_value_02.load() is False
