import logging
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
import uuid
import sys

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
FH = logging.FileHandler('themista.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(filename)s %(lineno)d %(levelname)s'
                              ' - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOG.addHandler(FH)


class Themista:
    """ class definition for the tool """
    def __init__(self):
        """ __init__ goodness - parameters, etc.. """
        LOG.info('Initialization of {}.'.format(__name__))
        self.driver = None
        self.prev_visited = dict()

    def initialize_driver(self, driver=None):
        """ initialize_driver """
        if not driver:
            self.driver = webdriver.Firefox()
            LOG.debug('Created self.driver {self.driver}')
        else:
            self.driver = driver
            LOG.debug("Using an already instantiated driver.")

    def goto(self, url):
        """ goto """
        self.url = url        
        LOG.info('Navigating to {self.url}')
        self.driver.maximize_window()
        self.driver.get(self.url)

    def close(self):
        """ close """
        LOG.info('closing browser')
        self.driver.close()

    def __repr__(self):
        """ __repr___ - method """
        return "<Themista>"

    def __str__(self):
        """ __str__ - method"""
        return "driver: {}".format(self.driver)

    def get_attributes(self, element):
        """ get_attributes """
        LOG.debug('Retrieving attributes for {}'.format(element.tag_name))
        return self.driver.execute_script(
            'var items = {}; for (index = 0; index < arguments[0]'
            '.attributes.length; ++index)'
            '{ items[arguments[0].attributes[index].name]'
            ' = arguments[0].attributes[index].value };'
            'return items;', element)

    def main(self, url=None, file_name=None):
        """ main """

        if url is None:
            raise IndexError
        self.initialize_driver()
        self.goto(url)
        elements = self.driver.find_elements_by_css_selector('*')

        for element in elements:
            """ html and body are big images - no need to waste space """
            if element.tag_name in ['html', 'body']:
                continue
            if self.is_clickable(element):
                print(element)
        self.close()

    def is_clickable(self, element):
        """ is_clickable """
        LOG.debug('Checking if {} {} is enabled and displayed'.
                  format(element, element.tag_name))
        return element.is_enabled() and element.is_displayed()
        # el = WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.TAG_NAME, element.tag_name)))
        # if el:
        #     return True
        # else:
        #     return False


""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    access_obj.main(sys.argv[1], 'output.html')
