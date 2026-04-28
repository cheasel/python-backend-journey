# Contact Book CLI

A command-line contact manager built with Python.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pytest
```

## Usage

```bash
# Add a contact
python contacts.py add "Name" "email@example.com" "0812345678"
python contacts.py add "Name" "email@example.com" "0812345678" --age 30

# List all contacts
python contacts.py list

# Search by name
python contacts.py search "Name"

# Delete a contact
python contacts.py delete "Name"
```

## Run tests

```bash
pytest test_contacts.py -v
```

## Built with

- Python 3.13
- argparse — CLI parsing
- dataclasses — data modeling
- pathlib — file handling
- pytest — testing