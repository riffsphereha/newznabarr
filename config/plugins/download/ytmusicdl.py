from ytmusicapi import YTMusic
import os
import yt_dlp
import eyed3

from plugin_download_interface import PluginDownloadBase

def get_youtube_track_links(browse_id):
    ytmusic = YTMusic()
    trackcounter=0
    
    # Get the album tracks
    album_info = ytmusic.get_album(browse_id)
    
    if album_info and 'tracks' in album_info:
        tracks = album_info['tracks']
        youtube_links = []
        for track in tracks:
            trackcounter = trackcounter + 1
            title = track['title']
            video_id = track['videoId']
            youtube_link = f"https://www.youtube.com/watch?v={video_id}"
            youtube_links.append({'title': title, 'youtube_link': youtube_link, 'track': trackcounter})
        
        return youtube_links
    else:
        print("Album tracks not found.")
        return None


class YTMusicDownload(PluginDownloadBase):
    def getprefix(self):
        return ["ytmusic"]

    def download(self, url, title, download_dir, cat):
        full_download_dir = os.path.join(download_dir, cat, title)
        os.makedirs(full_download_dir, exist_ok=True)
        full_filename = full_download_dir

        ytmusic = YTMusic()
        trackcounter=0
        album_info = ytmusic.get_album(url)
        if album_info and 'tracks' in album_info:
            tracks = album_info['tracks']
            youtube_links = []
            for track in tracks:
                trackcounter = track['trackNumber']
                title = track['title']
                artist = track['artists'][0]["name"]
                album = track["album"]
                video_id = track['videoId']
                youtube_link = f"https://www.youtube.com/watch?v={video_id}"
                youtube_links.append({'title': title, 'youtube_link': youtube_link, 'track': trackcounter, "artist": artist, "album":album})
        for item in youtube_links:
            full_filename = os.path.join(full_download_dir , str(item["track"]) + " - " + item["title"])
            try:
                ydl_opts = {
                    'quiet': True,
                    'noprogress': True,
                    'format': 'bestaudio/best',
                    'outtmpl': full_filename,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                        'preferredcodec': 'mp3',      # Save as MP3
                        'preferredquality': '128',    # Set quality
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(item["youtube_link"])
            except Exception as e:
                print(f"Error: {str(e)}")
                return 404
            audio = eyed3.load(full_filename + ".mp3")
            audio.tag.artist=item["artist"]
            audio.tag.title=item["title"]
            audio.tag.album=item["album"]
            audio.tag.track_num=item["track"]

            audio.tag.save()
        return full_download_dir
        