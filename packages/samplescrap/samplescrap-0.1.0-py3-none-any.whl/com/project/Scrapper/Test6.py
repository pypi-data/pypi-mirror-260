import logging
from logging.handlers import RotatingFileHandler
import os
from aspectlib import Aspect  # Import Aspect from aspectlib

class CustomLogger:
    _instance = None

    @staticmethod
    def get_instance(log_filename="logfile.log", max_file_size=100000, backup_count=1):
        if not CustomLogger._instance:
            CustomLogger._instance = CustomLogger(log_filename, max_file_size, backup_count)
        return CustomLogger._instance

    def __init__(self, log_filename="logfile.log", max_file_size=100000, backup_count=1):
        if CustomLogger._instance:
            raise Exception("This class is designed as a Singleton; obtain its instance using get_instance().")
        else:
            CustomLogger._instance = self

        self.log_filename = log_filename
        self.max_file_size = max_file_size
        self.backup_count = backup_count

        self.setup_logger()

    def setup_logger(self):
        logs_folder = "logs"
        log_file_path = os.path.join(logs_folder, self.log_filename)
        os.makedirs(logs_folder, exist_ok=True)

        handler = RotatingFileHandler(log_file_path, maxBytes=self.max_file_size, backupCount=self.backup_count)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

def log_around(log_level='INFO', message='Performing operation'):
    def aspect(wrapped):
        def wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__
            method_name = wrapped.__name__

            entry_message = f"Entering method '{class_name}.{method_name}' with parameters {args[1:]}"
            CustomLogger.get_instance().log_info(entry_message)

            try:
                result = wrapped(*args, **kwargs)
                exit_message = f"Exiting method '{class_name}.{method_name}' with parameters {args[1:]}"
                CustomLogger.get_instance().log_info(exit_message)
            except Exception as e:
                error_message = f"Error in method '{class_name}.{method_name}': {str(e)}"
                CustomLogger.get_instance().log_info(error_message)
                raise

            return result
        return wrapper
    return Aspect().log_around(wrapped=aspect)


class MyClass:
    @log_around()
    def my_method(self, param):
        print("Executing my_method with param:", param)

if __name__ == "__main__":
    custom_logger = CustomLogger.get_instance("custom_logfile.log", max_file_size=500000, backup_count=3)

    obj = MyClass()
    obj.my_method("example_param")