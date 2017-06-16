import pytest
from DataManager import *


@pytest.mark.skip(reason="The file has been restored after this test PASS")
def test_open_file_fail():
    with pytest.raises(FileNotFoundError):
        DataManager()


def test_search_section_list():
    dm = DataManager()
    assert dm.search_section_list('高公局') == 20
    assert dm.search_section_list('機場') == 25
    assert dm.search_section_list('石碇') == 8
    assert dm.search_section_list('南港') == 16
    assert dm.search_section_list('美國') == 0
    assert dm.search_section_list('日本') == 0


def test_get_road_section_name():
    dm = DataManager()
    assert dm.get_road_section_name('01F0005S-01F0017S.csv') == '01F0005S,(基隆端-基隆),01F0017S,(基隆-八堵),1,S\n'
    assert dm.get_road_section_name('01F0509S-03F0559S.csv') == '01F0509S,(桃園-機場系統),03F0559S,(鶯歌系統-大溪),1,S\n'
    assert dm.get_road_section_name('01F1389N-01F1292N.csv') == '01F1389N,(銅鑼-苗栗),01F1292N,(苗栗-頭屋),1,N\n'
    assert dm.get_road_section_name('01F2483N-03F2709S.csv') == '01F2483N,(大林-雲林系統),03F2709S,(古坑系統-古坑),1,N\n'
    assert dm.get_road_section_name('!#!$@-%$#%$#') is False
    assert dm.get_road_section_name('!#!as-dasf#') is False
    assert dm.get_road_section_name('000000-0000') is False
