import config as cf
import os
import sys
import time
from utilities.logger import Logger
from utilities.request import RequestSender
from utilities.webdriver import WebDriver
from services.whatsapp_checker import WhatsappChecker
from services.login_checker import LogInChecker
from services.screen_capturer import ScreenCapturer

class CheckHandler:

    def __init__(self, task_id, ret_url, phone_number):
        self.phone_number = phone_number

        self.logger = Logger()
        self.sender = RequestSender(self.logger, task_id, ret_url)
        self.driver = WebDriver(self.logger).driver

        self.whatsapp_checker = WhatsappChecker(self.driver, self.phone_number)
        self.screen_capturer = ScreenCapturer(self.driver, self.logger, self.sender)
        self.login_checker = LogInChecker(self.driver)

        self.result = None

    def run(self):
        try:
            self.logger.log(cf.INFO, cf.WHATSAPP_CHECK_INITIALIZED)

            if not self.login_checker.run():
                # log and slack whatsapp not logged in
                self.logger.log(cf.WARN, cf.WHATSAPP_CHECK_NOT_LOGGED_IN)
                self.sender.slack(cf.WHATSAPP_CHECK_NOT_LOGGED_IN)

                # take screen shot and send to slack
                self.screen_capturer.run()
                time.sleep(10)

                self.sender.post(cf.WHATSAPP_CHECK_NOT_LOGGED_IN)
            else:
                self.result = str(self.whatsapp_checker.run())

                # post result to server
                self.sender.post(self.result)

                self.logger.log(cf.INFO, cf.WHATSAPP_CHECK_COMPLETED)
                
        except Exception as e:
            # handles exception
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            # post error message to server
            self.sender.post(cf.WHATSAPP_CHECK_FAILED)

            # log and slack exception message
            self.logger.log(cf.ERROR, cf.WHATSAPP_CHECK_FAILED)
            self.logger.log(cf.ERROR, "Input number: {}".format(self.phone_number))
            self.logger.log(cf.ERROR, str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))
            
            self.sender.slack(cf.WHATSAPP_CHECK_FAILED)
            self.sender.slack("Input number: {}".format(self.phone_number))
            self.sender.slack(str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))

            raise e
        
        finally:
            if not self.driver is None:
                self.driver.quit()
