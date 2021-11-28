from tkinter import *
from hashwsalt_2 import *

def create_user():
    username_info = username.get()
    password_info = password.get()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    salt1 = os.urandom(32) # Remember this
    salt2 = os.urandom(32) # Remember this

    vault_key_wsalt = get_vault_key(password_info, salt1, username_info)
    salt = vault_key_wsalt[:32] # 32 is the length of the salt
    vault_key = vault_key_wsalt[32:]
    auth_hash_wsalt = get_auth_hash(vault_key, salt2, password_info)

    store_auth_hash(username_info, auth_hash_wsalt, salt1)

    Label(screen1, text = "Sign Up Success", fg = "green", font = ("calibri", 11)).pack()
    screen1.after(1000, screen1.destroy)

def sign_up():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Sign Up")
    screen1.geometry("500x400")

    global username, password, username_entry, password_entry

    username = StringVar()
    password = StringVar()

    Label(screen1, text = "Please enter details below to sign up").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Username").pack()
    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = "Password").pack()
    password_entry = Entry(screen1, textvariable = password, show="*")
    password_entry.pack()

    Label(screen1, text = "").pack()
    Button(screen1, text = "Sign Up", width = 10, height = 1, command = create_user).pack()
    
def view_passwords_button():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("500x400")

    global username_v, password_v, username_entry_v, password_entry_v

    username_v = StringVar()
    password_v = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    username_entry_v = Entry(screen2, textvariable = username_v)
    username_entry_v.pack()
    Label(screen2, text = "Password").pack()
    password_entry_v = Entry(screen2, textvariable = password_v, show="*")
    password_entry_v.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "View Passwords", width = 20, height = 1, command = view_passwords).pack()

def view_passwords():

    Label(screen2, text = "Connecting to database...", font = ("calibri", 11)).pack()
    usr = username_v.get()
    pwd = password_v.get()

    username_entry_v.delete(0, END)
    password_entry_v.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr)

    check = check_auth_hash(pwd, usr, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        Label(screen2, text = "Data Loading...", font = ("calibri", 11)).pack()
        screen2.after(200, screen2.destroy)
        record, nonce, tag = retrieve_record(usr)
        salt_vault = retrieve_vault_salt(usr)
        vault_key_wsalt = get_vault_key(pwd, salt_vault, usr)
        vault_key = vault_key_wsalt[32:]

        screen3 = Toplevel(screen)
        screen3.title("View Passwords")
        screen3.geometry("500x400")

        if(record == 'Empty'):
            Label(screen3, text = 'Password vault is empty.').pack()
        else:
            dec_record = decrypt(vault_key, nonce, tag, record)
            password_array = []
            password_array = dec_record.split('|||')
            for i in range(len(password_array)):
                password_array[i] = password_array[i].split('||')

        total_rows = len(password_array)
        total_columns = len(password_array[0])

        e = Entry(screen3, width=15,
                               font=('Calibri',12, 'bold'))
                  
        e.grid(row=0, column=0, padx=(40, 10), pady=(30, 10))
        e.insert(END, 'Website')
        e.bind("<Key>", lambda e: "break")

        e = Entry(screen3, width=20,
                               font=('Calibri',12, 'bold'))
                  
        e.grid(row=0, column=1, pady=(30, 10), padx=(0, 10))
        e.insert(END, 'Email/User ID')
        e.bind("<Key>", lambda e: "break")

        e = Entry(screen3, width=15,
                               font=('Calibri',12, 'bold'))
                  
        e.grid(row=0, column=2, pady=(30, 10))
        e.insert(END, 'Password')
        e.bind("<Key>", lambda e: "break")

        for i in range(total_rows):
            for j in range(total_columns):

                if j == 1:
                    e = Entry(screen3, width=20,
                               font=('Calibri',12))
                else:
                    e = Entry(screen3, width=15,
                               font=('Calibri',12))
                
                if j == 0:
                    e.grid(row=i+1, column=j, padx=(40, 10))
                elif j == 1:
                    e.grid(row=i+1, column=j, padx=(0, 10))
                else:
                    e.grid(row=i+1, column=j)
                e.insert(END, password_array[i][j])
                e.bind("<Key>", lambda e: "break")
        
def confirm_password_add():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("500x400")

    global username_a, password_a, username_entry_a, password_entry_a

    username_a = StringVar()
    password_a = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    username_entry_a = Entry(screen2, textvariable = username_a)
    username_entry_a.pack()
    Label(screen2, text = "Password").pack()
    password_entry_a = Entry(screen2, textvariable = password_a, show="*")
    password_entry_a.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "Confirm Password", width = 20, height = 1, command = add_passwords_button).pack()

