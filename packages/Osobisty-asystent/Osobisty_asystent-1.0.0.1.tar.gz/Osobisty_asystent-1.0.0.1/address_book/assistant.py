from .classes import *
from .utilities import *
from .sorting_module import main_sorting_folder
import pickle
import os

LOGO = """
@@@ @@@ @@@  @@@ @@@ @@@  @@@ @@@ @@@  @@@  @@@ @@@ @@@  @@@ @@@ @@@  @@@ @@@ @@@  @@@     @@@  @@@ @@@ @@@ 
@@@     @@@  @@@          @@@          @@@  @@@              @@@      @@@     @@@  @@@ @   @@@      @@@     
@@@ @@@ @@@  @@@ @@@ @@@  @@@ @@@ @@@  @@@  @@@ @@@ @@@      @@@      @@@ @@@ @@@  @@@ @@@ @@@      @@@     
@@@     @@@          @@@          @@@  @@@          @@@      @@@      @@@     @@@  @@@   @ @@@      @@@     
@@@     @@@  @@@ @@@ @@@  @@@ @@@ @@@  @@@  @@@ @@@ @@@      @@@      @@@     @@@  @@@     @@@      @@@     

                                                                                   by Syntax Conquerors
"""

address_book = load_from_file()

def add_contact():    
    name = input("Enter the contact's name and surname: ").lower()
    if name in address_book.contacts:
        print("A contact with this name already exists.")
    else:
        try:
            address_book.contacts[name] = Contact(name)
        except Exception as e:
            print(e)
        if name in address_book.contacts:
                print(f"Contact {name} was added.")

def delete_contact():
    name = input("Enter the contact's name and surname you'd like to delete: ").lower()
    if name in address_book.contacts:
        address_book.contacts.pop(name)
        print(f'Contact {name} deleted.')
    else:
        print(f'There is no contact {name}')

def add_phone():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    if address_book.contacts[name].phone.value:
        print(f'Contact have a phone number already. To change an existing number use "change phone" command.')
        return
    phone = input("Enter phone number: ")
    try:
        address_book.contacts[name].add_phone(phone)
        if address_book.contacts[name].phone.value:
            print(f"{phone} was added to contact {name}.")
    except:
        return

