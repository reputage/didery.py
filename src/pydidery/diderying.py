class DideryPyError(Exception):
    """
    Base Class for bluepea exceptions

    To use   raise BluepeaError("Error: message")
    """


class ValidationError(DideryPyError):
    """
    Validation related errors
    Usage:
        raise ValidationError("error message")
    """