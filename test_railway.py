import railway as r
import utilities as u
import pytest

#-- raise errors testing ###

#--- Station class 
    #-- __init__() 

        #- names tests
def test_init_name():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,0.,0)
    assert a.name == "aaaa bbbb"

        #- region tests
def test_init_region():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,0.,0)
    assert a.region == "aaaa"

        #- crs tests 
def test_crs_len_is_3():
    with pytest.raises(ValueError, match=r"'*' is not a valid CRS code, it must contain 3 characters"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABCD", 1.,1.,0)
def test_crs_is_upper():
    with pytest.raises(ValueError, match=r"'*' is not a valid CRS code, it must contain only uppercase characters"):
        _ = r.Station("aaaa bbbb", "aaaa", "AbC", 1.,1.,0)
def test_crs_is_alpha():
    with pytest.raises(ValueError, match=r"'*' is not a valid CRS code, it can not contain numeric characters"):
        _ = r.Station("aaaa bbbb", "aaaa", "A2C", 1.,1.,0)
def test_init_crs():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,0.,0)
    assert a.crs == "ABC"

        #- lat test 
def test_lat_is_high():
    with pytest.raises(ValueError, match=r"'*' is not a valid latitude value, it must be between -90 and 90"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 91.,1.,0)
def test_lat_is_low():
    with pytest.raises(ValueError, match=r"'*' is not a valid latitude value, it must be between -90 and 90"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", -91.,1.,0)
def test_init_lat():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 1.,0.,0)
    assert a.lat == 1.

        #- lon test 
def test_lon_is_high():
    with pytest.raises(ValueError, match=r"'*' is not a valid longitude value, it must be between -180 and 180"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,181.,0)
def test_lon_is_low():
    with pytest.raises(ValueError, match=r"'*' is not a valid longitude value, it must be between -180 and 180"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,-181.,0)
def test_init_lon():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,-1.,0)
    assert a.lon == -1

    #-- __str__() and __repr__() 
def test_str():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,-1.,0)
    assert f'{a}' == 'Station(ABC-aaaa bbbb/aaaa)'
def test_str_hub():
    a = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,-1.,1)
    assert f'{a}' == 'Station(ABC-aaaa bbbb/aaaa-hub)'

    #-- distance_to() 
def test_str():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 5.,41.4,0)
    b = r.Station("cccc dddd","aaaa", "ABC", 5.,41.5,0) 
    assert a.distance_to(b) == 11.07717962712117


#--- RailNetwork 
    #-- __init__() 
        #- input_stations test
def test_unique_crs():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "ABC", 1.,1.,0)   
    with pytest.raises(ValueError, match="there are 1 or more duplicate CRS codes in input list, CRS codes are required to be unique"):
        _ = r.RailNetwork([a,b])
def test_railnetwork_stations():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "DEF", 1.,1.,0)   
    railnetwork = r.RailNetwork([a,b])
    assert railnetwork.stations == {'ABC':a,'DEF':b}

    #-- closest_hub() 
def test_closest_hub():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "DEF", 1.,1.,0)
    rn = r.RailNetwork([a])  
    with pytest.raises(ValueError):
        rn.closest_hub(b)
def test_hub_on_region():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "DEF", 1.,1.,0)
    rn = r.RailNetwork([a,b])  
    with pytest.raises(LookupError):
        rn.closest_hub(b)






