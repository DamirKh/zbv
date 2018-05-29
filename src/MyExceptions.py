class NotDefinedError(Exception):
    # https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class BadUserError(Exception):
    # https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
