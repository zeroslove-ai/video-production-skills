import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_hand_relax_preview_r1 import main
main(probe=True)
