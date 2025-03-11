from selenium.webdriver.support.wait import WebDriverWait

class Driver(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        self.implicit_wait = 25



