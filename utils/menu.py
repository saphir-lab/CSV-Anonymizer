### Import personal modules
from utils.layout import *

def menu_choice_dynamic(lst_menu_display=[], colored=True):
    """Return correct menu selection from a menu build dynamically based on lst_menu_display 

    Args:
        lst_menu_display (lst): List of elements to display in sequence in a selection menu
        colored (boolean): display erro messages in color 

    Returns:
        [int]: index of the element in the list (starting at position 1).Return 0(zero) in case of Cancel Choice.
    """
    print_msg("INFO", "\nElements with your criteria:", colored=colored)
    print("0. Cancel")
    [print(f"{i+1}. {menu_display[0]}") for i, menu_display in enumerate(lst_menu_display)]
    print()
    bad_choice = True
    # Loop until a good option is selected
    while bad_choice:
        menu_choice = input("What is your choice: ")
        if not menu_choice.isdigit() or int(menu_choice) not in range(0, len(lst_menu_display)+1):
            print_msg("ERROR", "Bad menu choice, please retry.", colored=colored)
        else:
            bad_choice = False
    return int(menu_choice)

def menu_choice_fixed(menu="", menu_valid_choices=[], colored=True):
    """Print a menu & loop until selection is correct

    Args:
        menu (str) sring with the menu to display.
        menu_valid_choices (list: Array with valid response. Defaults to [].
    """
    print(menu)
    bad_choice = True
    # Loop until a good option is selected
    while bad_choice:
        menu_choice = input("What is your choice: ")
        if menu_choice not in menu_valid_choices:
            print_msg("ERROR", "Bad menu choice, please retry.", colored=colored)
        else:
            bad_choice = False
    return menu_choice

def menu_choice_YN(msg="", colored=True):
    confirm = False
    while not confirm == "Y" and not confirm == "N": 
        confirm = input(f"{msg} (Y/N) ? ").upper()
        if not confirm == "Y" and not confirm == "N":
            print_msg("ERROR", "*** Bad menu choice, please retry.", colored=colored)
    return confirm

