import uuid
import io
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.utils import load_image_from_upload, tensor_to_image
from app.style_transfer import run_style_transfer

app = FastAPI(title="Picassify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

jobs = {}

@app.get("/")
def health_check():
    return {"status": "ok"}


def process_job(job_id, content_bytes, style_bytes, steps, style_weight, image_size):
    try:
        content_tensor = load_image_from_upload(io.BytesIO(content_bytes), size=image_size)
        style_tensor = load_image_from_upload(io.BytesIO(style_bytes), size=image_size)

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

        jobs[job_id] = {"status": "done", "result": buf.getvalue()}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}


@app.post("/generate/start")
async def start_generate(
    background_tasks: BackgroundTasks,
    content_image: UploadFile = File(...),
    style_image: UploadFile = File(...),
    steps: int = Form(150),
    style_weight: int = Form(1000000),
    image_size: int = Form(192),
):
    content_bytes = await content_image.read()
    style_bytes = await style_image.read()

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}

    background_tasks.add_task(
        process_job, job_id, content_bytes, style_bytes, steps, style_weight, image_size
    )

    return {"job_id": job_id}


@app.get("/generate/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": job["status"]}


@app.get("/generate/result/{job_id}")
def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "done":
        raise HTTPException(status_code=400, detail="Job not finished yet")

    buf = io.BytesIO(job["result"])
    return StreamingResponse(buf, media_type="image/png")