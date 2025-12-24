"""
UL-DNIP - Unified Futuristic Drug Network Intelligence Platform
FastAPI application for OSINT intelligence analysis.
Enhanced with image, video, text, emoji, and slang detection.
"""
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, JSONResponse
import json
import os
from tempfile import NamedTemporaryFile
from agents.text_agent import analyze_text
from agents.image_agent import analyze_image, analyze_image_from_pil
from agents.video_agent import analyze_video
from agents.behavior_agent import behavior_score
from agents.crypto_agent import crypto_pattern
from correlation import correlate

app = FastAPI(title="UL-DNIP", description="Unified Futuristic Drug Network Intelligence Platform")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "UL-DNIP - Unified Futuristic Drug Network Intelligence Platform",
        "status": "operational"
    }


@app.get("/favicon.ico")
def favicon():
    """Handle favicon requests to prevent 404 errors."""
    return Response(status_code=204)


@app.post("/analyze")
def analyze(data: dict):
    """
    Analyze text data across multiple intelligence domains.
    Enhanced with emoji and slang detection.
    
    Expected input:
    {
        "text": "text content to analyze",  # REQUIRED: Type your text here
        "posts": number of posts (optional, default: 1),
        "tx": transaction frequency (optional, default: 2)
    }
    
    Returns:
    {
        "text_analysis": analysis result with slang, emojis, intent, funnel indicators,
        "behavior_score": behavioral persistence score,
        "crypto_score": crypto pattern score,
        "final_risk_score": correlated risk score
    }
    """
    # Extract text input (required parameter)
    text = data.get("text", "")
    
    # Extract optional parameters with defaults
    posts = data.get("posts", 1)
    tx_frequency = data.get("tx", 2)
    
    # Run enhanced text analysis (includes emoji and slang detection)
    text_result = analyze_text(text)
    
    # Calculate behavioral score
    beh_score = behavior_score(posts, True)  # Assuming repeated phrases detected
    
    # Calculate crypto pattern score
    crypto_score = crypto_pattern(tx_frequency)
    
    # Extract text score from analysis (simplified - using default 60)
    # In production, parse text_result JSON to extract confidence score
    text_score = 60
    
    # Correlate all scores
    final_risk = correlate(text_score, beh_score, crypto_score)
    
    return {
        "text_analysis": text_result,
        "behavior_score": beh_score,
        "crypto_score": crypto_score,
        "final_risk_score": final_risk
    }


@app.post("/analyze/image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Analyze uploaded image for drug-related content.
    Detects: drugs, packaging, cash, paraphernalia, text overlays.
    
    Parameters:
    - file: UploadFile - REQUIRED: Upload your image file here (jpg, png, jpeg, etc.)
    
    Returns:
    {
        "image_analysis": analysis result with detected items and risk level,
        "filename": original filename
    }
    """
    try:
        # Read uploaded image file
        image_bytes = await file.read()
        
        # Analyze image
        result = analyze_image(image_bytes=image_bytes)
        
        return JSONResponse(content={
            "image_analysis": json.loads(result) if result.startswith('{') else result,
            "filename": file.filename,
            "status": "success"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )


@app.post("/analyze/video")
async def analyze_video_endpoint(file: UploadFile = File(...), max_frames: int = Form(5)):
    """
    Analyze uploaded video for drug-related content.
    Extracts frames and analyzes them for visual indicators.
    
    Parameters:
    - file: UploadFile - REQUIRED: Upload your video file here (mp4, avi, mov, etc.)
    - max_frames: Maximum number of frames to analyze (default: 5)
    
    Returns:
    {
        "video_analysis": analysis result with frame-by-frame breakdown,
        "filename": original filename
    }
    """
    try:
        # Save uploaded file temporarily
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Analyze video
            result = analyze_video(tmp_path, max_frames=max_frames)
            
            return JSONResponse(content={
                "video_analysis": json.loads(result) if result.startswith('{') else result,
                "filename": file.filename,
                "status": "success"
            })
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "failed"}
        )


@app.post("/analyze/comprehensive")
async def analyze_comprehensive(
    text: str = Form(None),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
    posts: int = Form(1),
    tx: int = Form(2)
):
    """
    Comprehensive analysis combining text, image, and video analysis.
    
    Parameters:
    - text: str - OPTIONAL: Type your text here
    - image: UploadFile - OPTIONAL: Upload your image file here
    - video: UploadFile - OPTIONAL: Upload your video file here
    - posts: Number of posts for behavioral analysis (default: 1)
    - tx: Transaction frequency for crypto analysis (default: 2)
    
    Returns:
    Combined analysis results from all provided inputs.
    """
    results = {}
    
    # Text analysis
    if text:
        results["text_analysis"] = analyze_text(text)
    
    # Image analysis
    if image:
        try:
            image_bytes = await image.read()
            results["image_analysis"] = analyze_image(image_bytes=image_bytes)
        except Exception as e:
            results["image_analysis"] = {"error": str(e)}
    
    # Video analysis
    if video:
        try:
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(video.filename)[1]) as tmp_file:
                content = await video.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                results["video_analysis"] = analyze_video(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        except Exception as e:
            results["video_analysis"] = {"error": str(e)}
    
    # Behavioral and crypto scores
    beh_score = behavior_score(posts, True)
    crypto_score = crypto_pattern(tx)
    
    # Calculate overall risk (simplified)
    scores = [beh_score, crypto_score]
    if text:
        scores.append(60)  # Default text score
    
    final_risk = round(sum(scores) / len(scores), 2) if scores else 0
    
    results["behavior_score"] = beh_score
    results["crypto_score"] = crypto_score
    results["final_risk_score"] = final_risk
    
    return JSONResponse(content=results)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

