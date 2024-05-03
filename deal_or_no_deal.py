import sys
from files.Case import *
from files.Global import *
from files.Player import *

'''
This file contains is the 'main'

When this file is ran it will run the 'Deal or No Deal' game 

    'python3 deal_or_no_deal.py'

'''

class DealOrNoDealController:
    '''
        init():
        display_cases(self):
        display_values(self):
        display_all(self):
        select_case(self, case_number, output_value=True):
        generate_cases(self):
        get_offer(self):
        play_game(self):
        update_winnings(self):

    '''

    def __init__(self):

        '''

        The initial setup for the Deal or No Deal game controller. 
        This method generates the cases, initializes a new player, 
        and starts the game.

        '''

        self.all_cases = generate_cases()
        self.available_cases = self.all_cases.copy() 
        self.player = None

        clear_console()
        self.play_game()

    def display_cases(self):

        '''

        Prints the remaining cases in the game to the console. 
        Opened cases are marked with an 'X' and colored red.

        '''

        print(Color.BLUE + "Remaining Cases" + Color.END + '\n')
         
        i = 2
        for case in self.all_cases:
            display_num = case.number
            color = Color.YELLOW
            if self.player.check_if_already_selected(case.number):
                display_num = 'X'
                color = Color.RED

            if i % 7 > 0:
                print(color + f"{display_num:<10}", end='' + Color.END)
            else:
                print(color + str(display_num) + Color.END)
            i += 1

    def display_values(self):
        '''

        Prints the remaining possible values that can be inside the cases.
        Values that have already been revealed are marked with an 'X' and colored red.

        '''
        column_one = []
        column_two = []

        print(Color.BLUE + "\n\nRemaining Values" + Color.END + '\n')
         
        i = 0
        for case in sorted(self.all_cases):
            i += 1
            display_num = case.value
            color = Color.YELLOW
            if self.player.check_if_already_selected(case.number, ignore_self=True):
                display_num = 'X'
                color = Color.RED

            if i < 14:
                column_one.append([color, str(display_num)])
            else:
                column_two.append([color, str(display_num)])

        # Display Columns 1 and 2
        for i in range(0, 13):
            col1_element = column_one[i]
            col2_element = column_two[i]

            print(col1_element[0] + f"{add_commas_to_number(str(col1_element[1])):<10}" + Color.END, end='')
            print(col2_element[0] + add_commas_to_number(str(col2_element[1])) + Color.END)

    def display_all(self):
        '''

        Utility method to display both the remaining cases and the potential values at once.

        '''
       
        self.display_cases()
        self.display_values()
       
    def select_case(self, case_number, output_value=True):
        '''

        Selects a case based on the case_number passed to the function.
        If output_value is True, the value of the selected case will also be printed.
        The selected case is stored in the player's list of picked cases.

        '''


        if output_value:
            print(f"You selected case {case_number}")
            print(f"Case {case_number}: ${add_commas_to_number(str(self.all_cases[case_number - 1].value))}")
    
        for case in self.available_cases:
            if case.number == case_number:
                self.player.selected_cases.append(case)
                self.available_cases.remove(case)
                break

    def get_offer(self):
        '''
        Calculates the banker's offer by averaging the value of all remaining cases 
        and returning half of that average.

        '''
        cases_left = len(self.available_cases)
        #Total up all availble cases left
        total_case_value = sum(case.value for case in self.available_cases)
        # Add Personal Case
        total_case_value += sum(case.value for case in self.all_cases if case.number == self.player.personal_case)

        print(f"total = {total_case_value}")
        if cases_left > 7 and total_case_value > 1400000:
            total_case_value -= 800000

        avg = total_case_value / cases_left
        print(f"avg = {avg}")

        num = 0.54

        num -= len(self.available_cases) / 100.0
        offer = avg * 0.45
        reversedlist = self.available_cases[::-1]
        if offer > reversedlist[1].value: #2nd to last
            return int(offer) / 2

        return int(offer)
    
    def play_game(self):
        '''
        Runs the core game loop where the player chooses cases, receives offers,
        and decides whether to take the deal or continue playing.
        '''

        print(f"Welcome to Python Deal or No Deal!\n")
        self.player = Player()
        self.select_case(self.player.personal_case, False)

        while len(self.available_cases) > 1:
            print("\nRound Start!")

            cases_to_select = 6 if len(self.available_cases) > 8 else 3

            for i in range(0, cases_to_select):
                print(f"\nCases Left This Round: {cases_to_select - i}\n")
                self.display_all()
                while True:
                    try:
                        print("\nSelect a case to open (1-26): ", end='')
                        inp = int(input())
                        clear_console()
                        if inp in self.player.selected_cases or inp == self.player.personal_case:
                            print(f"Invalid Selection, already picked case {inp}")
                            print(f"\nCases Left This Round: {6 - i}\n")
                        elif 1 <= inp <= 26:
                            self.player.selected_cases.append(inp)
                            self.select_case(inp)
                            break
                        else:
                            print("Invalid input: Please enter a number between 1 and 26.")
                            print(f"\nCases Left This Round: {6 - i}\n")
                        self.display_all()
                    except:
                        clear_console()
                        print("Invalid input: Please enter a number between 1 and 26.")
                        print(f"\nCases Left This Round: {6 - i}\n")
                        self.display_all()

            if len(self.available_cases) != 1:
                offer = self.get_offer()
                print(f"\nBanker's Offer: ${add_commas_to_number(str(offer))}\n")
                print(f"Cases Left: {len(self.available_cases)}")
                self.display_values()
                decision = input("\nDeal (D) or No Deal (N)? ").strip().lower()
                clear_console()
            else:
                self.display_values()
                while True:
                    try:
                        decision = input("Will you keep your case (K), or trade (T)? ").strip().lower()
                        if decision == 'k' or decision == 't':
                            break
                    except:
                        print("Invalid Input. (K) or (T)")
                clear_console()

            self.handle_decision(decision, offer)
        
    def handle_decision(self, decision, offer):
        '''
        Handles the decision logic, by taking in the user decision and the offer amount,
        This then passes the offer to the correct function if needed, or outputting and exiting

        '''
        if decision == 'd':
                print("Congratulations! You've accepted the banker's offer.")
                self.end_game(offer)
                return
        elif decision == 'n':
            print("No deal!")
        elif decision == 'k':
            print("You kept your case!")
            self.end_game(self.all_cases[self.player.personal_case - 1].value)
        elif decision == 't':
            print("You Traded!")
            self.end_game(self.available_cases[0].value)
        else:
            print("Invalid input. No deal!")
    
    def end_game(self, winnings):
        '''
        Finalizes the game, showing the player's winnings, the content of their personal case,
        and updates the total winnings in an external file.
        '''

        print("\nGame Over!\n")
        print(f"Your personal case value: ${add_commas_to_number(str(self.all_cases[self.player.personal_case - 1].value))}")
        print(f"Amount of Money Won - ${add_commas_to_number(str(winnings))}\n")
        self.update_winnings(winnings)

    def update_winnings(self, new):
        '''
        Updates the total accumulative winnings by adding a new amount (from the last game/s) 
        to the total and writes it to an external file.
        '''

        try:
            with open(file_path_to_winnings, 'r') as file:
                old = int(file.read())
        except:
            old = 0
        total = old + new

        with open(file_path_to_winnings, 'w') as file:
            file.write(str(total))

        print(f"Total Winnings: ${add_commas_to_number(str(total))}\n")
        sys.exit()

DealOrNoDealController()