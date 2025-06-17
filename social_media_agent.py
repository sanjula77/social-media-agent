"""
Social Media Agent
A Python script for managing social media interactions using Ollama's llama3 model.
"""
import os
import asyncio
from typing import List, Optional
from dataclasses import dataclass

import ollama
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

@dataclass
class Post:
    platform: str
    content: str

async def generate_content(video_transcript: str, social_media_platform: str) -> List[Post]:
    """Generate social media content from a video transcript."""
    print(f"🔧 Generating content for {social_media_platform} from video transcript...")

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "You are a social media agent that generates engaging posts based on video transcripts.",
            },
            {
                "role": "user",
                "content": f"Write a creative and platform-appropriate post for {social_media_platform} using this transcript:\n\n{video_transcript}",
            },
        ],
    )

    content = response["message"]["content"]
    result = [Post(platform=social_media_platform, content=content)]
    print(f"DEBUG: generate_content returns: {result} (type: {type(result[0])})")
    return result

def fetch_video_transcript(video_id: str) -> Optional[str]:
    """Fetch transcript by YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript])
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
        return None

async def main(video_id: str, platform: str):
    transcript = fetch_video_transcript(video_id)

    if not transcript:
        print("❌ Transcript fetch failed.")
        return

    print("\n📝 Transcript preview (first 500 chars):")
    print(transcript[:500] + "...\n")

    result = await generate_content(transcript, platform)

    print(f"DEBUG: Generated result type: {type(result)}")

    if result:
        for post in result:
            print(f"\n📱 Generated {post.platform} post:")
            print("-" * 50)
            print(post.content)
            print("-" * 50)
    else:
        print("❌ No result generated.")

if __name__ == "__main__":
    video_id = input("🔗 Enter YouTube video ID (e.g., zOFxHmjIhvY): ").strip()
    platform = input("📱 Enter social media platform (e.g., Twitter, Instagram, LinkedIn): ").strip()
    
    asyncio.run(main(video_id, platform))
