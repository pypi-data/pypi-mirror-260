
import pytest
import sys
sys.path.append('/home/ptm/Documents/Python-Projects/burmethon')

from burmethon.g2j import t2d

class TestT2d:

    # Returns a decimal representation of the day for valid input values.
    def test_valid_input(self):
        # Arrange
        hours = 12
        minutes = 30
        seconds = 0
    
        # Act
        result = t2d(hours, minutes, seconds)
    
        # Assert
        assert result == 0.020833333333333332

    # Returns 1 for 24:00:00.
    def test_midnight(self):
        # Arrange
        hours = 24
        minutes = 0
        seconds = 0
    
        # Act
        result = t2d(hours, minutes, seconds)
    
        # Assert
        assert result == 0.5