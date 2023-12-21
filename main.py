import pickle
from datetime import datetime
from address_book import AddressBook, Record, Color
from birthday_reminder import get_birthdays_per_week
from notebook import Notebook, add_note, delete_note, edit_note, search_notes
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate
import exceptions


# function block

@exceptions.input_error
def parse_input(user_input: str):
    """
    Takes a string of user input and splits it into words using the split() method.
    It returns the first word as the command 'cmd' and the rest as a list of arguments *args.
    :param user_input:
    :return the first word as 'cmd' and the rest as a list of arguments:
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@exceptions.input_error
def add_contact(args: list, contacts: AddressBook):
    """
    Adding a new contact to the contact AddressBook.
    If the contact already exists, adds another phone number.
    :param args:
    :param contacts:
    :return "Contact added." if the addition was successful:
    """
    try:
        name, phone = args
    except ValueError:
        raise exceptions.AddContactValueError
    if name in contacts:
        user = contacts[name]
        user.add_phone(phone)
    else:
        user = Record(name)
        user.add_phone(phone)
        contacts.add_record(user)


@exceptions.input_error
def change_contact(args: list, contacts: AddressBook):
    """
    Stores in memory a new phone number for the username contact that already exists in the AddressBook.
    :param args:
    :param contacts: 
    :return "Contact changed." if the changing was successful: 
    """
    try:
        name, old_phone, new_phone = args
    except ValueError:
        raise exceptions.ChangeContactValueError
    if name not in contacts:
        print(f"{Color.RED}Contact not found.\n{Color.RESET}")
        return None
    for u_name, record in contacts.data.items():
        if u_name == name:
            if record.find_phone(old_phone):
                record.edit_phone(old_phone, new_phone)
                break
            else:
                print(f"{Color.RED}Old phone number not found.\n{Color.RESET}")


@exceptions.input_error
def find_by_name(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found.
    KeyError if the contact does not exist
    :param args:
    :param contacts:
    :return The name and phone number if the contact is found.
    Return KeyError if the contact does not exist :
    """
    data = []
    headers = ["Name", "Phone"]
    try:
        name = args[0]
    except IndexError:
        raise exceptions.FindNameIndexError
    if name in contacts:
        data.append([name.title(), [phone.value for phone in contacts[name].phones]])
    else:
        raise KeyError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@exceptions.input_error
def find_by_phone(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found by phone number.
    KeyError if the contact does not exist
    :param args:
    :param contacts:
    :return The name and phone number if the contact is found.
    Return KeyError if the contact does not exist :
    """
    try:
        if len(args[0]) != 10:
            raise exceptions.PhoneLengthError
    except IndexError:
        raise exceptions.FindPhoneIndexError

    data = []
    headers = ["Name", "Phone"]
    result = contacts.find_by_phone(args[0])
    if result is not None:
        data.append([result.name.value.capitalize(), args[0]])
    else:
        raise KeyError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@exceptions.input_error
def find_by_birthday(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found by birthday.
    KeyError if the contact does not exist or if the date format is invalid.
    :param args:
    :param contacts:
    :return The name and phone number if the contact is found.
    Return KeyError if the contact does not exist or if the date format is invalid.
    """
    try:
        datetime.strptime(args[0], '%d.%m.%Y')
    except ValueError:
        raise exceptions.BirthdayFormatError
    except IndexError:
        raise exceptions.BirthdayIndexError

    data = []
    headers = ["Name", "Birthday"]
    results = contacts.find_by_birthday(args[0])

    if results:
        for result in results:
            data.append([result.name.value.capitalize(), result.birthday])
    else:
        raise exceptions.BirthdayNotFoundError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


def get_all_phones(args, contacts: AddressBook):
    """
    Return all saved contacts with phone numbers and birthdays to the console, if any.
    Addresses are displayed only once in the specified format.
    :param args:
    :param contacts:
    :return all saved contacts:
    """
    data = []
    headers = ["Name", "Phones", "Birthday", "Addresses"]
    if len(contacts) == 0:
        print(f"{Color.RED}There are still no entries in your notebook. Try making one.\n{Color.RESET}")
    else:
        for name, record in contacts.data.items():
            data.append([name.title(), [phone.value for phone in record.phones], record.birthday, record.addresses])
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)


@exceptions.open_file_error
def read_data(path='data'):
    """
    Read users from the given file using 'pickle' package.
    By default, path = 'data'.
    :param path:
    :return AddressBook:
    """
    with open(path, "rb") as file:
        unpacked = pickle.load(file)
    return unpacked


def write_data(contacts: AddressBook, path='data'):
    """
    Write contacts to the given file using 'pickle' package.
    By default path = 'data'.
    :param contacts:
    :param path:
    :return  None:
    """
    with open(path, "wb") as file:
        pickle.dump(contacts, file)


