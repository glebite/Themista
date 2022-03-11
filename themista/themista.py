"""
themista.py

A test generation helping tool using selenium.
"""

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

    def is_clickable(self, element):
        """ is_clickable """
        LOG.debug('Checking if {} {} is enabled and displayed'.
                  format(element, element.tag_name))
        # return element.is_enabled() and element.is_displayed()
        el = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, element.tag_name)))
        if el:
            return True
        else:
            return False

    def generate_xpath(self, tag_name, attributes):
        """ generate xpaths based on a tag_name and attributes

        Keyword arguments:
        tag_name   -- the tag (such as id, div, span, ...)
        attributes -- a list of attributes for the tag and create <ul>...</ul>
        """
        xpaths_plural = "<ul>"
        for key in attributes.keys():
            xpaths_plural += "<li>.//{}[contains(@{}, '{}')]</li>".format(
                tag_name, key, attributes[key])
        xpaths_plural += "</ul>"
        return xpaths_plural

    def capture_element(self, element, name):
        """ capture image of the element that is pointed to.

        https://stackoverflow.com/questions/15018372/
        how-to-take-partial-screenshot-with-selenium-webdriver-in-python

        Keyword arguments:
        elemnt -- the element to retriee the image of
        name   -- the name of the file to write to
        """
        LOG.info(f'Performing element image capture {element}')
        location = element.location
        size = element.size
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        LOG.debug('Name: {} Image Range: {}'.format(name,
                                                    (int(left),
                                                     int(top),
                                                     int(right),
                                                     int(bottom))))
        img = img.crop((int(left), int(top), int(right), int(bottom)))
        try:
            img.save(name)
        except SystemError as e:
            LOG.error(e)
        return name

    def point_retrieve_and_write(self, element, file_pointer):
        """ point_retrieve_and_write a"""
        print(element.tag_name, type(element))

        if element.tag_name in ['script', 'meta', 'link']:
            return
        
        uuid_value = uuid.uuid1()
        pointer = ActionChains(self.driver)
        pointer.move_to_element(element).perform()

        if self.get_attributes(element) == {}:
            return
        file_name = f'/tmp/element-{uuid_value}.png'
        self.capture_element(element, file_name)
        temp = '<tr><td>{}'.format(element.tag_name)
        attr = self.generate_xpath(element.tag_name,
                                   self.get_attributes(element))
        temp += f'</td><td>{attr}'
        LOG.info(f'Type of element: {type(element)} value: {element}')
        temp += f'</td><td><img src="{file_name}" alt="screenshot"></td></tr>'

        output_string = temp
        try:
            LOG.debug(output_string)
            if file_pointer:
                file_pointer.write(output_string)
            else:
                print(output_string)
        except TypeError as e:
            LOG.error('Exception encountered (capturing image): {}'.format(e))
        except Exception as f:
            LOG.error('Exception encountered (trying to actionchains): {}'.
                      format(f))

    def explore(self):
        if self.url is None:
            raise IndexError

        elements = self.driver.find_elements_by_css_selector('*')
        for element in elements:
            try:
                check_button_link = element.tag_name in ['button', 'a']
                check_text_link = element.tag_name in ['input', 'textarea']
                check_a_link = (element.tag_name == 'a')
                LOG.debug(f'{element} -> {check_button_link}'
                          f' {check_text_link} {check_a_link}')
            except Exception as e:
                print(f"Hmmmm - caught {e}")
            if check_button_link:
                if check_a_link:
                    href = element.get_attribute('href')
                    if not href:
                        continue
                    if self.url not in href:
                        LOG.debug("Sorry - not navigating offsite: {href}")
                    else:
                        text = element.text
                        self.driver.refresh()
                        try:
                            LOG.debug(
                                f"Navigating to: {text} {element.tag_name} {href}")
                            element.click()
                        except Exception as e:
                            LOG.debug(f"Next situation {e}")

            elif check_text_link:
                LOG.debug("-> {}".format(element.get_attribute('name')))

        self.close()

    def insertion(self, file_name=None):
        """ insertion for live use with ipython session... """
        elements = self.driver.find_elements_by_css_selector('*')
        if file_name:
            file_pointer = open(file_name, 'r')
            file_pointer.write("<html><body><table border='1'>")
        else:
            file_pointer = None
            LOG.debug("<html><body><table border='1'>")
        for element in elements:
            """ html and body are big images - no need to waste space """
            if element.tag_name in ['html', 'body']:
                continue
            if self.is_clickable(element):
                self.point_retrieve_and_write(element, file_pointer)
        if file_name:
            file_pointer.write("</table></body></html>")
            file_pointer.close()
        else:
            LOG.debug("</table></body></html>")
        self.close()

    def main(self, url=None, file_name=None):
        """ main """

        if url is None:
            raise IndexError
        self.initialize_driver()
        self.goto(url)
        elements = self.driver.find_elements_by_css_selector('*')
        if file_name:
            file_pointer = open(file_name, 'w')
            file_pointer.write("<html><body><table border='1'>")
        else:
            file_pointer = None
            LOG.debug("<html><body><table border='1'>")
        for element in elements:
            """ html and body are big images - no need to waste space """
            if element.tag_name in ['html', 'body', 'head', 'title', 'p', 'style']:
                continue
            if self.is_clickable(element):
                self.point_retrieve_and_write(element, file_pointer)
        if file_name:
            file_pointer.write("</table></body></html>")
            file_pointer.close()
        else:
            LOG.debug("</table></body></html>")
        self.close()


""" main dunder goodness """
if __name__ == "__main__":
    access_obj = Themista()
    access_obj.main(sys.argv[1], 'output.html')
