# PyEmailHandler

Receive and Send emails at ease. 

Intended for quick and easy projects that does not require specific function other than to receive, send and reply to emails.

**Supports:**
* IMAP4
* SMTP

Basic Usage: 

**Send Email**
```py
from PyEmailHandler import EmailSMTP
email = EmailSMTP(
        username="smtp_username",
        password="smtp_password",
        sender_mail="sender@example.com",
        sender_name="WeSend",
        smtp_server="smtp.example.com",
        port = 587,
        protocol = "starttls"
    )
email.start_connection()
email.send(
    receiver="recepient@mailaddress.com",
    subject="Subject of the e-mail",
    body="Content of the e-mail, can be as long as you want"
)
```

**Receive Inbox:**
```py
from PyEmailHandler import EmailIMAP
inbox = EmailIMAP(
        username="imap_username",
        password="imap_password",
        imap_server="imap.example.com",
        port=993,
        protocol="ssl"      
    )
inbox.start_connection()
mails = inbox.get_mails()
for mail in mails:
    print(mail)
```