def user_help(*args, **kwargs):
    """
    Prints a list of all commands to the console.
    :param args:
    :param kwargs:
    :return None:
    """
    data = [
        [1, 'add', '<name> <phone number>', 'Adding a new contact to the contacts'],
        [2, 'change', '<name> <old p_number> <new p_number>',
         'Stores in memory a new phone number for the username.'],
        [3, 'find-phone', '<name>', 'Return the name and phone number of contact.'],
        [4, 'find-name', '<phone>', 'Returns the phone number and the contact to whom it belongs.'],
        [5, 'find-birthday', '<birthday>', 'Returns the names of contacts who have a birthday on this day.'],
        [6, 'all', '', 'Return all saved contacts with p_numbers, birthdays and addresses.'],
        [7, 'add-birthday', '<name> <DD.MM.YYYY>', 'Adding a birthday date to the contact.'],
        [8, 'show-birthday', '<name>', 'Return birthday of the requested user from contacts.'],
        [9, 'birthdays', '', 'Print a list of people who need to be greeted by days in the n_week.'],
        [10, 'add-address', '<name> <country> <city> <...>', 'Adding an address to the contact.'],
        [11, 'add-note', '<text>', "Adding note to user's notebook."],
        [12, 'edit-note', '<id> <text>', "Editing note by id from user's notebook."],
        [13, 'delete-note', '<id>', "Deleting note from user's notebook."],
        [14, 'search-notes', '<query>', "Searching notes in user's notebook by specified query."],
        [15, 'close/Exit', '', "Exit the program."],
        [16, 'add-email', '<name> <email address>', "Adding an email to the contact."],
        [17, 'edit-email', '<name> <old email address> <new email address>', "Changes the email address"]
    ]
    headers = ["#", "Command", "Arguments", "Description"]
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@exceptions.input_error
def add_birthday(args, contacts: AddressBook):
    """
    Adds a birthday to the user in contacts.
    :param args:
    :param contacts:
    :return raise 'AttributeError' if the name does not exist in contact.:
    """
    try:
        name, birthday = args
    except ValueError:
        raise exceptions.AddBirthdayValueError()
    if name in contacts:
        user = contacts[name]
        user.add_birthday(birthday)
    else:
        raise exceptions.BirthdayKeyError


@exceptions.input_error
def show_birthday(args, contacts: AddressBook):
    """
    Print the birthday of the requested user from contacts to the console.
    :param args:
    :param contacts:
    :return Birthday of the requested user:
    """
    try:
        name = args[0]
    except IndexError:
        raise exceptions.ShowBirthdayIndexError
    if name in contacts:
        print(
            f'{Color.YELLOW}{name.title()}{Color.RESET}\'s birthday is on {Color.WHITE_BOLD}{contacts[name].birthday}\n{Color.RESET}')
    else:
        raise exceptions.BirthdayKeyError


@exceptions.input_error
def add_address(args: list, contacts: AddressBook):
    """
    Adds an address to the user in contacts.
    :param args:
    :param contacts:
    :return "Address added." if the addition was successful:
    """
    name, country, city, street, house_number, apartment_number = args
    if name in contacts:
        user = contacts[name]
        user.add_address(country, city, street, house_number, apartment_number)
        print(f"{Color.GREEN}Address added.{Color.RESET}")
    else:
        raise AttributeError


@exceptions.input_error
def add_email(args: list, contacts: AddressBook):
    """
    Adds an email to the user in contacts.
    :param args:
    :param contacts:
    """
    name, email = args
    if name in contacts:
        user = contacts[name]
        user.add_email(email)
        write_data(contacts)
    else:
        raise AttributeError


@exceptions.input_error
def edit_email(args: list, contacts: AddressBook):
    """
    Edits an email for the user in contacts.
    :param args:
    :param contacts:
    """
    name, old_email, new_email = args
    if name in contacts:
        user = contacts[name]
        user.edit_email(old_email, new_email)
        write_data(contacts)
    else:
        raise AttributeError


# main block

def main():
    contacts = read_data()
    notebook = Notebook()
    address_book_menu = {
        "add": add_contact,
        "change": change_contact,
        "find-name": find_by_name,
        "find-phone": find_by_phone,
        "find-birthday": find_by_birthday,
        "all": get_all_phones,
        "help": user_help,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_birthdays_per_week,
        "add-address": add_address,
        "add-email": add_email,
        "edit-email": edit_email,
    }
    notebook_menu = {
        "add-note": add_note,
        "edit-note": edit_note,
        "search-notes": search_notes,
        "delete-note": delete_note
    }
    menu = list(address_book_menu.keys()) + list(notebook_menu.keys())
    commands_list = list(menu) + ["close", "exit", "good bye", 'hello']
    completer = WordCompleter(commands_list)
    print(
        f"{Color.MAGENTA_BOLD}Welcome to the assistant bot!{Color.RESET}\nPrint {Color.YELLOW_BOLD}'Help'{Color.RESET} to see all commands.\n")
    while True:
        user_input = prompt('Enter a command: ', completer=completer, complete_while_typing=False)
        command, *args = parse_input(user_input) if len(user_input) > 0 else " "
        if command in ["close", "exit", "good bye"]:
            print(f"{Color.YELLOW_BOLD}Good bye!{Color.RESET}")
            write_data(contacts)
            notebook.save_notes()
            break
        elif command == 'hello':
            print("How can I help you?\n")
        elif command in address_book_menu:
            address_book_menu[command](args, contacts)
            write_data(contacts)
        elif command in notebook_menu:
            notebook_menu[command](notebook, args)
            notebook.save_notes()
        else:
            print(f"{Color.RED}Invalid command. Print 'Help' to see all commands.\n{Color.RESET}")


if __name__ == "__main__":
    main()
