"""
themista.py

A test generation helping tool using selenium.
"""
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains

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
        LOG.info('Initialization of {__name__}')

    def initialize_driver(self):
        """ """
        self.driver = webdriver.Firefox()
        LOG.debug('created self.driver {self.driver}')

    def goto(self, url):
        LOG.info('Navigating to {url}')
        self.driver.get(url)
        
    def close(self):
        """ """
        LOG.info('closing browser')
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

    def capture_element(self, element, name):
        """ capture_element 
        https://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python
        """
        location = element.location
        size = element.size
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        img = img.crop((int(left), int(top), int(right), int(bottom)))
        img.save(name)
  
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
            builder = ActionChains(access_obj.driver)
            builder.move_to_element(element).perform()
            access_obj.capture_element(element, '/tmp/element-{}.png'.format(counter))
            counter += 1
            print("Woohoo!")
        except TypeError as e:
            print("Woonoo... {}".format(e))
        except Exception as f:
            print("Shazbot!")
