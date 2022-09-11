import VRC_OSCLib


class OscHandler:
    def __init__(self, logger):
        self.logger = logger

    def trigger_osc_bool(self, parameter):
        self.logger.debug("Sending OSC signal to VRC")
        VRC_OSCLib.Bool(True, f"/avatar/parameters/{parameter}", "127.0.0.1", 9000)
        self.logger.log("OSC signal sent")
