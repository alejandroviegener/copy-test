from muttlib import utils
import datetime
import pytest
from collections import OrderedDict, namedtuple, deque
import pandas as pd
import numpy as np
import tempfile
import pandas as pd

def test_str_to_datetime():
    #Testing all posible datetime formats and the exception for wrong format
    assert utils.str_to_datetime('2019-10-25 18:35:22') == datetime.datetime(2019, 10, 25, 18, 35, 22)
    assert utils.str_to_datetime('2019-10-25') == datetime.datetime(2019, 10, 25, 0, 0)
    assert utils.str_to_datetime('2019-10-25 18:35:22.000333') == datetime.datetime(2019, 10, 25, 18, 35, 22, 333)
    assert utils.str_to_datetime('18:35:22.000333') == datetime.datetime(1900, 1, 1, 18, 35, 22, 333)
    assert utils.str_to_datetime('18:35:22') == datetime.datetime(1900, 1, 1, 18, 35, 22)
    assert utils.str_to_datetime('20191025T18:35:22') == datetime.datetime(2019, 10, 25, 18, 35, 22)
    assert utils.str_to_datetime('2019-10-25T18:35:22') == datetime.datetime(2019, 10, 25, 18, 35, 22)
    assert utils.str_to_datetime('20191025') == datetime.datetime(2019, 10, 25, 0, 0)
    assert utils.str_to_datetime('2019-10-25T18') == datetime.datetime(2019, 10, 25, 18, 0)
    assert utils.str_to_datetime('201910') == datetime.datetime(2019, 10, 1, 0, 0)
    with pytest.raises(ValueError):
        utils.str_to_datetime("25/10/2019")

def test_dict_to_namedtuple():
    tuple_1 = namedtuple('pepe','don_jose') ('paso por mi casa') 
    tuple_2 = utils.dict_to_namedtuple('pepe',{'don_jose': 'paso por mi casa'})
    assert tuple_1 == tuple_2

def test_create_dict_id():
    assert '67fe8ab7b5' == utils.create_dict_id({'don_jose': 'paso por mi casa'})

def test_get_ordered_factor_levels():
    data = {'B': [25, 94, 57, 62, 70]}
    df = pd.DataFrame(data, columns = ['B'])
    df2 = utils.get_ordered_factor_levels(df,'B')
    assert np.array_equal(np.array([70, 94, 62, 25, 57]),df2[0])
    assert 5 == df2[1]

def test_query_yes_no(monkeypatch):
    #Testing the possible defaults and rewriting the input for the valid or invalid inputs
    og = utils.__builtins__["input"]
    with pytest.raises(ValueError):
        utils.query_yes_no("hit or miss?", 's')
    utils.__builtins__["input"] = lambda: ''
    assert False == utils.query_yes_no("hit or miss?")
    utils.__builtins__["input"] = lambda: ''
    assert True == utils.query_yes_no("hit or miss?",'yes')
    utils.__builtins__["input"] = lambda: 'yes'
    assert True == utils.query_yes_no("hit or miss?")
    utils.__builtins__["input"] = lambda: 'y'
    assert True == utils.query_yes_no("hit or miss?")
    utils.__builtins__["input"] = lambda: 'ye'
    assert True == utils.query_yes_no("hit or miss?")
    utils.__builtins__["input"] = lambda: 'no'
    assert False == utils.query_yes_no("hit or miss?")
    utils.__builtins__["input"] = lambda: 'n'
    assert False == utils.query_yes_no("hit or miss?")

    #[TODO]Validate the while. Need to rewrite this shit to rise an exception but idk shit
    #utils.sys.stdout["write"] = raise Exception('shit happended')    

    utils.__builtins__["input"] = og

def test_path_or_string():
    #generate a tmp file for this test
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b'True')
        fp.seek(0)
        assert 'True' == utils.path_or_string(fp.name)
    assert 'True' == utils.path_or_string('True')

def test_hash_str():
    assert '0c5024ed' == utils.hash_str("hit or miss")

