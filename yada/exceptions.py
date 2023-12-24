from yada.address_book import AddressBook, Color


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


class AddAddressValueError(Exception):
    pass


class AddEmailValueError(Exception):
    pass


class EditEmailValueError(Exception):
    pass


class BirthdayIndexError(Exception):
    pass


class ShowBirthdayIndexError(Exception):
    pass


class RemoveContactIndexError(Exception):
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


class FindBirthdayIndexError(Exception):
    pass


class AddNoteError(Exception):
    pass


class EditNoteError(Exception):
    pass


class SearchNoteByTextError(Exception):
    pass


class SearchNoteByTagError(Exception):
    pass


class DeleteNoteError(Exception):
    pass


class AddTagError(Exception):
    pass


class DeleteTagError(Exception):
    pass


# decorators block

def input_note_error(func):
    """
    Handles exception "ValueError", "IndexError" on user input for note functionality.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AddNoteError:
            print(
                f"{Color.RED}Enter a valid command in this format {Color.RESET}--->>>"
                f" {Color.YELLOW}add-note <text>\n{Color.RESET}")
        except EditNoteError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}edit-note <note id> <new text>\n{Color.RESET}")
        except DeleteNoteError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}delete-note <note id>\n{Color.RESET}")
        except SearchNoteByTextError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}search-notes-by-text <query>\n{Color.RESET}")
        except SearchNoteByTagError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}search-notes-by-tag <tag>\n{Color.RESET}")
        except AddTagError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}add-tag <note id> <tag>\n{Color.RESET}")
        except DeleteTagError:
            print(
                f"{Color.RED}Enter a valid command in format {Color.RESET}--->>>"
                f" {Color.YELLOW}delete-tag <note id> <tag>\n{Color.RESET}")

    return inner


def input_error(func):
    """
    Handles exception "ValueError", "KeyError", "IndexError", "AttributeError" on user input.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AddContactValueError:
            print(
                f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<add> <name> <phone number>\n{Color.RESET}")
        except RemoveContactIndexError:
            print(
                f"{Color.RED}Enter a valid command in this format {Color.RESET}--->>>"
                f" {Color.YELLOW}remove <name>\n{Color.RESET}")
        except ChangeContactValueError:
            print(
                f"{Color.RED}Enter a valid command in format{Color.RESET} --->>>"
                f" {Color.YELLOW}<change> <name> <old phone number> <new phone number>\n{Color.RESET}")
        except AddBirthdayValueError:
            print(
                f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<add-birthday> <name> <DD.MM.YYYY.>\n{Color.RESET}")
        except BirthdayConflictError:
            print(f"{Color.RED}Birthday already exists for this contact.{Color.RESET}\n")
        except AddAddressValueError:
            print(
                f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<add-address> <name> <country> <city> <street> <house_number>\n{Color.RESET}")
        except AddEmailValueError:
            print(
                f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<add-email> <name> <email>\n{Color.RESET}")
        except EditEmailValueError:
            print(
                f"{Color.RED}Enter a valid command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<adit-email> <name> <old_email> <new_email>\n{Color.RESET}")
        except KeyError:
            print(f"{Color.RED}This contact was not found in the system. Try again.\n{Color.RESET}")
        except ShowBirthdayIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<show-birthday> <name>\n{Color.RESET}")
        except FindPhoneIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-phone> <name>\n{Color.RESET}")
        except FindNameIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-name> <phone>\n{Color.RESET}")
        except FindEmailIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-email> <email>\n{Color.RESET}")
        except FindAddressIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-address> <city>\n{Color.RESET}")
        except FindBirthdayIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-birthday> <DD.MM.YYYY.>\n{Color.RESET}")
        except PhoneLengthError:
            print(f"{Color.RED}Phone number must be 10 digits long\n{Color.RESET}")
        except BirthdayFormatError:
            print(
                f"{Color.RED}Birthday date must be in this format{Color.RESET} {Color.YELLOW}'DD.MM.YYYY.'\n{Color.RESET}")
        except BirthdayIndexError:
            print(
                f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
                f" {Color.YELLOW}<find-birthday> <'DD.MM.YYYY.'>\n{Color.RESET}")
        except BirthdayKeyError:
            print(f"{Color.RED}This contact was not found in the system. Try again.\n{Color.RESET}")
        except BirthdayNotFoundError:
            print(f"{Color.RED}Contact with this birthday date was not found. Try again.\n{Color.RESET}")

    return inner


def open_file_error(func):
    """
    Handles exception "FileNotFoundError" when trying to open a non-existent file.
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
