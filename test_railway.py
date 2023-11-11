import railway as r
import utilities as u
import pytest




def test_crs_len_is_3():
    with pytest.raises(ValueError, match=r"'*' is not a valid CRS code, it must contain 3 characters"):
        _ = r.Station("aaaa bbbb", "aaaa", "ABCD", 1.,1.,0)

 
"""
with pytest.raises(ValueError, match=r'must be \d+$'):
    raise ValueError('value must be 42')

with pytest.raises(ValueError, match='must be 0 or None'):
    raise ValueError('value must be 0 or None')
"""