def test_deque_to_geo_hierarchy_dict():
    #Testing the creation of the orderedDict for the 4 levels
    lst = [{'level': 'National', 'select_clause': '', 'group_clause': ''}, 
           {'level': 'Provincial', 'select_clause': "existence is pain", 'post_join_select': 'province_name,', 'group_clause': '1,'},
           {'level': 'Departamental', 'select_clause': "existence is pain", 'post_join_select': 'departament_name,', 'group_clause': '2,'},
           {'level': 'Local', 'select_clause': ("existence is pain",), 'post_join_select': 'locality_name,', 'group_clause': '3,'},
          ]
    deque_lst = deque(lst)
    
    orde = OrderedDict([('National', {'select_clause': '', 'group_clause': ''})])
    assert orde == utils.deque_to_geo_hierarchy_dict(deque_lst,'National')

    orde = OrderedDict([('National', {'select_clause': '', 'group_clause': ''}), 
                 ('Provincial', {'select_clause': "existence is pain", 'post_join_select': 'province_name,', 'group_clause': '1,'})])
    assert orde == utils.deque_to_geo_hierarchy_dict(deque_lst,'Provincial')

    orde = OrderedDict([('National', {'select_clause': '', 'group_clause': ''}), 
                        ('Provincial', {'select_clause': "existence is pain", 'post_join_select': 'province_name,', 'group_clause': '1,'}), 
                        ('Departamental', {'select_clause': "existence is pain", 'post_join_select': 'departament_name,', 'group_clause': '2,'})])
    assert orde == utils.deque_to_geo_hierarchy_dict(deque_lst,'Departamental')

    orde = OrderedDict([('National', {'select_clause': '', 'group_clause': ''}), 
                        ('Provincial', {'select_clause': "existence is pain", 'post_join_select': 'province_name,', 'group_clause': '1,'}), 
                        ('Departamental', {'select_clause': "existence is pain", 'post_join_select': 'departament_name,', 'group_clause': '2,'}), 
                        ('Local', {'select_clause': ("existence is pain",), 'post_join_select': 'locality_name,', 'group_clause': '3,'})])
    assert orde == utils.deque_to_geo_hierarchy_dict(deque_lst,'Local')

def test_read_yaml():
    #generate a tmp file for this test
    lst_test = ['meme', 'clap', 'review', 'clap']
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b"""
                - meme
                - clap
                - review
                - clap
             """)
        fp.seek(0)
        assert lst_test == utils.read_yaml(fp.name)
    pass

def test_get_fathers_mothers_kids_day():
    dates = (pd.Timestamp('2019-06-16', freq='W-SUN'),
             pd.Timestamp('2019-10-20', freq='W-SUN'),
             pd.Timestamp('2019-08-18', freq='W-SUN'),
            )
    assert dates == utils.get_fathers_mothers_kids_day(2019)

def test_is_special_day():
    # Testing ds as date and string.
    ds = datetime.datetime(2018, 1, 18)
    timestamps_inclause = (pd.Timestamp('2018-06-17 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-10-21 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-08-19 00:00:00', freq='W-SUN'))

    res = utils.is_special_day(ds,
                               timestamps_inclause = timestamps_inclause)
    
    assert 0 == res

    ds = datetime.datetime(2018, 6, 17)
    timestamps_inclause = (pd.Timestamp('2018-06-17 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-10-21 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-08-19 00:00:00', freq='W-SUN'))

    res = utils.is_special_day(ds,
                               timestamps_inclause = timestamps_inclause)
    
    assert 1 == res
    # Testing if is in 'feriadous' lst or not
    # Testing ds as date and string.
    ds = "2018-01-18"
    timestamps_inclause = (pd.Timestamp('2018-06-17 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-10-21 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-08-19 00:00:00', freq='W-SUN'))

    res = utils.is_special_day(ds,
                               timestamps_inclause = timestamps_inclause)
    
    assert 0 == res

    ds = "2018-06-17"
    timestamps_inclause = (pd.Timestamp('2018-06-17 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-10-21 00:00:00', freq='W-SUN'), 
                           pd.Timestamp('2018-08-19 00:00:00', freq='W-SUN'))

    res = utils.is_special_day(ds,
                               timestamps_inclause = timestamps_inclause)
    
    assert 1 == res

def test_get_friends_day():
    # just pass a year(int) and gives you the "amigos's day
    assert datetime.datetime(2018, 7, 20) == utils.get_friends_day(2018)

def test_get_semi_month_pay_days():
    dates = [pd.Timestamp('2018-02-16 00:00:00'), 
             pd.Timestamp('2018-03-02 00:00:00'), 
             pd.Timestamp('2018-03-16 00:00:00'), 
             pd.Timestamp('2018-03-30 00:00:00')]

    assert dates == utils.get_semi_month_pay_days('2018-01-01','2018-02-28')

#[TODO] Need to make special shit for this ones
def test_make_dirs():
    #Need to make a test folder
    pass
def test_non_empty_dirs():
    #Need to make a test folder
    pass
def test_template():
    #Need to make test template n' shit
    pass
def test_render_jinja_template():
    #utils.render_jinja_template()
    pass