from flask import jsonify
from app import app


class APIError:
    """
    Class to create a JSON response for errors
    """

    def __init__(self, error):
        self.detail = error.description
        self.message = error.name
        self.code = error.code

    def to_json(self):
        error_dict = {k: v for k, v in self.__dict__.items() if k != 'code'}
        return jsonify(error_dict), self.code


class ErrorResponder:
    """
    Class to register error handlers for the API
    If a new error code is added, it should be added to the list of registered errors    
    """
    def __init__(self) -> None:
        self.registered_errors = [400, 401, 404, 500, 502]
        self.register_error_handlers()

    def create_error_handler(self, code):
        def error_handler(error):
            return APIError(error).to_json()
        return error_handler

    def register_error_handlers(self):
        for error_code in self.registered_errors:
            app.register_error_handler(error_code, self.create_error_handler(error_code))
