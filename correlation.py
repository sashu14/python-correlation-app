"""
Correlation Engine - The Core Intelligence Component.
Correlates scores from multiple domains (text, behavior, crypto).
"""


def correlate(text_score, behavior_score, crypto_score):
    """
    Correlate scores from multiple intelligence domains.
    
    Args:
        text_score: Score from text analysis (0-100)
        behavior_score: Score from behavioral analysis (0-100)
        crypto_score: Score from crypto pattern analysis (0-100)
        
    Returns:
        Correlated risk score (0-100), rounded to 2 decimal places
    """
    return round((text_score + behavior_score + crypto_score) / 3, 2)

