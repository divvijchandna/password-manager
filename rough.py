# record = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||&4yRbk|||Google||dc@gmail.com||bleh|||Yahoo||dc@yahoo.com||z#bF!CR:9k*g|||Snapchat||divvij04||cool|||Reddit||chandbabu||hot'

# websites = []
# emails = []
# passwords = []

# website = 'facebOK'
# email = 'divvij@NTu.com'


# for tup in record.split('|||'):
#     li = str(tup).split('||')
#     websites.append(str(li[0]).lower())
#     emails.append(str(li[1]).lower())
#     passwords.append(str(li[2]))

# print(websites)
# print()
# print(emails)
# print()
# print(passwords)
# print()

# print(websites.index(website.lower()))
# print(emails.index(email.lower()))
import secrets
import tkinter     

li = ['1','2','3','4','5', '2']
indices = [i for i, x in enumerate(li) if x == '2']
print(indices)

rec1 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||&4yRbk|||Google||dc@gmail.com||bleh|||Yahoo||dc@yahoo.com||z#bF!CR:9k*g|||Snapchat||divvij04||cool|||Reddit||chandbabu||hot|||Reddit||chandbabu||/ApYU0W|||Google||dc@gmail.com||H.p)360'

rec2 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||~oGv5'

rec3 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'
rec4 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'
rec5 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7|||facebook||divvij@fb.com||Z*R3v'
rec6 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7|||facebook||divvij@fb.com||ontCfMbw3f%h!uQm/4mh'
rec7 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7|||miniclip||gamerboy||L$VSF4m93,pu'
rec8 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'
rec8 = 'instagram||divvij.chandna@gmail.com||:8KG0Shf|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'
rec9 = 'instagram||divvij.chandna@gmail.com||pp1!#p=($k7EC#MfxU):|||facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'
reca = '                                                            facebook||divvij@ntu.com||$Dq:um94!hTV|||google||dc@gmail.com||bleh|||yahoo||dc@yahoo.com||z#bF!CR:9k*g|||snapchat||divvij04||cool|||reddit||chandbabu||hot|||reddit||chandbabu||/ApYU0W|||google||dc@gmail.com||H.p)360|||qwerty||divvij@qwerty.com||Rpdk&0RAY7'

print(secrets.randbits(10))
