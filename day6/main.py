from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
from pathlib import Path

app = FastAPI(title="Contact Book API", version="1.0.0")

DB_PATH = Path("contacts.json")

# Models
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    age: Optional[int] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    age: Optional[int] = None

# File helpers
def load_contacts() -> list[dict]:
    try:
        return json.loads(DB_PATH.read_text())
    except FileNotFoundError:
        return []
    
def save_contacts(contacts: list[dict]) -> None:
    DB_PATH.write_text(json.dumps(contacts, indent=2))

# Routes
@app.get("/contacts", response_model=list[ContactResponse])
def get_contacts():
    return load_contacts()

@app.post("/contacts", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    contacts = load_contacts()
    # Check duplicate email
    if any(c["email"] == contact.email for c in contacts):
        raise HTTPException(status_code=400, detail="Email already exists")
    # Auto generate id
    new_id = max((c["id"] for c in contacts), default=0) + 1 
    new_contact = {"id": new_id, **contact.model_dump()}
    contacts.append(new_contact)
    save_contacts(contacts)
    return new_contact

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    contacts = load_contacts()
    for c in contacts:
        if c["id"] == contact_id:
            return c
    raise HTTPException(status_code=404, detail="Contact not found")

@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int):
    contacts = load_contacts()
    new_contacts = [c for c in contacts if c["id"] != contact_id]
    if len(new_contacts) == len(contacts):
        raise HTTPException(status_code=404, detail="Contact not found")
    save_contacts(new_contacts)

