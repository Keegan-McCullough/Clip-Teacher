from transformers import pipeline
import os
import time

# Instantiate the HF pipeline once per-process (reuse across calls)
_generator = pipeline("text2text-generation", model="google/flan-t5-base")


def generate_script(topic):
    prompt = f"Explain the concept of {topic} in 3 short sentences suitable for a video narration."
    t0 = time.perf_counter()
    script = _generator(prompt, max_length=150)[0]["generated_text"]

    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print(f"[generate_script] generated script in {time.perf_counter() - t0:.1f}s")
    return script
