
import pytest
import sys
sys.path.append('/home/ptm/Documents/Python-Projects/burmethon')

from burmethon.g2j import g2j
class TestG2j:

    # Convert a given date and time in the Gregorian calendar to Julian Day Number (JD) with default values.
    def test_default_values(self):
        assert g2j(2022, 9, 14) == 2459837

    # Convert a given date and time in the Gregorian calendar to Julian Day Number (JD) with year=0.
    def test_year_zero(self):
        assert g2j(0, 9, 14) == 1721315