def add_passwords_button():

    global usr, pwd
    usr = username_a.get()
    pwd = password_a.get()

    username_entry_a.delete(0, END)
    password_entry_a.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr)

    check = check_auth_hash(pwd, usr, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        screen2.after(0, screen2.destroy)

        global screen4
        screen4 = Toplevel(screen)
        screen4.title("Add Passwords")
        screen4.geometry("500x400")

        global website, password_record, email, website_entry, password_record_entry, email_entry

        website = StringVar()
        password_record = StringVar()
        email = StringVar()

        Label(screen4, text = "Please enter details below").pack()
        Label(screen4, text = "").pack()
        Label(screen4, text = "Website name").pack()
        website_entry = Entry(screen4, textvariable = website)
        website_entry.pack()
        Label(screen4, text = "Email/User ID on Website").pack()
        email_entry = Entry(screen4, textvariable = email)
        email_entry.pack()
        Label(screen4, text = "Password").pack()
        password_record_entry = Entry(screen4, textvariable = password_record, show="*")
        password_record_entry.pack()
        Label(screen4, text = "").pack()
        Button(screen4, text = "Add Password", width = 20, height = 1, command = add_passwords).pack()
        Button(screen4, text = "Update Password", width = 20, height = 1, command = add_passwords).pack()

def add_passwords():

    wbs = website.get()
    pwr = password_record.get()
    eid = email.get()

    website_entry.delete(0, END)
    password_record_entry.delete(0, END)
    email_entry.delete(0, END)

    record, nonce, tag = retrieve_record(usr)
    vault_salt = retrieve_vault_salt(usr)
    vault_key_wsalt = get_vault_key(pwd, vault_salt, usr)
    vault_key = vault_key_wsalt[32:]

    if(record == 'Empty'):
        nonce, ciphertext, tag = encrypt(wbs+'||'+eid+'||'+pwr, vault_key)
        store_record(usr, ciphertext, nonce, tag)
        Label(screen4, text = "Password Added Successfully", fg = "green", font = ("calibri", 11)).pack()

    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        websites_all = []
        emails_all = []
        passwords_all = []
        for tup in dec_record.split('|||'):
            li = str(tup).split('||')
            websites_all.append(str(li[0]).lower())
            emails_all.append(str(li[1]).lower())
            passwords_all.append(str(li[2]))
        
        flag = 0
        if (wbs.lower() in websites_all) and (eid.lower() in emails_all):
            indices_of_website = [i for i, x in enumerate(websites_all) if x == wbs]
            for ind in indices_of_website:
                if(emails_all[ind] == eid.lower()):
                    flag = 1
                    passwords_all[ind] = pwr
                    dec_record = ''
                    dec_record = websites_all[0] + '||' + emails_all[0] + '||' + passwords_all[0]
                    for i in range(1, len(websites_all)):
                        dec_record = dec_record + '|||' + websites_all[i] + '||' + emails_all[i] + '||' + passwords_all[i]
                    break

        if(flag==0):
            dec_record = dec_record + '|||' + wbs+'||'+eid+'||'+pwr

        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr, ciphertext, nonce, tag)
        if flag == 0:
            Label(screen4, text = "Password Added Successfully", fg = "green", font = ("calibri", 11)).pack()
        else:
            Label(screen4, text = "Password Updated Successfully", fg = "green", font = ("calibri", 11)).pack()

def confirm_password_gen():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("500x400")

    global username_g, password_g, username_entry_g, password_entry_g

    username_g = StringVar()
    password_g = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    username_entry_g = Entry(screen2, textvariable = username_g)
    username_entry_g.pack()
    Label(screen2, text = "Password").pack()
    password_entry_g = Entry(screen2, textvariable = password_g, show="*")
    password_entry_g.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "Confirm Password", width = 20, height = 1, command = gen_passwords_button).pack()

