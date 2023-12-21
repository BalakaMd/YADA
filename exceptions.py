from address_book import AddressBook, Color


class PhoneLengthError(Exception):
    pass


class BirthdayFormatError(Exception):
    pass


class BirthdayKeyError(Exception):
    pass


class BirthdayNotFoundError(Exception):
    pass


class BirthdayConflictError(Exception):
    pass


class AddBirthdayValueError(Exception):
    pass


class AddAddresssValueError(Exception):
    pass


class AddEmailValueError(Exception):
    pass


class EditEmailValueError(Exception):
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


class FindEmailIndexError(Exception):
    pass


class FindAddressIndexError(Exception):
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
            print("Enter a valid command in this format --->>> <add> <name> <phone number>\n")
        except ChangeContactValueError:
            print("Enter a valid command in format --->>> <change> <name> <old phone number> <new phone number>\n")
        except AddBirthdayValueError:
            print("Enter a valid command in this format --->>> <add-birthday> <name> <DD.MM.YYYY.>\n")
        except BirthdayConflictError:
            print(f"{Color.RED}Error{Color.RESET}: Birthday already exists for this contact.\n")
        except AddAddresssValueError:
            print("Enter a valid command in this format --->>> <add-address> <name> <country> <city> <street> <house_number>\n")
        except AddEmailValueError:
            print("Enter a valid command in this format --->>> <add-email> <name> <email>")
        except EditEmailValueError:
            print("Enter a valid command in this format --->>> <adit-email> <name> <old_email> <new_email>")
        except KeyError:
            print('This contact was not found in the system. Try again.\n')
        except ShowBirthdayIndexError:
            print('Enter a command in this format --->>> <show-birthday> <name>\n')
        except FindPhoneIndexError:
            print("Enter a command in this format --->>> <find-phone> <name>\n")
        except FindNameIndexError:
            print("Enter a command in this format --->>> <find-name> <phone>\n")
        except FindEmailIndexError:
            print("Enter a command in this format --->>> <find-email> <email>\n")
        except FindAddressIndexError:
            print("Enter a command in this format --->>> <find-address> <country> <city> <street> <house_number>\n")
        except PhoneLengthError:
            print("Phone number must be 10 digits long\n")
        except BirthdayFormatError:
            print("Birthday date must in this format 'DD.MM.YYYY.'\n")
        except BirthdayIndexError:
            print("Enter a command in this format --->>> <find-birthday> <'DD.MM.YYYY.'>\n")
        except BirthdayKeyError:
            print('This contact was not found in the system. Try again.\n')
        except BirthdayNotFoundError:
            print('Contact with this birthday date was not found. Try again.\n')

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
            print('Contact book was not found. A new one was created.\n')
            return AddressBook()

    return inner
