import re
import asyncio
import edge_tts

def generate_mp3_from_ssml(ssml_string: str, output_path: str):
    """
    Consumes an SSML string and securely interfaces with Edge-TTS.
    Edge-TTS websockets strictly reject unescaped nested XML child nodes. 
    To maintain audible <break> pauses without hitting server injection crashes,
    we translate SSML pauses into natural neural punctuation markers (ellipses, commas)
    which physically force the TTS model to pause appropriately.
    """
    # Extract structural components
    rate_match = re.search(r'rate="([^"]+)"', ssml_string)
    pitch_match = re.search(r'pitch="([^"]+)"', ssml_string)
    volume_match = re.search(r'volume="([^"]+)"', ssml_string)
    voice_match = re.search(r'<voice name="([^"]+)">', ssml_string)
    
    text_match = re.search(r'<prosody[^>]*>(.*?)</prosody>', ssml_string, re.DOTALL)
    
    rate = rate_match.group(1) if rate_match else "+0%"
    pitch = pitch_match.group(1) if pitch_match else "+0Hz"
    volume = volume_match.group(1) if volume_match else "+0%"
    voice = voice_match.group(1) if voice_match else "en-US-AriaNeural"
    text = text_match.group(1).strip() if text_match else ""

    # Translate SSML break tags into physical neural pauses
    text = re.sub(r'<break time="700ms"\s*/>', '... ', text)
    text = re.sub(r'<break time="400ms"\s*/>', '... ', text)
    text = re.sub(r'<break time="350ms"\s*/>', ', ', text)
    text = re.sub(r'<break time="200ms"\s*/>', ', ', text)
    # Strip any straggler tags to guarantee MS Edge doesn't terminate the WebSocket
    text = re.sub(r'<break[^>]*>', '', text)
    
    async def _generate():
        comm = edge_tts.Communicate(
            text=text, 
            voice=voice,
            rate=rate, 
            pitch=pitch, 
            volume=volume
        )
        await comm.save(output_path)
        
    asyncio.run(_generate())
