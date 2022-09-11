import configparser


class Config:

    def __init__(self, path_to_ini_file="./config.ini"):
        config_obj = configparser.ConfigParser()
        config_obj.read(path_to_ini_file)
        bot_config = config_obj["CheersOClockBot"]

        self.platform = bot_config["platform"]
        self.channel_id = bot_config["channel_id"]
        self.drinkies_frequency = bot_config["drinkies_frequency"]
        self.parameter_name = bot_config["parameter_name"]
        self.default_token = bot_config["default_token"]
        self.debug_mode = bot_config["debug_mode"]
        self.start_message = f"Heya! Time to start drinking! Shots every {self.drinkies_frequency} minutes? " \
                             f"Sounds good to me!"
        self.message_api_endpoint = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"

    @staticmethod
    def add_to_config(key, value, path_to_ini_file="./config.ini"):
        config = configparser.ConfigParser()
        config.read(path_to_ini_file)
        config.set("CheersOClockBot", key, value)
        with open(path_to_ini_file, 'w') as configfile:
            config.write(configfile)
