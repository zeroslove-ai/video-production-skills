import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_alpha_walk_turn_preview_r4 import main
for view in ['front','quarter','side']:main(view,probe=True)
