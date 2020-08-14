from argparse import ArgumentParser
from aridity.config import Config
from collections import defaultdict
from elasticsearch import Elasticsearch
from lagoon import date
import logging, re, sys

log = logging.getLogger(__name__)
maxsize = 10000
xforms = {('message',): lambda m: m.rstrip()}
tspattern = re.compile('[0-9]{2}[.][0-9]{9}')

class Display:

    def add(self, source, value):
        print(tspattern.search(source['@timestamp']).group(), source['stream'][-3], value)

    def flush(self):
        pass

class Unique:

    def __init__(self):
        self.counts = defaultdict(int)

    def add(self, source, value):
        self.counts[value] += 1

    def flush(self):
        for c, v in sorted([c, v] for v, c in self.counts.items()):
            print(c, v)

def main_k8slogs():
    logging.basicConfig(format = "[%(levelname)s] %(message)s", level = logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--ago', default = '1 hour')
    parser.add_argument('--env', default = 'non-prod')
    parser.add_argument('-u', action = 'store_true')
    parser.add_argument('k8s_pod_prefix')
    parser.add_argument('path', nargs = '?', type = lambda p: tuple(p.split('.')), default = ('message',))
    args = parser.parse_args()
    config = Config.blank()
    config.loadsettings()
    try:
        log.info(config.elasticsearch.motd)
    except AttributeError:
        pass
    interval = dict(gte = date._Iseconds._d(f"{args.ago} ago").rstrip())
    xform = xforms.get(args.path, lambda x: x)
    es = Elasticsearch(getattr(config.elasticsearch.host, args.env))
    agg = (Unique if args.u else Display)()
    while True:
        must = [dict(range = {'@timestamp': interval})]
        if args.k8s_pod_prefix:
            # XXX: Really no way to match exact prefix?
            must.append(dict(match = {'kubernetes.pod_name': args.k8s_pod_prefix}))
            accept = lambda hit: hit['_source']['kubernetes']['pod_name'].startswith(args.k8s_pod_prefix)
        else:
            accept = lambda hit: hit.get('_source', {}).get('kubernetes', {}).get('pod_name') is not None
        log.info("Fetch: %s", interval)
        hits = [hit for hit in es.search(
            size = maxsize,
            allow_partial_search_results = False, # XXX: What does this actually do?
            body = dict(query = dict(bool = dict(must = must))),
        )['hits']['hits'] if accept(hit)]
        if not hits:
            break
        hits.sort(key = lambda hit: hit['_source']['@timestamp']) # Much less problematic than ES sort.
        for source in (hit['_source'] for hit in hits):
            field = source
            if ('',) != args.path:
                for name in args.path:
                    field = field[name]
            agg.add(source, xform(field))
        interval = dict(gt = hits[-1]['_source']['@timestamp'])
    agg.flush()
