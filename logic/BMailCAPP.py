import npyscreen

from forms.Setup import Setup
from forms.Login import Login
from forms.Inbox import Inbox
from forms.MailboxSelect import MailboxSelect
from forms.Message import Message
from forms.NewMessage import NewMessage
from logic.Store import Store

class BMailCAPP(npyscreen.NPSAppManaged):

    def onStart(self):

        inbox_form = Inbox()
        setup_form = Setup()
        login_form = Login()

        if Store.server_set and Store.user_set:
            self.registerForm('MAIN', inbox_form)
        elif Store.server_set and not Store.user_set:
            self.registerForm('MAIN', login_form)
        else:
            self.registerForm('MAIN', setup_form)

        self.registerForm('SETUP', setup_form)
        self.registerForm('LOGIN', login_form)
        self.registerForm('INBOX', inbox_form)
        self.registerForm('MAILBOX_SELECT', MailboxSelect())
        self.registerForm('MESSAGE', Message())
        self.registerForm('NEW_MESSAGE', NewMessage())

