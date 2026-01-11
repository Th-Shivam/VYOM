import json
import datetime
from pathlib import Path
import os
from utils.logger import get_logger

class ProductivityManager:
    def __init__(self):
        self.data_dir = Path("Data/Productivity")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.todo_file = self.data_dir / "todos.json"
        self.reminders_file = self.data_dir / "reminders.json"
        self.notes_file = self.data_dir / "notes.json"
        self.logger = get_logger(__name__)
        self._initialize_files()

    def _initialize_files(self):
        """Initialize JSON files if they don't exist"""
        for file in [self.todo_file, self.reminders_file, self.notes_file]:
            if not file.exists():
                with open(file, 'w') as f:
                    json.dump([], f)

    def add_todo(self, task):
        """Add a new todo item"""
        todos = self._read_json(self.todo_file)
        todo = {
            "id": len(todos) + 1,
            "task": task,
            "completed": False,
            "created_at": datetime.datetime.now().isoformat()
        }
        todos.append(todo)
        self._write_json(self.todo_file, todos)
        return f"Added task: {task}"

    def list_todos(self):
        """List all todo items"""
        todos = self._read_json(self.todo_file)
        if not todos:
            return "No tasks in your todo list."
        
        response = "Here are your tasks:\n"
        for todo in todos:
            status = "✓" if todo["completed"] else "□"
            response += f"{status} {todo['task']}\n"
        return response

    def complete_todo(self, task_id):
        """Mark a todo as completed"""
        todos = self._read_json(self.todo_file)
        for todo in todos:
            if todo["id"] == task_id:
                todo["completed"] = True
                self._write_json(self.todo_file, todos)
                return f"Marked task as completed: {todo['task']}"
        return "Task not found."

    def add_reminder(self, task, time):
        """Add a new reminder"""
        reminders = self._read_json(self.reminders_file)
        reminder = {
            "id": len(reminders) + 1,
            "task": task,
            "time": time,
            "created_at": datetime.datetime.now().isoformat()
        }
        reminders.append(reminder)
        self._write_json(self.reminders_file, reminders)
        return f"Added reminder: {task} at {time}"

    def list_reminders(self):
        """List all reminders"""
        reminders = self._read_json(self.reminders_file)
        if not reminders:
            return "No reminders set."
        
        response = "Here are your reminders:\n"
        for reminder in reminders:
            response += f"• {reminder['task']} at {reminder['time']}\n"
        return response

    def add_note(self, title, content):
        """Add a new note"""
        notes = self._read_json(self.notes_file)
        # Clean the title and content
        title = title.strip()
        content = content.strip()
        
        # Check if note with same title already exists
        for note in notes:
            if note["title"].lower().strip() == title.lower().strip():
                return f"Note with title '{title}' already exists"
        
        note = {
            "id": len(notes) + 1,
            "title": title,
            "content": content,
            "created_at": datetime.datetime.now().isoformat()
        }
        notes.append(note)
        self._write_json(self.notes_file, notes)
        return f"Added note: {title}"

    def list_notes(self):
        """List all notes"""
        notes = self._read_json(self.notes_file)
        if not notes:
            return "No notes found."
        
        response = "Here are your notes:\n"
        for note in notes:
            response += f"• {note['title']}\n"
        return response

    def get_note(self, title):
        """Get a specific note by title"""
        notes = self._read_json(self.notes_file)
        for note in notes:
            if note["title"].lower() == title.lower():
                return f"Note: {note['title']}\n{note['content']}"
        return "Note not found."

    def delete_note(self, title):
        """Delete a note by title"""
        notes = self._read_json(self.notes_file)
        self.logger.info(f"Attempting to delete note with title: {title}")
        self.logger.debug(f"Current notes: {[note['title'] for note in notes]}")

        # Convert both the search title and stored titles to lowercase for comparison
        title_lower = title.lower().strip()
        for i, note in enumerate(notes):
            if note["title"].lower().strip() == title_lower:
                deleted_note = notes.pop(i)
                self._write_json(self.notes_file, notes)
                self.logger.info(f"Successfully deleted note: {deleted_note['title']}")
                return f"Deleted note: {deleted_note['title']}"

        self.logger.warning(f"Note not found: {title}")
        return f"Note not found: {title}"

    def delete_todo(self, task_id):
        """Delete a todo by ID"""
        todos = self._read_json(self.todo_file)
        for i, todo in enumerate(todos):
            if todo["id"] == task_id:
                deleted_todo = todos.pop(i)
                # Update IDs of remaining todos
                for j in range(i, len(todos)):
                    todos[j]["id"] = j + 1
                self._write_json(self.todo_file, todos)
                return f"Deleted task: {deleted_todo['task']}"
        return "Task not found."

    def _read_json(self, file):
        """Read JSON file"""
        with open(file, 'r') as f:
            return json.load(f)

    def _write_json(self, file, data):
        """Write to JSON file"""
        with open(file, 'w') as f:
            json.dump(data, f, indent=4) 