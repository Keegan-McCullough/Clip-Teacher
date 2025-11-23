import os
import time
import shutil
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

from generate_content import generate_content
from generate_audio import create_audio
from generate_video import create_video_clip

OUTPUT_DIR = "outputs"

def cleanup_outputs(keep_final=True):
    """Deletes temp files to save space."""
    if not os.path.exists(OUTPUT_DIR):
        return
    
    print("\n[Cleanup] Removing temporary files...")
    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)
        if keep_final and filename == "final_video.mp4":
            continue
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def compose_final(video_path, audio_path):
    """Loops the short video clip to match audio duration."""
    print("[Compose] Merging Audio and Video...")
    
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path)
    
    # Speed Hack: Loop the generated video clip to match audio duration
    # This saves us from having to generate 100+ frames of AI video
    final_clip = video.fx(vfx.loop, duration=audio.duration)
    final_clip = final_clip.set_audio(audio)
    
    final_output = os.path.join(OUTPUT_DIR, "final_video.mp4")
    final_clip.write_videofile(final_output, fps=24, codec="libx264", audio_codec="aac")
    
    # Close handles to allow cleanup
    video.close()
    audio.close()
    final_clip.close()
    
    return final_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Delete temp files after run")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. User Input
    user_topic = input("\nWhat topic do you want to explain? ")
    
    # 2. Content Generation
    script_text, visual_prompt = generate_content(user_topic)
    
    # 3. Parallel Generation (Conceptual, done sequentially here for simplicity)
    audio_path = create_audio(script_text)
    video_path = create_video_clip(visual_prompt)
    
    # 4. Composition
    if video_path and audio_path:
        final_video = compose_final(video_path, audio_path)
        if final_video:
            print(f"\n✅ SUCCESS! Video saved to: {final_video}")
            os.startfile(final_video) # Windows: Attempts to open the video automatically
    else:
        print("\n[Error] Could not join clips because one failed to generate.")
    
    # 5. Storage Management
    if args.clean:
        cleanup_outputs(keep_final=True)
    else:
        print(f"[Tip] Run with --clean to auto-delete raw clips and audio.")