from email import message_from_string
from getpass import getpass
from imaplib import IMAP4_SSL
import re

number = re.compile(b'[0-9]+')

def main_spamtrash():
    mail = IMAP4_SSL("imap.gmail.com")
    mail.login('andrzej.cichocki@gmail.com', getpass())
    #_, v = mail.list()
    #for x in v: print(x)
    mail.select('[Gmail]/Spam')
    _, (v,) = mail.search(None, 'ALL')
    ids = number.findall(v)
    for id in ids:
        _, data = mail.fetch(id, '(RFC822)')
        print(message_from_string(data[0][1].decode('latin-1')))
        break
