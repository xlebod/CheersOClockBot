import os
from CheersOClockRuntimeError import CheersOClockRuntimeError


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
            raise CheersOClockRuntimeError("That platform has not been implemented!")
        return path
