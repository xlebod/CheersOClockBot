import time
from datetime import datetime, timedelta
from CheersOClockRuntimeError import CheersOClockRuntimeError


class CheersOClockBot:
    def __init__(self, config, logger, message_api, token_handler, osc_handler):
        self.logger = logger
        self.message_api = message_api
        self.token_handler = token_handler
        self.osc_handler = osc_handler
        self.config = config

    def do_loop(self, shot_datetime, shot_frequency):
        self.osc_handler.trigger_osc_bool(self.config.parameter_name)
        seconds_to_sleep = (shot_datetime - datetime.now(shot_datetime.tzinfo)).total_seconds()
        self.logger.debug(f"Going to sleep for '{seconds_to_sleep}' seconds")
        time.sleep(seconds_to_sleep)
        shot_datetime = self.get_next_datetime(shot_datetime, shot_frequency)
        self.do_loop(shot_datetime, shot_frequency)

    def join_party(self, token):
        self.logger.debug("Joining party")
        messages = self.message_api.get_messages(token)
        message = self.get_first_message(messages)
        shot_frequency = self.get_shot_frequency(message["content"])
        self.logger.debug(f"Got shot frequency '{shot_frequency}'")
        next_shot_datetime = self.get_shot_datetime(message["timestamp"], shot_frequency)
        self.logger.debug(f"Got start time for shots {next_shot_datetime}")
        self.do_loop(next_shot_datetime, shot_frequency)

    @staticmethod
    def get_next_datetime(datetime_obj, shot_frequency):
        while datetime_obj < datetime.now(datetime_obj.tzinfo):
            datetime_obj = datetime_obj + timedelta(minutes=shot_frequency)
        return datetime_obj

    def get_shot_datetime(self, str_timestamp, shot_frequency):
        datetime_obj = datetime.strptime(str_timestamp, "%Y-%m-%dT%X.%f%z")
        return self.get_next_datetime(datetime_obj, shot_frequency)

    @staticmethod
    def get_shot_frequency(message):
        numbers_in_message = [int(s) for s in message.split() if s.isdigit()]
        if len(numbers_in_message) != 1:
            raise CheersOClockRuntimeError("Did not find exactly one number in party message!" +
                                           " Please ensure only the frequency of shots is present in the message!")
        return numbers_in_message[0]

    @staticmethod
    def get_first_message(messages):
        if len(messages) != 1:
            raise CheersOClockRuntimeError("Found multiple messages in channel!" +
                                           " Please clean channel before running the program!")
        message = messages[0]
        return message

    def start_party(self, token):
        self.logger.debug("Trying to start party")
        self.message_api.send_message(token, self.config.start_message)
        self.logger.debug("Started party")

    def main(self):
        try:
            token = self.token_handler.get_token()
            self.logger.debug(f"Chose token '{token}'")
            messages = self.message_api.get_messages(token)
            if len(messages) == 0:
                self.start_party(token)
            self.join_party(token)

        except CheersOClockRuntimeError as e:
            if e.message:
                self.logger.error(e.message)
        finally:
            time.sleep(0.5)
            self.logger.log("Waiting for input before closing!")
            input()
