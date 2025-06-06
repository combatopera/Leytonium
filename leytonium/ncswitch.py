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

'Wrap nc for use as ssh ProxyCommand.'
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from foyndation import initlogging
from lagoon.text import nc
from socket import gaierror, gethostbyname
import logging, re

log = logging.getLogger(__name__)

def main():
    def prepend():
        if re.search(config.destregex, destination) is not None:
            log.debug("Match: %s", destination)
            try:
                gethostbyname(config.tryhost)
            except gaierror:
                log.debug('Use proxy.')
                return config.prepend
        return ()
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'ncswitch.arid')
    parser = ArgumentParser()
    parser.add_argument('destination', help = '%%h')
    parser.add_argument('port', help = '%%p')
    parser.parse_args(namespace = config.cli)
    destination = config.destination
    nc[exec](*prepend(), destination, config.port)

if '__main__' == __name__:
    main()
