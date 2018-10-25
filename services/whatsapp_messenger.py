import config as cf
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class WhatsappMessenger:

    def __init_(self, driver, phone_number, message):
        self.driver = driver
        self.phone_number = phone_number
        self.message = message
        self.status = cf.NONE

    def result_check(self, driver):
        try:
            driver.find_element_by_class_name("_3AwwN")
            self.status = cf.TRUE
            return True
        except NoSuchElementException:
            pass
        try:
            driver.find_element_by_class_name("_1CnF3")
            self.status = cf.FALSE
            return True
        except NoSuchElementException:
            pass
        return False

    def run(self):
        self.driver.get(cf.WHATSAPP_MESSAGE_URL.format(self.phone_number, self.message))
        wait = WebDriverWait(self.driver, 15, poll_frequency=2)

        # wait for website to load
        wait.until(self.result_check)

        # return result
        if self.status is None:
            raise Exception(cf.WHATSAPP_WEB_ERROR)
        if self.status == True:
            self.driver.find_element_by_class_name("_2S1VP").send_keys(Keys.RETURN)
            time.sleep(1)
        return self.status
