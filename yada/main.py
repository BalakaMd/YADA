import pickle
from datetime import datetime
from yada.address_book import Record
from yada.birthday_reminder import get_birthdays_per_week
from yada.notebook import (Notebook, add_note, add_tag_to_note, delete_note, delete_tag,
                           edit_note, search_notes_by_tag, search_notes_by_text, show_all_notes, sort_notes_by_tags)
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate
from yada.exceptions import *
from yada.logo import logo
from yada.jokes import get_joke


# function block

@input_error
def parse_input(user_input: str):
    """
    Takes a string of user input and splits it into words using the split() method.
    It returns the first word as the command "cmd" and the rest as a list of arguments *args.
    :param user_input:
    :return the first word as "cmd" and the rest as a list of arguments:
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    args = [arg.lower() for arg in args]
    return cmd, *args


@input_error
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
        raise AddContactValueError
    if name in contacts:
        user = contacts[name]
        user.add_phone(phone)
    else:
        user = Record(name)
        user.add_phone(phone)
        contacts.add_record(user)


@input_error
def remove_contact(args: list, contacts: AddressBook):
    """
    Removing a contact from the contact AddressBook if exist .
    :param args:
    :param contacts:
    :return None:
    """
    try:
        name = args[0]
    except IndexError:
        raise RemoveContactIndexError

    if name in contacts:
        contacts.delete(name)
        print(f"{Color.GREEN}Contact was deleted successfully.{Color.RESET}\n")
    else:
        raise KeyError


@input_error
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
        raise ChangeContactValueError
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


@input_error
def find_by_name(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found.
    KeyError if the contact does not exist
    :param args:
    :param contacts:
    return The name and phone number if the contact is found.
    KeyError if the contact does not exist :
    """
    data = []
    headers = ["Name", "Phone"]
    try:
        name = args[0]
    except IndexError:
        raise FindNameIndexError
    if name in contacts:
        data.append([name.title(), [phone.value for phone in contacts[name].phones]])
    else:
        raise KeyError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_error
def find_by_phone(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found by phone number.
    KeyError if the contact does not exist
    :param args:
    :param contacts:
    return The name and phone number if the contact is found.
    KeyError if the contact does not exist :
    """
    try:
        if len(args[0]) != 10:
            raise PhoneLengthError
    except IndexError:
        raise FindPhoneIndexError

    data = []
    headers = ["Name", "Phone"]
    result = contacts.find_by_phone(args[0])
    if result is not None:
        data.append([result.name.value.capitalize(), args[0]])
    else:
        raise KeyError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_error
def find_by_birthday(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found by birthday.
    KeyError if the contact does not exist or if the date format is invalid.
    :param args:
    :param contacts:
    return The name and phone number if the contact is found.
    KeyError if the contact does not exist or if the date format is invalid.
    """
    try:
        datetime.strptime(args[0], "%d.%m.%Y")
    except ValueError:
        raise BirthdayFormatError
    except IndexError:
        raise BirthdayIndexError

    data = []
    headers = ["Name", "Birthday"]
    results = contacts.find_by_birthday(args[0])

    if results:
        for result in results:
            data.append([result.name.value.capitalize(), result.birthday])
    else:
        raise BirthdayNotFoundError
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_error
def find_by_email(args: list, contacts: AddressBook):
    """
    Returns the name and birthday if the contact is found by email.
    KeyError if the contact does not exist.
    :param args:
    :param contacts:
    return The name and birthday if the contact is found.
    KeyError if the contact does not exist.
    """
    try:
        email_to_find = args[0]
    except IndexError:
        raise FindEmailIndexError

    data = []
    headers = ["Name", "Email"]
    results = contacts.find_by_email(email_to_find)

    if results:
        for result in results:
            data.append([result.name.value.capitalize(), args[0]])
    else:
        raise KeyError

    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_error
def find_by_address(args: list, contacts: AddressBook):
    """
    Returns the name and birthday if the contact is found by address.
    KeyError if the contact does not exist.
    :param args:
    :param contacts:
    return The name and birthday if the contact is found.
    KeyError if the contact does not exist.
    """
    try:
        address_to_find = args[0]
    except IndexError:
        raise FindBirthdayIndexError

    data = []
    headers = ["Name", "Address"]
    results = contacts.find_by_address(address_to_find)

    if results:
        for result in results:
            search_address = '\n'.join(
                [address.value for address in result.addresses if address_to_find.lower() in address.value.lower()])
            data.append([result.name.value.capitalize(), search_address])
    else:
        raise KeyError

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
    headers = ["Name", "Phones", "Emails", "Birthday", "Addresses"]
    if len(contacts) == 0:
        print(f"{Color.RED}There are still no entries in your notebook. Try making one.\n{Color.RESET}")
    else:
        for name, record in contacts.data.items():
            addresses_str = '\n'.join([address.value for address in record.addresses])
            phones_str = '\n'.join([phone.value for phone in record.phones])
            email_str = '\n'.join([email.value for email in record.emails])

            data.append([name.title(), phones_str, email_str, record.birthday, addresses_str])
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)


