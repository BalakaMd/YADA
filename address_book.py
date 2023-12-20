from collections import UserDict
from datetime import date
import re

#Colors
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    YELLOW_BOLD = "\033[93;1m"  
    BLUE_BOLD = "\033[94;1m"    
    MAGENTA_BOLD = "\033[95;1m" 
    CYAN_BOLD = "\033[96;1m"    
    WHITE_BOLD = "\033[97;1m"  

def data_validator(func):
    """
    Wrapper function.
    Validates a phone number and birthday date in special format.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        """
        Handles exception 'ValueError' if the phone number or birthday is in incorrect format.
        :param args:
        :param kwargs:
        :return None:
        """
        try:
            func(*args, **kwargs)
        except ValueError:
            if func.__name__ == 'add_birthday':
                # print("Birthday date must in this format 'DD.MM.YYYY'\n")
                print(f"{Color.RED}Birthday date must in this format 'DD.MM.YYYY'\n{Color.RESET}")
            else:
                # print("Phone number must be 10 digits long\n")
                print(f"{Color.RED}Phone number must be 10 digits long\n{Color.RESET}")

    return inner


class Field:
    """
    Base class for record fields.
    """

    def __init__(self, value: str):
        """
        Initializes a Field object with a given value.
        :param value:
        """
        self.value = value

    def __str__(self):
        """
        Returns the string representation of the field value.
        :return str(self.value):
        """
        return str(self.value)


class Name(Field):
    """
    Class to store contact names. Mandatory field.
    """

    def __init__(self, value: str):
        super().__init__(value)
        self.name = value


class Phone(Field):
    """
    Class to store phone numbers. Validates the phone number using
    validate_phone_number function for thr required format (10 digits).
    """

    def __init__(self, value: str):
        """
        Initializes a Phone object with a given value.
        :param value:
        """
        super().__init__(value)
        self.phone = self.validate_phone_number()

    def validate_phone_number(self):
        """
        Validates the required format (10 digits) of the phone number.
        :return: Raises 'ValueError' if the phone number format is invalid.
        """
        if re.findall(r'^\d{10}$', str(self.value.replace('+38', ''))):
            # print("Contacts updated.\n")
            print(f"{Color.GREEN}Contacts updated.\n{Color.RESET}")
            return self.value
        else:
            # raise ValueError("Phone number must be 10 digits long.")
            raise ValueError(f"{Color.RED}Phone number must be 10 digits long.\n{Color.RESET}")



class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.birthday = self.validate_birthday()

    def validate_birthday(self):
        date_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
        """
        Validates the required format (DD.MM.YYYY) of the birthday date.
        :return: Raises 'ValueError' if the birthday date format is invalid.
        """
        if date_pattern.match(self.value):
            day, month, year = self.value.split('.')
            if int(day) <= 31 and int(month) <= 12:
                print("Birthday added.\n")
                return date(int(year), int(month), int(day))
            # print("Birthday date must in this format 'DD.MM.YYYY'\n")
            print(f"{Color.RED}Birthday date must in this format 'DD.MM.YYYY'\n{Color.RESET}")
        else:
            # raise ValueError("Birthday date must in this format 'DD.MM.YYYY'")
            raise ValueError(f"{Color.RED}Birthday date must in this format 'DD.MM.YYYY'{Color.RESET}")


#CLASS Address
class Address(Field):
    def __init__(self, country: str, city: str, street: str, house_number: str, apartment_number: str = ''):
        super().__init__(f"Country: {country}, City: {city}, Street: {street}, House_Number: {house_number}, Apartment_Number: {apartment_number}")
        self.country = country
        self.city = city
        self.street = street
        self.house_number = house_number
        self.apartment_number = apartment_number
    
    def __str__(self):
        return f"Country: {self.country}, City: {self.city}, Street: {self.street}, House_Number: {self.house_number}, Apartment_Number: {self.apartment_number}"

class Email(Field):
    """
    Class to store email addresses. Validates the email using a regular expression.
    """

    def __init__(self, value: str):
        """
        Initializes an Email object with a given value.
        :param value:
        """
        super().__init__(value)
        self.email = self.validate_email()

    def validate_email(self):
        """
        Validates the email address using a regular expression.
        :return: Raises 'ValueError' if the email format is invalid.
        """
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if email_pattern.match(self.value):
            return self.value
        else:
            # raise ValueError("Invalid email address.")
            raise ValueError(f"{Color.RED}Invalid email address.{Color.RESET}")

    def set_email(self, value: str):
        """
        Set a new email address and validate it.
        :param value:
        :return: None
        """
        self.value = value
        self.email = self.validate_email()
        
    def __str__(self):
        return f"Email: {self.email}"

class Record:
    """
    Class to store contact information including name and phone numbers.
    """

    def __init__(self, name: str):
        """
        Initializes a Record object with a given name.
        :param name:
        """
        self.name = Name(name.lower())
        self.phones = []
        self.birthday = 'Unknown'
        self.addresses = []  # Add addresses attribute
        self.emails = []  # Add emails attribute

    @data_validator
    def add_phone(self, phone: str):
        """
        Adds a phone number to the contact.
        :param phone:
        :return None:
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number: str):
        """
        Removes a phone number from the contact.
        :param phone_number:
        :return None:
        """
        for p in self.phones:
            if p.value == phone_number:
                self.phones.remove(p)

    @data_validator
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        """
        Edits a phone number in the phone list.
        :param old_phone_number:
        :param new_phone_number:
        :return None:
        """
        for p in self.phones:
            if p.value == old_phone_number:
                p.value = str(Phone(str(new_phone_number)))

    def find_phone(self, phone_number: str):
        """
        Searches for a specific phone number in the contact.
        :param phone_number:
        :return phone_number if found, None otherwise:
        """
        for p in self.phones:
            if p.value == phone_number:
                return phone_number

    @data_validator
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
    
    # Add addresses attribute
    @data_validator
    def add_address(self, country, city, street, house_number, apartment_number):
        self.addresses.append(Address(country, city, street, house_number, apartment_number))
        
    @data_validator
    def add_email(self, email: str):
        """
        Adds an email address to the contact.
        :param email:
        :return None:
        """
        try:
            new_email = Email(email)
            self.emails.append(new_email)
            # print("Email added.")
            print(f"{Color.GREEN}Email added.{Color.RESET}")
        except ValueError as e:
            # print(f"Error: {e}")
            print(f"{Color.RED}Error{Color.RESET}: {e}")

            
    def edit_email(self, old_email: str, new_email: str):
        """
        Edits an email address in the email list.
        :param old_email:
        :param new_email:
        :return None:
        """
        for e in self.emails:
            if e.value == old_email:
                e.set_email(new_email)
                # print("Email updated.")
                print(f"{Color.GREEN}Email updated.{Color.RESET}")
                break
        else:
            # print("Old email not found.")
            print(f"{Color.RED}Old email not found.{Color.RESET}")


    def __str__(self):
        phone_info = '; '.join([p.value for p in self.phones])
        birthday_info = self.birthday if self.birthday != "Unknown" else "Unknown"
        address_info = '; '.join([a.value for a in getattr(self, 'addresses', [])]) if hasattr(self, 'addresses') else "Unknown"

        return f"Contact name: {self.name}, phones: {phone_info}, birthday: {birthday_info}, addresses: {address_info}"

class AddressBook(UserDict):
    """
    Class to manage and store records in an address book.
    """

    def add_record(self, user: Record):
        """
        Adds a record to the address book.
        :param user:
        :return None:
        """
        self.data[user.name.value] = user

    def find(self, name: str):
        """
        Finds a record in the address book by name.
        :param name:
        :return returns the string representation of the contact information:
        """
        return f'{self.data.get(name.lower())}\n'

    def delete(self, name: str):
        """
        Deletes a record from the address book by name.
        :param name:
        :return None:
        """
        if name.lower() in self.data:
            del self.data[name.lower()]
