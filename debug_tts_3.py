import asyncio
import edge_tts
import edge_tts.communicate

async def test_ssml():
    orig_esc = edge_tts.communicate.escape
    orig_rm = getattr(edge_tts.communicate, 'remove_incompatible_characters', lambda x: x)
    
    try:
        edge_tts.communicate.escape = lambda x: x
        if hasattr(edge_tts.communicate, 'remove_incompatible_characters'):
            edge_tts.communicate.remove_incompatible_characters = lambda x: x
            
        # We manually close the prosody tag, inject break, and reopen an empty prosody tag so mkssml closing tag matches it!
        text = "hello </prosody><break time='700ms'/><prosody pitch='+0Hz' rate='+0%' volume='+0%'> world"
        comm = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
        await comm.save("debug4.mp3")
        print("SUCCESS")
    except Exception as e:
        print("ERROR:", e)
    finally:
        edge_tts.communicate.escape = orig_esc
        if hasattr(edge_tts.communicate, 'remove_incompatible_characters'):
            edge_tts.communicate.remove_incompatible_characters = orig_rm

asyncio.run(test_ssml())
