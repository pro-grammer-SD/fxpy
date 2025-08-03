import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from cam_ovly import cam_ovly

cam_ovly("samples/input_2.mp4", "samples/face.mp4", "output.mp4", radius=100)
