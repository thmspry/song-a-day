from TikTokVideo import TikTokVideo
from tiktok_uploader.upload import upload_video

def publish_video(video: TikTokVideo, sessionId: str, headless: bool = True) -> bool:
    failed_videos = upload_video(video.path, description=video.description, sessionid=sessionId, headless=headless)
    return len(failed_videos) == 0
        
        
        