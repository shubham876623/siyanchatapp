import os
import json
from datetime import datetime
import uuid

SESSION_DIR = "chat_history"
MAX_SESSIONS = 60

os.makedirs(SESSION_DIR, exist_ok=True)

def list_sessions():
    files = sorted(os.listdir(SESSION_DIR), reverse=True)
    sessions = []
    for f in files:
        try:
            with open(os.path.join(SESSION_DIR, f), "r", encoding="utf-8") as file:
                data = json.load(file)
                title = data.get("title", f)
                sessions.append({"filename": f, "title": title})
        except:
            continue
    return sessions[:MAX_SESSIONS]

def load_session(filename):
    path = os.path.join(SESSION_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"title": "Untitled", "history": []}

def save_session(filename, title, history):
    path = os.path.join(SESSION_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"title": title, "history": history}, file)

def delete_session(filename):
    path = os.path.join(SESSION_DIR, filename)
    if os.path.exists(path):
        os.remove(path)

def create_new_session():
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return f"session_{timestamp}_{uuid.uuid4().hex[:6]}.json"
