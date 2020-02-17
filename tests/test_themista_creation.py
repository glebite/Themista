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
    
