import pickle
from .classes import AddressBook
import json
import os

def load_default_contacts(address_book: AddressBook, exists = False):
    if not exists:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(dir_path, "default_contacts.json")

        with open(json_path, "r") as rff:
            random_contacts =  json.load(rff)
        for person in random_contacts:
            address_book.add_contact(person['name'])
            address_book.contacts[person['name']].add_phone(person['phone'])
            address_book.contacts[person['name']].add_email(person['email'])
            address_book.contacts[person['name']].add_birthday(person['birthday'])
            address_book.contacts[person['name']].add_address(person['address'])
    return address_book

def load_from_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(dir_path, "data_save.bin")
    try:
        with open(save_path,"rb") as fh:
            address_book = pickle.load(fh)
            print('The adress_book has been loaded from file')
    except FileNotFoundError:
        print("File with address_book doesn't exist yet! Creating new Addressbook")
        address_book = AddressBook()
        address_book = load_default_contacts(address_book)
        return address_book
    return address_book
