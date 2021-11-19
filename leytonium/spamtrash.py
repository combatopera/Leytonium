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

from .util import keyring
from aridity.config import ConfigCtrl
from email import message_from_string

def main_spamtrash():
    'Delete spam emails.'
    cc = ConfigCtrl()
    cc.node.keyring = keyring
    config = cc.loadappconfig(main_spamtrash, 'spamtrash.arid')
    imap = config.imap(config.host)
    with config.password as password:
        imap.login(config.user, password)
    try:
        imap.select(config.mailbox)
        _, (ids,) = imap.search(None, 'ALL')
        message_set = ','.join(id.decode() for id in ids.split())
        _, data = imap.fetch(message_set, '(RFC822)')
        for d in data:
            print(type(d))
    finally:
        imap.logout()
