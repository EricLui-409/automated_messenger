import config as cf
import os
import sys
import time
from utilities.logger import Logger
from utilities.request import RequestSender
from utilities.webdriver import WebDriver
from services.login_checker import LogInChecker
from services.screen_capturer import ScreenCapturer

class LogInHandler:

    def __init__(self, task_id, ret_url):
        self.logger = Logger()
        self.sender = RequestSender(self.logger, task_id, ret_url)
        self.driver = WebDriver(self.logger).driver

        self.screen_capturer = ScreenCapturer(self.driver, self.logger, self.sender)
        self.login_checker = LogInChecker(self.driver)
    
    def run(self):
        try:
            self.logger.log(cf.INFO, cf.WHATSAPP_LOGIN_INITIALIZED)

            if not self.login_checker.run():
                # take screen shot and send to slack
                self.screen_capturer.run()
                time.sleep(10)

                self.sender.post(cf.QR_CODE_SENT)
            
            else:
                self.logger.log(cf.INFO, cf.ALREADY_LOGGED_IN)

                self.sender.post(cf.ALREADY_LOGGED_IN)

        except Exception as e:
            # handles exception
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            # post error message to server
            self.sender.post(cf.WHATSAPP_LOGIN_FAILED)

            # log and slack exception message
            self.logger.log(cf.ERROR, cf.WHATSAPP_LOGIN_FAILED)
            self.logger.log(cf.ERROR, str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))
            
            self.sender.slack(cf.WHATSAPP_LOGIN_FAILED)
            self.sender.slack(str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))

            raise e
        
        finally:
            if not self.driver is None:
                self.driver.quit()
