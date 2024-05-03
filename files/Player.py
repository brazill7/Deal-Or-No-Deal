class Player:
    def __init__(self):
        self.selected_cases = []
        self.personal_case = self.get_personal_case()

    def check_if_already_selected(self, case, ignore_self=False):
        if case in self.selected_cases:
            return True
        if case == self.personal_case and not ignore_self:
            return True
        return False

    def get_personal_case(self) -> int:
        while True:
            print("Select your personal case (1-26): ", end='')
            try:
                user_inp = int(input())
                if 1 <= user_inp <= 26:    
                    return user_inp
                else:
                    print("Invalid input: Please enter a number between 1 and 26.")
            except ValueError:
                print("Invalid input: Please enter a valid number.")
