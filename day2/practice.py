# f-strings - the modern way to format strings
name = "cheasel"
age = 30
print(f"Hello {name}, you are {age} years old")
print(f"In 10 years you will be {age + 10}")

# List comprehensions - replaces most for loops
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
doubled = [n * 2 for n in numbers]
print(evens)
print(doubled)

# Unpacking
first, *rest = numbers
print(first) # 1
print(rest) # [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Type hints - required for modern backend Python
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

def add(a: int, b: int) -> int:
    return a + b

def is_even(n: int) -> bool:
    return n % 2 == 0

# Default arguments
def greet_with_title(name: str, title: str = "Mr") -> str:
    return f"Hello {title}. {name}"

# Test them
print(greet("cheasel", 30))
print(add(5, 10))
print(is_even(4))
print(is_even(7))
print(greet_with_title("cheasel"))
print(greet_with_title("cheasel", title="Dr"))

from dataclasses import dataclass
from typing import Optional

@dataclass
class Contact:
    name: str
    email: str
    phone: str
    age: Optional[int] = None #Optional means it can be None

# Create some contacts
c1 = Contact(name="cheasel", email="cheasel@email.com", phone="0812345678")
c2 = Contact(name="John", email="John@email.com", phone="0898765432", age=25)

print(c1)
print(c2)
print(c1.name)
print(c2.age)

# A function that takes a Contact and returns a string
def format_contact(contact: Contact) -> str:
    age_info = f", age {contact.age}" if contact.age else ""
    return f"{contact.name} | {contact.email} | {contact.phone}{age_info}"

print(format_contact(c1))
print(format_contact(c2))

# A list of contacts
contacts = [c1, c2]
filtered = [c for c in contacts if "email.com" in c.email]
print(filtered)