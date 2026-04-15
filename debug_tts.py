import asyncio
from tts_engine import generate_mp3_from_ssml

ssml = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <prosody rate="-14%" pitch="-10Hz" volume="-14%">
            I felt bad that you lost your earrings <break time="700ms"/>
        </prosody>
    </voice>
</speak>"""

print("Running...")
generate_mp3_from_ssml(ssml, "debug2.mp3")
print("Done!")
