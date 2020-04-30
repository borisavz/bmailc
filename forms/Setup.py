import npyscreen

from logic.Store import Store

encryption = ['SSL', 'TLS', 'None']

class Setup(npyscreen.Form):
    def create(self):
        self.name = 'Server setup'

        self.imap_server_input = self.add(npyscreen.TitleText, name = 'IMAP server')
        self.imap_port_input = self.add(npyscreen.TitleText, name = 'Port')
        self.imap_encryption_input = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0], name='Encryption',
                   values=encryption, scroll_exit=True)

        self.nextrely += 1

        self.smtp_server_input = self.add(npyscreen.TitleText, name = 'SMTP server')
        self.smtp_port_input = self.add(npyscreen.TitleText, name = 'Port')
        self.smtp_encryption_input = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0], name='Encryption',
                   values=encryption, scroll_exit=True)

    def afterEditing(self):
        Store.imap_server = self.imap_server_input.value
        Store.imap_port = int(self.imap_port_input.value)
        Store.imap_encryption = encryption[self.imap_encryption_input.value[0]]

        Store.smtp_server = self.smtp_server_input.value
        Store.smtp_port = int(self.smtp_port_input.value)
        Store.smtp_encryption = encryption[self.smtp_encryption_input.value[0]]

        self.parentApp.setNextForm('LOGIN')