from CheersOClockBot import CheersOClockBot
from Config import Config
from DiscordMessageApiHandler import DiscordMessageApiHandler
from DiscordTokenHandler import DiscordTokenHandler
from Logger import Logger
from OscHandler import OscHandler


def main():
    config = Config()
    logger = Logger(True)
    message_api = DiscordMessageApiHandler(config, logger)
    token_handler = DiscordTokenHandler(config, logger, message_api)
    osc_handler = OscHandler(logger)
    bot = CheersOClockBot(config, logger, message_api, token_handler, osc_handler)
    bot.main()


if __name__ == '__main__':
    main()
