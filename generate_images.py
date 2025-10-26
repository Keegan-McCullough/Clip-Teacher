from diffusers import StableDiffusionPipeline
import torch, os

def create_images(topic):
    os.makedirs("outputs/frames", exist_ok=True)
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
    ).to("cuda")
    
    prompts = [
        f"An educational illustration of {topic}",
        f"A diagram explaining {topic}",
        f"A conceptual image representing {topic}"
    ]
    
    for i, p in enumerate(prompts, 1):
        image = pipe(p).images[0]
        image.save(f"outputs/frames/frame_{i}.png")