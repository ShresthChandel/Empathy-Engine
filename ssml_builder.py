def build_ssml(text: str, voice_params: dict, voice_name: str = "en-US-AriaNeural") -> str:
    """
    Builds the explicit SSML XML string that will be sent to the TTS engine.
    """
    rate = voice_params.get("rate", "+0%")
    pitch = voice_params.get("pitch", "+0Hz")
    volume = voice_params.get("volume", "+0%")
    
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{voice_name}">
        <prosody rate="{rate}" pitch="{pitch}" volume="{volume}">
            {text}
        </prosody>
    </voice>
</speak>"""
    return ssml.strip()
