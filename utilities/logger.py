import sys
import logging
import bugsnag
import config as cf
from datetime import datetime
from bugsnag.handlers import BugsnagHandler

class Logger:

    def __init__(self):
        # initiating logger
        self.logger = logging.getLogger("log")
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def log(self, level, content):
        if level == cf.DEBUG:
            self.logger.debug(str(datetime.now()) + ' ' + content)

        elif level == cf.INFO:
            self.logger.info(str(datetime.now()) + ' ' + content)

        elif level == cf.WARN:
            self.logger.warn(str(datetime.now()) + ' ' + content)
            
        elif level == cf.ERROR:
            self.logger.error(str(datetime.now()) + ' ' + content)