def change_phone_num():
    name = input("Enter the contact's name and surename: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    if not address_book.contacts[name].phone.value:
        print(f"Contact {name} doesnt have a phone number yet. However we can proceed.")
    new_phone = input("Enter the new phone number: ")
    try:
        address_book.contacts[name].add_phone(new_phone)
        if address_book.contacts[name].phone.value == new_phone[0:3] + '-' + new_phone[3:6] + '-' + new_phone[6:]:
            print(f"Number was changed for contact {name}.")
    except:
        return

def delete_phone():
    name = input("Enter the contact's name and surename: ").lower()
    if name in address_book.contacts:
        address_book.contacts[name].delete_phone()
        print(f"Phone number deleted for {name}.")
    else:
        print("Contact not found.")

def add_email():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    if address_book.contacts[name].email.value:
        print(f'Contact have an email already. To change an existing email use "change email" command.')
        return
    email = input("Enter the email: ")
    try:
        address_book.contacts[name].add_email(email)
        if address_book.contacts[name].email.value:
            print(f"{email} was added to contact {name}.")
    except:
        return
    
def change_email():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    if not address_book.contacts[name].email.value:
        print(f"Contact {name} doesnt have a email yet. However we can proceed.")
    email = input("Enter the email: ")
    try:
        address_book.contacts[name].add_email(email)
        if address_book.contacts[name].email.value == email:
            print(f"{email} was changed for contact {name}.")
    except:
        return
    
def delete_email():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    address_book.contacts[name].remove_email()
    print(f'Email deleted')

def get_valid_date_input(prompt):
    while True:
        try:
            year = int(input("\n" + prompt + " (year): "))
            month = int(input(prompt + " (month): "))
            day = int(input(prompt + " (day): "))
            date = datetime(year, month, day).date()
            today = datetime.now().date()
            if date > today:
                print("\nInvalid date. Please enter a date not further into the future than today.")
            else:
                return date.strftime('%Y-%m-%d')
        except ValueError:
            print("\nInvalid date. Please enter a valid date.")

def set_birthday():
    name = input("Enter the contact's name and surname: ").lower()
    if name in address_book.contacts:
        if address_book.contacts[name].birthday.value:
            print(f"\nContact {name.title()} already has a birthday date set to {address_book.contacts[name].birthday.value}.")
            edit_birthday = input("Do you want to edit the birthday date? (yes/no): ").lower()
            if edit_birthday == "yes":
                birthday_to_add = get_valid_date_input("Enter the new birthday date")
                address_book.contacts[name].add_birthday(birthday_to_add)
                print(f"\nNew birthday date ({birthday_to_add}) added to contact {name.title()}")
            else:
                print(f"\nBirthday date for {name.title()} remains unchanged.")
        else:
            birthday_to_add = get_valid_date_input("Enter the contact's birthday date")
            address_book.contacts[name].add_birthday(birthday_to_add)
            print(f"\nBirthday date ({birthday_to_add}) added to contact {name.title()}")
    else:
        print("\nContact not found.")

def days_to_birthday():
    width = 123
    print("\n+" + "-" * width + "+")
    print('|{:^30}|{:^30}|{:^30}|{:^30}|'.format("NAME", "BIRTHDAY", "DAYS TO BIRTHDAY", "UPCOMING"))
    print("+" + "-" * width + "+")
    
    for contact_name in address_book.contacts:
        contact = address_book.contacts[contact_name]
        if contact.birthday.value and contact.days_to_birthday < 31:
            format_value = lambda x: x if x is not None else "---"
            print('|{:^30}'.format(format_value(contact.name.value.title())), end="")
            print('|{:^30}'.format(format_value(contact.birthday.value)), end="")
            print('|{:^30}'.format(format_value(contact.days_to_birthday)), end="")

            days_to_birthday = contact.days_to_birthday
            
            if contact.birthday.value:
                birthday_date = datetime.strptime(contact.birthday.value, "%Y-%m-%d")
                today = datetime.today()
                next_birthday = datetime(today.year, birthday_date.month, birthday_date.day)
                
                if today > next_birthday:
                    next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day)
                
                days_from_beginning_of_week = (today.weekday() - 7) % 7
                
                if days_to_birthday == 0:
                    print('|{:^30}|'.format("Today"), end="\n")
                elif days_to_birthday == 1:
                    print('|{:^30}|'.format("Tomorrow"), end="\n")
                elif days_to_birthday < 7 - days_from_beginning_of_week:
                    print('|{:^30}|'.format("This week"), end="\n")
                elif days_to_birthday < 14 - days_from_beginning_of_week:
                    print('|{:^30}|'.format("Next week"), end="\n")
                elif next_birthday.month == today.month:
                    print('|{:^30}|'.format("This month"), end="\n")
                elif (today.month + 1) % 12 == next_birthday.month % 12:
                    print('|{:^30}|'.format("Next month"), end="\n")
                else:
                    print('|{:^30}|'.format("---"), end="\n")
            else:
                print('|{:^30}|'.format("---"), end="\n")
            
    print("+" + "-" * width + "+\n")

def add_address():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    city = input("City: ")
    street = input("Street: ")
    number = input("House and flat number: ")
    address = city + ' ' + street + ' ' + number
    try:
        address_book.contacts[name].add_address(address.title())
        if address_book.contacts[name].address.value:
            print(f"{address} was added to contact {name}.")
    except:
        return
    
def change_address():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    if not address_book.contacts[name].address.value:
        print(f"Contact {name} doesnt have a email yet. However we can proceed.")
    city = input("City: ")
    street = input("Street: ")
    number = input("House and flat number: ")
    address = city + ' ' + street + ' ' + number
    try:
        address_book.contacts[name].add_address(address.title())
        if address_book.contacts[name].address.value == address.title():
            print(f"{address} was changed for contact {name}.")
    except:
        return
    
def delete_address():
    name = input("Enter the contact's name and surname: ").lower()
    if not name in address_book.contacts:
        print(f'There is no contact {name}')
        return
    address_book.contacts[name].remove_address()
    print(f'Address deleted')

def add_note():
    note = input("Enter the note text: ")
    tags = input("Enter tags: ")
    address_book.notebook.add_note(note, tags)

def edit_note():
    if not address_book.notebook.data:
        print('Notebook is empty')
    else:
        show_notes()
        num_of_note = input('Enter number of note: ')
        address_book.notebook.edit_note(num_of_note)

def remove_note():
    if not address_book.notebook.data:
        print('Notebook is empty')
    else:
        show_notes()
        num_of_note = input('Enter number of note or write "all" to remove all notes: ')
        address_book.notebook.remove_note(num_of_note)

