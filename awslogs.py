from lagoon.binary import bash, date
import argparse, json

logs = '-ic', 'aws logs "$@"', 'logs'
tskey = 'lastIngestionTime'

def _shorten(line, radius = 250):
    if len(line) <= 2 * radius:
        return line
    sep = '...'
    return line[:radius - len(sep)] + sep + line[-radius:]

def streamnames(group, starttime):
    streams = json.loads(bash(*logs, 'describe-log-streams', '--log-group-name', group))['logStreams']
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
    parser.add_argument('group')
    config = parser.parse_args()
    shorten = (lambda x: x) if config.no_trunc else _shorten
    for stream in streamnames(config.group, int(date('-d', "%s ago" % config.ago, '+%s000'))):
        token = []
        while True:
            page = json.loads(bash(*logs, 'get-log-events', '--start-from-head', '--log-group-name', config.group, '--log-stream-name', stream, *token))
            for m in (e['message'] for e in page['events']):
                if m and '\n' == m[0]:
                    print('$ ', end = '')
                    m = m[1:]
                for i, l in enumerate(m.split('\r')):
                    if i:
                        print()
                        print('> ', end = '')
                    print(shorten(l), end = '')
            t = page['nextForwardToken']
            if token and t == token[1]: # Looks like first page can never be final page.
                break
            token = ['--next-token', t]
