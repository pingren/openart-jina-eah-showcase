from jina import Flow, Executor, DocumentArray, Document, requests
from typing import Dict
from PIL import Image
from io import BytesIO
from urllib.request import urlopen
import time
from diffusers import StableDiffusionInstructPix2PixPipeline
import torch

MODEL_ID = "timbrooks/instruct-pix2pix"
REVISION = "fp16"


def download_image(url):
    data = urlopen(url)
    image = Image.open(BytesIO(data.read()))
    image = image.convert("RGB")
    return image


class EditExecutor(Executor):
    pipe = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load Model, cached in ./huggingface/cache
        print("Loading Model from local cache...")
        pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            MODEL_ID,  revision=REVISION, local_files_only=True, cache_dir="./huggingface/cache", safety_checker=None, requires_safety_checker=False, torch_dtype=torch.float16)
        if torch.cuda.is_available():
            self.pipe = pipe.to("cuda")
        else:
            try:
                # Try to use mps for MacOS
                self.pipe = pipe.to("mps")
            except Exception:
                self.pipe = pipe.to("cpu")

    @requests(on="/")
    def edit(self, docs: DocumentArray, parameters: Dict, **kwargs):
        request_time = time.time()

        # Image Generation Parameters
        steps = int(parameters.get('steps', 20))
        guidance_scale = float(parameters.get('guidance_scale', 7.5))
        image_guidance_scale = float(
            parameters.get('image_guidance_scale', 1.5))

        # Image Output Parameters
        image_format = parameters.get("image_format", "jpeg")
        image_quality = parameters.get("image_quality", 95)

        # Generate Images
        for doc in docs:
            prompt = doc.text
            image = download_image(doc.uri)
            edit_image = self.pipe(prompt, image=image, num_inference_steps=steps,
                                   image_guidance_scale=image_guidance_scale, guidance_scale=guidance_scale).images[0]
            buffered = BytesIO()
            edit_image.save(buffered, format=image_format,
                            quality=image_quality)
            _d = Document(
                blob=buffered.getvalue(),
                mime_type="image" + "/" + image_format,
                tags={
                    'request': {
                        'api': 'edit',
                        'steps': steps,
                        'guidance_scale': guidance_scale,
                        'image_guidance_scale': image_guidance_scale,
                        'image_format': image_format,
                        'image_quality': image_quality,
                    },
                    'text': prompt,
                    'generator': MODEL_ID,
                    'request_time': request_time,
                    'created_time': time.time(),
                },
            ).convert_blob_to_datauri()
            _d.text = prompt
            doc.matches.append(_d)

if __name__ == "__main__":
    f = Flow().config_gateway(cors=True, protocol="http", port_expose=8088).add(
        uses=EditExecutor, prefetch=1)

    # f = Flow.load_config('flow.yml')
    with f:
        f.block()

# Use either way to start the flow
# 1. JINA_MP_START_METHOD=spawn python flow.py
# 2. jina flow --uses flow.yml