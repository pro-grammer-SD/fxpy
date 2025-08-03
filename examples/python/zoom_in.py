import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from zoom_in import zoom_in

zoom_in("samples/input_2.mp4", (0.3, 0.5), (0, 4), "out.mp4")
