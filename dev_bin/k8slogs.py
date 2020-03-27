from argparse import ArgumentParser
from aridimpl.util import NoSuchPathException
from aridity import Context, Repl
from elasticsearch import Elasticsearch
from lagoon import date
import logging

log = logging.getLogger(__name__)

def main_k8slogs():
    logging.basicConfig(format = "[%(levelname)s] %(message)s", level = logging.DEBUG)
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
    es = Elasticsearch(context.resolved('elasticsearch', 'hosts').unravel())
    res = es.search(body = dict(query = dict(bool = dict(must = [
        dict(match = {'kubernetes.container_name': config.container_name}),
        dict(range = {'@timestamp': dict(gte = date._Iseconds._d(f"{config.ago} ago").rstrip())}),
    ]))))
    print(res)
