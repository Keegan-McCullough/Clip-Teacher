from generate_script import generate_script
from generate_audio import create_audio
from generate_images import create_images
from compose_video import compose_video
from generate_script import generate_script
from generate_audio import create_audio
from generate_images import create_images
from compose_video import compose_video
import os

if __name__ == "__main__":
    # Ensure outputs folder exists
    os.makedirs("outputs/frames", exist_ok=True)

    topic = input("Enter a concept to explain: ")
    print("Generating script...")
    script = generate_script(topic)
    
    print("Creating narration...")
    create_audio(script)
    
    print("Generating visuals...")
    create_images(topic)
    
    print("Composing final video...")
    compose_video()
    
    print("✅ Done! Video saved in outputs/final_video.mp4")

