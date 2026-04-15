import asyncio
import edge_tts
import edge_tts.communicate

def generate_mp3_from_ssml(ssml_string: str, output_path: str):
    import re
    # Extract SSML attributes using Regex
    rate_match = re.search(r'rate="([^"]+)"', ssml_string)
    pitch_match = re.search(r'pitch="([^"]+)"', ssml_string)
    volume_match = re.search(r'volume="([^"]+)"', ssml_string)
    voice_match = re.search(r'<voice name="([^"]+)">', ssml_string)
    
    # Extract the text payload (which contains <break> tags now)
    text_match = re.search(r'<prosody[^>]*>(.*?)</prosody>', ssml_string, re.DOTALL)
    
    rate = rate_match.group(1) if rate_match else "+0%"
    pitch = pitch_match.group(1) if pitch_match else "+0Hz"
    volume = volume_match.group(1) if volume_match else "+0%"
    voice = voice_match.group(1) if voice_match else "en-US-AriaNeural"
    text = text_match.group(1).strip() if text_match else ""
    
    # Monkey-patch the escape function so our <break> tags are preserved in the text block
    orig_esc = edge_tts.communicate.escape
    orig_rm = getattr(edge_tts.communicate, 'remove_incompatible_characters', lambda x: x)
    
    try:
        edge_tts.communicate.escape = lambda x: x
        if hasattr(edge_tts.communicate, 'remove_incompatible_characters'):
            edge_tts.communicate.remove_incompatible_characters = lambda x: x
            
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
    finally:
        edge_tts.communicate.escape = orig_esc
        if hasattr(edge_tts.communicate, 'remove_incompatible_characters'):
            edge_tts.communicate.remove_incompatible_characters = orig_rm
