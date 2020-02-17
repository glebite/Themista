"""
themista.py

A test generation helping tool using selenium.
"""
import logging
from selenium import webdriver


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
FH = logging.FileHandler('themista.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOG.addHandler(FH)


class Themista:
    """ class definition for the tool """
    def __init__(self):
        """ __init__ goodness - parameters, etc.. """
        LOG.info(f'Initialization of {__name__}')

    def __repr__(self):
        """ __repr___ - method """ 
        return "<Themista>"

    def __str__(self):
        """ __str__ - method"""
        return ""

    
""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    print(access_obj.__repr__())
    print(access_obj.__str__())
