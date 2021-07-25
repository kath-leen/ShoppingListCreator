class Ut:
    @staticmethod
    def check_equal(expected_value, upcoming_value):
        if expected_value != upcoming_value:
            raise Exception("Unexpected value " + str(upcoming_value) + " received! Expected: " + str(expected_value))

    @staticmethod
    def check_not_equal(expected_value, upcoming_value):
        if expected_value == upcoming_value:
            raise Exception(
                "Value " + str(upcoming_value) + " should not be equal to the expected value, but it is!")

    @staticmethod
    def check_true(value):
        if not value:
            raise Exception("Value " + str(value) + " is False while should be True!")

    @staticmethod
    def check_false(value):
        if value:
            raise Exception("Value " + str(value) + " is True while should be False!")

    @staticmethod
    def check_throws(fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
        except Exception:
            return
        raise Exception("No expected exception is thrown!")

    @staticmethod
    def check_not_throws(fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
        except Exception:
            raise Exception("Unexpected exception thrown!")
