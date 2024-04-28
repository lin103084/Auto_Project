from selenium.webdriver.support.ui  import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.by import By



def use_wait_visible(driver, method, method_value, time):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located((method, method_value))
        )

def use_wait_not_visible(driver, method, method_value, time):
    WebDriverWait(driver, time).until_not(
        EC.visibility_of_element_located((method, method_value))
        )

def use_wait_visible_keyword(driver, method, method_value, value, time):

    locator = (method, method_value)
    WebDriverWait(driver, time).until(
        EC.text_to_be_present_in_element(locator, value)
        )