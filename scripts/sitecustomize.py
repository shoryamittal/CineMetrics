"""Make every standalone generator safe for legacy Windows consoles.

Python imports ``sitecustomize`` automatically when the script directory is on
``sys.path``.  That keeps all generators usable directly as well as through
the UTF-8-enabled master pipeline.
"""

import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
