import os
import re

from CheersOClockRuntimeError import CheersOClockRuntimeError
from Platforms import Platforms


class DiscordTokenHandler:
    def __init__(self, config, logger, api):
        self.config = config
        self.logger = logger
        self.message_api = api

    def find_tokens(self):
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
        tokens = self.find_tokens()
        for token in tokens:
            self.logger.debug(f"Trying validity of token {token}")
            if self.check_token_authority(token):
                self.logger.debug(f"Token is valid")
                return token
            self.logger.debug(f"Token is invalid")

        raise CheersOClockRuntimeError("Found no valid tokens!")

    def check_token_authority(self, token):
        headers = {
            'authorization': token
        }
        if self.message_api.get_request(headers).status_code == 401:
            return False
        return True
