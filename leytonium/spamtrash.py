# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

from aridity.config import ConfigCtrl
from aridity.model import Scalar
from email import message_from_string
from functools import partial
from getpass import getpass
from imaplib import IMAP4_SSL
import re

number = re.compile(b'[0-9]+')

class Password:

    null_exc_info = None, None, None

    def __init__(self, password, setter):
        self.password = password
        self.setter = setter

    def __enter__(self):
        return self.password

    def __exit__(self, *exc_info):
        if self.setter is not None and self.null_exc_info == exc_info:
            self.setter(self.password)

def _keyring(context, serviceres, usernameres):
    from keyring import get_password, set_password
    service = serviceres.resolve(context).cat()
    username = usernameres.resolve(context).cat()
    password = get_password(service, username)
    return Scalar(Password(*[getpass(), partial(set_password, service, username)] if password is None else [password, None]))

def main_spamtrash():
    'Delete spam emails.'
    cc = ConfigCtrl()
    cc.node.keyring = _keyring
    config = cc.loadappconfig(main_spamtrash, 'spamtrash.arid')
    mail = IMAP4_SSL(config.host)
    with config.password as password:
        mail.login(config.user, password)
    #_, v = mail.list()
    #for x in v: print(x)
    mail.select('[Gmail]/Spam')
    _, (v,) = mail.search(None, 'ALL')
    ids = number.findall(v)
    for id in ids:
        _, data = mail.fetch(id, '(RFC822)')
        print(message_from_string(data[0][1].decode('latin-1')))
        break
