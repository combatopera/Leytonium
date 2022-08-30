from . import initlogging
from lagoon import ffmpeg
from lagoon.program import partial
from pathlib import Path
import logging, sys

log = logging.getLogger(__name__)

def main_extractaudio():
    initlogging()
    for inpath in map(Path, sys.argv[1:]):
        outpath = inpath.with_suffix('.aac')
        log.info("Extract: %s", outpath)
        ffmpeg._i[partial](inpath)._vn._acodec.copy(outpath)
