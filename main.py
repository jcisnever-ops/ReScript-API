"""
ReScript Transcription API
Hosted backend service for Base44 ReScript app
Handles: yt-dlp download + Deepgram transcription
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import tempfile
import subprocess
import requests
import json

app = FastAPI(title="ReScript Transcription API")

# Config from environment
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "0b45d86683f50c93301257790761a1c33128b775")

def download_video_audio(video_url: str) -> str:
    """Download audio from video URL using yt-dlp"""
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "audio.wav")
    
    try:
        # yt-dlp command - extract audio, convert to WAV
        cmd = [
            "yt-dlp",
            "-x",  # extract audio
            "--audio-format", "wav",
            "-o", audio_path,
            video_url,
            "--no-playlist",  # single video only
            "--quiet",  # suppress output
            "--no-warnings"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            raise Exception(f"yt-dlp failed: {result.stderr}")
        
        if not os.path.exists(audio_path):
            raise Exception("Audio file not created")
        
        return audio_path
        
    except subprocess.TimeoutExpired:
        raise Exception("Download timeout (120s)")
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using Deepgram API"""
    
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    # Deepgram API endpoint
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }
    params = {
        "model": "nova-2",  # best accuracy
        "smart_format": True,
        "punctuate": True,
        "language": "en"
    }
    
    response = requests.post(url, headers=headers, params=params, data=audio_data, timeout=60)
    
    if response.status_code != 200:
        raise Exception(f"Deepgram API error: {response.status_code} - {response.text}")
    
    result = response.json()
    
    # Extract transcript
    transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
    
    return transcript

@app.post("/transcribe")
async def transcribe_video(request: TranscribeRequest):
    """
    Download video + transcribe audio
    Called by Base44 ReScript frontend
    """
    try:
        # Step 1: Download audio
        audio_path = download_video_audio(video_url)
        
        # Step 2: Transcribe with Deepgram
        transcript = transcribe_audio(audio_path)
        
        # Step 3: Get duration (optional - parse from yt-dlp output)
        duration = 0.0  # TODO: extract from yt-dlp JSON output
        
        # Step 4: Cleanup temp files
        try:
            os.remove(audio_path)
            os.rmdir(os.path.dirname(audio_path))
        except:
            pass  # ignore cleanup errors
        
        return {
            "success": True,
            "transcript": transcript,
            "duration_seconds": duration,
            "project_name": project_name,
            "error": ""
        }
        
    except Exception as e:
        return {
            "success": False,
            "transcript": "",
            "duration_seconds": 0.0,
            "project_name": project_name,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "rescript-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
