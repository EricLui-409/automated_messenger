import os

# environment variables
TOKEN = os.environ["TOKEN"]
REDIS_URL = os.environ["REDIS_URL"]
DOCKER_PATH_TO_USER_DIR = os.environ["DOCKER_PATH_TO_USER_DIR"]
DOCKER_PATH_TO_QR_CODE = os.environ["DOCKER_PATH_TO_QR_CODE"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
SLACK_API_FILE_UPLOAD_PATH = os.environ["SLACK_API_FILE_UPLOAD_PATH"]
CHROME_PATH = os.environ["CHROME_PATH"]

# REDIS QUEUE NAME
REDIS_QUEUE_NAME = "ws"

# logger levels
DEBUG = "debug"
INFO = "info"
WARN = "warn"
ERROR = "error"

# API routes
HEALTH_CHECK_ROUTE = "/internal/ping"
WHATSAPP_CHECK_ROUTE = "/ws/check/<string:phone_number>/<path:ret_url>"
WHATSAPP_MESSAGE_ROUTE = "/ws/message/<string:phone_number>/<string:message>/<path:ret_url>"
WHATSAPP_LOGIN_ROUTE = "/ws/login/<path:ret_url>"
WHATSAPP_LOGOUT_ROUTE = "/ws/logout/<path:ret_url>"

# API task status
API_SUCCESS = "success"
API_FAILED = "failed"

# API response messages
API_AUTH_FAILED = "Request rejected. Token incorrect or not provided"
API_PONG = "<html><body>pong</body></html>"
API_INVALID_PATH = "Invalid path"

# API service types
WHATSAPP_CHECK = "whatsapp check"
WHATSAPP_MESSAGE = "whatsapp message"
WHATSAPP_LOGIN = "whatsapp login"
WHATSAPP_LOGOUT = "whatsapp logout"

# Search status
TRUE = True
FALSE = False
NONE = None

# URLs
WHATSAPP_WEB_URL = "http://web.whatsapp.com"
WHATSAPP_CHECK_URL = "https://web.whatsapp.com/send?phone={}"
WHATSAPP_MESSAGE_URL = "https://web.whatsapp.com/send?phone={}&text={}&source=&data="

# log messages
DRIVER_INITIALIZED = "Webdriver initialized"
QR_CODE_SENT = "QR code sent through slack"
WHATSAPP_WEB_ERROR = "Whatsapp web error"

WHATSAPP_CHECK_INITIALIZED = "Whatsapp check initialized"
WHATSAPP_CHECK_NOT_LOGGED_IN = "Whatsapp Web not logged in, please scan qr code"
WHATSAPP_CHECK_COMPLETED = "Whatsapp check completed successfully"
WHATSAPP_CHECK_FAILED = "Whatsapp check failed, exception raised"

WHATSAPP_MESSAGE_INITIALIZED = "Whatsapp messaging initialized"
RECIPIENT_NO_NUMBER = "Recipient number does not have whatsapp"
WHATSAPP_MESSAGE_COMPLETED = "Message sent successfully"
WHATSAPP_MESSAGE_FAILED = "Whatsapp messaging failed, exception raised"

WHATSAPP_LOGIN_INITIALIZED = "Whatsapp login initialized"
ALREADY_LOGGED_IN = "Whatsapp already logged in"
WHATSAPP_LOGIN_COMPLETED = "Log in successful"
WHATSAPP_LOGIN_FAILED = "Whatsapp login failed, exception raised"

WHATSAPP_LOGOUT_INITIALIZED = "Whatsapp logout initialized"
ALREADY_LOGGED_OUT = "Currently not logged in to any account"
WHATSAPP_LOGOUT_COMPLETED = "Log out successful"
WHATSAPP_LOGOUT_FAILED = "Whatsapp logout failed, exception raised"
