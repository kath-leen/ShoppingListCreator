class Ut:
    def check_equal(self, expected_value, upcoming_value):
        if (expected != upcoming)
            raise Exception("Unexpected value " + str(upcoming_value) + " received! Expected: " + str(expected_value))

    def check_true(self, value):
        if (!value)
            raise Exception("Value " + str(value) + " is False while should be True!")

    def check_false(self, value):
        if (value)
            raise Exception("Value " + str(value) + " is True while should be False!")

    def check_throws(self, fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
        except Exception:
            return
        raise Exception("No expected exception is thrown!")

    def check_not_trhows(self, fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
        except Exception:
            raise Exception("Unexpected exception thrown!")
