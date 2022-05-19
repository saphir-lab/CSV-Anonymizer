### Import personal modules
from utils.console import Console

class Menu():
    def __init__(self, colored=True):
        self.console = Console(colored)
        self.menu_display=""
        self.valid_choices=[]

    def menu_choice_dynamic(self, lst_menu_display=[]):
        """Return correct menu selection from a menu build dynamically based on lst_menu_display 

        Args:
            lst_menu_display (lst): List of elements to display in sequence in a selection menu

        Returns:
            [int]: index of the element in the list (starting at position 1).Return 0(zero) in case of Cancel Choice.
        """
        self.console.print_msg("INFO", "\nElements with your criteria:")
        print("0. Cancel")
        [print(f"{i+1}. {menu_display[0]}") for i, menu_display in enumerate(lst_menu_display)]
        print()
        bad_choice = True
        # Loop until a good option is selected
        while bad_choice:
            menu_choice = input("What is your choice: ")
            if not menu_choice.isdigit() or int(menu_choice) not in range(0, len(lst_menu_display)+1):
                self.console.print_msg("ERROR", "Bad menu choice, please retry.")
            else:
                bad_choice = False
        return int(menu_choice)

    def menu_choice_fixed(self, menu="", menu_valid_choices=[]):
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
                self.console.print_msg("ERROR", "Bad menu choice, please retry.")
            else:
                bad_choice = False
        return menu_choice

    def menu_choice_YN(self, msg=""):
        confirm = False
        while not confirm == "Y" and not confirm == "N": 
            confirm = input(f"{msg} (Y/N) ? ").upper()
            if not confirm == "Y" and not confirm == "N":
                self.console.print_msg("ERROR", "Bad menu choice, please retry.")
        return confirm

