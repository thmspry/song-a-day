# For editing
from moviepy import *
from moviepy.editor import *
from skimage.filters import gaussian

# To get country flag and manipulate it
import requests
from PIL import Image
import numpy as np
from io import BytesIO

import random

from Song import Song
from api.song_downloader import SONG_PATH

def url_to_rgb_array(image_url: str) -> list:
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image using PIL
        image = Image.open(BytesIO(response.content))

        # Convert the image to RGB mode
        image = image.convert('RGB')

        # Convert the PIL image to a NumPy array
        rgb_array = np.array(image)

        return rgb_array

    except Exception as e:
        print(f"Error: {e}")
        return None


def create_text(text: str, start: int, end: int, pos_x_perc: int = -1, pos_y_perc: int = -1, color: str = "white", fontsize: int = 50) -> TextClip:
    """Create a TextClip object with the given text, start and end

    Args:
        text (str): the text to display
        start (int): the start time of the text (in seconds)
        end (int): the end time of the text (in seconds)

    Returns:
        TextClip: a TextClip object
    """
    position = (pos_x_perc, pos_y_perc) if pos_x_perc != -1 and pos_y_perc != -1 else 'center'
    relative = type(position) == tuple
    
    text = TextClip(str(text), fontsize=fontsize, color=color, stroke_width=3, stroke_color='black', font='Rubik-Bold', align="West")
    text = text.set_position(position, relative=relative).set_duration(end - start).set_start(start)
    return text

def create_image(rgb_array: str, start: int, end: int, pos_x_perc: int = -1, pos_y_perc: int = -1, scale: int = 1) -> ImageClip:
    """Create an ImageClip object with the given image, start and end

    Args:
        path (str): an array representing the RGB image
        start (int): the start time of the image (in seconds)
        end (int): the end time of the image (in seconds)

    Returns:
        ImageClip: an ImageClip object
    """
    position = (pos_x_perc, pos_y_perc) if pos_x_perc != -1 and pos_y_perc != -1 else 'center'
    relative = type(position) == tuple
    
    image = ImageClip(rgb_array, duration=end - start)
    image = image.set_position(position, relative=relative).set_start(start).resize(0.7)
    image = image.resize(scale)
    return image

def box_text(text: str, number_char_in_line: int) -> str:
    separator = " "
    if "feat" in text:
        separator = ", "
    text_splitted = text.split(separator)
    char_count = 0
    for word in text_splitted:
        char_count += len(word)
        if char_count >= number_char_in_line:
            text_splitted.insert(text_splitted.index(word), "\n")
            char_count = 0
        
    text_boxed = separator.join(text_splitted)
    text_boxed = text_boxed.replace("\n ", "\n")
    return text_boxed

def generate_video(song: Song, VIDEO_PATH: str, fps: int = 60):
    
    # Constants
    VIDEO_LENGTH = 30
    BIG_FONT_SIZE = 75
    MID_FONT_SIZE = 75
    BOX_SIZE_RIGHT_COVER_BT = 12
    BOX_SIZE_RIGHT_COVER_ST = 17
    BOX_SIZE_UNDER_COVER_MT = 20
    BOX_SIZE_UNDER_COVER_ST = 28
    
    # 🎵 Audio
    song_seconds = song.lenght_in_seconds()
    range_start = round(song_seconds*0.3)
    range_end = round(song_seconds*0.7)
    song_start_audio = random.randint(range_start, range_end)
    
    background_music = AudioFileClip(SONG_PATH).subclip(song_start_audio, song_start_audio + VIDEO_LENGTH)
    
    # 🎥 Video
    cover_array = url_to_rgb_array(song.album.cover)
    
    # Blurry background
    def blur(image):
        return gaussian(image.astype(float), sigma=75)
    blurry_background = create_image(cover_array, 0, VIDEO_LENGTH, -1, -0.5, 7)
    blurry_background = blurry_background.fl_image(blur)

    TOP = 0.1
    
    # Cover
    cover_image = create_image(cover_array, 0, VIDEO_LENGTH, 0.05, TOP)
    
    # Infos
    infos = []
        # Right cover
    TEXT_MIDDLE_ALIGN = 0.5
    title = create_text(box_text(song.title, BOX_SIZE_RIGHT_COVER_BT), 0, VIDEO_LENGTH, TEXT_MIDDLE_ALIGN, TOP, fontsize=BIG_FONT_SIZE)
    artist = create_text(box_text(song.artist, BOX_SIZE_RIGHT_COVER_BT), 0, VIDEO_LENGTH, TEXT_MIDDLE_ALIGN, TOP + 0.13, fontsize=BIG_FONT_SIZE)
        # feat
    if song.is_feat():
        feat_text = box_text(f"feat. {', '.join(song.featurings)}", BOX_SIZE_RIGHT_COVER_ST)
        feat = create_text(feat_text, 0, VIDEO_LENGTH, TEXT_MIDDLE_ALIGN, TOP + 0.18)
        infos.append(feat)
        
    infos += [title, artist]
    
        # Under cover
    TEXT_LEFT_ALIGN = 0.05
    under_text_str = box_text(song.album.title, BOX_SIZE_UNDER_COVER_MT)
    under_text = create_text(under_text_str, 0, VIDEO_LENGTH, TEXT_LEFT_ALIGN, TOP + 0.25, fontsize=MID_FONT_SIZE)
    under_text2 = f"{song.length} · {song.album.date.strftime('%d %B %Y')}"
    offset = 0
    if "\n" in under_text_str:
        offset = 0.02
    under_text2 = create_text(under_text2, 0, VIDEO_LENGTH, TEXT_LEFT_ALIGN, TOP + 0.3 + offset)
    
    infos += [under_text, under_text2]
    
    # Comment
    comment_song = box_text(song.comment, BOX_SIZE_UNDER_COVER_ST)
    comment = create_text(comment_song, 0, VIDEO_LENGTH, TEXT_LEFT_ALIGN, TOP + 0.4)
    
    
    text = infos + [comment]
    # 📼 Render
    audio = CompositeAudioClip([background_music])
    result = CompositeVideoClip([blurry_background, cover_image] + text, size=(1080, 1920))
    result.audio = audio
    result.write_videofile(VIDEO_PATH, fps=fps)