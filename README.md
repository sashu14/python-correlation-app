# UL-DNIP - Unified Futuristic Drug Network Intelligence Platform

OSINT intelligence platform for analyzing publicly available data related to drug trafficking indicators across social media, images, and videos.

## Features

- **Text Analysis**: Detects slang, emojis, intent, funnel indicators, and pricing patterns
- **Image Analysis**: Identifies drugs, packaging, cash, paraphernalia, and text overlays
- **Video Analysis**: Extracts frames and analyzes visual content, text, and behavioral cues
- **Behavioral Analysis**: Calculates persistence scores based on posting patterns
- **Crypto Analysis**: Analyzes transaction patterns (public blockchain data only)
- **Cross-Domain Correlation**: Combines all intelligence sources for risk scoring

## Prerequisites

1. **Python 3.10+**
   ```bash
   python --version
   ```

2. **Ollama**
   - Install from: https://ollama.com
   - Verify: `ollama --version`
   - Pull models:
     ```bash
     ollama pull gemma3:1b  # Primary model (recommended)
     ollama pull gemma:2b    # Fallback model
     ```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### 1. Text Analysis (`POST /analyze`)
Analyzes text with emoji and slang detection:
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Sample text with emojis 💊💰",
       "posts": 10,
       "tx": 15
     }'
```

### 2. Image Analysis (`POST /analyze/image`)
Upload and analyze images:
```bash
curl -X POST "http://127.0.0.1:8000/analyze/image" \
     -F "file=@image.jpg"
```

### 3. Video Analysis (`POST /analyze/video`)
Upload and analyze videos (extracts frames):
```bash
curl -X POST "http://127.0.0.1:8000/analyze/video" \
     -F "file=@video.mp4" \
     -F "max_frames=5"
```

### 4. Comprehensive Analysis (`POST /analyze/comprehensive`)
Combine text, image, and video analysis:
```bash
curl -X POST "http://127.0.0.1:8000/analyze/comprehensive" \
     -F "text=Sample text" \
     -F "image=@image.jpg" \
     -F "video=@video.mp4" \
     -F "posts=10" \
     -F "tx=15"
```

## Project Structure

```
ul-dnip/
├── main.py                 # FastAPI application with all endpoints
├── agents/
│   ├── __init__.py
│   ├── text_agent.py      # Text intelligence (slang, emoji, intent)
│   ├── image_agent.py     # Image analysis (drugs, packaging, cash)
│   ├── video_agent.py     # Video frame extraction and analysis
│   ├── behavior_agent.py  # Behavioral persistence scoring
│   └── crypto_agent.py    # Crypto pattern analysis
├── correlation.py          # Cross-domain correlation engine
├── prompts.py             # Enhanced system prompts
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Components

- **Text Agent**: Uses Ollama Gemma3:1b for slang, emoji, intent, and funnel detection
- **Image Agent**: Vision-based analysis for drugs, packaging, cash, and text overlays
- **Video Agent**: Frame extraction and analysis using OpenCV and Ollama vision
- **Behavior Agent**: Calculates behavioral persistence scores based on posting patterns
- **Crypto Agent**: Analyzes public blockchain transaction patterns (safe version)
- **Correlation Engine**: Correlates scores from all domains for final risk assessment

## Analysis Capabilities

### Text Analysis
- **Slang Detection**: Identifies coded language and drug-related terms
- **Emoji Analysis**: Detects emojis commonly used in drug trade (💊, 💉, 🌿, 💰)
- **Intent Classification**: Selling, buying, promoting, or discussing
- **Funnel Indicators**: Signs of moving from public to private channels
- **Pricing Patterns**: Numbers that might indicate prices or quantities

### Image Analysis
- **Drug Substances**: Pills, powders, plants, syringes, paraphernalia
- **Packaging**: Baggies, containers, scales, wrapping materials
- **Cash Detection**: Large amounts of money, counting money
- **Text Overlays**: Prices, contact info, drug names
- **Settings**: Drug-related environments

### Video Analysis
- **Visual Elements**: Drugs, packaging, cash, paraphernalia
- **Text/Subtitles**: Slang, prices, contact information
- **Speech Indicators**: Keywords that might indicate drug trade
- **Behavioral Cues**: Suspicious activities, counting, packaging

## Legal Notice

This platform is designed for lawful OSINT intelligence analysis only. It analyzes ONLY publicly available data and does not infer identity or guilt. Use responsibly and in compliance with applicable laws.

## References

Based on:
- Lawful Analysis of Drug Trafficking on Social Media (PDF)
- Unified Futuristic Drug Network Intelligence Platform (concept-to-implementation) (PDF)

