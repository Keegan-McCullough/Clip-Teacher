from transformers import pipeline
import time

# Initialize the model (Flan-T5 Base is fast and local)
_generator = pipeline("text2text-generation", model="google/flan-t5-base", device_map="auto")

def generate_content(topic):
    t0 = time.perf_counter()
    
    # --- IMPROVED PROMPTING STRATEGY ---
    
    # 1. Generate Script
    # We use a direct command. 'do_sample=True' prevents repetitive loops.
    prompt_script = f"Explain the concept of {topic} simply."
    script_result = _generator(
        prompt_script, 
        max_length=80, 
        do_sample=True, 
        temperature=0.7,
        top_k=50
    )
    script = script_result[0]["generated_text"]
    
    # 2. Generate Visual Prompt
    # We ask for a physical description to give the video model concrete nouns.
    prompt_visual = f"Describe a physical image that represents {topic}."
    visual_result = _generator(
        prompt_visual, 
        max_length=50, 
        do_sample=True, 
        temperature=0.7
    )
    video_prompt = visual_result[0]["generated_text"]

    # Clean up text (remove trailing periods that might confuse some TTS)
    script = script.strip()
    video_prompt = video_prompt.strip()

    print(f"[Content] Generated in {time.perf_counter() - t0:.1f}s")
    print(f"   > Script: {script}")
    print(f"   > Visual: {video_prompt}")
    
    return script, video_prompt