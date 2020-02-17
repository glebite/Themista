""" test_themista_creation.py """
import pytest
# TODO: hack solution - need to fix later
import sys
sys.path.append('themista')
from themista.themista import Themista

@pytest.mark.test_id(1)
def test_themista_cration():
    x = Themista()
    assert x is not None
    
@pytest.mark.test_id(2)
def test_themista_repr():
    x = Themista()
    assert x.__repr__() == "<Themista>"

@pytest.mark.test_id(3)
def test_themista_str():
    x = Themista()
    assert x.__str__() == ""

@pytest.mark.test_id(4)
def test_themista_driver_set():
    x = Themista()
    x.initialize_driver()
    assert x.driver is not None
    x.close()
