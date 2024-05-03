import os

class Color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

file_path_to_winnings = 'files/winnings.txt'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_commas_to_number(num_str):
    '''
    
    Takes in a string which is a str(int);
    returns the string with added commas in the correct spots

    '''
    num_str_cp = num_str[::-1]
    result = ""
    decimal_found = False

    for i in range(len(num_str_cp)):
        if num_str_cp[i] == '.':
            decimal_found = True
            break

    for i in range(len(num_str_cp)):
        if i % 3 == 0 and i != 0 and not decimal_found:
            result += ","
        result += num_str_cp[i]

    result = result[::-1]

    return result


