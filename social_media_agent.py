"""
Social Media Agent
A Python script for managing social media interactions using Ollama's llama3 model.
"""

import os
import asyncio
import logging
from typing import List, Optional
from dataclasses import dataclass

import ollama
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Data class for social media posts
@dataclass
class Post:
    platform: str
    content: str

# Fetch video transcript
def fetch_video_transcript(video_id: str) -> Optional[str]:
    """Fetch transcript by YouTube video ID."""
    try:
        logging.info(f"🎥 Fetching transcript for video ID: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item["text"] for item in transcript])
        return full_text
    except Exception as e:
        logging.error(f"❌ Error fetching transcript: {e}")
        return None

# Generate content using Ollama
async def generate_content(video_transcript: str, social_media_platform: str) -> List[Post]:
    """Generate social media content using Ollama."""
    logging.info(f"🛠️ Generating content for platform: {social_media_platform}")

    # Truncate transcript to avoid token overflow (adjust as needed)
    max_chars = 2000
    truncated_transcript = video_transcript[:max_chars]

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media agent that generates engaging posts based on video transcripts.",
                },
                {
                    "role": "user",
                    "content": f"Write a short, creative and engaging social media post suitable for {social_media_platform} using the transcript:\n\n{truncated_transcript}",
                },
            ],
        )
        content = response["message"]["content"]
        return [Post(platform=social_media_platform, content=content)]

    except Exception as e:
        logging.error(f"❌ Error generating content for {social_media_platform}: {e}")
        return []

# Save post to file (optional)
def save_post_to_file(post: Post, video_id: str):
    """Save generated post to a .txt file."""
    filename = f"{video_id}_{post.platform.lower()}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(post.content)
        logging.info(f"📁 Post saved to {filename}")
    except Exception as e:
        logging.error(f"❌ Failed to save post: {e}")

# Main execution logic
async def main(video_id: str, platforms: List[str], save_to_file: bool = True):
    transcript = fetch_video_transcript(video_id)

    if not transcript:
        logging.warning("⚠️ Transcript fetch failed. Exiting.")
        return

    logging.info("📄 Transcript preview (first 300 chars):")
    print(transcript[:300] + "...\n")

    for platform in platforms:
        results = await generate_content(transcript, platform)

        for post in results:
            print(f"\n📱 Generated {post.platform} Post:\n" + "-" * 50)
            print(post.content)
            print("-" * 50)

            if save_to_file:
                save_post_to_file(post, video_id)

# CLI interaction
if __name__ == "__main__":
    video_id = input("🔗 Enter YouTube video ID (e.g., zOFxHmjIhvY): ").strip()
    platforms_input = input("📱 Enter platforms (comma-separated): ").strip()
    platforms = [p.strip().capitalize() for p in platforms_input.split(",") if p.strip()]

    asyncio.run(main(video_id, platforms))

# """
# Social Media Agent
# A Python script for managing social media interactions using Ollama's llama3 model.
# """
# import os
# import asyncio
# from typing import List, Optional
# from dataclasses import dataclass

# import ollama
# from dotenv import load_dotenv
# from youtube_transcript_api import YouTubeTranscriptApi

# load_dotenv()

# @dataclass
# class Post:
#     platform: str
#     content: str

# async def generate_content(video_transcript: str, social_media_platform: str) -> List[Post]:
#     """Generate social media content from a video transcript."""
#     print(f"🔧 Generating content for {social_media_platform} from video transcript...")

#     try:
#         response = ollama.chat(
#             model="llama3",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a social media agent that generates engaging posts based on video transcripts.",
#                 },
#                 {
#                     "role": "user",
#                     "content": f"Write a creative and platform-appropriate post for {social_media_platform} using this transcript:\n\n{video_transcript}",
#                 },
#             ],
#         )
#     except Exception as e:
#         print(f"❌ Error generating content with Ollama: {e}")
#         return []

#     content = response["message"]["content"]
#     result = [Post(platform=social_media_platform, content=content)]
#     print(f"DEBUG: generate_content returns: {result} (type: {type(result[0])})")
#     return result

# def fetch_video_transcript(video_id: str) -> Optional[str]:
#     """Fetch transcript by YouTube video ID."""
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         return " ".join([item["text"] for item in transcript])
#     except Exception as e:
#         print(f"❌ Error fetching transcript: {e}")
#         return None

# async def main(video_id: str, platform: str):
#     transcript = fetch_video_transcript(video_id)

#     if not transcript:
#         print("❌ Transcript fetch failed.")
#         return

#     print("\n📝 Transcript preview (first 500 chars):")
#     print(transcript[:500] + "...\n")

#     result = await generate_content(transcript, platform)

#     print(f"DEBUG: Generated result type: {type(result)}")

#     if result:
#         for post in result:
#             print(f"\n📱 Generated {post.platform} post:")
#             print("-" * 50)
#             print(post.content)
#             print("-" * 50)
#     else:
#         print("❌ No result generated.")

# if __name__ == "__main__":
#     video_id = input("🔗 Enter YouTube video ID (e.g., zOFxHmjIhvY): ").strip()
#     platform = input("📱 Enter social media platform (e.g., Twitter, Instagram, LinkedIn): ").strip()
    
#     asyncio.run(main(video_id, platform))
