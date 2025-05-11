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

'Wait for network then become given command.'
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from foyndation import initlogging
from ipaddress import ip_address, ip_network
from lagoon.program import Program
from lagoon.text import ip
from lagoon.util import wrappercli
from time import sleep
import json, logging

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'afternet.arid')
    parser = ArgumentParser()
    parser.add_argument('command', nargs = '+')
    command = parser.parse_args(wrappercli()).command
    network = ip_network(config.network)
    while not any(ip_address(ip['local']) in network for iface in ip._j.address[json]() for ip in iface['addr_info']):
        log.debug('Wait for network.')
        sleep(config.sleeptime)
    Program.binary(command[0])[exec](*command[1:])

if '__main__' == __name__:
    main()
