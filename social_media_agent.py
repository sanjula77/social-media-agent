"""
Social Media Agent
A Python script for managing social media interactions.
""" 
import os
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from agents import Agent, Runner, WebSearchTool, function_tool, ItemHelpers
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=openai_api_key)

@function_tool
def genarate_content(video_transcript: str, social_media_platform: str):
    print(f"Generating content for {social_media_platform} from video transcript...")

    # initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

   # Genarate content
   response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a social media agent that generates content for a given video transcript and social media platform."},
        
    ],
    max_tokens=2500,
   )
   return response.output_text
