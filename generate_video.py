import replicate
import requests
import time
import os
import numpy as np

# --- OPTIONAL: PASTE KEY HERE IF TERMINAL FAILS ---
# os.environ["REPLICATE_API_TOKEN"] = "r8_..."

def create_video_clip(prompt, output_path="outputs/raw_clip.mp4"):
    t0 = time.perf_counter()
    os.makedirs("outputs", exist_ok=True)
    
    print(f"[Video] Sending request to Minimax Video-01...")
    
    try:
        # Check for key before running
        if not os.environ.get("REPLICATE_API_TOKEN"):
            raise ValueError("Replicate API Token is missing!")

        # 1. RUN THE MODEL
        # Minimax Video-01 generates ~6 seconds at 1280x720
        output = replicate.run(
            "minimax/video-01",
            input={
                "prompt": prompt,
                "prompt_optimizer": True
            }
        )
        
        # 2. SAVE THE FILE
        # Handle 'FileOutput' object or URL string
        print(f"[Video] Downloading content...")
        
        # If output is a list (rare for this model), take first item
        if isinstance(output, list):
            output = output[0]
            
        # Write to file
        with open(output_path, "wb") as file:
            # If it's a file object, read it. If it's a URL, download it.
            if hasattr(output, "read"):
                file.write(output.read())
            else:
                resp = requests.get(str(output))
                file.write(resp.content)
            
        print(f"[Video] Saved to {output_path} in {time.perf_counter() - t0:.1f}s")
        return output_path

    except Exception as e:
        print(f"\n[ERROR] Replicate failed: {e}")
        print("[Video] Switching to fallback (Black Screen)...")
        return _create_fallback_video(output_path)

def _create_fallback_video(output_path):
    """
    Creates a simple black screen video without relying on 'ColorClip',
    which can be buggy in MoviePy 2.0.
    """
    from moviepy import ImageClip
    
    # Create a black image using numpy (1280x720)
    # This is 100% robust and works on all versions
    black_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    # Create clip
    clip = ImageClip(black_frame)
    clip = clip.with_duration(6).with_fps(24) # MoviePy 2.0 syntax
    
    clip.write_videofile(output_path, codec="libx264", logger=None)
    return output_path