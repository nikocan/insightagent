"""Pytest configuration ensuring local packages resolve without installation."""

# Bu dosya, FastAPI shim paketinin import edilebilmesi için proje kökünü
# sys.path'e ekler.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
