import sys
from pathlib import Path

# Allow `import eda_analysis` when running pytest from project root
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
