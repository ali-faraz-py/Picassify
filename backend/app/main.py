from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

from app.utils import load_image_from_upload, tensor_to_image
from app.style_transfer import run_style_transfer

app = FastAPI(title="Picassify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate(
    content_image: UploadFile = File(...),
    style_image: UploadFile = File(...),
    steps: int = Form(150),
    style_weight: int = Form(1000000),
    image_size: int = Form(192),
):
    content_tensor = load_image_from_upload(content_image.file, size=image_size)
    style_tensor = load_image_from_upload(style_image.file, size=image_size)

    generated = run_style_transfer(
        content_tensor,
        style_tensor,
        steps=steps,
        content_weight=1,
        style_weight=style_weight,
    )

    result_image = tensor_to_image(generated)

    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")