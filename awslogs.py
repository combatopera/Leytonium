from dev_bin.common import menu
import json, subprocess, argparse

logs = ['bash', '-ic', 'aws logs "$@"', 'logs']
tskey = 'lastEventTimestamp'

def _shorten(line, radius = 250):
    if len(line) <= 2 * radius:
        return line
    sep = '...'
    return line[:radius - len(sep)] + sep + line[-radius:]

def streamnames(group, starttime):
    streams = json.loads(subprocess.check_output(logs + ['describe-log-streams', '--log-group-name', group]))['logStreams']
    streams.sort(key = lambda s: -s.get(tskey, 0)) # Freshest first.
    def g():
        for s in streams:
            if s.get(tskey, 0) < starttime:
                break
            yield s['logStreamName']
    names = list(g())
    names.reverse()
    return names

def main_awslogs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-trunc', action='store_true')
    parser.add_argument('--ago', default='1 hour')
    config = parser.parse_args()
    shorten = (lambda x: x) if config.no_trunc else _shorten
    names = [g['logGroupName'] for g in json.loads(subprocess.check_output(logs + ['describe-log-groups']))['logGroups']]
    _, group = menu([(n, '') for n in names], 'Group')
    for stream in streamnames(group, int(subprocess.check_output(['date', '-d', f"{config.ago} ago", '+%s000']))):
        events = json.loads(subprocess.check_output(logs + ['get-log-events', '--log-group-name', group, '--log-stream-name', stream]))['events']
        for e in events:
            print(shorten(e['message']), end = '')
