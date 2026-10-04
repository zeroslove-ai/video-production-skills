from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_walk_contact_preview_r2 import main
for view in ['front','quarter','side']:main(view,probe=False)
