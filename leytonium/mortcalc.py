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
from functools import cache

maxmonth = timedelta(31)
oneday = timedelta(1)

@cache
def _yearlen(year):
    return int((date(year + 1, 1, 1) - date(year, 1, 1)) / oneday)

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
        nextmark = (mark + maxmonth).replace(day = 1)
        dayrate = rate / _yearlen(mark.year)
        paymark = mark
        while paymark.weekday() > 4 or paymark in holidays:
            paymark += oneday
        payments = {paymark: payment, nextmark: 0}
        interest = 0
        cursor = mark
        for m, p in sorted(payments.items()):
            days = int((m - cursor) / oneday)
            for d in range(days):
                interest += balance * dayrate
                b = balance + interest
                print(cursor + timedelta(d), interest, b, b / value * 100)
            cursor = m
            balance -= p
        balance += round(interest, 2)
        mark = nextmark

if '__main__' == __name__:
    main()
