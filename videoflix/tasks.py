import subprocess # run commands from terminal
from django.conf import settings
import os

# FFMPEG_PATH = "/usr/bin/ffmpeg"
FFMPEG_PATH = "/Users/mariuskatzer/ffmpeg"

def create_thumbnail(source_path, time="00:00:00", width=640, height=360):
    """
    Create a thumbnail for a video file at a specified time.
    
    This function uses the FFMPEG tool to generate a thumbnail image 
    from a video. The thumbnail is saved in the 'thumbnails' directory 
    within the MEDIA_ROOT.
    
    Parameters:
    - source_path (str): The path to the video file from which to generate the thumbnail.
    - time (str, optional): The timestamp (in HH:MM:SS) at which to capture the thumbnail. Defaults to "00:00:00".
    - width (int, optional): The width of the thumbnail. Defaults to 640 pixels.
    - height (int, optional): The height of the thumbnail. Defaults to 360 pixels.
    
    Returns:
    - str: The file path to the generated thumbnail image.
    """
    
    file_name = os.path.splitext(os.path.basename(source_path))[0]
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, "thumbnails", f"{file_name}.jpg")
    cmd = '{} -i "{}" -ss {} -vframes 1 -vf "scale={}:{}" -update 1 "{}"'.format(
       FFMPEG_PATH, source_path, time, width, height, thumbnail_path
    )
    subprocess.run(cmd, shell=True)
    return thumbnail_path


def convert720p(source_path):

    """
    Convert a video to 720p resolution.
    
    This function uses the FFMPEG tool to convert a video file to 
    720p resolution and saves it with a new file name.
    
    Parameters:
    - source_path (str): The path to the original video file.
    
    Returns:
    - None
    """

    new_file_name = convert_path(source_path, "720p")
    cmd = (
        '{} -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
           FFMPEG_PATH, source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert480p(source_path):
    """
    Convert a video to 480p resolution.
    
    This function uses the FFMPEG tool to convert a video file to 
    480p resolution and saves it with a new file name.
    
    Parameters:
    - source_path (str): The path to the original video file.
    
    Returns:
    - None
    """
    
    new_file_name = convert_path(source_path, "480p")
    cmd = (
        '{} -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
           FFMPEG_PATH, source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert_path(source_path, resolution):
    """
    Generate a new file name for the converted video based on resolution.
    
    This helper function modifies the original video file's path by appending
    the resolution suffix (e.g., '_720p' or '_480p') to the file name.
    
    Parameters:
    - source_path (str): The path to the original video file.
    - resolution (str): The resolution suffix (e.g., '720p', '480p') to append to the file name.
    
    Returns:
    - str: The new file path with the resolution suffix added to the file name.
    """
    
    dot_index = source_path.rfind(".")
    base_name = source_path[:dot_index]
    ext = source_path[dot_index:]
    return f"{base_name}_{resolution}{ext}"