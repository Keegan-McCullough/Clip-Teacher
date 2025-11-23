from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import time
import os

# Global cache
_processor = None
_model = None
_vocoder = None
_speaker_embeddings = None

def _load_models():
    global _processor, _model, _vocoder, _speaker_embeddings
    if _model is None:
        print("[Audio] Loading SpeechT5 (Fast)...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        _processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        _model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
        _vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)
        
        # --- FIX: Use the safe Parquet version of the dataset ---
        # The original 'Matthijs' version is blocked by the new 'datasets' library security.
        embeddings_dataset = load_dataset("regisss/cmu-arctic-xvectors", split="validation")

        # Select a speaker (Index 7306 is a clean male voice 'bdl')
        # We assume the parquet conversion preserved the order or contains valid xvectors
        speaker_vector = embeddings_dataset[7306]["xvector"]
        _speaker_embeddings = torch.tensor(speaker_vector).unsqueeze(0).to(device)

def create_audio(text, output_path="outputs/narration.wav"):
    t0 = time.perf_counter()
    _load_models()
    
    inputs = _processor(text=text, return_tensors="pt").to(_model.device)
    
    # Generate audio
    with torch.no_grad():
        speech = _model.generate_speech(inputs["input_ids"], _speaker_embeddings, vocoder=_vocoder)

    os.makedirs("outputs", exist_ok=True)
    
    # Save using soundfile
    sf.write(output_path, speech.cpu().numpy(), samplerate=16000)
    
    print(f"[Audio] Generated in {time.perf_counter() - t0:.1f}s")
    return output_path