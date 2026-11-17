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

'Render Markdown file in browser.'
from lagoon.text import pandoc
from pathlib import Path
from tempfile import NamedTemporaryFile
import asyncio, sys, webbrowser

async def _main():
    args = sys.argv[1:]
    with NamedTemporaryFile(dir = Path.home(), suffix = '.html') as f:
        pandoc[:f]('--title-prefix', Path(args[-1]).name, '--toc', *args)
        webbrowser.open(f.name)
        await asyncio.get_running_loop().create_future()

def main():
    asyncio.run(_main())

if '__main__' == __name__:
    main()
