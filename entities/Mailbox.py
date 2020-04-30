from imapclient import imap_utf7

class Mailbox:
    def __init__(self, name, flags):
        self.name = name
        self.name_dec = imap_utf7.decode(name.encode())
        self.flags = flags
        self.max_uid = 0
        self.last_loaded_uid = None
        self.loaded = False
        self.messages = []