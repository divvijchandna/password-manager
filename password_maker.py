# # Code based on: https://www.geeksforgeeks.org/generating-strong-password-using-python/
# # from Crypto import Random  # This one giving error for now
# import random #Maybe change random package to better package
# import array
import string
import secrets

def make_password(password_len, lower, upper, digit, special, special_set):
    alphabet = string.ascii_letters + string.digits + special_set
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(password_len))
        if (sum(c.islower() for c in password) >= lower
                and sum(c.isupper() for c in password) >= upper
                and sum(c.isdigit() for c in password) >= digit
                and sum(not c.isalnum() for c in password) >= special):
            break
    return password

# def make_password(password_len):
#     digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 

#     lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
#                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
#                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
#                         'z']
    
#     upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
#                         'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
#                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
#                         'Z']

#     symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/','|', '~', '>', 
#             '*', '(', ')', '<', '!', '&']

#     combined = digits + lower_case + upper_case + symbols

#     random_digit = random.choice(digits)
#     random_lower = random.choice(lower_case)
#     random_upper = random.choice(upper_case)
#     random_symbol = random.choice(symbols)



#     tmp_password = random_digit + random_lower + random_upper + random_symbol

#     for i in range (0, password_len-4):
#         tmp_password = tmp_password + random.choice(combined)
#         temp_pass_list = array.array('u', tmp_password)
#         random.shuffle(temp_pass_list)

#     password = ""
#     for x in temp_pass_list:
#             password = password + x

#     return password


# password_len = int(input('enter password length: '))
# print('Password is : ', make_password(password_len))

# special_set = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

# pw = make_password(15, 1, 1, 2, 1, special_set)
# print(pw)