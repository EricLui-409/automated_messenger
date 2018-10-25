import requests
import json
import config as cf
from datetime import datetime

class RequestSender:

    def __init__(self, logger, task_id, ret_url):
        self.logger = logger
        self.task_id = task_id
        self.ret_url = ret_url

    def slack(self, message):
        webhook_URL = cf.SLACK_WEBHOOK
        payload = {"text": message}
        r = requests.post(webhook_URL, data=json.dumps(payload))
        self.logger.log(cf.INFO, "Slack response: " + r.content.decode("utf-8"))

    def slack_qr_code(self):
        qr_code = {"file": (cf.DOCKER_PATH_TO_QR_CODE, open(cf.DOCKER_PATH_TO_QR_CODE, 'rb'), 'image/png')}
        payload = {
            "filename": str(datetime.now()) + "_qr.png",
            "channels": cf.SLACK_CHANNEL,
            "token": cf.SLACK_TOKEN
            }
        r = requests.post(cf.SLACK_API_FILE_UPLOAD_PATH, params=payload, files=qr_code)
        # self.logger.log(cf.INFO, "Slack response: " + r.content.decode("utf-8"))
        self.logger.log(cf.INFO, cf.QR_CODE_SENT)

    def post(self, result):
        header = {
            'Authorization': "Token token=" + cf.TOKEN, 
            'Content-Type': 'application/json', 
            'Accept': 'application/json'
            }

        payload = {
            "task_id": self.task_id, 
            "result": result
            }

        final_url = self.ret_url
        r = requests.post(final_url, json=payload, headers=header, verify=True)
        self.logger.log(cf.INFO, "Server response: " + r.content.decode("utf-8"))