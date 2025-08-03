from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image
import numpy as np

def zoom_in(input_file: str, targetcs: tuple[float, float], duration: tuple[float, float], output_file: str = "output.mp4"):
    """Zooms into a specific region of a video clip over time.

    Args:
        input_file(str): Path to the input video file.
        targetcs(tuple[float, float]): Target coordinates (x, y) as a fraction of the video width and height.
        duration(tuple[float, float]): Start and end time of the clip to zoom in (seconds).
        output_file(str): Path to save the output video file. Defaults to 'output.mp4'

    Returns:
        None: No return value.

    Raises:
        FileNotFoundError: Raised if the input video file is not found.
        ValueError: Raised if the target coordinates or duration are invalid.
    """
    clip = VideoFileClip(input_file).subclipped(*duration)
    frames = []
    fps = clip.fps
    w, h = clip.size

    tx, ty = targetcs
    target_x = int(tx * w)
    target_y = int(ty * h)

    total_duration = duration[1] - duration[0]

    for t in np.arange(0, total_duration, 1 / fps):
        frame = clip.get_frame(t)
        progress = t / total_duration
        ease = np.sin(progress * np.pi / 2) ** 2
        zoom_factor = 1 + 2.0 * ease

        new_w = int(w / zoom_factor)
        new_h = int(h / zoom_factor)
        x1 = max(0, target_x - new_w // 2)
        y1 = max(0, target_y - new_h // 2)
        x2 = min(w, x1 + new_w)
        y2 = min(h, y1 + new_h)

        cropped = frame[y1:y2, x1:x2]
        resized = np.array(Image.fromarray(cropped).resize((w, h)))
        frames.append(resized)

    zoomed_clip = ImageSequenceClip(frames, fps=fps)

    zoomed_clip.write_videofile(
        output_file,
        codec="libx264",
        ffmpeg_params=["-preset", "fast", "-crf", "18"],
        threads=4,
        audio=False,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )
    