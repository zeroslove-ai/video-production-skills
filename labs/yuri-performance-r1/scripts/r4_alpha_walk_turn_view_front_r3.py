import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_alpha_walk_turn_preview_r3 import main
main('front')
