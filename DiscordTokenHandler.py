import os
import re

from CheersOClockRuntimeError import CheersOClockRuntimeError
from Platforms import Platforms


class DiscordTokenHandler:
    def __init__(self, config, logger, api, crypto_service):
        self.config = config
        self.logger = logger
        self.message_api = api
        self.crypto_service = crypto_service

    def find_tokens(self):
        self.logger.debug("Trying to grab tokens from PC")
        path = Platforms.get_path(self.config.platform)
        path += '\\Local Storage\\leveldb'
        tokens = []

        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)

        self.logger.debug(f"Got tokens: {tokens}")
        return tokens

    def get_token(self):
        if self.is_default_token_valid():
            return self.get_default_token()

        if self.is_default_token_saved():
            self.logger.error("Saved token is not valid!")

        tokens = self.find_tokens()
        for token in tokens:
            if self.check_token_authority(token):
                self.save_default_token(token)
                return token

        token = self.get_token_from_user()
        self.save_default_token(token)
        return token

    def check_token_authority(self, token):
        self.logger.debug(f"Trying validity of token {token}")
        headers = {
            'authorization': token
        }
        if self.message_api.get_request(headers, "?limit=1").status_code == 401:
            self.logger.debug(f"Token is invalid")
            return False

        self.logger.debug(f"Token is valid")
        return True

    def is_default_token_valid(self):
        if not self.is_default_token_saved():
            return
        try:
            return self.check_token_authority(self.get_default_token())
        except UnicodeDecodeError:
            return False

    def get_default_token(self):
        return self.crypto_service.decrypt(self.config.default_token)

    def is_default_token_saved(self):
        return self.config.default_token != ''

    def save_default_token(self, token):
        while True:
            user_input = input("Found valid discord token. Do you wish to save it for future use? (y/n): ")
            if user_input == "y" or user_input == "yes":
                try:
                    token = self.crypto_service.encrypt(token).decode('utf-8')
                    self.config.add_to_config('default_token', token)
                except UnicodeDecodeError:
                    self.logger.log("Because of technical limitations, this password-token combination cannot be saved")
                return
            if user_input == "n" or user_input == "no":
                return
            self.logger.log("Unexpected input. Please try 'y' or 'n'")

    def get_token_from_user(self):
        user_input = input("Found no valid discord tokens. Please provide your token: ")
        if self.check_token_authority(user_input):
            return user_input

        raise CheersOClockRuntimeError("Provided token is not valid!")
