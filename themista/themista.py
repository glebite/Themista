"""
themista.py

A test generation helping tool using selenium.
"""
import logging
from selenium import webdriver


LOG = logging.getLogger('uatu')
LOG.setLevel(logging.DEBUG)
FH = logging.FileHandler('uatu.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOG.addHandler(FH)


class Themista:
    """ class definition for the tool """
    def __init__(self):
        """ __init__ goodness - parameters, etc.. """
        pass

    
""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
