import time

import VRC_OSCLib


class OscHandler:
    def __init__(self, logger):
        self.logger = logger

    def trigger_osc_bool(self, parameter):
        self.logger.debug("Sending OSC signal to VRC - toggle param on")
        VRC_OSCLib.Bool(True, f"/avatar/parameters/{parameter}", "127.0.0.1", 9000)
        self.logger.log("OSC signal sent - toggle param on")
        time.sleep(0.5)
        self.logger.debug("Sending OSC signal to VRC - toggle param off")
        VRC_OSCLib.Bool(False, f"/avatar/parameters/{parameter}", "127.0.0.1", 9000)
        self.logger.debug("OSC signal sent - toggle param off")
        self.logger.log("Sent OSC toggle")
