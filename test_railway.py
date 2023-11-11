import railway as r
import utilities as u
import pytest

#-- raise errors testing ###

#--- Station class 
    #-- __init__() 
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

        #- lat test 
def test_lat_is_high():
    with pytest.raises(ValueError, match=r"'*' is not a valid latitude value, it must be between -90 and 90"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 91.,1.,0)
def test_lat_is_low():
    with pytest.raises(ValueError, match=r"'*' is not a valid latitude value, it must be between -90 and 90"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", -91.,1.,0)
   
        #- lon test 
def test_lon_is_high():
    with pytest.raises(ValueError, match=r"'*' is not a valid longitude value, it must be between -180 and 180"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,181.,0)
def test_lon_is_low():
    with pytest.raises(ValueError, match=r"'*' is not a valid longitude value, it must be between -180 and 180"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABC", 0.,-181.,0)

#--- RailNetwork 
    #-- __init__() 
        #- input_stations test
def test_unique_crs():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "ABC", 1.,1.,0)   
    with pytest.raises(ValueError, match="there are 1 or more duplicate CRS codes in input list, CRS codes are required to be unique"):
        _ = r.RailNetwork([a,b])

    #-- closest_hub() 
def test_closest_hub():
    a = r.Station("aaaa bbbb","aaaa", "ABC", 1.,1.,0)
    b = r.Station("cccc dddd","aaaa", "DEF", 1.,1.,0)
    rn = r.RailNetwork([a])  
    with pytest.raises(ValueError, match=r"station * is not on this network"):
        rn.closest_hub(b)




"""

raise ValueError(f"there are 1 or more duplicate CRS codes in input list, CRS codes are required to be unique")
raise ValueError(f'station {s.crs} is not on this network')
raise LookupError('No hubs exist in this region')


with pytest.raises(ValueError, match=r'must be \d+$'):
    raise ValueError('value must be 42')

with pytest.raises(ValueError, match='must be 0 or None'):
    raise ValueError('value must be 0 or None')
"""

