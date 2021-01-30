import csv
import logging
import mimetypes
import os
import smtplib
from email.message import EmailMessage
from copy import deepcopy

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)


DFLT_BODY = """
Descărcați subiectul atașat și urmăriți cu atenție cerința.

Succes!
"""
DFLT_SUBJECT = 'Test de laborator la Inteligență Artificială, seria 35'
DFLT_SENDER = 'sergiu.nisioi@unibuc.ro"'

DFLT_MESSAGE = EmailMessage()
DFLT_MESSAGE['From'] = DFLT_SENDER
DFLT_MESSAGE['Subject'] = DFLT_SUBJECT
DFLT_MESSAGE.set_content(DFLT_BODY)



def get_mime(fisier):
    mime_type, _ = mimetypes.guess_type(fisier)
    mime_type, mime_subtype = mime_type.split('/')
    return (mime_type, mime_subtype)


def get_content(fisier):
    with open(fisier, 'rb') as file:
        return file.read()


def get_mesaj(fisier, email_student):
    mesaj = deepcopy(DFLT_MESSAGE)
    mesaj['To'] = email_student.strip()
    mime_type, mime_subtype = get_mime(fisier)
    atasament = get_content(fisier)
    mesaj.add_attachment(atasament,
                           maintype=mime_type,
                           subtype=mime_subtype,
                           filename=os.path.basename(fisier))
    return mesaj


def files_in_folder(directory):
    return [os.path.join(directory, fis) for fis in os.listdir(directory) if not os.path.isdir(fis)]


def main():
    # make sure you enable less secure apps from:
    # https://myaccount.google.com/lesssecureapps 
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.set_debuglevel(1)
    mail_server.login("email@unibuc.ro", '**********')

    # input: un director in care se afla toate arhivele cu subiecte 
    #        cu numele format din emailul studetilor
    arhive_subiecte = './arhive_subiecte'
    subiecte = files_in_folder(arhive_subiecte)
    for arhiva in subiecte:
        subiect = os.path.basename(arhiva)
        email_student = subiect.replace('.zip', '')
        mesaj = get_mesaj(arhiva, email_student)
        mail_server.send_message(mesaj)
    mail_server.quit()


if __name__ == '__main__':
    main()

