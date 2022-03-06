""" test_themista_exeution.py """
import pytest
# TODO: hack solution - need to fix later
import sys
sys.path.append('themista')
from themista.themista import Themista


@pytest.mark.test_id(1)
def test_no_argument():
    try:
        access_obj = Themista()
        access_obj.main()
        assert False
    except IndexError as raised_exception:
        assert True

@pytest.mark.test_id(2)
def test_simple_argument():
    try:
        access_obj = Themista()
        access_obj.main('http://www.practiceselenium.com/')
        assert True
    except Exception as e:
        assert False
