import re
import asyncio
import edge_tts

def generate_mp3_from_ssml(ssml_string: str, output_path: str):
    """
    Consumes an SSML string, extracts the parameters securely, and uses edge-tts Native Python API 
    to generate the .mp3 file without subprocess pathing issues.
    """
    # Extract SSML attributes using Regex
    rate_match = re.search(r'rate="([^"]+)"', ssml_string)
    pitch_match = re.search(r'pitch="([^"]+)"', ssml_string)
    volume_match = re.search(r'volume="([^"]+)"', ssml_string)
    
    # Extract the text payload
    text_match = re.search(r'<prosody[^>]*>(.*?)</prosody>', ssml_string, re.DOTALL)
    
    rate = rate_match.group(1) if rate_match else "+0%"
    pitch = pitch_match.group(1) if pitch_match else "+0Hz"
    volume = volume_match.group(1) if volume_match else "+0%"
    text = text_match.group(1).strip() if text_match else ""
    
    async def _generate():
        comm = edge_tts.Communicate(
            text=text, 
            voice="en-US-AriaNeural",
            rate=rate, 
            pitch=pitch, 
            volume=volume
        )
        await comm.save(output_path)
        
    # Execute the asynchronous generation
    asyncio.run(_generate())