def gen_passwords_button():

    global usr2, pwd2
    usr2 = username_g.get()
    pwd2 = password_g.get()

    username_entry_g.delete(0, END)
    password_entry_g.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr2)

    check = check_auth_hash(pwd2, usr2, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        screen2.after(0, screen2.destroy)

        global screen5
        screen5 = Toplevel(screen)
        screen5.title("Add Passwords")
        screen5.geometry("500x500")

        global website2, password_length, email2, website_entry2, password_length_entry, email_entry2
        global lower, upper, digit, special, lower_entry, upper_entry, digit_entry, special_entry, special_set, special_set_entry

        website2 = StringVar()
        password_length = StringVar()
        email2 = StringVar()
        lower = StringVar()
        upper = StringVar()
        digit = StringVar()
        special = StringVar()
        special_set = StringVar()

        Label(screen5, text = "Please enter details below").pack()
        Label(screen5, text = "").pack()
        Label(screen5, text = "Website name").pack()
        website_entry2 = Entry(screen5, textvariable = website2)
        website_entry2.pack()
        Label(screen5, text = "Email/User ID on Website").pack()
        email_entry2 = Entry(screen5, textvariable = email2)
        email_entry2.pack()
        Label(screen5, text = "Password Length").pack()
        password_length_entry = Entry(screen5, textvariable = password_length)
        password_length_entry.insert(END, '12')
        password_length_entry.pack()
        Label(screen5, text = "Min Lowercase Letters").pack()
        lower_entry = Entry(screen5, textvariable = lower)
        lower_entry.insert(END, '1')
        lower_entry.pack()
        Label(screen5, text = "Min Uppercase Letters").pack()
        upper_entry = Entry(screen5, textvariable = upper)
        upper_entry.insert(END, '1')
        upper_entry.pack()
        Label(screen5, text = "Min Digits").pack()
        digit_entry = Entry(screen5, textvariable = digit)
        digit_entry.insert(END, '1')
        digit_entry.pack()
        Label(screen5, text = "Min Special Characters").pack()
        special_entry = Entry(screen5, textvariable = special)
        special_entry.insert(END, '1')
        special_entry.pack()
        Label(screen5, text = "Special Character Set").pack()
        special_set_entry = Entry(screen5, textvariable = special_set)
        special_set_entry.insert(END, " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
        special_set_entry.pack()
        Label(screen5, text = "").pack()
        Button(screen5, text = "Generate Password", width = 20, height = 1, command = gen_passwords).pack()
        Button(screen5, text = "Update Password", width = 20, height = 1, command = gen_passwords).pack()

def gen_passwords():

    wbt = website2.get()
    pwl = password_length.get()
    eml = email2.get()
    upp = upper.get()
    low = lower.get()
    dig = digit.get()
    spe = special.get()
    sps = special_set.get()

    website_entry2.delete(0, END)
    password_length_entry.delete(0, END)
    password_length_entry.insert(END, '12')
    email_entry2.delete(0, END)
    upper_entry.delete(0, END)
    upper_entry.insert(END, '1')
    lower_entry.delete(0, END)
    lower_entry.insert(END, '1')
    digit_entry.delete(0, END)
    digit_entry.insert(END, '1')
    special_entry.delete(0, END)
    special_entry.insert(END, '1')
    special_set_entry.delete(0, END)
    special_set_entry.insert(END, " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")

    if (int(upp)+int(low)+int(dig)+int(spe) > int(pwl)):
        Label(screen5, text = "Invalid inputs", fg = "red", font = ("calibri", 11)).pack()

    elif int(upp) == 0 and int(low) == 0 and int(dig) == 0 and int(spe) == 0:
        Label(screen5, text = "Invalid inputs", fg = "red", font = ("calibri", 11)).pack()

    elif int(pwl) <= 4:
        Label(screen5, text = "Password length too short", fg = "red", font = ("calibri", 11)).pack()

    else:
        record, nonce, tag = retrieve_record(usr2)
        vault_salt = retrieve_vault_salt(usr2)
        vault_key_wsalt = get_vault_key(pwd2, vault_salt, usr2)
        vault_key = vault_key_wsalt[32:]
        password_record2 = str(make_password(int(pwl), int(low), int(upp), int(dig), int(spe), sps))

    if(record == 'Empty'):
        nonce, ciphertext, tag = encrypt(wbt+'||'+eml+'||'+password_record2, vault_key)
        store_record(usr2, ciphertext, nonce, tag)
        Label(screen5, text = "Password Generated Successfully", fg = "green", font = ("calibri", 11)).pack()
        Label(screen5, text = password_record2, font = ("calibri", 11)).pack()

    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        websites_all = []
        emails_all = []
        passwords_all = []
        for tup in dec_record.split('|||'):
            li = str(tup).split('||')
            websites_all.append(str(li[0]).lower())
            emails_all.append(str(li[1]).lower())
            passwords_all.append(str(li[2]))
        
        flag = 0
        if (wbt.lower() in websites_all) and (eml.lower() in emails_all):
            indices_of_website = [i for i, x in enumerate(websites_all) if x == wbt]
            for ind in indices_of_website:
                if(emails_all[ind] == eml.lower()):
                    flag = 1
                    passwords_all[ind] = password_record2
                    dec_record = ''
                    dec_record = websites_all[0] + '||' + emails_all[0] + '||' + passwords_all[0]
                    for i in range(1, len(websites_all)):
                        dec_record = dec_record + '|||' + websites_all[i] + '||' + emails_all[i] + '||' + passwords_all[i]
                    break

        if(flag==0):
            dec_record = dec_record + '|||' + wbt+'||'+eml+'||'+password_record2

        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr2, ciphertext, nonce, tag)
        if flag == 0:
            Label(screen5, text = "Password Generated Successfully", fg = "green", font = ("calibri", 11)).pack()
        else:
            Label(screen5, text = "Password Updated Successfully", fg = "green", font = ("calibri", 11)).pack()

def confirm_password_del():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("500x400")

    global username_d, password_d, username_entry_d, password_entry_d

    username_d = StringVar()
    password_d = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    username_entry_d = Entry(screen2, textvariable = username_d)
    username_entry_d.pack()
    Label(screen2, text = "Password").pack()
    password_entry_d = Entry(screen2, textvariable = password_d, show="*")
    password_entry_d.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "Confirm Password", width = 20, height = 1, command = del_passwords_button).pack()

