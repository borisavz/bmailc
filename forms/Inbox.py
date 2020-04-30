import npyscreen

from logic.Store import Store
from logic.Service import Service

class InboxList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        Store.current_message = act_on_this

        if not Store.current_message.loaded_content:
            Service.load_message(Store.current_message)

        self.parent.parentApp.switchForm('MESSAGE')

    def display_value(self, vl):
        return vl.subject

class NewMessageButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('NEW_MESSAGE')

class LoadMoreButton(npyscreen.ButtonPress):
    def whenPressed(self):
        Service.fetch_more(Store.current_mailbox)
        self.parent.list.values = Store.current_mailbox.messages
        self.parent.list.display()

class MailboxButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('MAILBOX_SELECT')

class QuitButton(npyscreen.ButtonPress):
    def whenPressed(self):
        Service.imap_refresh.stop()
        Service.imap_conn.logout()
        self.parent.parentApp.switchForm(None)

class Inbox(npyscreen.FormBaseNew):
    def create(self):
        self.list = self.add(InboxList, max_height=self.max_y - 6)

        self.new_message_button = self.add(NewMessageButton, rely=self.max_y - 3, name='New message')
        self.prev_button = self.add(LoadMoreButton, rely=self.max_y - 3, relx=15, name='Load more')
        self.mailbox_button = self.add(MailboxButton, rely=self.max_y - 3, relx=26, name='Mailbox')
        self.quit_button = self.add(QuitButton, rely=self.max_y - 3, relx=35, name='Quit')

    def beforeEditing(self):
        if not Store.initialized:
            Store.initialized = True

            Service.connect_imap()
            Store.current_mailbox = Store.mailboxes[0]

            Service.select_mailbox(Store.current_mailbox)
            Service.fetch_more(Store.current_mailbox)

        self.name = f'{Store.current_mailbox.name_dec} [{Store.username}]'
        self.list.values = Store.current_mailbox.messages
        self.list.display()
