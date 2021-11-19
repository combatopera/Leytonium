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
from email import message_from_bytes
from itertools import islice
import re

number = re.compile(b'[0-9]+')

def _headerstr(header):
    if header is not None:
        if isinstance(header, str):
            return header
        (text, charset), = header._chunks
        assert 'unknown-8bit' == charset
        parts = re.split(r'([\udc00-\udcff]+)', text)
        def g():
            yield parts[0]
            for q, p in zip(islice(parts, 1, None, 2), islice(parts, 2, None, 2)):
                yield bytes(ord(x) & 0xff for x in q).decode('utf-8')
                yield p
        return ''.join(g())

class Regex:

    def __init__(self, config):
        self.froms = list(map(re.compile, config.regex.froms))
        self.subjects = list(map(re.compile, config.regex.subjects))

    def delete(self, msg):
        _from = _headerstr(msg['From'])
        if _from is not None:
            for fromre in self.froms:
                if fromre.search(_from) is not None:
                    return True
        subject = _headerstr(msg['Subject'])
        if subject is not None:
            for subjectre in self.subjects:
                if subjectre.search(subject) is not None:
                    return True

def main_spamtrash():
    'Delete spam emails.'
    cc = ConfigCtrl()
    cc.node.keyring = keyring
    config = cc.loadappconfig(main_spamtrash, 'spamtrash.arid', encoding = 'utf-8')
    regex = Regex(config)
    with config.imap(config.host) as imap:
        with config.password as password:
            imap.login(config.user, password)
        imap.select(config.mailbox)
        ok, (ids,) = imap.search(None, 'ALL')
        assert 'OK' == ok
        message_set = ','.join(id.decode() for id in ids.split())
        ok, v = imap.fetch(message_set, '(RFC822)')
        assert 'OK' == ok
        hmm = []
        for (info, msgbytes), x in zip(islice(v, 0, None, 2), islice(v, 1, None, 2)):
            if b')' != x:
                raise Exception(x)
            id = number.match(info).group()
            msg = message_from_bytes(msgbytes)
            if not regex.delete(msg):
                hmm.append(_headerstr(msg['Subject']))
        for s in sorted(s for s in hmm if s is not None): print(s)
