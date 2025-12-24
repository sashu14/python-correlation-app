"""
Prompt templates for OSINT intelligence analysis.
Enhanced for drug trafficking detection on social media.
"""

SYSTEM_PROMPT = """
You are a lawful OSINT intelligence assistant.
Analyze ONLY publicly available data.
Detect behavioral indicators of drug trafficking.
Do not infer identity or guilt.
Generate explainable investigative leads only.
"""

TEXT_ANALYSIS_PROMPT = """
Analyze this public social media post for drug trafficking indicators.

Focus on:
1. SLANG DETECTION: Identify coded language, drug-related terms, street names
2. EMOJI ANALYSIS: Detect emojis commonly used in drug trade (💊, 💉, 🌿, 💰, etc.)
3. INTENT CLASSIFICATION: Selling, buying, promoting, or discussing
4. FUNNEL INDICATORS: Signs of moving from public to private (DM, Telegram, etc.)
5. PRICING PATTERNS: Numbers that might indicate prices or quantities

Return JSON format:
{
    "slang": ["list of detected slang terms"],
    "emojis": ["list of detected emojis"],
    "intent": "selling|buying|promoting|discussing|neutral",
    "funnel_indicator": true/false,
    "pricing_indicators": ["detected price patterns"],
    "confidence": 0-100,
    "risk_level": "low|medium|high"
}
"""

IMAGE_ANALYSIS_PROMPT = """
Analyze this image for drug trafficking indicators.

Look for:
1. DRUG SUBSTANCES: Pills, powders, plants, syringes, paraphernalia
2. PACKAGING: Baggies, containers, scales, wrapping materials
3. CASH: Large amounts of money, counting money
4. TEXT OVERLAYS: Prices, contact info, drug names
5. SETTINGS: Drug-related environments

Return JSON format:
{
    "drugs_detected": true/false,
    "packaging_detected": true/false,
    "cash_detected": true/false,
    "items_found": ["list of detected items"],
    "confidence": 0-100,
    "risk_level": "low|medium|high",
    "description": "detailed description of findings"
}
"""

VIDEO_ANALYSIS_PROMPT = """
Analyze this video frame for drug trafficking indicators.

Look for:
1. VISUAL ELEMENTS: Drugs, packaging, cash, paraphernalia
2. TEXT/SUBTITLES: Slang, prices, contact information
3. SPEECH INDICATORS: Keywords that might indicate drug trade
4. BEHAVIORAL CUES: Suspicious activities, counting, packaging

Return JSON format:
{
    "visual_indicators": ["list of visual findings"],
    "text_indicators": ["list of text/subtitle findings"],
    "audio_keywords": ["list of detected keywords"],
    "confidence": 0-100,
    "risk_level": "low|medium|high"
}
"""

