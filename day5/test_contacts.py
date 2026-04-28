import pytest
import json
from pathlib import Path
from contacts import Contact, load_contacts, save_contacts, cmd_add, cmd_delete, cmd_search
import contacts as contacts_module

# Setup & teardown
# This runs before each test - gives us a clean fresh file
@pytest.fixture(autouse=True)
def clean_db(tmp_path, monkeypatch):
    # Point DB_PATH to a temporary file for each test
    import contacts
    test_db = tmp_path / "test_contacts.json"
    monkeypatch.setattr(contacts, "DB_PATH", test_db)
    yield

# Tests
def test_add_contact():
    cmd_add("cheasel", "cheasel@email.com", "0812345678", 30)
    contacts = load_contacts(contacts_module.DB_PATH)
    assert len(contacts) == 1
    assert contacts[0].name == "cheasel"
    assert contacts[0].email == "cheasel@email.com"
    assert contacts[0].age == 30

def test_add_duplicate_email(capsys):
    cmd_add("cheasel", "cheasel@email.com", "0812345678", None)
    cmd_add("cheasel2", "cheasel@email.com", "0899999999", None)
    captured = capsys.readouterr()
    assert "already exists" in captured.out
    # Only 1 contact should exist
    assert len(load_contacts(contacts_module.DB_PATH)) == 1

def test_list_empty(capsys):
    from contacts import cmd_list
    cmd_list()
    captured = capsys.readouterr()
    assert "No contacts yet" in captured.out

def test_search_found(capsys):
    cmd_add("cheasel", "cheasel@email.com", "0812345678", None)
    cmd_add("John", "john@email.com", "0898765432", None)
    capsys.readouterr()
    cmd_search("chea")
    captured = capsys.readouterr()
    assert "cheasel" in captured.out
    assert "John" not in captured.out

def test_search_not_found(capsys):
    cmd_add("cheasel", "cheasel@email.com", "0812345678", None)
    cmd_search("nobody")
    captured = capsys.readouterr()
    assert "No contacts found" in captured.out

def test_delete_contact():
    cmd_add("cheasel", "cheasel@email.com", "0812345678", None)
    cmd_delete("cheasel")
    assert len(load_contacts(contacts_module.DB_PATH)) == 0

def test_delete_not_found(capsys):
    cmd_delete("nobody")
    captured = capsys.readouterr()
    assert "not found" in captured.out