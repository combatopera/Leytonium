from pathlib import Path
import os

effectivehome = Path("~%s" % os.environ.get('SUDO_USER', '')).expanduser()
