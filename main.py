import json
import sys
import requests
from datetime import datetime, timedelta
import os
import re
import time

PLATFORM = 'Discord'
CHANNEL_ID = FILL_THIS_IN
MESSAGE_API = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages?limit=100"
DRINKIES_FREQUENCY = 1
START_MESSAGE = f"Heya! Time to start drinking! Shots every {DRINKIES_FREQUENCY} minutes? Sounds good to me!"
DEBUG_MODE = True


class Logger:
    @staticmethod
    def log(message):
        print(f"{[{datetime.now()}]} {message}  ")

    @staticmethod
    def error(message):
        print(f"[{datetime.now()}] [ERROR] {message}", file=sys.stderr)

    @staticmethod
    def debug(message):
        if DEBUG_MODE:
            print(f"[{datetime.now()}] [DEBUG] {message}")

class Platforms:
    @staticmethod
    def get_path(platform):
        roaming = os.getenv('APPDATA')
        _platform_dict = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb'
        }
        path = _platform_dict.get(platform)

        if path is None:
            raise NotImplementedError("That platform has not been implemented!")
        return path


def find_token():
    path = Platforms.get_path(PLATFORM)
    path += '\\Local Storage\\leveldb'
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def trigger_osc():
    Logger.debug("Sending OSC signal to VRC")


def do_loop(shot_datetime, shot_frequency):
    trigger_osc()
    seconds_to_sleep = (shot_datetime - datetime.now(shot_datetime.tzinfo)).total_seconds()
    Logger.debug(f"Going to sleep for '{seconds_to_sleep}' seconds")
    time.sleep(seconds_to_sleep)
    shot_datetime = get_next_datetime(shot_datetime, shot_frequency)
    do_loop(shot_datetime, shot_frequency)

def join_party(token):
    Logger.debug("Joining party")
    messages = get_messages(token)
    message = get_first_message(messages)
    shot_frequency = get_shot_frequency(message["content"])
    Logger.debug(f"Got shot frequency '{shot_frequency}'")
    next_shot_datetime = get_shot_datetime(message["timestamp"], shot_frequency)
    Logger.debug(f"Got start time for shots {next_shot_datetime}")
    do_loop(next_shot_datetime, shot_frequency)



def get_next_datetime(datetime_obj, shot_frequency):
    while datetime_obj < datetime.now(datetime_obj.tzinfo):
        datetime_obj = datetime_obj + timedelta(minutes=shot_frequency)
    return datetime_obj


def get_shot_datetime(str_timestamp, shot_frequency):
    datetime_obj = datetime.strptime(str_timestamp, "%Y-%m-%dT%X.%f%z")
    return get_next_datetime(datetime_obj, shot_frequency)


def get_shot_frequency(message):
    numbers_in_message = [int(s) for s in message.split() if s.isdigit()]
    if len(numbers_in_message) != 1:
        Logger.error("Did not find exactly one number in party message!" +
                     "Please ensure only the frequency of shots is present in the message!")
        raise RuntimeError
    return numbers_in_message[0]


def get_first_message(messages):
    if len(messages) != 1:
        Logger.error("Found multiple messages in channel! Please clean channel before running the program!")
        raise RuntimeError
    message = messages[0]
    return message


def send_message(token, message):
    headers = {
        'authorization': token
    }

    payload = {
        'content': message
    }
    Logger.debug(f"Trying to send message '{message}'")
    r = requests.post(MESSAGE_API, headers=headers, data=payload)
    if r.status_code != 200:
        Logger.error(f"Message '{message}' was not sent as expected!")
        return False

    Logger.debug("Successfully sent message")
    return True


def start_party(token):
    Logger.debug("Trying to start party")
    send_message(token, START_MESSAGE)
    Logger.debug("Started party")


def get_messages(token):
    headers = {
        'authorization': token
    }
    r = requests.get(MESSAGE_API, headers=headers)
    if r.status_code != 200:
        Logger.error(f"Messages were not able to be loaded!")

    messages = json.loads(r.text)
    for message in messages:
        Logger.debug(f"Retrieved message: {message}")

    return messages


def get_token():
    tokens = find_token()

    Logger.debug(f"Got tokens: {tokens}")

    if len(tokens) <= 0:
        raise RuntimeError("No viable tokens found!")

    if len(tokens) > 1:
        while True:
            for count, token in enumerate(tokens):
                Logger.log(f"[{count}] {token}")
            user_input = input("Choose a token to use:")
            if user_input.isnumeric():
                return tokens[int(user_input)]
            Logger.log("Input was not a number!")

    return tokens[0]


def main():
    token = get_token()
    Logger.debug(f"Chose token '{token}'")
    messages = get_messages(token)
    if len(messages) == 0:
        while not start_party(token):
            messages = get_messages(token)
            if len(messages) != 0:
                break
    join_party(token)


if __name__ == '__main__':
    main()

