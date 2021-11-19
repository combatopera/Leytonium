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
fromres = list(map(re.compile, [
    '^"💲CashApp💲" <',
    '^Male👅Elongator....  <',
    '^"💕Wanna-F#ck💕" <info@',
    '^"S e ✘ ⛔ S e c r et"  <',
    '^"💕Asian Nudes♥️" <',
    '^❣️Kirsten😍" <info@',
    '^helplaw✅  <info@',
    '^💋Enjoy-with-me💋 <',
    '^"📏🍌𝗣𝗲𝗻𝗶𝘀.𝟭𝟱-𝗶𝗻𝗰𝗵🔥"<nooreply@',
    '^"👙🍌Fuck_Me_Tonight.🍌" <info@webmd.com>$',
    '^"𝙂𝙤𝙡𝙙-𝙄𝙍𝘼✔️"<nooreply@',
    '^"TEXT😘ME💗" <info@webmd.com>$',
    '^"_FREE😍SEX_💕"',
    '^𝗥𝗼𝘂𝗻𝗱𝘂𝗽_𝗦𝗲𝘁𝘁𝗹𝗲𝗺𝗲𝗻𝘁✅ <nooreply@',
    '^Elongation Secret🔥[*] <',
]))

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

def main_spamtrash():
    'Delete spam emails.'
    cc = ConfigCtrl()
    cc.node.keyring = keyring
    config = cc.loadappconfig(main_spamtrash, 'spamtrash.arid')
    with config.imap(config.host) as imap:
        with config.password as password:
            imap.login(config.user, password)
        imap.select(config.mailbox)
        ok, (ids,) = imap.search(None, 'ALL')
        assert 'OK' == ok
        message_set = ','.join(id.decode() for id in ids.split())
        ok, v = imap.fetch(message_set, '(RFC822)')
        assert 'OK' == ok
        froms = []
        for (info, msgbytes), x in zip(islice(v, 0, None, 2), islice(v, 1, None, 2)):
            assert b')' == x
            id = number.match(info).group()
            msg = message_from_bytes(msgbytes)
            _from = _headerstr(msg['From'])
            subject = _headerstr(msg['Subject'])
            if _from is not None:
                for fromre in fromres:
                    if fromre.search(_from) is not None:
                        break
                else:
                    froms.append(_from)
        for f in sorted(froms): print(f)
