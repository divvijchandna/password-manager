# Code based on: https://www.geeksforgeeks.org/generating-strong-password-using-python/
from Crypto import Random  # This one giving error for now
import random #Maybe change random package to better package
import array


def make_password(password_len):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 

    lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']

    symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
            '*', '(', ')', '<']

    combined = digits + lower_case + upper_case + symbols

    random_digit = random.choice(digits)
    random_lower = random.choice(lower_case)
    random_upper = random.choice(upper_case)
    random_symbol = random.choice(symbols)



    tmp_password = random_digit + random_lower + random_upper + random_symbol

    for i in range (0, password_len-4):
        tmp_password = tmp_password + random.choice(combined)
        temp_pass_list = array.array('u', tmp_password)
        random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
            password = password + x
            
    return password


password_len = int(input('enter password length: '))
print('Password is : ', make_password(password_len))