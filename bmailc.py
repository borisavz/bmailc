from logic.BMailCAPP import BMailCAPP
from logic.Store import Store

if __name__ == '__main__':
    # Uncomment and hardcode these values to login automatically
    # Leaving password here is not advised, but is possible for development purposes
    # Currently, saving settings is not possible
    # port - number
    # encryption - 'SSL', 'TLS', 'None'

    #Store.server_set = True
    #Store.imap_server = ''
    #Store.imap_port = 0
    #Store.imap_encryption = ''
    #Store.smtp_server = ''
    #Store.smtp_port = 0
    #Store.smtp_encryption = ''

    #Store.user_set = True
    #Store.username = ''
    #Store.password = ''

    BMC = BMailCAPP()
    BMC.run()