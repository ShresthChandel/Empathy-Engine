import asyncio
import edge_tts

async def test_express_as():
    # We'll use edge_tts with direct text injection
    text = "<mstts:express-as style='sad' role='Girl'>I am feeling so sad today.</mstts:express-as>"
    comm = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
    await comm.save("express_as.mp3")

asyncio.run(test_express_as())
