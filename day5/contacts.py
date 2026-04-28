import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# Data model
@dataclass
class Contact:
    name: str
    email: str
    phone: str
    age: Optional[int] = None

# File helpers
DB_PATH = Path("contacts.json")

def load_contacts(path: Path = DB_PATH) -> list[Contact]:
    try:
        data = json.loads(path.read_text())
        return [Contact(**c) for c in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: contacts file corrupted, starting fresh")
        return []

def save_contacts(contacts: list[Contact], path: Path = DB_PATH) -> None:
    path.write_text(json.dumps([asdict(c) for c in contacts], indent=2))

# Commands
def cmd_add(name: str, email: str, phone: str, age: Optional[int]) -> None:
    contacts = load_contacts(DB_PATH)
    # Check for duplicate email
    if any(c.email == email for c in contacts):
        print(f"Error: {email} already exists")
        return
    contacts.append(Contact(name=name, email=email, phone=phone, age=age))
    save_contacts(contacts, DB_PATH)
    print(f"Added: {name}")

def cmd_list() -> None:
    contacts = load_contacts(DB_PATH)
    if not contacts:
        print("No contacts yet")
        return
    print(f"\n{len(contacts)} contact(s):\n")
    for c in contacts:
        age_info = f", age {c.age}" if c.age else ""
        print(f"  {c.name} | {c.email} | {c.phone}{age_info}")
    print()

def cmd_search(query: str) -> None:
    contacts = load_contacts(DB_PATH)
    # case-insensitive search by name
    results = [c for c in contacts if query.lower() in c.name.lower()]
    if not results:
        print(f"No contacts found for '{query}'")
        return
    print(f"\n{len(results)} result(s):\n")
    for c in results:
        age_info = f", age {c.age}" if c.age else ""
        print(f"  {c.name} | {c.email} | {c.phone}{age_info}")
    print()

def cmd_delete(name: str) -> None:
    contacts = load_contacts(DB_PATH)
    original_count = len(contacts)
    contacts = [c for c in contacts if c.name.lower() != name.lower()]
    if len(contacts) == original_count:
        print(f"Error: '{name}' not found")
        return
    save_contacts(contacts, DB_PATH)
    print(f"Deleted: {name}")


# Main entry point
def main():
    parser = argparse.ArgumentParser(description="Contact Book CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a contact")
    add_parser.add_argument("name")
    add_parser.add_argument("email")
    add_parser.add_argument("phone")
    add_parser.add_argument("--age", type=int, default=None)

    # list command
    subparsers.add_parser("list", help="List all contacts")

    # search command
    search_parser = subparsers.add_parser("search", help="Search contacts by name")
    search_parser.add_argument("query")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a contact by name")
    delete_parser.add_argument("name")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.name, args.email, args.phone, args.age)
    elif args.command == "list":
        cmd_list()
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "delete":
        cmd_delete(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
