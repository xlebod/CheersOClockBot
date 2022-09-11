from CheersOClockRuntimeError import CheersOClockRuntimeError
import requests
import json


class DiscordMessageApiHandler:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def get_messages_request(self, headers):
        r = self.get_request(headers)
        counter = 0
        while True:
            if r.status_code == 200:
                break
            self.logger.error(f"Received code {r.status_code} with response {r.text}")
            r = self.get_request(headers)
            counter += 1
            if counter == 10:
                raise CheersOClockRuntimeError(f"Failed to load messages after {counter} retries")
        return r

    def get_request(self, headers):
        r = requests.get(self.config.message_api_endpoint, headers=headers)
        return r

    def get_messages(self, token):
        self.logger.debug("Trying to retrieve all messages")
        headers = {
            'authorization': token
        }
        r = self.get_messages_request(headers)
        messages = json.loads(r.text)
        for message in messages:
            self.logger.debug(f"Retrieved message: {message}")

        return messages

    def try_send_message(self, token, message):
        self.logger.debug(f"Trying to send message '{message}'")
        headers = {
            'authorization': token
        }

        payload = {
            'content': message
        }
        r = requests.post(self.config.message_api_endpoint, headers=headers, data=payload)
        if r.status_code != 200:
            self.logger.error(f"Received code {r.status_code} with response {r.text}")
            return False

        self.logger.debug("Successfully sent message")
        return True

    def send_message(self, token, message):
        counter = 1
        while not self.try_send_message(token, message):
            counter += 1
            self.logger.debug(f"Checking if any message is present before trying again")
            messages = self.get_messages(token)
            if len(messages) != 0:
                self.logger.debug("Message has already been sent by a different program! Switching to joining mode")
                break
            if counter == 11:
                raise CheersOClockRuntimeError(f"Failed to send message after {counter - 1} retries")

