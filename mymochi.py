import torch
from diffusers import MochiPipeline
from diffusers.utils import export_to_video

pipe = MochiPipeline.from_pretrained("/root/zgp2/fanzheming/mochi-1-preview", variant="bf16", torch_dtype=torch.bfloat16)

# Enable memory savings
pipe.enable_model_cpu_offload()
pipe.enable_vae_tiling()



prompt = "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k."
frames = pipe(prompt, num_frames=50).frames[0]



export_to_video(frames, "mochi.mp4", fps=10)
