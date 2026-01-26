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
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from functools import cache

maxmonth = timedelta(31)
oneday = timedelta(1)

def _days(start, end):
    return int((end - start) / oneday)

@cache
def _yearlen(year):
    return _days(date(year, 1, 1), date(year + 1, 1, 1))

@dataclass
class Period:

    firstday: object
    payment: object
    rate: object

def main():
    config = ConfigCtrl().loadappconfig(main, 'mortcalc.arid')
    balance = config.anchor
    periods = [Period(date.fromisoformat(k), c.payment, c.rate / 100) for k, c in -config.firstday]
    mark = periods[0].firstday
    for p, q in zip(periods, periods[1:]):
        assert p.firstday < q.firstday
    value = config.value
    holidays = set(map(date.fromisoformat, config.holiday))
    overpays = {date.fromisoformat(k): v for k, v in -config.overpay}
    for period, nextperiod in zip(periods, periods[1:]):
        while mark < nextperiod.firstday:
            nextmark = (mark + maxmonth).replace(day = 1)
            dayrate = period.rate / _yearlen(mark.year)
            paymark = mark
            while paymark.weekday() > 4 or paymark in holidays:
                paymark += oneday
            payments = defaultdict(int)
            payments[paymark] = period.payment
            for m, p in overpays.items():
                if m.year == mark.year and m.month == mark.month:
                    payments[m] += p
            payments[nextmark] = 0
            interest = 0
            cursor = mark
            for m, p in sorted(payments.items()):
                for d in range(_days(cursor, m)):
                    interest += balance * dayrate
                    b = balance + interest
                    print(cursor + timedelta(d), interest, b, b / value * 100, balance)
                cursor = m
                balance -= p
            balance += round(interest, 2)
            mark = nextmark

if '__main__' == __name__:
    main()
