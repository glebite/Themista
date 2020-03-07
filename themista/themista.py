"""
themista.py

A test generation helping tool using selenium.
"""
import logging
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
import uuid
import sys

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
        LOG.info('Initialization of {}.'.format(__name__))
        self.driver = None

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
        LOG.info('Navigating to {url}')
        self.driver.maximize_window()
        self.driver.get(url)
        
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
            'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index)'
            '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value };'
            'return items;', element)

    def is_clickable(self, element):
        """ is_clickable """
        LOG.debug('Checking if {} {} is enabled and displayed'.format(element, element.tag_name))
        return element.is_enabled() and element.is_displayed()

    def generate_xpath(self, tag_name, attributes):
        """ generate xpaths based on a tag_name and attributes

        Keyword arguments:
        tag_name   -- the tag (such as id, div, span, ...)
        attributes -- a list of attributes for the tag and create <ul>...</ul> string
        """
        xpaths_plural = "<ul>"
        for key in attributes.keys():
            xpaths_plural +=  "<li>.//{}[contains(@{}, '{}')]</li>".format(tag_name, key, attributes[key])
        xpaths_plural += "</ul>"
        return xpaths_plural
            
    
    def capture_element(self, element, name):
        """ capture image of the element that is pointed to.

        https://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python

        Keyword arguments:
        elemnt -- the element to retriee the image of 
        name   -- the name of the file to write to
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

    def point_retrieve_and_write(self, element, file_pointer):
            try:
                uuid_value = uuid.uuid1()
                pointer = ActionChains(self.driver)
                pointer.move_to_element(element).perform()
                if self.get_attributes(element) == {}:
                    return
                self.capture_element(element, '/tmp/element-{}.png'.format(uuid_value))
                output_string = '<tr><td>{}</td><td>{}</td><td><img src="{}" alt="screenshot"></td></tr>'.format(element.tag_name,
                                self.generate_xpath(element.tag_name,
                                self.get_attributes(element)),
                                '/tmp/element-{}.png'.format(uuid_value))
                if file_pointer:
                    file_pointer.write(output_string)
                else:
                    print(output_string)
            except TypeError as e:
                LOG.error('Exception encountered (capturing image): {}'.format(e))
            except Exception as f:
                LOG.error('Exception encountered (trying to actionchains): {}'.format(f)) 
        
    def main(self, url=None, file_name=None):
        """ main """
        
        if url == None:
            raise IndexError
        self.initialize_driver()
        self.goto(url)
        elements = self.driver.find_elements_by_css_selector('*')
        if file_name:
            file_pointer = open(file_name, 'r')
            file_pointer.write("<html><body><table border='1'>")
        else:
            file_pointer = None
            print("<html><body><table border='1'>")
        for element in elements:
            """ html and body are big images - no need to waste space """
            if element.tag_name in ['html', 'body']:
                continue
            self.point_retrieve_and_write(element, file_pointer)
        if file_name:
            file_pointer.write("</table></body></html>")
            file_pointer.close()
        else:            
            print("</table></body></html>")
        self.close()
    
        
""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    access_obj.main(sys.argv[1])
