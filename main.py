"""
UL-DNIP - Unified Futuristic Drug Network Intelligence Platform
FastAPI application for OSINT intelligence analysis.
"""

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, JSONResponse
import json
import os
from tempfile import NamedTemporaryFile

# Agent imports (MUST exist)
from agents.text_agent import analyze_text
from agents.image_agent import analyze_image, analyze_image_from_pil
from agents.video_agent import analyze_video
from agents.behavior_agent import behavior_score
from agents.crypto_agent import crypto_pattern
from correlation import correlate

# --------------------------------------------------
# App initialization (THIS is what Render looks for)
# --------------------------------------------------
app = FastAPI(
    title="UL-DNIP",
    description="Unified Futuristic Drug Network Intelligence Platform"
)

# --------------------------------------------------
# Health check / root
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "UL-DNIP - Unified Futuristic Drug Network Intelligence Platform",
        "status": "operational"
    }

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

# --------------------------------------------------
# TEXT ANALYSIS
# --------------------------------------------------
@app.post("/analyze")
def analyze(data: dict):
    text = data.get("text", "")
    posts = data.get("posts", 1)
    tx_frequency = data.get("tx", 2)

    text_result = analyze_text(text)
    beh_score = behavior_score(posts, True)
    crypto_score = crypto_pattern(tx_frequency)

    text_score = 60  # placeholder
    final_risk = correlate(text_score, beh_score, crypto_score)

    return {
        "text_analysis": text_result,
        "behavior_score": beh_score,
        "crypto_score": crypto_score,
        "final_risk_score": final_risk
    }

# --------------------------------------------------
# IMAGE ANALYSIS
# --------------------------------------------------
@app.post("/analyze/image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = analyze_image(image_bytes=image_bytes)

        return {
            "image_analysis": result,
            "filename": file.filename,
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --------------------------------------------------
# VIDEO ANALYSIS
# --------------------------------------------------
@app.post("/analyze/video")
async def analyze_video_endpoint(
    file: UploadFile = File(...),
    max_frames: int = Form(5)
):
    try:
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            result = analyze_video(tmp_path, max_frames=max_frames)
            return {
                "video_analysis": result,
                "filename": file.filename,
                "status": "success"
            }
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --------------------------------------------------
# COMPREHENSIVE ANALYSIS
# --------------------------------------------------
@app.post("/analyze/comprehensive")
async def analyze_comprehensive(
    text: str = Form(None),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
    posts: int = Form(1),
    tx: int = Form(2)
):
    results = {}

    if text:
        results["text_analysis"] = analyze_text(text)

    if image:
        results["image_analysis"] = analyze_image(await image.read())

    if video:
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await video.read())
            tmp_path = tmp.name
        try:
            results["video_analysis"] = analyze_video(tmp_path)
        finally:
            os.unlink(tmp_path)

    beh_score = behavior_score(posts, True)
    crypto_score = crypto_pattern(tx)

    scores = [beh_score, crypto_score]
    if text:
        scores.append(60)

    results["behavior_score"] = beh_score
    results["crypto_score"] = crypto_score
    results["final_risk_score"] = round(sum(scores) / len(scores), 2)

    return results

# --------------------------------------------------
# LOCAL RUN ONLY (Render IGNORES THIS)
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
