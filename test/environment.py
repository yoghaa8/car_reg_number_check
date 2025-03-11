from lib.driver import Driver
from lib.common import Common
from selenium import webdriver
import logging
class SeleniumDriverNotFound(Exception):
    pass


def before_all(context):
    if context.config.userdata["browser"] == "chrome":
        from selenium.webdriver.chrome.options import Options
        chrome_option = Options()
        chrome_option.add_experimental_option("detach", True)
        context.driver = webdriver.Chrome(options=chrome_option)
    elif context.config.userdata["browser"] == "edge":
        from selenium.webdriver.edge.options import Options
        edge_option = Options()
        edge_option.add_experimental_option("detach", True)
        context.driver = webdriver.Chrome(options=edge_option)
    else:
        raise SeleniumDriverNotFound("This browser is not currently supported")

    context.web_driver = Driver(context.driver)
    context.lib_common = Common(context.web_driver)
    context.driver.maximize_window()

    logging.info("tests starting .......")

def after_all(context):
    context.driver.close()
    context.driver.quit()
    logging.info('Tests finished.')
