import config as cf
import os
import sys
import time
from utilities.logger import Logger
from utilities.request import RequestSender
from utilities.webdriver import WebDriver
from services.whatsapp_messenger import WhatsappMessenger
from services.login_checker import LogInChecker
from services.screen_capturer import ScreenCapturer

class MessageHandler:

    def __init__(self, task_id, ret_url, phone_number, message):
        self.phone_number = phone_number
        self.message = message

        self.logger = Logger()
        self.sender = RequestSender(self.logger, task_id, ret_url)
        self.driver = WebDriver(self.logger).driver

        self.whatsapp_messenger = WhatsappMessenger(self.driver, self.phone_number, self.message)
        self.screen_capturer = ScreenCapturer(self.driver, self.logger, self.sender)
        self.login_checker = LogInChecker(self.driver)

        self.result = None

    def run(self):
        try:
            self.logger.log(cf.INFO, cf.WHATSAPP_MESSAGE_INITIALIZED)

            if not self.login_checker.run():
                # log and slack whatsapp not logged in
                self.logger.log(cf.WARN, cf.WHATSAPP_CHECK_NOT_LOGGED_IN)
                self.sender.slack(cf.WHATSAPP_CHECK_NOT_LOGGED_IN)

                # take screen shot and send to slack
                self.screen_capturer.run()
                time.sleep(10)

                self.sender.post(cf.WHATSAPP_CHECK_NOT_LOGGED_IN)

            else:
                self.result = str(self.whatsapp_messenger.run())

                # if recipient number has no whatsapp installed
                if not self.result:
                    self.logger.log(cf.INFO, cf.RECIPIENT_NO_NUMBER)
                    self.sender.slack(cf.RECIPIENT_NO_NUMBER)

                # post result to server
                self.sender.post(self.result)

                self.logger.log(cf.INFO, cf.WHATSAPP_MESSAGE_COMPLETED)

        except Exception as e:
            # handles exception
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            # post error message to server
            self.sender.post(cf.WHATSAPP_MESSAGE_FAILED)

            # log and slack exception message
            self.logger.log(cf.ERROR, cf.WHATSAPP_MESSAGE_FAILED)
            self.logger.log(cf.ERROR, "Input number: {}  Message: {}".format(self.phone_number, self.message))
            self.logger.log(cf.ERROR, str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))
            
            self.sender.slack(cf.WHATSAPP_MESSAGE_FAILED)
            self.sender.slack("Input number: {}  Message: {}".format(self.phone_number, self.message))
            self.sender.slack(str(exc_type) + '  ' + str(fname) + '  ' + str(exc_tb.tb_lineno))

            raise e
        
        finally:
            if not self.driver is None:
                self.driver.quit()
