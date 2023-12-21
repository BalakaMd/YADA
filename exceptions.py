from address_book import AddressBook, Color


class PhoneLengthError(Exception):
    pass


class BirthdayFormatError(Exception):
    pass


class BirthdayKeyError(Exception):
    pass


class BirthdayNotFoundError(Exception):
    pass


class AddBirthdayValueError(Exception):
    pass


class BirthdayIndexError(Exception):
    pass


class ShowBirthdayIndexError(Exception):
    pass


class AddContactValueError(Exception):
    pass


class ChangeContactValueError(Exception):
    pass


class FindPhoneIndexError(Exception):
    pass


class FindNameIndexError(Exception):
    pass


# decorators block

def input_error(func):
    """
    Handles exception 'ValueError', 'KeyError', 'IndexError', 'AttributeError' on user input.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AddContactValueError:
            print(f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>> {Color.YELLOW}<add> <name> <phone number>\n{Color.RESET}")
        except ChangeContactValueError:
            print(f"{Color.RED}Enter a valid command in format{Color.RESET} --->>> {Color.YELLOW}<change> <name> <old phone number> <new phone number>\n{Color.RESET}")
        except AddBirthdayValueError:
            print(f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>> {Color.YELLOW}<add-birthday> <name> <DD.MM.YYYY.>\n{Color.RESET}")
        except KeyError:
            print(f"{Color.RED}This contact was not found in the system. Try again.\n{Color.RESET}")
        except ShowBirthdayIndexError:
            print(f"{Color.RED}Enter a command in this format{Color.RESET} --->>> {Color.YELLOW}<show-birthday> <name>\n{Color.RESET}")
        except FindPhoneIndexError:
            print(f"{Color.RED}Enter a command in this format{Color.RESET} --->>> {Color.YELLOW}<find-phone> <name>\n{Color.RESET}")
        except FindNameIndexError:
            print(f"{Color.RED}Enter a command in this format{Color.RESET} --->>> {Color.YELLOW}<find-name> <phone>\n{Color.RESET}")
        except PhoneLengthError:
            print(f"{Color.RED}Phone number must be 10 digits long\n{Color.RESET}")
        except BirthdayFormatError:
            print(f"{Color.RED}Birthday date must in this format{Color.RESET} {Color.YELLOW}'DD.MM.YYYY.'\n{Color.RESET}")
        except BirthdayIndexError:
            print(f"{Color.RED}Enter a command in this format{Color.RESET} --->>> {Color.YELLOW}<find-birthday> <'DD.MM.YYYY.'>\n{Color.RESET}")
        except BirthdayKeyError:
            print(f"{Color.RED}This contact was not found in the system. Try again.\n{Color.RESET}")
        except BirthdayNotFoundError:
            print(f"{Color.RED}Contact with this birthday date was not found. Try again.\n{Color.RESET}")

    return inner


def open_file_error(func):
    """
        Handles exception 'FileNotFoundError' when trying to open a non-existent file.
        :param func:
        :return wrapper:
        """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"{Color.RED}Contact book was not found. A new one was created.\n{Color.RESET}")
            return AddressBook()

    return inner
