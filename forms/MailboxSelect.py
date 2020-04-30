import npyscreen

from logic.Service import Service
from logic.Store import Store

class MailboxList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        Store.current_mailbox = act_on_this
        Service.select_mailbox(Store.current_mailbox)

        if not Store.current_mailbox.loaded:
            Service.fetch_more(Store.current_mailbox)

        self.parent.parentApp.switchForm('INBOX')

    def display_value(self, vl):
        return vl.name_dec

class MailboxSelect(npyscreen.FormBaseNew):
    def create(self):
        self.name = f'Mailbox [{Store.username}]'
        self.list = self.add(MailboxList)

    def beforeEditing(self):
        self.list.values = Store.mailboxes