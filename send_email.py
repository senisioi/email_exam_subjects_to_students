import csv
import getpass
import logging
import mimetypes
import os
import sys
import smtplib
from email.message import EmailMessage
from copy import deepcopy

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)


DFLT_BODY = """
Descărcați subiectul atașat și urmăriți cu atenție cerința.

Succes!
"""
DFLT_SUBJECT = 'Test de laborator la Inteligență Artificială, seria 35'
DFLT_SENDER = 'examen@unibuc.ro'

DFLT_MESSAGE = EmailMessage()
DFLT_MESSAGE['Subject'] = DFLT_SUBJECT
DFLT_MESSAGE.set_content(DFLT_BODY)



def get_mime(fisier):
    mime_type, _ = mimetypes.guess_type(fisier)
    mime_type, mime_subtype = mime_type.split('/')
    return (mime_type, mime_subtype)


def get_content(fisier):
    with open(fisier, 'rb') as file:
        return file.read()


def get_mesaj(fisier, email_student, sender=DFLT_SENDER):
    mesaj = deepcopy(DFLT_MESSAGE)
    mesaj['From'] = sender
    mesaj['To'] = email_student.strip()
    mime_type, mime_subtype = get_mime(fisier)
    atasament = get_content(fisier)
    mesaj.add_attachment(atasament,
                           maintype=mime_type,
                           subtype=mime_subtype,
                           filename=os.path.basename(fisier))
    return mesaj


def files_in_folder(directory, extension='.zip'):
    retval = []
    for fis in os.listdir(directory):
        _, file_ext = os.path.splitext(fis)
        file_ext = file_ext.strip()
        if not os.path.isdir(fis) and file_ext == extension:
            retval.append(os.path.join(directory, fis))
    return retval


def main():
    # make sure you enable less secure apps from:
    # https://myaccount.google.com/lesssecureapps
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.set_debuglevel(1)

    email = input("Sender email: ")
    email = email.strip()
    pwd = getpass.getpass(prompt='Password: ', stream=None)
    pwd = pwd.strip()
    #mail_server.login("email@unibuc.ro", '**********')
    tries = 3
    while tries > 0:
        try:
            mail_server.login(email, pwd)
            tries = -5
        except:
            logging.exception('Wrong email or password, try again.')
            email = input("Sender email: ")
            pwd = getpass.getpass(prompt='Password: ', stream=None)
            tries -= 1

    if tries != -5:
        logging.error('Too many attempts!')
        sys.exit(-1)


    # input: un director in care se afla toate arhivele cu subiecte 
    #        cu numele format din emailul studetilor
    arhive_subiecte = './arhive_subiecte'
    subiecte = files_in_folder(arhive_subiecte)
    for arhiva in subiecte:
        subiect = os.path.basename(arhiva).strip()
        logging.info("Sending %s ", subiect)
        email_student = subiect.replace('.zip', '')
        mesaj = get_mesaj(arhiva, email_student, email)
        mail_server.send_message(mesaj)
    mail_server.quit()


if __name__ == '__main__':
    main()

