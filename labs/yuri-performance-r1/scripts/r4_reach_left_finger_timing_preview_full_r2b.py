import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_reach_left_finger_timing_preview_r2 import main
main(probe=False)
