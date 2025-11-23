import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import time
import os

_pipeline = None

def _load_pipeline():
    global _pipeline
    if _pipeline is None:
        print("[Video] Loading Zeroscope (Text-to-Video)...")
        # Zeroscope is optimized for 16:9 and lower VRAM than ModelScope
        model_id = "cerspense/zeroscope_v2_576w" 
        
        _pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        
        # Scheduler for speed (fewer steps needed)
        _pipeline.scheduler = DPMSolverMultistepScheduler.from_config(_pipeline.scheduler.config)
        
        # Optimizations for speed/memory
        if torch.cuda.is_available():
            _pipeline.to("cuda")
            _pipeline.enable_model_cpu_offload() # Vital for running on consumer GPUs
            _pipeline.enable_vae_slicing()

def create_video_clip(prompt, output_path="outputs/raw_clip.mp4"):
    t0 = time.perf_counter()
    _load_pipeline()
    
    os.makedirs("outputs", exist_ok=True)
    
    print(f"[Video] Generating clip for: '{prompt}'")
    
    # Speed configuration:
    # num_frames=24 at 8fps = 3 seconds of video. 
    # We will LOOP this video to fill the 7 seconds. 
    # Generating 7 full seconds (56 frames) would take 3x longer.
    video_frames = _pipeline(
        prompt, 
        num_inference_steps=25, 
        height=320, width=576, 
        num_frames=24
    ).frames
    
    # Export
    video_path = export_to_video(video_frames, output_path)
    print(f"[Video] Clip generated in {time.perf_counter() - t0:.1f}s")
    return video_path