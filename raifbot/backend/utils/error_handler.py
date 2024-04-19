import logging


# Handling class
class UpdateError(Exception):
    """
    A custom exception class for handling update-related errors.

    This class extends the base Exception class and is used to raise exceptions specifically related to update processes in the application, such as database updates, API key changes, or other update operations. It includes an error message and a status code to be used in HTTP responses.

    Args:
        message (str): The error message describing what went wrong during the update process.
        status_code (int): The HTTP status code associated with this error, indicating the nature of the error.

    Upon initialization, this class logs the error message using the standard logging module.

    Attributes:fv
        message (str): Stores the error message.
        status_code (int): Stores the HTTP status code associated with the error.
    """

    def __init__(self, message, status_code):
        super().__init__(message)  # Initialize the base Exception class first
        self.message = message
        self.status_code = status_code
        self.log_error()  # Log the error after initializing

    def log_error(self):
        logging.error(self.message)
