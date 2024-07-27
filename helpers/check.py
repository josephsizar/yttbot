import re

def is_youtube_url(url):
    """Extract the video ID from a YouTube URL."""
    # Regular expression to match YouTube video IDs
    video_id_pattern = re.compile(r'(?:v=|\/|embed\/|video\/|watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})')
    match = video_id_pattern.search(url)
    return match.group(1) if match else None



def get_thumbnail_url(video_id, quality='hqdefault'):
    """Construct the URL for the thumbnail image."""
    return f'https://img.youtube.com/vi/{video_id}/{quality}.jpg'


