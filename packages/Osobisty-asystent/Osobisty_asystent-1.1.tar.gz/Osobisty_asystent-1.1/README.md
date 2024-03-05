_____________________________________________TO START_____________________________________________:

1. Open command line (cmd ).
2. Write in teminal: cd Bot---Syntax-Conquerors\Osobisty_asystent
3. Confirm by ENTER button.
4. Then write in terminal : pip install -e .
5. Push the ENTER button.
6. Write in terminal:  personal-assistant
7. Push the ENTER button.


Then you will be asked to enter the appropriate command from the list of commands that the bot accepts. To see them, type 'help' and push the ENTER bottom. Next write chosen by you commend, push the ENTER bottom and follow the instructions displayed by the bot. Remember about spaces where the bot requires!


An explanation of all the commands the bot accepts can be found in MANUAL presented belowe GENERAL BOT DESCRIPTION.



_________________________________________GENERAL BOT DESCRIPTION_________________________________________

The project is a console assistant bot that recognizes commands entered from the keyboard and reacts in accordance with the entered command.

The the bot starts working it loads the list of contacts from the "data_save.bin" file.

The bot allows you to enter and save information such as: Name, Surname, phone number, e-mail address and date of birth into the contact list and notes.

The bot allows you to search, edit and delete the information you enter.

The bot shows how many days are left until the selected contact's birthday.

The bot checks whether the phone number entered by the user into the contact book składa się z tylko i wyłącznie z 9 cyft.

The bot checks whether the e-mail address entered into the contact book has the correct format.

        A valid e-mail address consists of:

        1. The first part of the email address (before the @ sign) may consist of:
        - uppercase and/or lowercase letters of the Latin alphabet [A-Za-z],
        - numbers [0-9]
        - underscore [\_]
        - dot character at least once

        2. The second part of the email address consists only of:
        - @ sign (exactly one)

        3. The third part of the email address may consist of:
        - uppercase and/or lowercase letters of the Latin alphabet [A-Za-z]
        - numbers [0-9]
        - underscore character
        - dash character

        4. The fourth part of the email address may consist of:
        - two or three lowercase letters of the Latin alphabet [a-z]
        - dot character at least once (for example: .com.pl or .pl)


The bot only accepts commends presented below:

_____________________________________________THE BOT ACCEPTS COMMANDS_____________________________________________:

 1.  'add contact'
 2.  'delete contact'
 3.  'add phone'
 4.  'change phone'
 5.  'delete phone'
 6.  'add email'
 7.  'change email'
 8.  'delete email'
 9.  'add birthday' 
 10. 'birthday'
 11. 'add address'
 12. 'change address'
 13. 'delete address'
 14. 'add note'
 15. 'edit note'
 16. 'remove note' 
 17. 'show notes'
 18. 'search note'
 19. 'show all'
 20. 'find contact'
 21. 'sort folder'
 22. 'save'
 23. 'exit'
 24. 'help'

The bot saves the list of contacts in the "bot_save.bin" file, which is created when it finishes working.

The bot terminates after the user enters the 'exit' command.


_______________________________________________________MANUAL_______________________________________________________


add contact -   using this command, the bot adds the name and surname to the contact list.
                To do this, enter 'add contact', then press the ENTER button. Then enter First Name, Last Name - remembering about the space between the name and surname.   

delete contact - using this command, the bot removes the name and surname from the contact list.
                To do this, type 'delete contact', then press ENTER. Then enter First Name, Last Name 
                - remembering about the space between the name and surname and confirm with the ENTER bottom.

add phone -     using this command, the bot adds the phone number of the person the user indicates to  the  contact list. 
                To  do this, type "add phone" and then press ENTER. Then enter the name and surname you want to add the phone number to - remembering to include a space between the name and surname and confirm with the ENTER bottom.

change phone   - using this command, the bot will change the phone number of the person the user indicates in the contact
                 list. To do this, type "change phone" and then press ENTER. Then enter the Name and Surname whose phone number you want to change - remembering to include a space between the name and surname and confirm by pressing ENTER bottom.

delete phone   - using this command, the bot will delete the phone number of the person indicated by the user in the contact
                 list. To do this, type "delete phone" and then press ENTER. Then enter the Name and Surname whose phone number you want to change - remembering to put a space between the name and surname and confirm by pressing ENTER bottom.

add email -     using this command, the bot will add the e-mail address of the person indicated by the user to the contact
                list. To do this, type "add email" and then press ENTER. Then enter the Name and Surname whose the e-mail address you want to change - remembering to put a space between the name and surname and press ENTER. The last thing you need to do is enter your email address and confirm by pressing ENTER bottom.

change email -  using this command, the bot will change the e-mail address of the person indicated by the user in the contact
                list. To do this, type "change email" and then press ENTER. Then enter the Name and Surname whose e-mail address you want to change - remembering to put a space between the name and surname and press the ENTER button. The last thing you need to do is enter your email address and confirm by pressing ENTER bottom.

