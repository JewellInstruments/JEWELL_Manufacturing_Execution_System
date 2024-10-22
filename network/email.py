import logging
from typing import Union
import smtplib

from system import settings


# send an email over the email server.


def email(to: Union[list, str], msg: str = "") -> None:
    """ """
    if isinstance(to, str):
        to = to
    elif isinstance(to, list):
        if len(to) == 0:
            print("Email recipients is empty.")
            return
        else:
            to = "; ".join(to)
    else:
        print("Issue with the recipients emails...")
        return

    if not msg:
        body = "Please come help"
        subject = "help"
    else:
        body = msg
        subject = "Status Update"

    sent_from = settings.__EMAIL__

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (
        sent_from,
        to,
        subject,
        body,
    )
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.sendmail(sent_from, to, email_text)
        server.close()
    except Exception as e:
        logging.warning(f"Unable to send email... {e}")
        print(e)
    return
