from collections import defaultdict
from datetime import datetime
from address_book import AddressBook


def get_birthdays_per_week(args, contacts: AddressBook):
    """
    Gets the contacts of users and print to the console a list of people
    who need to be greeted by days in the next week.
    :param args:
    :param contacts:
    :return None:
    """
    today_date = datetime.today().date()
    birthdays_this_week = defaultdict(list)
    for n, r in contacts.data.items():
        name = n
        try:
            birthday = r.birthday.birthday
        except AttributeError:
            continue
        birthday_this_year = birthday.replace(year=today_date.year)
        if birthday_this_year < today_date:
            birthday_this_year = birthday.replace(year=today_date.year + 1)
        delta_days = (birthday_this_year - today_date).days
        if delta_days < 7:
            if birthday_this_year.weekday() in [5, 6]:
                birthdays_this_week['Monday'].append(f'{birthday_this_year.strftime("%d/%m")}--> {name}'.title())
            else:
                birthdays_this_week[birthday_this_year.strftime("%A")].append(
                    f'{birthday_this_year.strftime("%d/%m")}--> {name}'.title())
    if birthdays_this_week:
        for k, v in birthdays_this_week.items():
            print(k, v)
        print('')
    else:
        print('It seems like no one has a birthday this week\n')
