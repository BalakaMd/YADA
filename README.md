---

# Assistant Bot

This Python script is an Assistant Bot managing an Address Book with features to add, modify, and retrieve contact information, including phone numbers and birthdays. It allows users to interact via command-line inputs.

## Features

- **Add Contacts**: Add a new contact with a name and phone number.
- **Change Contacts**: Modify existing contact information by changing the phone number.
- **Retrieve Contact Information**: Fetch a contact's phone number.
- **Display All Contacts**: Show all saved contacts along with their phone numbers and birthdays.
- **Add Birthday Information**: Add birthday details for a contact.
- **Show Birthday Information**: Retrieve a contact's birthday.
- **Birthday Reminder**: Lists upcoming birthdays in the next week.

## Dependencies

This code requires the following Python modules:

- `pickle`: Used for serializing and deserializing Python objects.
- `address_book`: Contains classes for managing the address book.
- `birthday_reminder`: Includes functionality for retrieving upcoming birthdays.

## How to Use

1. **Setup**:
    - Ensure the required modules (`address_book`, `birthday_reminder`) are available.
    - Make sure the `data` file exists or is accessible for storing contact information.

2. **Run**:
    - Execute the script by running `python main.py`.
    - The Assistant Bot will start, prompting for commands.

3. **Commands**:
    - Enter commands following the specified formats (e.g., "Add <name> <phone number>").
    - Use 'Help' to view a list of available commands.

4. **Exiting**:
    - To exit the Assistant Bot, use commands such as 'Close', 'Exit', or 'Good bye'.

## Instructions

1. **Command Format**:
    - Commands follow a specific format (e.g., 'Add', 'Change', 'Phone', 'All', etc.).
    - Detailed instructions for each command are available in the 'Help' command.

2. **Error Handling**:
    - The code includes error handling for various input scenarios, providing guidance on correct usage.

3. **Data Persistence**:
    - The Assistant Bot utilizes 'pickle' to save and load contact information to/from the 'data' file.

## Author

This script was developed by [BalakaMd](https://github.com/BalakaMd).

---

