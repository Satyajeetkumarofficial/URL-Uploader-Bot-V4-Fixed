import yt_dlp
from plugins.config import Config

async def download_youtube_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Safe fallback
            'outtmpl': f'{Config.DOWNLOAD_LOCATION}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                'status': 'success',
                'filepath': ydl.prepare_filename(info),
                'title': info.get('title')
            }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
