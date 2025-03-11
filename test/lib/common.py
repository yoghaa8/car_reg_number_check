import re
import logging
from selenium.common import TimeoutException, NoSuchElementException
from lib.driver import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class NoSuchActionExist(Exception):
    pass

class Locator:
    def __init__(self, l_type, selector):
        self.l_type = l_type
        self.selector = selector

class Common(Driver):
    def __init__(self, context):
        Driver.__init__(self, context.driver)

    def _execute_with_wait(self, condition):
        return WebDriverWait(self.driver, 60).until(condition)

    def element_exists(self, locator):
        try:
            self._execute_with_wait(
                EC.presence_of_element_located(
                    (locator.l_type, locator.selector)))
            return True
        except TimeoutException:
            return False

    def get_element(self, locator, text=""):
        if not self.element_exists(locator):
            raise NoSuchElementException("Could not find ->" + locator.selector)
        return self.driver.find_element(locator.l_type, locator.selector)

    def find_element(self, locator):
        return self.driver.find_element(locator.l_type, locator.selector)

    def navigate_to_url(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def read_input_file(self, context):
        with open(context.config.userdata["input_file"],'r') as fp:
            # read all lines using readline()
            reg_num = []
            lines = fp.readlines()
            for row in lines:
                # check if string present on a current line
                search_word_1 = 'registration '
                search_word_2 = 'registrations'
                # find() method returns -1 if the value is not found,
                words = row.split()
                if row.find(search_word_1) != -1:
                    ix = words.index('registration')
                    if len(words[ix + 1]) == 4:
                        reg_num.append(words[ix + 1] + words[ix + 2])
                    else:
                        reg_num.append(words[ix + 1])
                elif row.find(search_word_2) != -1:
                    reg_numbers = words[words.index('registrations'): words.index('and')]
                    reg_numbers = reg_numbers[1:]
                    for index, val in enumerate(reg_numbers):
                        if len(val) <= 4:
                            reg_num.append(reg_numbers[index] + reg_numbers[index + 1])
                        else:
                            reg_num.append(reg_numbers[index])
                    idx = words.index('and')
                    if len(words[idx + 1]) <= 4:
                        reg_num.append(words[idx + 1] + words[idx + 2])
                    else:
                        reg_num.append(words[idx + 1])
                reg_num = [re.sub(r"[^a-zA-Z0-9]", "", val) for val in reg_num]
                logging.info("The car_reg_numbers are %s" %reg_num)
        fp.close()
        return reg_num

    def read_output_file_and_match(self, context, car_reg):
        with open(context.config.userdata["output_file"],'r') as fp:
            # read all lines using readline()
            lines = fp.readlines()
            lines.pop(0)
            for row in lines:
                words = row.split(",")
                words[0] = (words[0].replace(' ', ''))
                words = list(map(str.strip, words))
                if car_reg in words:
                    logging.info("match found")
                    break
                else:
                    logging.info("no match")
        fp.close()
        return words

    def read_website_car_info(self, info, car_reg):
        car_website_details = [car_reg]
        info = info.split()
        search_word1 = "Make"
        search_word2 = "Model"
        search_word3 = "manufacture"
        if search_word1 in info:
            ix1 = info.index('Make')
            car_website_details.append(info[ix1+1])
        if search_word2 in info:
            model = info[info.index('Model'): info.index('Colour')]
            model = model[1:]
            car_website_details.append((' '.join(model)))
        if search_word3 in info:
            ix3 = info.index('manufacture')
            car_website_details.append(info[ix3+1])
        logging.info("The car details from website %s" %car_website_details)
        return car_website_details

    def perform_action_on_element(self, locator_obj: str, action: str, text=""):
        try:
            action = action.lower()
            if action == "click":
                self.get_element(locator_obj).click()
            elif action == "text":
                element = self.get_element(locator_obj)
                return element.text
            elif action == "type":
                self.get_element(locator_obj).send_keys(text)
            elif action == "present":
                return self.get_element(locator_obj).is_displayed()
            else:
                raise NoSuchActionExist(action)
        except:
            logging.info(action + " on " + locator_obj.selector + " is not working")
            assert False, action + " on " + locator_obj.selector + " is failing"
