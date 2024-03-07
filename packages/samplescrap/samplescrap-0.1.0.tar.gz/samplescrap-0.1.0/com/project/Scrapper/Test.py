from com.project.Logger.Logger import  CustomLogger
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