import json
import os
import hashlib

DB_FILE = "db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def image_hash(img):
    return hashlib.md5(img.tobytes()).hexdigest()
