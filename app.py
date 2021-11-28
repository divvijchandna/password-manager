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

    usr = username_v.get()
    pwd = password_v.get()

    username_entry_v.delete(0, END)
    password_entry_v.delete(0, END)

    auth_hash_wsalt = retrieve_auth_hash(usr)

    check = check_auth_hash(pwd, usr, auth_hash_wsalt)

    if not check:
        Label(screen2, text = "Password is incorrect. Try again.", fg = "red", font = ("calibri", 11)).pack()
    else:
        screen2.after(200, screen2.destroy)
        record, nonce, tag = retrieve_record(usr)
        salt_vault = retrieve_vault_salt(usr)
        vault_key_wsalt = get_vault_key(pwd, salt_vault, usr)
        vault_key = vault_key_wsalt[32:]

        screen3 = Toplevel(screen)
        screen3.title("View Passwords")
        screen3.geometry("500x400")

        if(record == 'Empty'):
            Label(screen3, text = record).pack()
        else:
            dec_record = decrypt(vault_key, nonce, tag, record)
            Label(screen3, text = dec_record).pack()

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

        global website, password_record, website_entry, password_record_entry

        website = StringVar()
        password_record = StringVar()

        Label(screen4, text = "Please enter details below").pack()
        Label(screen4, text = "").pack()
        Label(screen4, text = "Website name").pack()
        website_entry = Entry(screen4, textvariable = website)
        website_entry.pack()
        Label(screen4, text = "Password").pack()
        password_record_entry = Entry(screen4, textvariable = password_record, show="*")
        password_record_entry.pack()
        Label(screen4, text = "").pack()
        Button(screen4, text = "Add Password", width = 20, height = 1, command = add_passwords).pack()

def add_passwords():

    wbs = website.get()
    pwr = password_record.get()

    website_entry.delete(0, END)
    password_record_entry.delete(0, END)    

    record, nonce, tag = retrieve_record(usr)
    vault_salt = retrieve_vault_salt(usr)
    vault_key_wsalt = get_vault_key(pwd, vault_salt, usr)
    vault_key = vault_key_wsalt[32:]

    if(record == 'Empty'):
        nonce, ciphertext, tag = encrypt(wbs+'||'+pwr, vault_key)
        store_record(usr, ciphertext, nonce, tag)
        Label(screen4, text = "Password Added Successfully", fg = "green", font = ("calibri", 11)).pack()
        screen4.after(1000, screen4.destroy)
    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        dec_record = dec_record + '|||' + wbs+'||'+pwr
        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr, ciphertext, nonce, tag)
        Label(screen4, text = "Password Added Successfully", fg = "green", font = ("calibri", 11)).pack()
        screen4.after(1000, screen4.destroy)

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
        screen5.geometry("500x400")

        global website2, password_length, website_entry2, password_length_entry

        website2 = StringVar()
        password_length = StringVar()

        Label(screen5, text = "Please enter details below").pack()
        Label(screen5, text = "").pack()
        Label(screen5, text = "Website name").pack()
        website_entry2 = Entry(screen5, textvariable = website2)
        website_entry2.pack()
        Label(screen5, text = "Password Length").pack()
        password_length_entry = Entry(screen5, textvariable = password_length, show="")
        password_length_entry.pack()
        Label(screen5, text = "").pack()
        Button(screen5, text = "Generate Password", width = 20, height = 1, command = gen_passwords).pack()

def gen_passwords():

    wbt = website2.get()
    pwl = password_length.get()

    website_entry2.delete(0, END)
    password_length_entry.delete(0, END)    

    record, nonce, tag = retrieve_record(usr2)
    vault_salt = retrieve_vault_salt(usr2)
    vault_key_wsalt = get_vault_key(pwd2, vault_salt, usr2)
    vault_key = vault_key_wsalt[32:]
    password_record2 = str(make_password(int(pwl)))

    if(record == 'Empty'):
        nonce, ciphertext, tag = encrypt(wbt+'||'+password_record2, vault_key)
        store_record(usr2, ciphertext, nonce, tag)
        Label(screen5, text = "Password Generated Successfully", fg = "green", font = ("calibri", 11)).pack()
        screen5.after(1000, screen5.destroy)
    else:
        dec_record = decrypt(vault_key, nonce, tag, record)
        dec_record = dec_record + '|||' + wbt+'||'+password_record2
        nonce, ciphertext, tag = encrypt(dec_record, vault_key)
        store_record(usr2, ciphertext, nonce, tag)
        Label(screen5, text = "Password Added Successfully", fg = "green", font = ("calibri", 11)).pack()
        screen5.after(1000, screen5.destroy)

def main_screen():
    global screen
    screen = Tk()
    screen.geometry("500x400")
    screen.title("CZ4010 Password Manager")
    Label (text = "CZ4010 Password Manager", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Sign Up", height = "2", width = "40", command = sign_up).pack()
    Label(text = "").pack()
    Button(text = "View Passwords", height = "2", width = "40", command = view_passwords_button).pack()
    Label(text = "").pack()
    Button(text = "Add Passwords", height = "2", width = "40", command = confirm_password_add).pack()
    Label(text = "").pack()
    Button(text = "Generate Passwords", height = "2", width = "40", command = confirm_password_gen).pack()

    screen.mainloop()

main_screen()
