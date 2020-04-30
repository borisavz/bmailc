import npyscreen

from logic.Utils import Utils
from logic.Store import Store
from logic.Service import Service
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class NewMessage(npyscreen.ActionForm):
    def create(self):
        self.name = 'New message'

        self.subject_input = self.add(npyscreen.TitleText, name = 'Subject')
        self.to_input = self.add(npyscreen.TitleText, name='To')
        self.cc_input = self.add(npyscreen.TitleText, name='Cc')
        self.bcc_input = self.add(npyscreen.TitleText, name='Bcc')

        self.text_input = self.add(npyscreen.MultiLineEdit, name = 'Text')

    def on_ok(self):
        send = npyscreen.notify_yes_no('Are you sure you want to send message?', title='Send message')

        if send:
            self.sendMessage()
            self.back()

    def on_cancel(self):
        discard = npyscreen.notify_yes_no('Are you sure you want to discard message?', title='Discard message')

        if discard:
            self.back()

    def back(self):
        if Store.reply:
            Store.reply = False
            self.parentApp.switchForm('MESSAGE')
        else:
            self.parentApp.switchForm('INBOX')

    def beforeEditing(self):
        self.text_input.value = ''
        self.cc_input.value = ''
        self.bcc_input.value = ''

        if Store.reply:
            self.subject_input.value = 'Re: ' + Store.current_message.subject
            self.to_input.value = Store.current_message.sender
        else:
            self.subject_input.value = ''
            self.to_input.value = ''

    def sendMessage(self):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(s=self.subject_input.value).encode()
        msg['Sender'] = Store.username
        msg['To'] = Utils.enc_addresses(self.to_input.value.split(','))
        msg['Cc'] = Utils.enc_addresses(self.cc_input.value.split(','))
        msg['Bcc'] = Utils.enc_addresses(self.bcc_input.value.split(',')) #smtplib uses this internally and then discards it

        if Store.reply:
            msg['In-Reply-To'] = Store.current_message.message_id

        part2 = MIMEText(self.text_input.value, 'html')
        msg.attach(part2)

        Service.send(msg)