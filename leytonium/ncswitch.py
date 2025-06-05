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
from aridity.config import ConfigCtrl
from foyndation import initlogging
from lagoon.text import nc
from socket import gaierror, gethostbyname
import logging, re, sys

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'ncswitch.arid')
    args = destination, port = sys.argv[1:]
    if re.search(config.destregex, destination) is not None:
        log.debug("Match: %s", destination)
        try:
            gethostbyname(config.tryhost)
        except gaierror:
            log.debug('Use proxy.')
            args = [*config.prepend, *args]
    nc[exec](*args)

if '__main__' == __name__:
    main()