def del_passwords_button():
    global usr3, pwd3
    usr3 = username_d.get()
    pwd3 = password_d.get()

    username_entry_d.delete(0, END)
    password_entry_d.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr3)

    check = check_auth_hash(pwd3, usr3, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        screen2.after(0, screen2.destroy)

        global screen6
        screen6 = Toplevel(screen)
        screen6.title("Delete Passwords")
        screen6.geometry("500x400")

        global website3, email3, website_entry3, email_entry3

        website3 = StringVar()
        email3 = StringVar()

        Label(screen6, text = "Please enter details below").pack()
        Label(screen6, text = "").pack()
        Label(screen6, text = "Website name").pack()
        website_entry3 = Entry(screen6, textvariable = website3)
        website_entry3.pack()
        Label(screen6, text = "Email/User ID on Website").pack()
        email_entry3 = Entry(screen6, textvariable = email3)
        email_entry3.pack()
        Label(screen6, text = "").pack()
        Button(screen6, text = "Delete Password", width = 20, height = 1, command = del_passwords).pack()

def del_passwords():
    ws = website3.get()
    em = email3.get()

    website_entry3.delete(0, END)
    email_entry3.delete(0, END)

    record, nonce, tag = retrieve_record(usr3)
    vault_salt = retrieve_vault_salt(usr3)
    vault_key_wsalt = get_vault_key(pwd3, vault_salt, usr3)
    vault_key = vault_key_wsalt[32:]

    if(record == 'Empty'):
        Label(screen6, text = "Password vault is empty.", font = ("calibri", 11)).pack()
    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        websites_all = []
        emails_all = []
        passwords_all = []
        for tup in dec_record.split('|||'):
            li = str(tup).split('||')
            websites_all.append(str(li[0]).lower())
            emails_all.append(str(li[1]).lower())
            passwords_all.append(str(li[2]))
        
        flag = 0
        if (ws.lower() in websites_all) and (em.lower() in emails_all):
            indices_of_website = [i for i, x in enumerate(websites_all) if x == ws]
            for ind in indices_of_website:
                if(emails_all[ind] == em.lower()):
                    flag = 1
                    websites_all.pop(ind)
                    emails_all.pop(ind)
                    passwords_all.pop(ind)
                    dec_record = ''
                    dec_record = websites_all[0] + '||' + emails_all[0] + '||' + passwords_all[0]
                    for i in range(1, len(websites_all)):
                        dec_record = dec_record + '|||' + websites_all[i] + '||' + emails_all[i] + '||' + passwords_all[i]
                    Label(screen6, text = "Password Deleted Successfully", fg = "green", font = ("calibri", 11)).pack()
                    break

        if(flag==0):
            Label(screen6, text = "Website-User ID Pair does not Exist", fg = "red", font = ("calibri", 11)).pack()

        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr3, ciphertext, nonce, tag) 

