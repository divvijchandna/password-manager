record = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||&4yRbk'

websites = []
emails = []
passwords = []

website = 'facebOK'
email = 'divvij@NTu.com'


for tup in record.split('|||'):
    li = str(tup).split('||')
    websites.append(str(li[0]).lower())
    emails.append(str(li[1]).lower())
    passwords.append(str(li[2]))

print(websites)
print()
print(emails)
print()
print(passwords)
print()

print(websites.index(website.lower()))
print(emails.index(email.lower()))