from config.config import Config
import boto3
import botocore.exceptions
import logging
import json

class AlertManager:
    config: Config = None

    def __init__(self, conf: Config):
        self.config = conf

    def sendAlert(self, message):

        logging.error("To implement alert")
        #dead code here :

        # sms_text = message.replace("\n"," ")
        # messages = {
        #     "default": message,
        #     "sms": self.config.title + " : " + sms_text,
        #     "email": message,
        # }
        #
        # client = boto3.client('sns')
        # try:
        #     response = client.publish(
        #         TopicArn=self.config.topic,
        #         Message=json.dumps(messages),
        #         MessageStructure="json",
        #         Subject=self.config.title
        #     )
        # except botocore.exceptions.ClientError as err:
        #     logging.exception("Couldn't publish message to topic %s.", self.config.topic)
        #     raise
        # else:
        #     if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        #         #http return 200 from AWS --> message sent
        #         response
        #         return True
        #     else:
        #         return False
        #
        #



