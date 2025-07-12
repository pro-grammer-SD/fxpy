from moviepy import ImageClip, VideoFileClip, CompositeVideoClip
import numpy as np

def cam_ovly(base_clip_path, cam_clip_path, output_path="output.mp4", radius=150, position=("right", "bottom"), size=0.25):
    """Overlays a smaller video clip onto a larger video clip, applying a circular mask to the smaller clip.

    Args:
        base_clip_path(str): Path to the base video clip.
        cam_clip_path(str): Path to the smaller video clip to overlay.
        output_path(str): Path to save the output video. Defaults to "output.mp4".
        radius(int): Radius of the circular mask applied to the overlay clip. Defaults to 150.
        position(tuple[str, str]): Tuple specifying the position of the overlay clip ("left" or "right", "top" or "bottom"). Defaults to ("right", "bottom").
        size(float): Scaling factor for the height of the overlay clip. Defaults to 0.25.
    """
    base = VideoFileClip(base_clip_path)
    bw, bh = base.size

    cam_raw = VideoFileClip(cam_clip_path).resized(height=int(bh * size))

    if cam_raw.duration < base.duration:
        last_frame = cam_raw.to_ImageClip(t=cam_raw.duration - 0.01).with_duration(base.duration - cam_raw.duration)
        cam = CompositeVideoClip([cam_raw, last_frame.with_start(cam_raw.duration)])
    else:
        cam = cam_raw.subclip(0, base.duration)

    w, h = cam.size
    cx, cy = w // 2, h // 2

    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    mask_array = (dist <= radius).astype(float)

    mask_clip = ImageClip(mask_array, is_mask=True).with_duration(base.duration).with_fps(cam.fps)
    cam = cam.with_mask(mask_clip)

    cam_w, cam_h = cam.size
    pos_x = bw - cam_w - 30 if position[0] == "right" else 30
    pos_y = bh - cam_h - 30 if position[1] == "bottom" else 30

    cam = cam.with_position((pos_x, pos_y)).with_duration(base.duration)

    final = CompositeVideoClip([base, cam], size=base.size).with_duration(base.duration)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)
