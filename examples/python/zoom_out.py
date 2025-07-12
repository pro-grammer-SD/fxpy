import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from zoom_out import zoom_out

zoom_out("samples/input.mp4", (0.5, 0.5), (3, 7))
