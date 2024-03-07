# # test_logger.py
#
# from com.project.Logger.Logger3 import CustomLogger
#
# # Instantiate the logger
# logger = CustomLogger.get_instance()
#
# class TestClass:
#     @CustomLogger.log_around
#     def method_with_self(self, a, b):
#         return a + b
#
#     @CustomLogger.log_around
#     def method_without_self(a, b):
#         return a - b
#
# if __name__ == "__main__":
#     # Test the methods
#     test_instance = TestClass()
#
#     # The following calls will automatically log the results
#     result_with_self = test_instance.method_with_self(5, 3)
#     result_without_self = TestClass.method_without_self(5, 3)

# from com.project.Logger.Logger4 import  CustomLogger
# class Calculator:
#     def __init__(self, logger):
#         self.logger = logger
#
#
#
#
#     @CustomLogger.log_around
#     def add(self, a, b):
#         return a + b
#
#     @staticmethod
#
#     @CustomLogger.log_around
#     def subtract(a,b):
#         return a - b
#
# if __name__ == "__main__":
#     custom_logger = CustomLogger.get_instance("t_logfile.log", max_file_size=500000, backup_count=3)
#     calculator = Calculator(custom_logger)
#
#     result_add = calculator.add(5, 3)
#
#     result_subtract = calculator.subtract(10, 4)




from com.project.Logger.Logger4 import  CustomLogger
class Calculator:
    def __init__(self, logger):
        self.logger = logger

    @CustomLogger.log_around
    def add(self, a, b):
        return a + b

    @CustomLogger.log_around
    def subtract(self, a, b):
        return a - b

if __name__ == "__main__":
    custom_logger = CustomLogger.get_instance("custom_logfile.log", max_file_size=500000, backup_count=3)
    calculator = Calculator(custom_logger)

    result_add = calculator.add(5, 3)

    result_subtract = calculator.subtract(10, 4)