"""Tools the office assistant agent can call. Data is stored in data.json."""
import json
from datetime import datetime
from pathlib import Path
 
DB = Path(__file__).parent / "data.json"
 
 
def _load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"tasks": [], "meetings": [], "notes": []}
 
 
def _save(data):
    DB.write_text(json.dumps(data, indent=2))
 
 
def get_datetime():
    return {"now": datetime.now().strftime("%A, %Y-%m-%d %H:%M")}
 
 
def add_task(title, due_date=None, priority="medium"):
    data = _load()
    task = {"id": len(data["tasks"]) + 1, "title": title,
            "due_date": due_date, "priority": priority, "done": False}
    data["tasks"].append(task)
    _save(data)
    return {"added": task}
 
 
def list_tasks(show_done=False):
    tasks = _load()["tasks"]
    if not show_done:
        tasks = [t for t in tasks if not t["done"]]
    return {"tasks": tasks}
 
 
def complete_task(task_id):
    data = _load()
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["done"] = True
            _save(data)
            return {"completed": t}
    return {"error": f"Task {task_id} not found"}
 
 
def schedule_meeting(title, date, time, attendees=None):
    data = _load()
    meeting = {"id": len(data["meetings"]) + 1, "title": title, "date": date,
               "time": time, "attendees": attendees or []}
    data["meetings"].append(meeting)
    _save(data)
    return {"scheduled": meeting}
 
 
def list_meetings(date=None):
    meetings = _load()["meetings"]
    if date:
        meetings = [m for m in meetings if m["date"] == date]
    return {"meetings": meetings}
 
 
def save_note(text):
    data = _load()
    note = {"id": len(data["notes"]) + 1, "text": text,
            "created": datetime.now().isoformat(timespec="minutes")}
    data["notes"].append(note)
    _save(data)
    return {"saved": note}
 
 
def search_notes(keyword):
    notes = _load()["notes"]
    return {"matches": [n for n in notes if keyword.lower() in n["text"].lower()]}
 
 
# Registry: name -> function
FUNCTIONS = {
    "get_datetime": get_datetime,
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "schedule_meeting": schedule_meeting,
    "list_meetings": list_meetings,
    "save_note": save_note,
    "search_notes": search_notes,
}
 
# Tool schemas the model sees
TOOL_SCHEMAS = [
    {"name": "get_datetime",
     "description": "Get the current date and time. Use to resolve 'today', 'tomorrow', 'next Monday'.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "add_task",
     "description": "Add a task to the to-do list.",
     "input_schema": {"type": "object", "properties": {
         "title": {"type": "string"},
         "due_date": {"type": "string", "description": "YYYY-MM-DD"},
         "priority": {"type": "string", "enum": ["low", "medium", "high"]}},
         "required": ["title"]}},
    {"name": "list_tasks",
     "description": "List tasks. Hides completed tasks unless show_done is true.",
     "input_schema": {"type": "object", "properties": {"show_done": {"type": "boolean"}}}},
    {"name": "complete_task",
     "description": "Mark a task as done by its id.",
     "input_schema": {"type": "object", "properties": {"task_id": {"type": "integer"}},
                      "required": ["task_id"]}},
    {"name": "schedule_meeting",
     "description": "Schedule a meeting.",
     "input_schema": {"type": "object", "properties": {
         "title": {"type": "string"},
         "date": {"type": "string", "description": "YYYY-MM-DD"},
         "time": {"type": "string", "description": "HH:MM, 24-hour"},
         "attendees": {"type": "array", "items": {"type": "string"}}},
         "required": ["title", "date", "time"]}},
    {"name": "list_meetings",
     "description": "List meetings, optionally for one date.",
     "input_schema": {"type": "object", "properties": {"date": {"type": "string"}}}},
    {"name": "save_note",
     "description": "Save a note or meeting summary for later.",
     "input_schema": {"type": "object", "properties": {"text": {"type": "string"}},
                      "required": ["text"]}},
    {"name": "search_notes",
     "description": "Search saved notes by keyword.",
     "input_schema": {"type": "object", "properties": {"keyword": {"type": "string"}},
                      "required": ["keyword"]}},
]
