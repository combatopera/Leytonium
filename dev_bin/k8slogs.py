from argparse import ArgumentParser
from aridity.config import Config
from elasticsearch import Elasticsearch
from lagoon import date
import logging, re, sys

log = logging.getLogger(__name__)
maxsize = 10000
xforms = {('message',): lambda m: m.rstrip()}
tspattern = re.compile('[0-9]{2}[.][0-9]{9}')

def main_k8slogs():
    logging.basicConfig(format = "[%(levelname)s] %(message)s", level = logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--ago', default = '1 hour')
    parser.add_argument('pod_name')
    parser.add_argument('path', nargs = '?', type = lambda p: tuple(p.split('.')), default = ('message',))
    parser.add_argument('--env', default = 'non-prod')
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
    while True:
        # XXX: What does allow_partial_search_results actually do?
        hits = [hit for hit in es.search(size = maxsize, allow_partial_search_results = False, body = dict(
            query = dict(bool = dict(must = [
                dict(match = {'kubernetes.pod_name': args.pod_name}), # XXX: Really no way to match exact prefix?
                dict(range = {'@timestamp': interval}),
            ])),
            sort = [{'@timestamp': 'asc'}],
        ))['hits']['hits'] if hit['_source']['kubernetes']['pod_name'].startswith(f"{args.pod_name}-")]
        hits.sort(key = lambda hit: hit['_source']['@timestamp']) # Not quite redundant apparently!
        for source in (hit['_source'] for hit in hits):
            field = source
            if ('',) != args.path:
                for name in args.path:
                    field = field[name]
            print(tspattern.search(source['@timestamp']).group(), xform(field), file = getattr(sys, source['stream']))
        if len(hits) < maxsize:
            break
        interval = dict(gt = hits[-1]['_source']['@timestamp'])
