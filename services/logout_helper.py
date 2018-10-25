from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LogOutHelper:

    def __init__(self, driver):
        self.driver = driver

    def run(self):
        self.driver.find_element_by_class_name("_3Kxus") \
            .find_element_by_xpath("//div[@class='rAUz7'][3]") \
		    .find_element_by_xpath("//div[@title='Menu']") \
            .click()

        wait = WebDriverWait(self.driver, 100, poll_frequency=1)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Log out']"))).click()
