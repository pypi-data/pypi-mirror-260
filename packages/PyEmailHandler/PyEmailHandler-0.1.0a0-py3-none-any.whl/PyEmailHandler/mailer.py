import smtplib, ssl
import imaplib
import email
import re
from email.message import Message
from email.mime.text import MIMEText # this object contains the html and ascii content
from email.mime.multipart import MIMEMultipart # this is where we combine the two 
from email.utils import formataddr
from email.header import Header
from typing import Union, Literal, List

class EmailSMTP:
    def __init__(self, 
                 username, 
                 password,
                 sender_mail,
                 sender_name,
                 smtp_server,
                 port=465,
                 protocol: Union[Literal['starttls'], Literal['ssl']]="ssl"):
        self.username = username
        self.password = password
        self.sender_mail = sender_mail
        self.sender_name = sender_name
        self.smtp_address = smtp_server
        self.port = port
        self.protocol = protocol
        self.context = ssl.create_default_context()
        self.smtp: smtplib.SMTP = None
        
    def start_connection(self):
        if self.protocol == 'ssl':
            self.smtp = smtplib.SMTP_SSL(self.smtp_address, self.port, context=self.context, timeout=30)
            self.smtp.login(user=self.username, password=self.password)
        elif self.protocol == 'starttls':
            self.smtp = smtplib.SMTP(self.smtp_address, self.port, timeout=30)
            self.smtp.starttls(context=self.context)
            self.smtp.login(user=self.username, password=self.password)
        self.smtp.ehlo()

    def send(self, receiver, subject, body, _type="plain"):
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self.sender_mail if not self.sender_name else formataddr((
            cast(Header(self.sender_name, 'utf-8'), str),
            self.sender_mail
        ))
        message['To'] = receiver
        message.attach(MIMEText(body, _type))
        if not self.smtp:
            raise ValueError('Connection to SMTP not established')
        self.connection_persist()
        self.smtp.sendmail(from_addr=self.sender_mail, to_addrs=receiver, msg=message.as_string())
    
    def send_raw(self, receiver, mime: MIMEText):
        message = mime
        if not self.smtp:
            raise ValueError('Connection to SMTP not established')
        self.connection_persist()
        self.smtp.sendmail(from_addr=self.sender_mail, to_addrs=receiver, msg=message.as_string())
    
    def connection_persist(self):
        "Reconnects connection if session is terminated"
        if not self._is_connected():
            self.start_connection()

    def _is_connected(self):
        try:
            status = self.smtp.noop()[0]
        except (smtplib.SMTPServerDisconnected, AttributeError):
            status = -1
        return True if status == 250 else False
    
    def close(self):
        self.smtp.close()

class EmailIMAP:
    def __init__(self, 
                 username, 
                 password,
                 imap_server,
                 port=993,
                 protocol: Union[Literal['starttls'], Literal['ssl']]="ssl"):
        self.username = username
        self.password = password
        self.imap_address = imap_server
        self.port = port
        self.protocol = protocol
        self.context = ssl.create_default_context()
        self.imap: imaplib.IMAP4 = None
    
    def start_connection(self):
        if self.protocol == 'ssl':
            self.imap = imaplib.IMAP4_SSL(self.imap_address, self.port, ssl_context=self.context, timeout=30)
            retcode, message_indices = self.imap.login(user=self.username, password=self.password)
        elif self.protocol == 'starttls':
            self.imap = imaplib.IMAP4(self.imap_address, self.port, timeout=30)
            self.imap.starttls(ssl_context=self.context)
            retcode, message_indices = self.smtp.login(user=self.username, password=self.password)
        if retcode != "OK":
            raise ValueError("IMAP login failed! Return code: '" + cast(retcode, str) + "'.")
    
    def get_folder(self, name):
        _retcode, msg_count = self.imap.select(name)
        try:
            self._recheck(_retcode)
        except ValueError:
            return False
        return msg_count
    
    def create_folder(self, name):
        _retcode, data = self.imap.create(name)
        try:
            self._recheck(_retcode)
        except ValueError:
            return False
        return data

    def get_mails(self, folder='Inbox', _indices=0):
        '''
        Collect all mails from the inbox
        '''
        self.imap.select(folder)
        _retcode, message_indices = self.imap.search(None, 'ALL')
        self._recheck(_retcode)
        mails: List[Message] = []
        for message_index in message_indices[_indices].split():
            _retcode, data  = self.imap.fetch(message_index, '(RFC822)')
            self._recheck(_retcode)
            message = email.message_from_string(data[0][1].decode('utf-8'))
            _retcode, data = self.imap.fetch(message_index, "(UID)")
            self._recheck(_retcode)
            mail_uid = self.parse_uid(cast(data[0], str, 'UTF-8'))
            message['mailserver_email_uid'] = mail_uid
            mails.append(message)
        return mails

    def delete_mail(self, mail, _trash_folder = 'Trash'):
        '''
        Deletes a mail
        '''
        _retcode, message = self.imap.uid('COPY', mail['mailserver_email_uid'], _trash_folder)
        self._recheck(_retcode, _reason=message)
        self.imap.uid('STORE', mail['mailserver_email_uid'], '+FLAGS', '(\Deleted)')
        self.imap.expunge()

    def _recheck(self, _retcode, _reason = None):
        if _retcode != "OK":
            if _reason:
                raise ValueError(f"An error occured due to: {_reason}")
            raise ValueError("An error occured while checking mail")
        
    def parse_uid(self, data):
        pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
        match = pattern_uid.match(data)
        return match.group('uid')

def cast(obj, to_type, options=None):
    try:
        if options is None:
            return to_type(obj)
        else:
            return to_type(obj, options)
    except ValueError and TypeError:
        return obj