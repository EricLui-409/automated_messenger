import config as cf
from selenium import webdriver

class WebDriver:

    def __init__(self, logger):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=" + cf.DOCKER_PATH_TO_USER_DIR)
        capabilities = chrome_options.to_capabilities()
        
        self.driver = webdriver.Remote(
            command_executor=cf.CHROME_PATH, 
            desired_capabilities=capabilities
            )

        logger.log(cf.INFO, cf.DRIVER_INITIALIZED)