@open_file_error
def read_data(path="data"):
    """
    Read users from the given file using "pickle" package.
    By default, path = "data".
    :param path:
    :return AddressBook:
    """
    with open(path, "rb") as file:
        unpacked = pickle.load(file)
    return unpacked


def write_data(contacts: AddressBook, path="data"):
    """
    Write contacts to the given file using "pickle" package.
    By default path = "data".
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
        [1, "add", "<name> <phone number>", "Adding a new contact to the contacts"],
        [2, "change", "<name> <old p_number>\n <new p_number>",
         "Stores in memory a new phone number for the username."],
        [3, "find-phone", "<name>", "Return the name and phone number of contact."],
        [4, "find-name", "<phone>", "Returns the phone number and the contact to whom it belongs."],
        [5, "find-email", "<email>", "Returns the email and the contact to whom it belongs."],
        [6, "find-birthday", "<birthday>", "Returns the names of contacts who have a birthday on this day."],
        [7, "find-address", "<address>", "Returns the name of the contact that has the following address."],
        [8, "all", "", "Return all saved contacts with p_numbers, birthdays and addresses."],
        [9, "add-birthday", "<name> <DD.MM.YYYY>", "Adding a birthday date to the contact."],
        [10, "show-birthday", "<name>", "Return birthday of the requested user from contacts."],
        [11, "birthdays", "", "Print a list of people who need to be greeted by days in the n_week."],
        [12, "add-address", "<name> <country> <city>\n <street> <house_number>", "Adding an address to the contact."],
        [13, "add-note", "<text>", "Adding note to user's notebook."],
        [14, "edit-note", "<id> <text>", "Editing note by id from user's notebook."],
        [15, "delete-note", "<id>", "Deleting note from user's notebook."],
        [16, "search-notes-by-text", "<query>", "Searching notes in user's notebook by specified query."],
        [17, "add-email", "<name> <email address>", "Adding an email to the contact."],
        [18, "edit-email", "<name> <old email address>\n <new email address>", "Changes the email address."],
        [19, "add-tag", "<note id> <tag>", "Adds tag to chosen note."],
        [20, "delete-tag", "<note id> <tag>", "Deletes tag of chosen note."],
        [21, "search-notes-by-tag", "<tag>", "Searching notes in user's notebook by specified tag."],
        [22, "all-notes", "", "Prints all notes for the user."],
        [23, "sort-notes", "", "Prints all notes sorted by tags."],
        [24, "close/Exit", "", "Exit the program."],
        [25, "tell-a-joke", "", "Returns a random joke."]
    ]
    headers = ["#", "Command", "Arguments", "Description"]
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_error
def add_birthday(args, contacts: AddressBook):
    """
    Adds a birthday to the user in contacts.
    :param args:
    :param contacts:
    :raise BirthdayConflictError: if a birthday already exists for the user.
    """
    try:
        name, birthday = args
    except ValueError:
        raise AddBirthdayValueError()

    if name in contacts:
        user = contacts[name]

        if user.birthday != "Unknown":
            raise BirthdayConflictError

        user.add_birthday(birthday)
    else:
        raise BirthdayKeyError


@input_error
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
        raise ShowBirthdayIndexError
    if name in contacts:
        print(
            f"{Color.YELLOW}{name.title()}{Color.RESET}\"s"
            f" birthday is on {Color.WHITE_BOLD}{contacts[name].birthday}\n{Color.RESET}")
    else:
        raise BirthdayKeyError


@input_error
def add_address(args: list, contacts: AddressBook):
    """
    Adds an address to the user in contacts.
    :param args:
    :param contacts:
    :return "Address added." if the addition was successful:
    """
    try:
        name, country, city, street, house_number = args
    except ValueError:
        raise AddAddressValueError()
    if name in contacts:
        user = contacts[name]
        user.add_address(country, city, street, house_number)
        print(f"{Color.GREEN}Address added.{Color.RESET}\n")
    else:
        raise KeyError


@input_error
def add_email(args: list, contacts: AddressBook):
    """
    Adds an email to the user in contacts.
    :param args:
    :param contacts:
    """
    try:
        name, email = args
    except ValueError:
        raise AddEmailValueError()
    if name in contacts:
        user = contacts[name]
        user.add_email(email)
    else:
        raise AttributeError


@input_error
def edit_email(args: list, contacts: AddressBook):
    """
    Edits an email for the user in contacts.
    :param args:
    :param contacts:
    """
    try:
        name, old_email, new_email = args
    except ValueError:
        raise EditEmailValueError()
    if name in contacts:
        user = contacts[name]
        user.edit_email(old_email, new_email)
    else:
        raise KeyError


# main block

def main():
    contacts = read_data()
    notebook = Notebook()
    address_book_menu = {
        "add": add_contact,
        'remove': remove_contact,
        "change": change_contact,
        "find-name": find_by_name,
        "find-phone": find_by_phone,
        "find-email": find_by_email,
        "find-birthday": find_by_birthday,
        "find-address": find_by_address,
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
        "search-notes-by-text": search_notes_by_text,
        "search-notes-by-tag": search_notes_by_tag,
        "delete-note": delete_note,
        "all-notes": show_all_notes,
        "add-tag": add_tag_to_note,
        "delete-tag": delete_tag,
        "sort-notes": sort_notes_by_tags
    }
    menu = list(address_book_menu.keys()) + list(notebook_menu.keys())
    commands_list = list(menu) + ["close", "exit", "good bye", "hello", "tell-a-joke"]
    completer = WordCompleter(commands_list)
    print(logo)
    print(
        f"{Color.MAGENTA_BOLD}Welcome to the assistant bot!{Color.RESET}\nPrint {Color.YELLOW_BOLD}'Help'{Color.RESET}"
        f" to see all commands.\n")
    while True:
        try:
            user_input = prompt("Enter a command: ", completer=completer, complete_while_typing=False)
        except KeyboardInterrupt:
            print(f"You pressed Ctrl+C! Exiting. {Color.YELLOW_BOLD}Good bye!{Color.RESET}")
            write_data(contacts)
            notebook.save_notes()
            break
        command, *args = parse_input(user_input) if len(user_input) > 0 else " "
        if command in ["close", "exit", "good bye"]:
            print(f"{Color.YELLOW_BOLD}Good bye!{Color.RESET}")
            write_data(contacts)
            notebook.save_notes()
            break
        elif command == "hello":
            print("How can I help you?\n")
        elif command in address_book_menu:
            address_book_menu[command](args, contacts)
            write_data(contacts)
        elif command in notebook_menu:
            notebook_menu[command](notebook, args)
            notebook.save_notes()
        elif command == "tell-a-joke":
            print(f'{Color.YELLOW_BOLD}{get_joke()}{Color.RESET}\n')
        else:
            print(f"{Color.RED}Invalid command. Print 'Help' to see all commands.\n{Color.RESET}")


if __name__ == "__main__":
    main()
