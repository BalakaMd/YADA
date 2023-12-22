# YADA

---

# Assistant Bot

## Overview

This Assistant Bot is designed to manage an address book and a notebook for users. It allows users to perform various operations related to contacts (adding, modifying, searching) and note management in a simple and intuitive way.

## Features

- **Address Book Functions**:
  - Add, remove, and modify contacts.
  - Find contacts by name, phone number, email, birthday, or address.
  - Add or edit birthdays, phone numbers, addresses, and emails for contacts.
  - Retrieve a list of all saved contacts with details.
- **Notebook Functions**:
  - Add, edit, delete, and search notes.
  - Add or delete tags for notes.
  - Sort and display notes based on tags.
- **Additional Features**:
  - Ability to receive a random joke for entertainment.

## Requirements

### Python Libraries

- `pickle`
- `datetime`
- `prompt_toolkit`
- `tabulate`
- `wcwidth`

## Usage

1. **Run the Program:**
   - Execute the `main()` function from the `main.py` file.
   ```bash
   python main.py
   ```

2. **Available Commands**:
   - Users can interact with the assistant bot using various commands:
     - `add`: Add a new contact.
     - `remove`: Remove a contact.
     - `change`: Modify contact details.
     - `find-name`, `find-phone`, `find-email`, `find-birthday`, `find-address`: Find contacts by specific parameters.
     - `all`: Retrieve all saved contacts.
     - `help`: Display a list of available commands.

3. **Exiting the Program**:
   - To exit the program, use commands like `close`, `exit`, or `good bye`.

4. **Notebook Commands**:
   - Notebook-related commands like `add-note`, `edit-note`, `search-notes-by-text`, `search-notes-by-tag`, etc., are available for managing notes.

## Contributors

- [Yevhen Havrysh]
- [Andrii Mashtaler]
- [Dmytro Balakin]
- [Andrii Lozinsky]