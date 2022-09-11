class CheersOClockRuntimeError(RuntimeError):
    _message = ''

    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message
