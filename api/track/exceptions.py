from http.client import INTERNAL_SERVER_ERROR


class CustomException(Exception):
    def __init__(self, message, status_code=INTERNAL_SERVER_ERROR, payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        serialized_error = dict(self.payload or ())
        serialized_error['message'] = self.message
        return serialized_error



