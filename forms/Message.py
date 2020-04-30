import npyscreen

from logic.Service import Service
from logic.Store import Store

class ReplyButton(npyscreen.ButtonPress):
    def whenPressed(self):
        Store.reply = True
        self.parent.parentApp.switchForm('NEW_MESSAGE')

class DeleteButton(npyscreen.ButtonPress):
    def whenPressed(self):
        delete = npyscreen.notify_yes_no('Are you sure you want to delete message?', title='Delete message')

        if delete:
            Service.delete(Store.current_message)
            self.parent.parentApp.switchForm('INBOX')

class CancelButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('INBOX')

class Message(npyscreen.FormBaseNew):
    def create(self):
        self.name = 'Message'

        self.subject_text = self.add(npyscreen.TitleFixedText, name = 'Subject')
        self.from_text = self.add(npyscreen.TitleFixedText, name = 'From')
        self.to_text = self.add(npyscreen.TitleFixedText, name='To')
        self.cc_text = self.add(npyscreen.TitleFixedText, name = 'Cc')
        self.date_text = self.add(npyscreen.TitleFixedText, name='Date')

        self.content = self.add(npyscreen.MultiLineEdit, max_height=self.max_y - 11, value = '')

        self.reply_button = self.add(ReplyButton, rely=self.max_y - 3, name='Reply')
        self.delete_button = self.add(DeleteButton, rely=self.max_y - 3, relx=9, name='Delete')
        self.cancel_button = self.add(CancelButton, rely=self.max_y - 3, relx=17, name='Cancel')

    def beforeEditing(self):
        self.subject_text.value = Store.current_message.subject
        self.from_text.value = Store.current_message.sender
        self.to_text.value = Store.current_message.to
        self.cc_text.value = Store.current_message.cc
        self.date_text.value = Store.current_message.date
        self.content.value = Store.current_message.content