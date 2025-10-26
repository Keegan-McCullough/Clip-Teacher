from transformers import pipeline
import os

def generate_script(topic):
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    prompt = f"Explain the concept of {topic} in 3 short sentences suitable for a video narration."
    script = generator(prompt, max_length=150)[0]['generated_text']

    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/script.txt", "w") as f:
        f.write(script)

    return script
