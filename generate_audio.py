from bark import generate_audio, preload_models
import torchaudio

def create_audio(script_text):
    preload_models()
    audio_array = generate_audio(script_text)
    torchaudio.save("outputs/narration.wav", audio_array.unsqueeze(0), 24000)