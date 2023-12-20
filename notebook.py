# models block

NOTES_FILE_NAME = "notes.txt"

# Model Note
class Note:
    """
    Class that represents note in notebook.
    """

    def __init__(self, text, id = None):
        self.text = text
        self.id = id

# Model Notebook
class Notebook:
    """
    Class to manage and store notes in an notebook.
    """

    def __init__(self):
        self.notes = []
        self.load_notes()
        
    def save_notes(self):
        """
        Saving notes into the text file.
        :return None:
        """
        with open(NOTES_FILE_NAME, "w") as file:
            for note in self.notes:
                file.write(f"{note.id}:{note.text}\n")

    def load_notes(self):
        """
        Loads notes from the text file.
        :return None:
        """
        try:
            with open(NOTES_FILE_NAME, "r") as file:
                self.notes = [Note(text = line.rstrip().split(":", 1)[1], id = int(line.split(":", 1)[0])) 
                              for line in file]
        except FileNotFoundError:
            print(f"File with notes {NOTES_FILE_NAME} doesn\'t exist!")
            pass
        
# decorators block
        
def input_error(func):
    """
    Handles exception 'ValueError', 'IndexError' on user input.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            if func.__name__ == 'add_note':
                print("Enter a valid command in this format --->>> add-note <text>\n")
            elif func.__name__ == 'edit_note':
                print("Enter a valid command in format --->>> edit-note <note id> <new text>\n")
            elif func.__name__ == 'delete_note':
                print("Enter a valid command in format --->>> delete-note <note id>\n")
            elif func.__name__ == 'search_notes':
                print("Enter a valid command in format --->>> search-notes <query>\n")

    return inner

# functions block

@input_error
def add_note(notebook, args):
    """
    Adds a note to users notebook.
    :param notebook:
    :param args:
    :return None:
    """
    text = args[0]
    new_id = max([note.id for note in notebook.notes], default = 0) + 1
    notebook.notes.append(Note(text, new_id))
    print(f"Note was added under the id:{new_id}.")
    notebook.save_notes()

@input_error
def edit_note(notebook, args):
    """
    Edits a note in the users notebook.
    :param notebook:
    :param args:
    :return None
    """
    note_id = int(args[0])
    new_text = args[1]
    for note in notebook.notes:
        if note.id == note_id:
            note.text = str(new_text)
            notebook.save_notes()
            print(f"Note {note_id} was edited.")
            return
    print(f"Note with Id:{note_id} doesn't exist.")

@input_error
def search_notes(notebook, args):
    """
    Searches and prints notes in the notebook by a query.
    :param notebook:
    :param args:
    :return None
    """
    count = 0;
    for note in notebook.notes:
        if args[0].lower() in note.text.lower():
            print(f"{note.id}:{note.text}")
            count += 1
    if count == 0:
        print("There are no notes matching specified criteria.")

@input_error
def delete_note(notebook, args):
    """
    Deletes note from user's notebook.
    :param notebook:
    :param note_id:
    """
    note_id = int(args[0])
    initial_length = len(notebook.notes)
    notebook.notes = [note for note in notebook.notes if note.id != note_id]
    if (initial_length == len(notebook.notes)):
        print(f"There is no note with id {note_id}.")
        return
    else:
      notebook.save_notes()
      print(f"Note with Id:{note_id} was deleted.")
