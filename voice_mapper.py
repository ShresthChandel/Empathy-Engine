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
