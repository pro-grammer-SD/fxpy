import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from zoom_out import zoom_out

zoom_out("samples/input_2.mp4", (0.2, 0.7), (0, 4))
