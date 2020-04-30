class EMail():
    def __init__(self):
        self.uid = None
        self.message_id = ''
        self.subject = 'subject'
        self.content = 'content'
        self.sender = 'from'
        self.to = ''
        self.cc = ''
        self.bcc = ''
        self.date = ''
        self.loaded_content = False

    def __eq__(self, other):
        return self.uid == other.uid