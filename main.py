from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import shutil
import re

def download_video(url, folder_path):
    try:
        def on_progress(stream, chunk, remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - remaining
            progress = (bytes_downloaded / total_size) * 100
            print(f"Downloading... {progress:.2f}% done", end='\r', flush=True)

        yt = YouTube(url, on_progress_callback=on_progress)
        video_title = yt.title

        video_title = sanitize_filename(video_title)

        video = yt.streams.get_highest_resolution()
        video_file_path = video.download(folder_path, filename_prefix=video_title)
        print("\nDownload Completed!")

        mp4_video = VideoFileClip(video_file_path)
        mp3_audio = mp4_video.audio
        mp3_audio_file_path = os.path.join(folder_path, f"{video_title}.mp3")
        mp3_audio.write_audiofile(mp3_audio_file_path)
        mp3_audio.close()

        mp3_target_path = os.path.join(r'D:\Project\YTTOMP3\downloads\MP3', f"{video_title}.mp3")
        shutil.move(mp3_audio_file_path, mp3_target_path)

        return "Downloaded, Converted, and Moved Successfully!", video_title, mp3_target_path
    except Exception as e:
        return f"An error occurred: {e}", None, None

def sanitize_filename(filename):
    # Replace invalid characters with a hyphen (-)
    return re.sub(r'[\\/|:?"<>*]', '-', filename)

folder_path = r'D:\Project\YTTOMP3\downloads\Youtube Videos'
os.makedirs(folder_path, exist_ok=True)

while True:
    video_url = input("Enter the YouTube video URL (or type 'exit' to quit): ")
    if video_url.lower() == 'exit':
        break

    status, video_title, mp3_audio_path = download_video(video_url, folder_path)

    if video_title and mp3_audio_path:
        print(f"Video Title: {video_title}")
        print(f"Status: {status}")
        print(f"MP3 Audio Path: {mp3_audio_path}")
    else:
        print(status)
