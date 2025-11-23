from moviepy import VideoFileClip, AudioFileClip

def join_audio_video(video_path, audio_path, output_path):
    # 1. Load the video and audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # 2. Add audio to video
    # Note: In MoviePy 2.0, we use '.with_audio()' instead of '.set_audio()'
    final_clip = video.with_audio(audio)
    
    # 3. Save the result
    # We use 'aac' codec for audio which is standard for mp4
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac"
    )

if __name__ == "__main__":
    # Update these filenames to match your actual files
    join_audio_video("my_video.mp4", "my_audio.wav", "final_output.mp4")