delete email -  using this command, the bot will delete the e-mail address of the person indicated by the user in the contact
                list. To do this, type "delete email" and then press ENTER. Then enter the Name and Surname whose e-mail address you want to remove - remembering to put a space between the name and surname - and press the ENTER button.

add birthday -  using this command, the bot will add the birthday of the person indicated by the user in the contact list.
                To do this, type "add birthday" and then press ENTER. Then enter the Name and Surname of the person whose birthday you want to add - remembering to put a space between the name and surname and press ENTER. Then follow the bot's instructions: enter your birthday in the YYYY format and confirm by pressing ENTER. In the next step, enter your month of birth in MM format and confirm by pressing ENTER. The last step is to enter the selected person's day of birth in the DD format and confirm by pressing ENTER bottom.

birthday -      using this command, the bot will display a list of people whose birthday falls in a given month - from today.
                To do this, type "birthday" and then press ENTER bottom.

add address -   using this command, the bot will add the residential address of the person indicated by the user to the
                contact list. To do this, type "add address" and press ENTER. Then enter the Name and Surname of the person whose address you want to add - remembering to put a space between the name and surname - and press ENTER. Then follow the bot's instructions: enter your City name and confirm by pressing ENTER. In the next step, enter the street name and confirm with the ENTER key. The last step is to enter the date, house or apartment number and confirm with the ENTER bottom.

change address - using this command, the bot will change the residential address of the person indicated by the user 
                in the contact list. To do this, type "change address" and press ENTER. Then enter the Name and Surname of the person whose address you want to change - remembering to put a space between the name and surname and press ENTER. Then follow the bot's instructions: enter your City name and confirm by pressing ENTER. In the next step, enter the street name and confirm with the ENTER key. The last step is to enter the date, house or apartment number and confirm with the ENTER bottom.

delete address - using this command, the bot will delete the residential address of the person indicated by the user 
                in the contact list. To do this, type "delete address" and press ENTER. Then enter the Name and Surname of the person whose address you want to remove - remembering to put a space between the name and surname - and press ENTER bottom.

add note -      using this command the bot will add a note (text). To do this, type "add note" and press ENTER. 
                Then enter the note text and press ENTER. In the last step, enter test as a tag and confirm by pressing ENTER.

edit note -     using this command, the bot edits the note (text). To do this, type "edit note" and press ENTER.
                The bot will then display a list of the entered notes. From the first column of the displayed list, select the number of the note you want to change, type that number on the command line and press ENTER. Then enter the content of the note to be saved after the change and confirm with the ENTER button. In the last step, enter test as a tag and confirm by pressing ENTER.

remove note -   using this command the bot will delete one selected note (text) or all notes.
                To do this, type "delete note" and press ENTER. The bot will then display a list of the entered notes. To delete all notes, enter "all" and confirm by pressing ENTER. If you want to delete only one note, then from the first column of the displayed list, select the number of the note you want to delete, enter this number in the command line and press ENTER. Then enter the content of the note that is to be saved after the change and confirm with the ENTER button. In the last step, enter test as a tag and confirm by pressing ENTER.

show notes -    using this command, the bot will display a table of all saved (text) notes along with their tags.
                To do this, type "show notes" and press ENTER.

search note -   using this command, the bot will search for a note (text) by tag. To do this, type "search note" 
                and press ENTER. The bot will ask you to enter the tag name of the note you are looking for. Enter it in the command line and confirm with the ENTER key. The bot will then display a table with the selected note.

show all -      using this command, the bot will display a contact list in the form of a table with all contacts
                saved so far. To do this, type "show all" and press ENTER.

find contact -  using this command, the bot will display information that has been assigned to the person 
                selected by the user. To do this, type "find contact" and press ENTER. Then enter the Name and Surname of the person you are looking for information about - remembering about the space between the name and surname and confirm with the lower ENTER bottom.

sort folder -   using this command, the bot sort files in the folder selected byt the user by selected 
                file extension. To do this, please enter in commend line "sort folder" and then press ENTER. 
                Then enter the path to the folder which you would like to sort and confirm by pressing the ENTER bottom. (Exaple for file's path : C:\Users\KUsername\Desktop\Mess). 

save -          using this command, the bot saves the contact table in the "bot_save.bin" file. To do this,
                type "save" on the command line and then press ENTER.

exit -          za pomocą tej komendy bot kończy pracę zapisuje tabelę kontaktów w pliku „bot_save.bin”.
                Aby to zrobić, wpisz w wierszu poleceń „exit”, a następnie naciśnij ENTER.

help -           using this command, the bot will display a list of accepted commands.
                 To do this, type "help" at the command line and then press ENTER.


________________________________________HAVE FUN WITH THE BOT!________________________________________
