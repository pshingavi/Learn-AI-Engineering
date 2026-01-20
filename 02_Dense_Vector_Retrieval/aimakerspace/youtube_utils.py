from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
import re


class YouTubeTranscriptLoader:
    def __init__(self, video_url: str):
        """
        Initialize with a YouTube video URL.
        
        Args:
            video_url: Full YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
        """
        self.video_url = video_url
        self.video_id = self._extract_video_id(video_url)
        self.documents = []
    
    def _extract_video_id(self, url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.
        
        Handles:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/watch?v=VIDEO_ID&list=...
        """
        # Pattern for standard youtube.com URLs
        # For watch?v= format
        pattern1 = r'[?&]v=([a-zA-Z0-9_-]{11})'
        pattern2 = r'youtu\.be/([a-zA-Z0-9_-]{11})'
        match = re.search(pattern1, url) or re.search(pattern2, url)
        return match.group(1) if match else None
    
    def load_transcript(self) -> str:
        # Create instance and fetch
        fetched_transcript = YouTubeTranscriptApi().fetch(self.video_id)
        
        # Each snippet has .text attribute, not ['text']
        texts = [snippet.text for snippet in fetched_transcript]
        return " ".join(texts)
    
    def load_documents(self) -> List[str]:
        """
        Load transcript as a document list (matches TextFileLoader interface).
        
        Returns:
            List containing the transcript as a single document
        """
        transcript = self.load_transcript()
        self.documents = [transcript]
        return self.documents