import re
from email.header import decode_header, Header
from email.utils import getaddresses
from entities.Mailbox import Mailbox


class Utils:

    list_pattern = re.compile(r'\((?P<dir_flags>.*?)\) "(?P<separator>.*)" (?P<dir_name>.*)')

    @staticmethod
    def dec_header(parsed_email, name):
        if name not in parsed_email:
            return ''

        dec_str = ''
        dec = decode_header(parsed_email[name])

        for d in dec:
            if type(d[0]) is str:
                dec_str += d[0]
            else:
                dec_str += d[0].decode('UTF-8' if d[1] == None else d[1])

        return dec_str

    @staticmethod
    def enc_addresses(addr_list):
        addr = []

        enc_addr = getaddresses(addr_list)

        for a in enc_addr:
            h = Header()
            h.append(a[0])
            h.append('<' + a[1] + '>')
            addr.append(h.encode())

        return ','.join(addr)

    @staticmethod
    def dec_list(res):
        dec = Utils.list_pattern.match(res.decode())
        dir_flags, separator, dir_name = dec.groups()

        flags = dir_flags.split()
        name = dir_name.strip('"')

        return Mailbox(name, flags)