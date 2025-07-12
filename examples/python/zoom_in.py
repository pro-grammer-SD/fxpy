import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from zoom_in import zoom_in

zoom_in("samples/input.mp4", (0.5, 0.5), (3, 7))
