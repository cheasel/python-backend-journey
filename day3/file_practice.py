from pathlib import Path

# pathlib is the modern way - forget os.path 
# Path works on Windows AND Mac/Linux automatically

# Create a path object
file_path = Path("notes.txt")

# Write to the file
file_path.write_text("Hello from Python!\nThis is line 2\nThis is line 3")

# Read it back
content = file_path.read_text()
print(content)

# Check if file exists
print(f"File exists: {file_path.exists()}")
print(f"File size: {file_path.stat().st_size} bytes")

# Read line by line
lines = content.splitlines()
for i, line in enumerate(lines):
    print(f"Line {i+1}: {line}")

import json

# Python dict -> JSON file (this is how you SAVE data)
contacts = [
    {"name": "cheasel", "email": "cheasel@email.com", "phone": "0812345678"},
    {"name": "John", "email": "John@email.com", "phone": "0898765432"}
]

json_path = Path("contacts.json")

# Write JSON to file
json_path.write_text(json.dumps(contacts, indent=2))
print("Saved contacts.json")

# Read JSON back from file (this is how you LOAD data)
loaded = json.loads(json_path.read_text())
print(f"Loaded {len(loaded)} contacts")

for contact in loaded:
    print(f"  - {contact['name']} | {contact['email']}")

# Add a new contact and save again
loaded.append({"name": "Sarah", "email": "sarah@email.com", "phone": "0891111111"})
json_path.write_text(json.dumps(loaded, indent=2))
print(f"Now we have {len(loaded)} contacts")

# Error handling — never let your program crash without a useful message

# BAD — this crashes with an ugly error
# data = Path("missing.json").read_text()

# GOOD — handle it gracefully
def load_contacts(path: Path) -> list:
    try:
        content = path.read_text()
        return json.loads(content)
    except FileNotFoundError:
        print(f"File {path} not found — starting with empty list")
        return []
    except json.JSONDecodeError:
        print(f"File {path} is corrupted — starting with empty list")
        return []

def save_contacts(path: Path, contacts: list) -> None:
    try:
        path.write_text(json.dumps(contacts, indent=2))
        print(f"Saved {len(contacts)} contacts")
    except PermissionError:
        print(f"Cannot write to {path} — permission denied")

# Test with existing file
existing = load_contacts(Path("contacts.json"))
print(f"Loaded: {len(existing)} contacts")

# Test with missing file — won't crash!
missing = load_contacts(Path("doesnt_exist.json"))
print(f"Missing file returned: {missing}")

# Save back
save_contacts(Path("contacts.json"), existing)