def confirm_password_v1():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("500x400")

    global username_v1, password_v1, username_entry_v1, password_entry_v1

    username_v1 = StringVar()
    password_v1 = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    username_entry_v1 = Entry(screen2, textvariable = username_v1)
    username_entry_v1.pack()
    Label(screen2, text = "Password").pack()
    password_entry_v1 = Entry(screen2, textvariable = password_v1, show="*")
    password_entry_v1.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "Confirm Password", width = 20, height = 1, command = v1_passwords_button).pack()

def v1_passwords_button():
    global usr4, pwd4
    usr4 = username_v1.get()
    pwd4 = password_v1.get()

    username_entry_v1.delete(0, END)
    password_entry_v1.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr4)

    check = check_auth_hash(pwd4, usr4, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        screen2.after(0, screen2.destroy)

        global screen7
        screen7 = Toplevel(screen)
        screen7.title("View Specific Password")
        screen7.geometry("500x400")

        global website4, email4, website_entry4, email_entry4

        website4 = StringVar()
        email4 = StringVar()

        Label(screen7, text = "Please enter details below").pack()
        Label(screen7, text = "").pack()
        Label(screen7, text = "Website name").pack()
        website_entry4 = Entry(screen7, textvariable = website4)
        website_entry4.pack()
        Label(screen7, text = "Email/User ID on Website").pack()
        email_entry4 = Entry(screen7, textvariable = email4)
        email_entry4.pack()
        Label(screen7, text = "").pack()
        Button(screen7, text = "View Specific Password", width = 20, height = 1, command = v1_passwords).pack()

def v1_passwords():
    w = website4.get()
    e = email4.get()

    website_entry4.delete(0, END)
    email_entry4.delete(0, END)

    record, nonce, tag = retrieve_record(usr4)
    vault_salt = retrieve_vault_salt(usr4)
    vault_key_wsalt = get_vault_key(pwd4, vault_salt, usr4)
    vault_key = vault_key_wsalt[32:]

    if(record == 'Empty'):
        Label(screen6, text = "Password vault is empty.", font = ("calibri", 11)).pack()
    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        websites_all = []
        emails_all = []
        passwords_all = []
        for tup in dec_record.split('|||'):
            li = str(tup).split('||')
            websites_all.append(str(li[0]).lower())
            emails_all.append(str(li[1]).lower())
            passwords_all.append(str(li[2]))
        
        flag = 0
        if (w.lower() in websites_all) and (e.lower() in emails_all):
            indices_of_website = [i for i, x in enumerate(websites_all) if x == w]
            for ind in indices_of_website:
                if(emails_all[ind] == e.lower()):
                    flag = 1
                    Label(screen7, text = "Password for this website and email pair:", font = ("calibri", 11)).pack()
                    Label(screen7, text = passwords_all[ind], font = ("calibri", 11)).pack()

        if(flag==0):
            Label(screen7, text = "Website-User ID Pair does not Exist", fg = "red", font = ("calibri", 11)).pack()

        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr4, ciphertext, nonce, tag)

def main_screen():
    global screen
    screen = Tk()
    screen.geometry("500x450")
    screen.title("CZ4010 Password Manager")
    Label (text = "CZ4010 Password Manager", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Sign Up", height = "2", width = "40", command = sign_up).pack()
    Label(text = "").pack()
    Button(text = "View Specific Password", height = "2", width = "40", command = confirm_password_v1).pack()
    Label(text = "").pack()
    Button(text = "View Passwords", height = "2", width = "40", command = view_passwords_button).pack()
    Label(text = "").pack()
    Button(text = "Add Passwords", height = "2", width = "40", command = confirm_password_add).pack()
    Label(text = "").pack()
    Button(text = "Generate Passwords", height = "2", width = "40", command = confirm_password_gen).pack()
    Label(text = "").pack()
    Button(text = "Delete Passwords", height = "2", width = "40", command = confirm_password_del).pack()

    screen.mainloop()

main_screen()
