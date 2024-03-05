class InfuzuError(Exception):
    pass


class NotFoundError(InfuzuError):
    pass


class EligibilityError(InfuzuError):
    pass


class InputError(InfuzuError):
    pass


class MissingRequiredFieldError(InputError):
    pass


class InvalidFieldError(InputError):
    pass


class InputFormatError(InputError):
    pass


class InputTypeError(InputError, TypeError):
    pass
