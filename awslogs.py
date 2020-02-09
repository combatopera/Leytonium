from dev_bin.common import menu
from datetime import datetime
import json, subprocess, argparse

logs = ['bash', '-ic', 'aws logs "$@"', 'logs']
tskey = 'lastEventTimestamp'

def _shorten(line, radius = 250):
    if len(line) <= 2 * radius:
        return line
    sep = '...'
    return line[:radius - len(sep)] + sep + line[-radius:]

def main_awslogs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-trunc', action='store_true')
    config = parser.parse_args()
    shorten = (lambda x: x) if config.no_trunc else _shorten
    names = [g['logGroupName'] for g in json.loads(subprocess.check_output(logs + ['describe-log-groups']))['logGroups']]
    _, group = menu([(n, '') for n in names], 'Group')
    streams = json.loads(subprocess.check_output(logs + ['describe-log-streams', '--log-group-name', group]))['logStreams']
    streams.sort(key = lambda s: -s.get(tskey, 0)) # Freshest first.
    del streams[100:]
    k, _ = menu([(datetime.fromtimestamp(s.get(tskey, 0) / 1000).isoformat(), s['storedBytes']) for s in streams], 'Stream')
    stream = streams[k - 1]['logStreamName']
    events = json.loads(subprocess.check_output(logs + ['get-log-events', '--log-group-name', group, '--log-stream-name', stream]))['events']
    for e in events:
        print(shorten(e['message']), end = '')
