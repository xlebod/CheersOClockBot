import os
import sys

from CheersOClockBot import CheersOClockBot
from Config import Config
from CryptoService import CryptoService
from DiscordMessageApiHandler import DiscordMessageApiHandler
from DiscordTokenHandler import DiscordTokenHandler
from Logger import Logger
from OscHandler import OscHandler


def main():
    config = Config()
    logger = Logger(config.debug_mode)
    crypto_service = CryptoService(logger)
    message_api = DiscordMessageApiHandler(config, logger)
    token_handler = DiscordTokenHandler(config, logger, message_api, crypto_service)
    osc_handler = OscHandler(logger)
    bot = CheersOClockBot(config, logger, message_api, token_handler, osc_handler, crypto_service)
    bot.main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception:
        input()
