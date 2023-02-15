from diffusers import StableDiffusionInstructPix2PixPipeline
import torch
from flow import MODEL_ID, REVISION

StableDiffusionInstructPix2PixPipeline.from_pretrained(
    MODEL_ID, revision=REVISION, resume_download=True, cache_dir="./huggingface/cache", safety_checker=None, requires_safety_checker=False, torch_dtype=torch.float16)
