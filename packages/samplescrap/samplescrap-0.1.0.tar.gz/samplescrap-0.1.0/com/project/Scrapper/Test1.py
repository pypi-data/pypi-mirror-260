# test_class.py

from com.project.Logger.Logger1 import CustomLogger

class TestClass:
    def __init__(self, logger):
        self.logger = logger

    @CustomLogger.log_around
    def method_with_self(self, param, operation_message="Custom operation message"):
        return f"Result from method_with_self: {param}"

    @classmethod
    @CustomLogger.log_around
    def method_without_self(cls, param, operation_message="Custom operation message"):
        # Note: This method intentionally does not have 'self' in its parameters
        return f"Result from method_without_self: {param}"

if __name__ == "__main__":
    custom_logger = CustomLogger.get_instance("test_logfile.log", max_file_size=500000, backup_count=3)

    test_class_instance = TestClass(custom_logger)

    # Testing method_with_self
    result_with_self = test_class_instance.method_with_self("test_param_with_self")

    # Testing method_without_self
    result_without_self = TestClass.method_without_self("test_param_without_self")
