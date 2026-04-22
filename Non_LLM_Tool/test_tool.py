# test_tool.py
import pytest
from tool import irrigation_volume

def test_happy_path():
    result = irrigation_volume(1000, 0.8, 4)
    assert result["result"] == 3200
    assert result["unit"] == "liters"

def test_edge_case():
    result = irrigation_volume(1, 0.5, 3)
    assert result["result"] == 1.5
    assert result["unit"] == "liters"

def test_invalid_input_raises():
    with pytest.raises(ValueError):
        irrigation_volume(-1000, 0.3, 4)