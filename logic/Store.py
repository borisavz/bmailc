class Store():
    server_set = False
    user_set = False

    initialized = False
    reply = False

    mailboxes = []
    current_mailbox = None
    current_message = None

    username = ''
    password = ''

    imap_server = ''
    imap_port = ''
    imap_encryption = ''

    smtp_server = ''
    smtp_port = ''
    smtp_encryption = ''