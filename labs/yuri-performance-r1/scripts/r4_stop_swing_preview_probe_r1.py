from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_stop_swing_preview_r1 import main
for view in ['front','quarter','side']:main(view,probe=True)
