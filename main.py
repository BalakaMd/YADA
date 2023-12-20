import pickle
from address_book import AddressBook, Record
from birthday_reminder import get_birthdays_per_week
from notebook import Notebook, add_note, delete_note, edit_note, search_notes
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


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
        except ValueError:
            if func.__name__ == 'add_contact':
                print("Enter a valid command in this format --->>> <add> <name> <phone number>\n")
            elif func.__name__ == 'add_birthday':
                print("Enter a valid command in this format --->>> <add-birthday> <name> <DD.MM.YYYY>\n")
            elif func.__name__ == 'change_contact':
                print("Enter a valid command in format --->>> <change> <name> <old phone number> <new phone number>\n")
        except (KeyError, AttributeError):
            print('This contact was not found in the system. Try again.\n')
        except IndexError:
            if func.__name__ == 'show_birthday':
                print('Enter a command in this format --->>> <show-birthday> <name>\n')
            else:
                print("Enter a command in this format --->>> <phone> <name>\n")

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


# function block

@input_error
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


@input_error
def add_contact(args: list, contacts: AddressBook):
    """
    Adding a new contact to the contact AddressBook.
    If the contact already exists, adds another phone number.
    :param args:
    :param contacts:
    :return "Contact added." if the addition was successful:
    """
    name, phone = args
    if name in contacts:
        user = contacts[name]
        user.add_phone(phone)
    else:
        user = Record(name)
        user.add_phone(phone)
        contacts.add_record(user)


@input_error
def change_contact(args: list, contacts: AddressBook):
    """
    Stores in memory a new phone number for the username contact that already exists in the AddressBook.
    :param args:
    :param contacts: 
    :return "Contact changed." if the changing was successful: 
    """
    name, old_phone, new_phone = args
    if name not in contacts:
        print('Contact not found.\n')
        return None
    for u_name, record in contacts.data.items():
        if u_name == name:
            if record.find_phone(old_phone):
                record.edit_phone(old_phone, new_phone)
                break
            else:
                print('Old phone number not found.\n')


@input_error
def get_phone(args: list, contacts: AddressBook):
    """
    Returns the name and phone number if the contact is found.
    KeyError if the contact does not exist
    :param args:
    :param contacts:
    :return The name and phone number if the contact is found.
    Return KeyError if the contact does not exist :
    """
    name = args[0]
    if name in contacts:
        print(f'{name.title()} phone(\'s) is: {[phone.value for phone in contacts[name].phones]}\n')
    else:
        raise KeyError


def get_all_phones(args, contacts: AddressBook):
    """
    Return all saved contacts with phone numbers and birthdays to the console, if any.
    Addresses are displayed only once in the specified format.
    :param args:
    :param contacts:
    :return all saved contacts:
    """
    if len(contacts) == 0:
        print("There are still no entries in your notebook. Try making one.\n")
    else:
        for name, record in contacts.data.items():
            phone_info = '; '.join([phone.value for phone in record.phones])
            birthday_info = record.birthday if record.birthday != "Unknown" else "Unknown"

            address_info = ''
            if hasattr(record, 'addresses') and record.addresses:
                address_info = f"\nAddresses: {[a.value for a in record.addresses]}"

            print(f"Contact name: {name.title()}, phones: {phone_info}, birthday: {birthday_info}{address_info}\n")


@open_file_error
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


def hello(*args, **kwargs):
    """
    Prints a greeting to the console.
    :param args:
    :param kwargs:
    :return None:
    """
    print("How can I help you?\n")


def user_help(*args, **kwargs):
    """
    Prints a list of all commands to the console.
    :param args:
    :param kwargs:
    :return None:
    """
    print("""
    1. 'Add' <name> <phone number> --> Adding a new contact to the contacts.
    2. 'Change' <name> <old phone number> <new phone number> --> Stores in memory a new phone number for the username.
    3. 'Phone' <name> --> Return the name and phone number of contact.
    4. 'All' --> Return all saved contacts with phone numbers, birthdays and addresses-info.
    6. 'Add-birthday' <name> <DD.MM.YYYY> --> Adding a birthday date to the contact.
    7. 'Show-birthday' <name> --> Return birthday of the requested user from contacts.
    8. 'Birthdays' --> Print a list of people who need to be greeted by days in the next week.
    9. 'add-address' <name> <country> <city> <street> <house number> <apartment number> --> Adding an address to the contact.
    10. 'add-note' <text> --> Adding note to user\'s notebook.
    10. 'edit-note' <id> <text> --> Editing note by id from user\'s notebook.
    10. 'delete-note' <id> --> Deleting note from user\'s notebook.
    11. 'search-notes' <query> --> Searching notes in user\'s notebook by specified query.
    10. 'Close' or 'Exit' --> Exit the program.
        """)


@input_error
def add_birthday(args, contacts: AddressBook):
    """
    Adds a birthday to the user in contacts.
    :param args:
    :param contacts:
    :return raise 'AttributeError' if the name does not exist in contact.:
    """
    name, birthday = args
    if name in contacts:
        user = contacts[name]
        user.add_birthday(birthday)
    else:
        raise AttributeError


@input_error
def show_birthday(args, contacts: AddressBook):
    """
    Print the birthday of the requested user from contacts to the console.
    :param args:
    :param contacts:
    :return Birthday of the requested user:
    """
    name = args[0]
    if name in contacts:
        print(f'{name.title()}\'s birthday is on {contacts[name].birthday}\n')
    else:
        raise KeyError


@input_error
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
        print("Address added.")
    else:
        raise AttributeError


# main block

def main():
    contacts = read_data()
    notebook = Notebook()
    address_book_menu = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "all": get_all_phones,
        "help": user_help,
        'add-birthday': add_birthday,
        'show-birthday': show_birthday,
        'birthdays': get_birthdays_per_week,
        "add-address": add_address,
    }
    notebook_menu = {
            "add-note": add_note, 
            "edit-note": edit_note,
            "search-notes": search_notes,
            "delete-note": delete_note
        }
    menu = list(address_book_menu.keys()) + list(notebook_menu.keys())
    commands_list = list(menu)
    completer = WordCompleter(commands_list)
    print("Welcome to the assistant bot!\nPrint 'Help' to see all commands.\n")
    while True:
        user_input = prompt('Enter a command: ', completer=completer)
        command, *args = parse_input(user_input) if len(user_input) > 0 else " "
        if command in ["close", "exit", "good bye"]:
            print("Good bye!")
            write_data(contacts)
            notebook.save_notes()
            break
        elif command in address_book_menu:
            address_book_menu[command](args, contacts)
            write_data(contacts)
        elif command in notebook_menu:
            notebook_menu[command](notebook, args)
            notebook.save_notes()
        else:
            print("Invalid command. Print 'Help' to see all commands.\n")


if __name__ == "__main__":
    main()
