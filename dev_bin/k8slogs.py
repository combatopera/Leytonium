from argparse import ArgumentParser
from aridimpl.util import NoSuchPathException
from aridity import Context, Repl
from elasticsearch import Elasticsearch
from lagoon import date
import logging, sys

log = logging.getLogger(__name__)
maxsize = 10000

def main_k8slogs():
    logging.basicConfig(format = "[%(levelname)s] %(message)s", level = logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('--ago', default='1 hour')
    parser.add_argument('container_name')
    config = parser.parse_args()
    context = Context()
    with Repl(context) as repl:
        repl('. $/($(~) .settings.arid)')
    try:
        log.info(context.resolved('elasticsearch', 'motd').cat())
    except NoSuchPathException:
        pass
    interval = dict(gte = date._Iseconds._d(f"{config.ago} ago").rstrip())
    es = Elasticsearch(context.resolved('elasticsearch', 'hosts').unravel())
    while True:
        # XXX: What does allow_partial_search_results actually do?
        hits = es.search(size = maxsize, allow_partial_search_results = False, body = dict(
            query = dict(bool = dict(must = [
                dict(match = {'kubernetes.container_name': config.container_name}), # TODO: Match whole field not substring.
                dict(range = {'@timestamp': interval}),
            ])),
            sort = [{'@timestamp': 'asc'}],
        ))['hits']['hits']
        for source in (hit['_source'] for hit in hits):
            getattr(sys, source['stream']).write(source['message'])
        if len(hits) < maxsize:
            break
        interval = dict(gt = hits[-1]['_source']['@timestamp'])
