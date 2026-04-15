import re
import asyncio
import edge_tts

def generate_mp3_from_ssml(ssml_string: str, output_path: str):
    """
    Consumes an SSML string directly and streams it to Edge-TTS.
    This unlocks native SSML capacities (breaks, emphasis, phonetics) 
    without recreating parameters manually.
    """
    async def _generate():
        # Some edge_tts versions detect SSML automatically if it begins with <speak
        comm = edge_tts.Communicate(text=ssml_string)
        await comm.save(output_path)
        
    # Execute the asynchronous generation
    asyncio.run(_generate())
