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

'Instant mortgage statement.'
from aridity.config import ConfigCtrl
from datetime import date, timedelta

maxmonth = timedelta(31)
oneday = timedelta(1)

def main():
    config = ConfigCtrl().loadappconfig(main, 'mortcalc.arid')
    balance = config.balance
    rate = config.rate / 100
    mark = date.fromisoformat(f"{config.month.first}-01")
    lastmark = date.fromisoformat(f"{config.month.last}-01")
    payment = config.payment
    value = config.value
    holidays = set(map(date.fromisoformat, config.holiday))
    while mark <= lastmark:
        dayrate = rate / int((date(mark.year + 1, 1, 1) - date(mark.year, 1, 1)) / oneday)
        paymark = mark
        while paymark.weekday() > 4 or paymark in holidays:
            paymark += oneday
        nextmark = (mark + maxmonth).replace(day = 1)
        days1 = int((paymark - mark) / oneday)
        days2 = int((nextmark - paymark) / oneday)
        interest = 0
        for d in range(days1):
            interest += balance * dayrate
            b = balance + interest
            print(mark + timedelta(d), interest, b, b / value * 100)
        balance -= payment
        for d in range(days2):
            interest += balance * dayrate
            b = balance + interest
            print(mark + timedelta(days1 + d), interest, b, b / value * 100)
        balance += round(interest, 2)
        mark = nextmark

if '__main__' == __name__:
    main()
