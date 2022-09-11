from CheersOClockRuntimeError import CheersOClockRuntimeError
from Platforms import Platforms
import os
import re


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

        if len(tokens) <= 0:
            raise CheersOClockRuntimeError("No viable tokens found!")

        self.logger.debug(f"Got tokens: {tokens}")

        return tokens

    def get_token(self):
        tokens = self.find_tokens()

        if len(tokens) > 1:
            self.logger.log("Found multiple tokens! Please choose the appropriate one")
            while True:
                for count, token in enumerate(tokens):
                    self.logger.log(f"[{count}] {token}")
                user_input = input("Choose a token to use:")
                if user_input.isnumeric():
                    return tokens[int(user_input)]
                self.logger.log("Input was not a number!")

        return tokens[0]

    def check_token_authority(self, token):
        if self.message_api.get_request(token).status_code == 401:
            return False
        return True
