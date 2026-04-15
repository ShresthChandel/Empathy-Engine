def map_params(emotion: str, intensity: float):
    # Base table from requirements
    base_map = {
        "joy": {"rate_base": 20, "pitch_base": 15, "volume_base": 10, "pauses": "few"},
        "sadness": {"rate_base": -20, "pitch_base": -15, "volume_base": -20, "pauses": "long"},
        "anger": {"rate_base": 25, "pitch_base": 20, "volume_base": 25, "pauses": "abrupt"},
        "fear": {"rate_base": 30, "pitch_base": 20, "volume_base": -5, "pauses": "short"},
        "disgust": {"rate_base": -15, "pitch_base": -10, "volume_base": 5, "pauses": "contemptuous"},
        "surprise": {"rate_base": 35, "pitch_base": 30, "volume_base": 15, "pauses": "pause before key"},
        "neutral": {"rate_base": 0, "pitch_base": 0, "volume_base": 0, "pauses": "standard"}
    }
    
    cfg = base_map.get(emotion, base_map["neutral"])
    
    # Scale via intensity 0-1
    rate_val = int(cfg["rate_base"] * intensity)
    pitch_val = int(cfg["pitch_base"] * intensity)
    volume_val = int(cfg["volume_base"] * intensity)
    
    # Generate syntax
    return {
        "rate": f"+{rate_val}%" if rate_val >= 0 else f"{rate_val}%",
        "pitch": f"+{pitch_val}Hz" if pitch_val >= 0 else f"{pitch_val}Hz",
        "volume": f"+{volume_val}%" if volume_val >= 0 else f"{volume_val}%",
        "pauses_style": cfg["pauses"]
    }

def get_dynamic_voice(emotion: str) -> str:
    # Route specific emotions to neural personas with inherently matching timbre boundaries.
    # IMPORTANT: We only use verified Edge-TTS native free voices
    routing = {
        "joy": "en-US-EmmaNeural",          # Cheerful, Clear
        "surprise": "en-US-EmmaNeural",
        "anger": "en-US-GuyNeural",         # Passion, High energy
        "sadness": "en-US-AvaNeural",       # Caring, Expressive (softens beautifully)
        "fear": "en-US-AvaNeural",
        "disgust": "en-US-EricNeural",      # Rational, Stern
        "neutral": "en-US-AriaNeural"       # Positive, Confident
    }
    return routing.get(emotion, "en-US-AriaNeural")

def apply_lexical_padding(text: str, emotion: str, intensity: float) -> str:
    # Context Shading: We silently prepend structural punctuation/timing to the stream
    # to trick the neural network into changing its posture gracefully.
    
    if emotion in ["sadness", "fear"] and intensity > 0.4:
        # Pushing a silent breath hesitation at the beginning softens the delivery naturally
        return "... " + text
        
    elif emotion == "disgust" and intensity > 0.4:
        # A disjointed start mimics contempt/appallment
        return "... " + text
        
    elif emotion == "anger" and intensity > 0.5:
        # Naturally forces a louder volume projection
        return text.upper()
        
    return text
