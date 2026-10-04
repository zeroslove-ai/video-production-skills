import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_alpha_a1_render_preview_r3 import main
main('front',range(1,302))
