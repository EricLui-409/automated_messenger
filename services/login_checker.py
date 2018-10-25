import config as cf
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class LogInChecker:

    def __init__(self, driver):
        self.driver = driver

    def run(self):
        self.driver.get(cf.WHATSAPP_WEB_URL)

        # returns True if logged in, False if otherwise
        try:
		    # explicit wait for loading
            wait = WebDriverWait(self.driver, 6, poll_frequency=1)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_2Uo0Z')))
            return True
        except (NoSuchElementException, TimeoutException):
            return False
