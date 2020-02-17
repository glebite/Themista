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
import uuid

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
        self.driver.maximize_window()
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
        LOG.debug('Retrieving attributes for {}'.format(element.tag_name))
        return access_obj.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)

    def is_clickable(self, element):
        """ is_clickable """
        LOG.debug('Checking if {} {} is enabled and displayed'.format(element, element.tag_name))
        return element.is_enabled() and element.is_displayed()

    def capture_element(self, element, name):
        """ capture_element 
        https://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python
        """
        LOG.info('Performing element image capture')
        location = element.location
        size = element.size
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        LOG.debug('Name: {} Image Range: {}'.format( name, (int(left), int(top), int(right), int(bottom))))
        img = img.crop( (int(left), int(top), int(right), int(bottom)))
        img.save(name)
  
""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    access_obj.initialize_driver()
    access_obj.goto('http://the-internet.herokuapp.com/disappearing_elements')
    elements = access_obj.driver.find_elements_by_css_selector('*')
    print("<html><body><table border='1'>")
    for element in elements:
        if element.tag_name in ['html', 'body']:
            continue
        try:
            uuid_value = uuid.uuid1()
            pointer = ActionChains(access_obj.driver)
            pointer.move_to_element(element).perform()
            if access_obj.get_attributes(element) == {}:
                continue
            access_obj.capture_element(element, '/tmp/element-{}.png'.format(uuid_value))
            print('<tr><td>{}</td><td>{}</td><td>{}</td><td><img src="{}" alt="screenshot"></td></tr>'.
                  format(element.tag_name, access_obj.get_attributes(element),
                         access_obj.is_clickable(element), '/tmp/element-{}.png'.format(uuid_value)))
        except TypeError as e:
            LOG.error('Exception encountered (capturing image): {}'.format(e))
        except Exception as f:
            LOG.error('Exception encountered (trying to actionchains): {}'.format(f))
    print("</table></body></html>")
    access_obj.close()
