from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_contact_by_email(contact_email: str, db: Session):
    contacts = db.query(Contact).filter_by(last_name=contact_email).all()
    return contacts


async def find_contact_by_firstname(contact_firstname: str, db: Session):
    contacts = db.query(Contact).filter_by(first_name=contact_firstname).all()
    return contacts


async def find_contact_by_lastname(contact_lastname: str, db: Session):
    contacts = db.query(Contact).filter_by(last_name=contact_lastname).all()
    return contacts


async def find_contacts_birthday(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)
    birthday_list = []
    contacts = db.query(Contact).all()
    for contact in contacts:
        current_year_birthdays = contact.date_of_birth.replace(year=today.year)
        if today <= current_year_birthdays <= end_date:
            birthday_list.append(contact)
    return birthday_list