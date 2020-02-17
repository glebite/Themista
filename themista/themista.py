"""
themista.py

A test generation helping tool using selenium.
"""
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


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

    def initialize_driver(self):
        """ """
        self.driver = webdriver.Firefox()
        LOG.debug(f'created self.driver {self.driver}')

    def goto(self, url):
        LOG.info(f'Navigating to {url}')
        self.driver.get(url)
        
    def close(self):
        """ """
        LOG.info(f'closing browser')
        self.driver.close()

    def __repr__(self):
        """ __repr___ - method """ 
        return "<Themista>"

    def __str__(self):
        """ __str__ - method"""
        return ""

    def get_attributes(self, element):
        """ get_attributes """
        return access_obj.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)

    def is_clickable(self, element):
        """ is_clickable """
        return element.is_enabled() and element.is_displayed()
    
""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    access_obj.initialize_driver()
    access_obj.goto('https://python.org')
    elements = access_obj.driver.find_elements_by_css_selector('*')
    counter = 0
    print(dir(elements[0]))
    for element in elements:
        print(element.tag_name, access_obj.is_clickable(element))
        try:
            element.screenshot_as_png(f'/tmp/element-{counter}.png')
            counter += 1
        except: TypeError:
            pass
