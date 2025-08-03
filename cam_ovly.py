from moviepy import ImageClip, VideoFileClip, CompositeVideoClip
import numpy as np

def cam_ovly(base_clip_path, cam_clip_path, output_path="output.mp4", radius=150, position=("right", "bottom"), size=0.25):
    """Applies a circular mask to a camera clip and overlays it onto a base video clip.

    Args:
        base_clip_path(str): Path to the base video clip.
        cam_clip_path(str): Path to the camera video clip.
        output_path(str): Path to save the output video. Defaults to "output.mp4".
        radius(int): Radius of the circular mask in pixels. Defaults to 150.
        position(tuple[str, str] or tuple[int, int]): Position of the camera clip overlay. Can be a tuple of strings ("left"/"right", "top"/"bottom") or a tuple of integers (x, y) representing coordinates. Defaults to ("right", "bottom").
        size(float): Scaling factor for the camera clip height. Defaults to 0.25.

    Returns:
        None: No explicit return value.

    Raises:
        ValueError: Raised if the position parameter is not in the correct format.
    """
    
    base = VideoFileClip(base_clip_path)
    bw, bh = base.size

    cam_raw = VideoFileClip(cam_clip_path).resized(height=int(bh * size))

    if cam_raw.duration < base.duration:
        last_frame = cam_raw.to_ImageClip(t=cam_raw.duration - 0.01).with_duration(base.duration - cam_raw.duration)
        cam = CompositeVideoClip([cam_raw, last_frame.with_start(cam_raw.duration)])
    else:
        cam = cam_raw.subclipped(0, base.duration)

    w, h = cam.size
    cx, cy = w // 2, h // 2

    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    mask_array = (dist <= radius).astype(float)

    mask_clip = ImageClip(mask_array, is_mask=True).with_duration(base.duration).with_fps(cam.fps)

    cam_w, cam_h = cam.size
    if isinstance(position, tuple) and len(position) == 2:
        if all(isinstance(p, str) for p in position):
            pos_x = bw - cam_w - 10 if position[0] == "right" else 10
            pos_y = bh - cam_h - 10 if position[1] == "bottom" else 10
        elif all(isinstance(p, (int, float)) for p in position):
            pos_x, pos_y = position
        else:
            raise ValueError("Position must be ('left'/'right', 'top'/'bottom') or (x:int, y:int)")
    else:
        raise ValueError("Position must be a tuple of 2 values.")

    cam = cam.with_mask(mask_clip).with_position((pos_x, pos_y)).with_duration(base.duration)

    final = CompositeVideoClip([base, cam], size=base.size).with_duration(base.duration)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)
    