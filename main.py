# import block
import pickle


# decorators block
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
            return {}

    return inner


# function block

@open_file_error
def load_data(path='data'):
    """
    Read users from the given file using 'pickle' package.
    By default, path = 'data'.
    :param path:
    :return AddressBook:
    """
    with open(path, "rb") as file:
        unpacked = pickle.load(file)
    return unpacked


def update_data(contacts: dict, path='data'):
    """
    Write contacts to the given file using 'pickle' package.
    By default path = 'data'.
    :param contacts:
    :param path:
    :return  None:
    """
    with open(path, "wb") as file:
        pickle.dump(contacts, file)


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


def say_hello(*args, **kwargs):
    """
    Prints a greeting to the command line.
    :param args:
    :param kwargs:
    :return None:
    """
    print("Hello! How can I help you?\n")


# def_main_block

def main():
    contacts = load_data(path='data')
    print("Welcome to the assistant bot!\n")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input) if len(user_input) > 0 else " "
        menu = {
            "hello": say_hello,
        }

        if command in ["close", "exit", "good bye"]:
            print("Good bye!")
            update_data(contacts)
            break
        elif command in menu:
            menu[command](args, contacts)
            update_data(contacts)
        else:
            print("Invalid command.\n")


if __name__ == "__main__":
    main()
