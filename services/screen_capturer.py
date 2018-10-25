import config as cf

class ScreenCapturer:

    def __init__(self, driver, logger, sender):
        self.driver = driver
        self.logger = logger
        self.sender = sender

    def run(self):
        self.driver.get_screenshot_as_file(cf.DOCKER_PATH_TO_QR_CODE)
        self.logger.log(cf.INFO, "Screen captured")
        self.sender.slack_qr_code()