def show_notes():
    print('List of notes: \n', address_book.notebook.show_notes())

def search_note_by_tags():
    searched_tags = input("Enter tags: ")
    print(address_book.notebook.search_note_by_tags(searched_tags))

def show_all():
    width = 154
    print("\n+" + "-" * width + "+")
    print('|{:^30}|{:^13}|{:^35}|{:^12}|{:^60}|'.format("NAME", "PHONE", "EMAIL", "BIRTHDAY", "ADDRESS"))
    print("+" + "-" * width + "+")
    for contact_name in address_book.contacts:
        contact = address_book.contacts[contact_name]
        format_value = lambda x: x if x is not None else "---"
        print('|{:^30}'.format(format_value(contact.name.value.title())), end="")
        print('|{:^13}'.format(format_value(contact.phone.value)), end="")
        print('|{:^35}'.format(format_value(contact.email.value)), end="")
        print('|{:^12}'.format(format_value(contact.birthday.value)), end="")
        print('|{:^60}|'.format(format_value(contact.address.value)), end="\n")
    print("+" + "-" * width + "+\n")

def find_contact():
    search_phrase = input("Enter the contact's name and surname: ").strip().lower()
    width = 154
    print("\n+" + "-" * width + "+")
    print('|{:^30}|{:^13}|{:^35}|{:^12}|{:^60}|'.format("NAME", "PHONE", "EMAIL", "BIRTHDAY", "ADDRESS"))
    print("+" + "-" * width + "+")
    found = False
    for name, contact in address_book.contacts.items():
        if search_phrase in name:
            found = True
            format_value = lambda x: x if x is not None else "---"
            print('|{:^30}'.format(format_value(contact.name.value.title())), end="")
            print('|{:^13}'.format(format_value(contact.phone.value)), end="")
            print('|{:^35}'.format(format_value(contact.email.value)), end="")
            print('|{:^12}'.format(format_value(contact.birthday.value)), end="")
            print('|{:^60}|'.format(format_value(contact.address.value)), end="\n")
    if not found:
        print("|{:^154}|".format("\"" + search_phrase + "\" not present in the address book."))
    print("+" + "-" * width + "+\n")

def sort_folder():
    current_path = os.getcwd()
    path_to_folder = input(" Enter path to folder that should be sorted: ")
    main_sorting_folder(path_to_folder)
    os.chdir(current_path)

def save_to_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(dir_path, "data_save.bin")
    with open(save_path, "wb") as fh:
        pickle.dump(address_book, fh)
    print('File has been saved')

def end_program():
    save_to_file()
    print('Goodbye')

def accepted_commands(commands: dict, col = 4):
    width = 20 * col + col - 1
    c = 1
    print("\n+" + "-" * width + "+")
    for command in commands.keys():
        if c < col:            
            print("|{:^20}".format(command), end="")
            c += 1
        else:
            print("|{:^20}|".format(command), end="\n")
            c = 1
    print("+" + "-" * width + "+\n")

def unknown_command():
    print("\nUnknown command! Please type 'help' to get the list of available commands.")

def input_parser():
    """Functions runs in a while loop, takes input from user and returns apropiate functions
    """
    commands = {
    'add contact': add_contact,
    'delete contact': delete_contact,
    'add phone': add_phone,
    'change phone': change_phone_num,
    'delete phone': delete_phone,
    'add email': add_email,
    'change email': change_email,
    'delete email': delete_email,
    'add birthday' : set_birthday,
    'birthday': days_to_birthday,
    'add address': add_address,
    'change address': change_address,
    'delete address': delete_address,
    'add note': add_note,
    'edit note': edit_note,
    'delete note': remove_note,
    'show notes':show_notes,
    'find note': search_note_by_tags,
    'show all': show_all,
    'find contact' : find_contact,
    'sort folder': sort_folder,
    'save': save_to_file,
    'exit': end_program,
    'help': accepted_commands, 
}   
    command = input('\nEnter your command: ').lower()
    if command == 'help':
        return accepted_commands(commands)
    elif command in commands:
        return commands[command]  
    else:
        return unknown_command

def main():
    print(LOGO)
    print('Type "help" to get a command list.')
    while True:
        function_to_execute = input_parser()
        try:
            if function_to_execute == end_program:
                end_program()
                break
            else:
                function_to_execute()
        except:
            continue
            
if __name__ == '__main__':
    main()
