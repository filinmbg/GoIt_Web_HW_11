from typing import List

from fastapi import Depends, Query, Path, HTTPException, status, APIRouter
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel


router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists!")
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body,  db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.get("/find/{contact_email}", response_model=List[ContactResponse])
async def find_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.find_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.get("/find/{contact_firstname}", response_model=List[ContactResponse])
async def find_contact_by_firstname(contact_firstname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.find_contact_by_firstname(contact_firstname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.get("/find/{contact_lastname}", response_model=List[ContactResponse])
async def find_contact_by_lastname(contact_lastname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.find_contact_by_lastname(contact_lastname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.get("/birthday", response_model=List[ContactResponse])
async def find_contacts_birthday(db: Session = Depends(get_db)):
    contacts = await repository_contacts.find_contacts_birthday(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contacts
