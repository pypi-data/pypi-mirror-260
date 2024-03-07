# test_example.py

from com.project.Logger.Logger5 import CustomLogger

class TestExample:

    @CustomLogger.log_around
    def test_addition(self, param1, param2):
        """
        Test addition functionality.
        """
        result = param1 + param2
        return result
    @staticmethod

    @CustomLogger.log_around
    def test_subtraction(param1, param2):
        """
        Test subtraction functionality.
        """
        result = param1 - param2
        return result

# Example usage:
if __name__ == "__main__":
    test_instance = TestExample()

    # Call the decorated test methods
    test_instance.test_addition(10, 20)
    test_instance.test_subtraction(10, 20)
