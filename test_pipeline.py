from emotion import EmotionAnalyzer
from voice_mapper import map_params
from ssml_builder import build_ssml
from tts_engine import generate_mp3_from_ssml
import os

print("Testing Pipeline...")
try:
    analyzer = EmotionAnalyzer()
    text = "THIS IS INCREDIBLE!"
    res = analyzer.analyze(text)
    print("Emotion Analysis:", res)
    
    params = map_params(res['top_emotion'], res['intensity'])
    print("Voice Params:", params)
    
    ssml = build_ssml(text, params)
    print("SSML Payload Length:", len(ssml))
    print(ssml)
    
    output_path = "test_output.mp3"
    generate_mp3_from_ssml(ssml, output_path)
    
    if os.path.exists(output_path):
        print(f"Success! Output generated at {output_path}")
        os.remove(output_path)
    else:
        print("Failed to generate output")
        
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error:", str(e))
