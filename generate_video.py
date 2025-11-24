from gradio_client import Client
import time
import os
import shutil
import numpy as np

def create_video_clip(prompt, output_path="outputs/raw_clip.mp4"):
    t0 = time.perf_counter()
    os.makedirs("outputs", exist_ok=True)
    
    print(f"[Video] Connecting to Hugging Face (Zeroscope)...")
    print(f"        Prompt: '{prompt}'")
    print("        (This is free but uses a public queue. Please wait...)")
    
    try:
        # 1. Connect to a working Space
        # 'fffiloni/zeroscope' is a popular, reliable alternative
        client = Client("fffiloni/zeroscope")
        
        # 2. Send Request
        # Zeroscope takes the prompt and a "model_choice" (use "576w" for speed)
        result = client.predict(
            prompt,  # str  in 'Prompt' Textbox component
            "576w",  # str  in 'Model Selection' Radio component
            api_name="/predict"
        )
        
        # 3. Handle Result (It returns a video path)
        # The result is a temporary file path on your machine
        temp_video_path = result[0] if isinstance(result, (list, tuple)) else result
        
        # Move it to your output folder
        if os.path.exists(output_path):
            os.remove(output_path)
        shutil.move(temp_video_path, output_path)
            
        print(f"[Video] Saved to {output_path} in {time.perf_counter() - t0:.1f}s")
        return output_path

    except Exception as e:
        print(f"\n[ERROR] Hugging Face generation failed: {e}")
        print("[Video] Switching to fallback black screen...")
        return _create_fallback_video(output_path)

def _create_fallback_video(output_path):
    """Creates a simple black screen video if the API fails."""
    # FIX: Correct imports for MoviePy 2.0
    from moviepy.video.VideoClip import ImageClip
    
    # Create a black frame (576x320 to match Zeroscope)
    black_frame = np.zeros((320, 576, 3), dtype=np.uint8)
    
    # Create clip
    clip = ImageClip(black_frame)
    clip = clip.with_duration(3).with_fps(24)
    
    clip.write_videofile(output_path, codec="libx264", logger=None)
    return output_path