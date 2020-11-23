from datetime import datetime
import pytz, re, sys

tz = pytz.timezone('Europe/London')
pattern = re.compile('(9[0-9]{8}|[1-3][0-9]{9})([0-9]{3})?')

def _repl(m):
    tstr, mstr = m.groups()
    t = int(tstr) + (int(mstr) / 1000 if mstr else 0)
    dt = datetime.utcfromtimestamp(t).replace(tzinfo = pytz.utc).astimezone(tz)
    return f"{dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}{dt.strftime('%z')}"

def main_isotime():
    'Filter UNIX timestamps to human-readable form.'
    for line in sys.stdin:
        sys.stdout.write(pattern.sub(_repl, line))
