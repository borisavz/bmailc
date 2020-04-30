import npyscreen

from logic.Store import Store

class Login(npyscreen.Form):
    def create(self):
        self.name = 'Login'

        self.username_input = self.add(npyscreen.TitleText, name = 'Username')
        self.password_input = self.add(npyscreen.TitlePassword, name='Password')

    def afterEditing(self):
        Store.username = self.username_input.value
        Store.password = self.password_input.value

        self.parentApp.setNextForm('INBOX')