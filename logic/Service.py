import quopri
import re
import ssl
import email

from threading import Thread, Event, Lock
from datetime import timedelta

from bs4 import BeautifulSoup
from imaplib import IMAP4_SSL, IMAP4
from smtplib import SMTP_SSL, SMTP
from entities.EMail import EMail
from logic.Store import Store
from logic.Utils import Utils

class IMAPRefresh(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = False
        self.stopped = Event()
        self.interval = timedelta(seconds=300)

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            Service.imap_mutex.acquire()
            Service.imap_conn.noop()
            Service.imap_mutex.release()

class Service:
    imap_mutex = None
    imap_refresh = None
    imap_conn = None
    smtp_conn = None

    ssl_context = ssl.create_default_context()

    @staticmethod
    def connect_imap():
        if Store.imap_encryption == 'SSL':
            Service.imap_conn = IMAP4_SSL(Store.imap_server, Store.imap_port, ssl_context=Service.ssl_context)
        else:
            Service.imap_conn = IMAP4(Store.imap_server, Store.imap_port)

            if Store.imap_encryption == 'TLS':
                Service.imap_conn.starttls(ssl_context=Service.ssl_context)

        Service.imap_conn.login(Store.username, Store.password)
        typ, folder_list = Service.imap_conn.list()

        for f in folder_list:
            Store.mailboxes.append(Utils.dec_list(f))

        Service.imap_mutex = Lock()

        Service.imap_refresh = IMAPRefresh()
        Service.imap_refresh.start()

    @staticmethod
    def select_mailbox(box):
        Service.imap_mutex.acquire()
        box.max_uid = int(Service.imap_conn.select(f'"{box.name}"')[1][0])
        Service.imap_mutex.release()

    @staticmethod
    def fetch_more(box):
        num = 20

        if box.max_uid == 0 or box.last_loaded_uid == 1:
            return

        Service.imap_mutex.acquire()

        from_uid = 1
        to_uid = 1

        if box.last_loaded_uid is None:
            to_uid = box.max_uid
        else:
            to_uid = box.last_loaded_uid - 1

        if to_uid > num:
            from_uid = to_uid - num + 1

        typ, data = Service.imap_conn.uid('FETCH', f'{from_uid}:{to_uid}', '(BODY.PEEK[HEADER])')
        data.reverse()
        box.last_loaded_uid = from_uid

        for i in range(1, len(data), 2):
            message = email.message_from_bytes(data[i][1])

            m = EMail()

            # 3 (UID 3 BODY[HEADER]{2779}
            m.uid = data[i][0].decode().split()[2]

            m.message_id = Utils.dec_header(message, 'Message-ID')
            m.subject = Utils.dec_header(message, 'Subject')
            m.sender = Utils.dec_header(message, 'From')
            m.to = Utils.dec_header(message, 'To')
            m.cc = Utils.dec_header(message, 'Cc')
            m.date = Utils.dec_header(message, 'Date')
            m.loaded_headers = True

            box.messages.append(m)

        box.loaded = True
        Service.imap_mutex.release()

    @staticmethod
    def load_message(message):
        Service.imap_mutex.acquire()

        typ, data = Service.imap_conn.uid('FETCH', message.uid, '(RFC822)')

        msg = email.message_from_bytes(data[0][1])
        html = ''

        if msg.is_multipart():
            for part in msg.walk():
                if 'html' in part.get_content_type():
                    html = part.get_payload()
                    break
        else:
            html = msg.get_payload()

        html_dec = quopri.decodestring(html)
        soup = BeautifulSoup(html_dec, 'html.parser')
        message.content = re.sub('\n+', '\n', soup.get_text()).strip()
        message.loaded_content = True

        Service.imap_mutex.release()

    @staticmethod
    def send(msg):
        if Store.smtp_encryption == 'SSL':
            Service.smtp_conn = SMTP_SSL(Store.smtp_server, Store.smtp_port, context=Service.ssl_context)
        else:
            Service.smtp_conn = SMTP(Store.smtp_server, Store.smtp_port)

            if Store.smtp_encryption == 'TLS':
                Service.smtp_conn.starttls(context=Service.ssl_context)

        Service.smtp_conn.login(Store.username, Store.password)
        Service.smtp_conn.send_message(msg)
        Service.smtp_conn.quit()

    @staticmethod
    def delete(message):
        Service.imap_mutex.acquire()
        Store.current_mailbox.messages.remove(message)
        Service.imap_conn.uid('STORE', message.uid, '+FLAGS', '(\\Deleted)')
        Service.imap_conn.expunge()
        Service.imap_mutex.release()