from . import EmailSMTP
from .mailer import cast
from email.message import Message as emailMessage
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid, parseaddr
from email.header import Header, decode_header

def reply_mail(
        smtp: EmailSMTP,
        mail: emailMessage,
        message: MIMEText,
):
    '''
    Reply to the Received receipient on selected mail on IMAP.

    EmailSMTP: EmailSMTP instance that has active smtp connection
    mail: Selected recepient to reply to
    message: MIMEText that contains the `body` and `Subject`. `To` and `From` is not required
    '''
    msg = message
    receiver_full = decode_header(mail['Reply-To'] or mail['From'])[0][0]
    receiver_name, receiver_address = parseaddr(receiver_full)
    sender = smtp.sender_mail
    sender_name = smtp.sender_name
    msg['To'] = receiver_full
    msg["Message-ID"] = make_msgid()
    msg['Subject'] = "Re: " + (mail["Subject"] or '(no subject)')
    msg["In-Reply-To"] = mail["Message-ID"]
    msg["References"] = (mail["References"] or "") + " " + mail["Message-Id"]
    if sender:
        msg['From'] = formataddr((
            cast(Header(sender_name, 'utf-8'), str),
            sender
        ))
    smtp.connection_persist()
    smtp.send_raw(receiver=receiver_address, mime=msg)
