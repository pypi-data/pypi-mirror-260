
import pytest
import sys
sys.path.append('/home/ptm/Documents/Python-Projects/burmethon')

from burmethon.j2g import j2g

class TestJ2g:

    # Should convert a Julian date to Gregorian date and time
    def test_convert_julian_date(self):
        # Arrange
        jd = 2459459.5
        expected_result = {'y': 2021, 'm': 9, 'd': 2, 'h': 0, 'n': 0, 's': 0.0}
    
        # Act
        result = j2g(jd)
    
        # Assert
        assert result == expected_result

    # Should work with a Julian date equal to the start of Gregorian calendar
    def test_convert_start_of_gregorian_calendar(self):
        # Arrange
        jd = 2361222
        expected_result = {'y': 1752, 'm': 9, 'd': 14, 'h': 12, 'n': 0, 's': 0.0}
    
        # Act
        result = j2g(jd)
    
        # Assert
        assert result == expected_result