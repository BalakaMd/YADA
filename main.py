# import block


# decorators block


# function block
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
    contacts = {}
    print("Welcome to the assistant bot!\n")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input) if len(user_input) > 0 else " "
        menu = {
            "hello": say_hello,
        }

        if command in ["close", "exit", "good bye"]:
            print("Good bye!")
            break
        elif command in menu:
            menu[command](args, contacts)
        else:
            print("Invalid command.\n")


if __name__ == "__main__":
    main()
