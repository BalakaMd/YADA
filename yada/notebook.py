# models block
from tabulate import tabulate
from yada.address_book import Color
from yada.exceptions import (AddNoteError, AddTagError,
                             DeleteNoteError, DeleteTagError, EditNoteError, SearchNoteByTagError,
                             SearchNoteByTextError, input_note_error)

NOTES_FILE_NAME = "notes.txt"


# Model Note
class Note:
    """
    Class that represents note in notebook.
    """

    def __init__(self, text, note_id=None, tags=None):
        self.text = text
        self.id = note_id
        self.tags = tags if tags else []

    def add_tag(self, tag):
        """
        Adds a new tag to the note.
        """
        if tag not in self.tags:
            self.tags.append(str(tag))

    def delete_tag(self, tag_to_delete):
        """
        Deletes a selected tag from the note's tags.
        """
        initial_tag_length = len(self.tags)
        self.tags = [tag for tag in self.tags if tag != tag_to_delete]
        return initial_tag_length != len(self.tags)


# Model Notebook
class Notebook:
    """
    Class to manage and store notes in a notebook.
    """

    def __init__(self):
        self.notes = []
        self.load_notes()

    def save_notes(self):
        with open(NOTES_FILE_NAME, "w") as file:
            for note in self.notes:
                tags_str = ", ".join(note.tags)
                file.write(f"{tags_str}\n{note.id}:{note.text}\n")

    def load_notes(self):
        try:
            with open(NOTES_FILE_NAME, "r") as file:
                self.notes = []
                lines = file.readlines()
                for i in range(0, len(lines), 2):
                    tags_line = lines[i].strip()
                    note_line = lines[i + 1].strip()

                    tags = [tag.strip() for tag in tags_line.split(",") if tag.strip()]

                    note_id, text = note_line.split(":", 1)
                    self.notes.append(Note(text=text, note_id=int(note_id), tags=tags))
        except FileNotFoundError:
            print(f"{Color.RED}File with notes {NOTES_FILE_NAME} doesn't exist! A new one was created{Color.RESET}\n")

    def find_note_by_id(self, note_id):
        """
        Finds a note by its ID.
        :param note_id: ID of the note to find.
        :return: Note object or None if not found.
        """
        for note in self.notes:
            if int(note.id) == int(note_id):
                return note
        return None


# functions block

@input_note_error
def add_note(notebook, args):
    """
    Adds a note to users notebook.
    :param notebook:
    :param args:
    :return None:
    """
    try:
        text = args[0]
        new_id = max([note.id for note in notebook.notes], default=0) + 1
        notebook.notes.append(Note(text, new_id))
        print(f"{Color.GREEN}Note was added under the id:{new_id}.{Color.RESET}\n")
        notebook.save_notes()
    except (ValueError, IndexError):
        raise AddNoteError


@input_note_error
def edit_note(notebook, args):
    """
    Edits a note in the users' notebook.
    :param notebook:
    :param args:
    return None
    """
    try:
        note_id = int(args[0])
        new_text = args[1]
        for note in notebook.notes:
            if note.id == note_id:
                note.text = str(new_text)
                notebook.save_notes()
                print(f"Note {note_id} was edited.\n")
                return
        print(f"Note with Id:{note_id} doesn't exist.\n")
    except (ValueError, IndexError):
        raise EditNoteError


@input_note_error
def search_notes_by_text(notebook, args):
    """
    Searches and prints notes in the notebook by a query.
    :param notebook:
    :param args:
    return None
    """
    try:
        data = []
        count = 0
        for note in notebook.notes:
            if args[0].lower() in note.text.lower():
                tags_str = ", ".join(note.tags)
                data.append([note.id, str(tags_str), note.text])
                count += 1
        if count == 0:
            print(f"{Color.RED}There are no notes matching specified criteria.{Color.RESET}\n")
            return
        headers = ["Id", "Tags", "Note Text"]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)
    except (ValueError, IndexError):
        raise SearchNoteByTextError


