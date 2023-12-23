from collections import defaultdict
from datetime import datetime
from tabulate import tabulate

from yada.address_book import AddressBook, Color


def get_birthdays_per_week(args: list, contacts: AddressBook):
    """
    Gets the contacts of users and print to the console a list of people
    who need to be greeted by days in the next week.
    :param args:
    :param contacts:
    :return None:
    """
    today_date = datetime.today().date()
    birthdays_this_week = defaultdict(list)
    try:
        sought_interval = 7 if not args else int(args[0])
    except ValueError:
        print(
            f"{Color.RED}Enter a command in this format{Color.RESET} --->>>"
            f" {Color.YELLOW}<birthday> <*sought_interval>{Color.RESET}\n")
        return None
    for u_name, record in contacts.data.items():
        name = u_name
        try:
            birthday = record.birthday.birthday
        except AttributeError:
            continue
        birthday_this_year = birthday.replace(year=today_date.year)
        if birthday_this_year < today_date:
            birthday_this_year = birthday.replace(year=today_date.year + 1)
        delta_days = (birthday_this_year - today_date).days
        if delta_days < sought_interval:
            if birthday_this_year.weekday() in [5, 6]:
                birthdays_this_week["Monday"].append(birthday_this_year.strftime('%d/%m'))
                birthdays_this_week["Monday"].append(name.title())
            else:
                birthdays_this_week[birthday_this_year.strftime("%A")].append(birthday_this_year.strftime("%d/%m"))
                birthdays_this_week[birthday_this_year.strftime("%A")].append(name.title())
    if birthdays_this_week:
        headers = [f"{Color.CYAN}Week Day{Color.RESET}", f"{Color.CYAN}Date{Color.RESET}",
                   f"{Color.CYAN}Name{Color.RESET}"]
        data = [[name, birthday[0], birthday[1]] for name, birthday in birthdays_this_week.items()]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)
    else:
        print(f"{Color.GREEN}It seems like no one has a birthday this week{Color.RESET}\n")
