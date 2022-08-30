from . import initlogging
from argparse import ArgumentParser
from lagoon import ffmpeg
from lagoon.program import partial
from pathlib import Path
import logging, sys

log = logging.getLogger(__name__)

def main_extractaudio():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-d', action = 'store_true')
    parser.add_argument('path', nargs = '+', type = Path)
    args = parser.parse_args()
    for inpath in args.path:
        outpath = inpath.with_suffix('.aac')
        log.info("Extract: %s", outpath)
        ffmpeg._i[partial](inpath)._vn._acodec.copy(outpath)
        if args.d:
            log.info("Delete: %s", inpath)
            inpath.unlink()
