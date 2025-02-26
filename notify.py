import requests
import logging


class Telegram:
    def __init__(self, TG_INFO, logger):
        self.api_token = TG_INFO['api_token']
        self.chat_id = TG_INFO['chat_id']
        self.log = logger

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.api_token}/sendMessage?chat_id={self.chat_id}&text={message}"
        res = requests.get(url).json()
        if res['ok']:
            return res
        self.log.warning("Telegram failed to send message")
        self.log.debug(f"message: {message}")
        self.log.debug(f"response: {res}")


class Logger:
    def __init__(self, filename, notify_config):
        logging.basicConfig(filename=filename, filemode='a', format='[%(asctime)s] %(levelname)-8s %(message)s') 
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.notify_connector = Telegram(notify_config, self)

    def info(self, message):
        self.log.info(message)

    def warning(self, message):
        self.log.warning(message)

    def error(self, message):
        self.log.error(message)

    def debug(self, message):
        self.log.debug(message)

    def notify(self, message):
        self.info(f"Notifying the operator: {message}")
        self.notify_connector.send_message(message)
