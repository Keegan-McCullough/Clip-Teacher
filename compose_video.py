from moviepy import ImageSequenceClip, AudioFileClip, VideoFileClip

def compose_video():
    clip = ImageSequenceClip("outputs/frames", fps=1)
    audio = AudioFileClip("outputs/narration.wav")
    final = clip.set_audio(audio)
    final.write_videofile("outputs/final_video.mp4", fps=24)
