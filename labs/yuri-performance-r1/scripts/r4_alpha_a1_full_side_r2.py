import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_alpha_a1_render_preview_r2 import main
main('side',range(1,302))
