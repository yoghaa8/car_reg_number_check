from selenium.webdriver.common.by import By
from lib.common import Locator

class CarObjectRepo:
    text_box = Locator(By.XPATH, "//input[@id='subForm1']")
    check_now_button = Locator(By.XPATH, "//button[normalize-space()='Check Now']")
    bmw_maker = Locator(By.XPATH, "(//table[@class='table table-responsive'])[1]")