@input_note_error
def search_notes_by_tag(notebook, args):
    """
    Searches and prints notes in the notebook by a query.
    :param notebook:
    :param args:
    return None
    """
    try:
        data = []
        count = 0
        for note in notebook.notes:
            for tag in note.tags:
                if str(tag.lower()) == args[0].lower():
                    tags_str = ", ".join(note.tags)
                    data.append([note.id, str(tags_str), note.text])
                    count += 1
        if count == 0:
            print(f"{Color.RED}There are no notes matching specified criteria.{Color.RESET}\n")
            return
        headers = ["Id", "Tags", "Note Text"]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print(table)
    except (ValueError, IndexError):
        raise SearchNoteByTagError


@input_note_error
def delete_note(notebook, args):
    """
    Deletes note from user's notebook.
    :param notebook:
    :param args:
    """
    try:
        note_id = int(args[0])
        initial_length = len(notebook.notes)
        notebook.notes = [note for note in notebook.notes if note.id != note_id]
        if initial_length == len(notebook.notes):
            print(f"There is no note with id {note_id}.\n")
            return
        else:
            notebook.save_notes()
            print(f"Note with Id:{note_id} was deleted.\n")
    except (ValueError, IndexError):
        raise DeleteNoteError


@input_note_error
def show_all_notes(notebook, args):
    """
    Displays all notes in the notebook.
    :return None:
    """
    if not notebook.notes:
        print(f"{Color.RED}There are no notes in the notebook.{Color.RESET}\n")
        return
    data = []
    headers = ["Id", "Tags", "Note Text"]
    for note in notebook.notes:
        tags_str = ''
        if len(note.tags) != 0:
            tags_str = ", ".join(note.tags)
        data.append([note.id, str(tags_str), note.text])
    table = tabulate(data, headers=headers, tablefmt="fancy_grid")
    print(table)


@input_note_error
def add_tag_to_note(notebook, args):
    """
    Adds a tag to a specific note.
    :param notebook:
    :param args:
    """
    try:
        note_id = args[0]
        tag = str(args[1])
        note = notebook.find_note_by_id(note_id)
        if note:
            note.add_tag(tag)
            notebook.save_notes()
            print(f"{Color.GREEN}Tag '{tag}' added to note ID {note_id}.{Color.RESET}\n")
        else:
            print(f"{Color.RED}Note with ID {note_id} not found.{Color.RESET}\n")
    except (ValueError, IndexError):
        raise AddTagError


@input_note_error
def delete_tag(notebook, args):
    """
    Edits tags of a specific note.
    :param notebook:
    :param args:
    """
    try:
        note_id = args[0]
        tag = args[1]
        note = notebook.find_note_by_id(note_id)
        if note:
            result = note.delete_tag(str(tag))
            notebook.save_notes()
            if result:
                print(f"{Color.GREEN}Tag {str(tag)} of note ID {note_id} deleted.{Color.RESET}\n")
            else:
                print(f"{Color.RED}No tag {str(tag)} found in note ID {note_id}.{Color.RESET}\n")
        else:
            print(f"{Color.RED}Note with ID {note_id} not found.{Color.RESET}\n")
    except (ValueError, IndexError):
        raise DeleteTagError


def sort_notes_by_tags(notebook, args):
    """
    Sorts notes by their tags and prints them.
    """
    if not notebook.notes:
        print(f"{Color.RED}There are no notes in the notebook.{Color.RESET}\n")
        return
    sorted_by_tags = {}
    for note in notebook.notes:
        for tag in note.tags:
            if tag not in sorted_by_tags:
                sorted_by_tags[tag] = []
            sorted_by_tags[tag].append(note)

    for tag, notes in sorted_by_tags.items():
        print(f"{Color.GREEN}Tag: {tag}{Color.RESET}")
        for note in notes:
            print(f" - ID: {note.id}, Text: {note.text}")
