from transformers import pipeline
import time

# Initialize the model (Flan-T5 Large for better quality while remaining free/accessible)
_generator = pipeline("text2text-generation", model="google/flan-t5-large", device_map="auto")

def generate_content(topic):
    t0 = time.perf_counter()
    
    # --- IMPROVED PROMPTING STRATEGY ---
    # To generate a robust and long script without loops, we break it down into logical sections.
    
    script_parts = []

    # 1. Definition
    prompt_def = f"Explain {topic} in simple terms."
    res_def = _generator(prompt_def, max_new_tokens=60, do_sample=True, temperature=0.4, repetition_penalty=1.1)
    script_parts.append(res_def[0]["generated_text"].strip())

    # 2. Explanation
    prompt_exp = f"How does {topic} work?"
    res_exp = _generator(prompt_exp, max_new_tokens=100, do_sample=True, temperature=0.5, repetition_penalty=1.1)
    script_parts.append(res_exp[0]["generated_text"].strip())
    
    # 3. Importance
    prompt_imp = f"Why is {topic} important?"
    res_imp = _generator(prompt_imp, max_new_tokens=60, do_sample=True, temperature=0.5, repetition_penalty=1.1)
    script_parts.append(res_imp[0]["generated_text"].strip())

    script = " ".join(script_parts)

    # 4. Visual Prompt
    prompt_visual = f"Describe a picture of {topic}."
    visual_result = _generator(
        prompt_visual, 
        max_new_tokens=60,
        do_sample=True, 
        temperature=0.7
    )
    video_prompt = visual_result[0]["generated_text"].strip()

    print(f"[Content] Generated in {time.perf_counter() - t0:.1f}s")
    print(f"   > Script: {script}")
    print(f"   > Visual: {video_prompt}")
    
    return script, video_prompt
