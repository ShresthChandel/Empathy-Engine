from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid
from emotion import EmotionAnalyzer
from voice_mapper import map_params, get_dynamic_voice, apply_lexical_padding
from ssml_builder import build_ssml
from tts_engine import generate_mp3_from_ssml

app = Flask(__name__)

print("Starting Empathy Engine...")
try:
    analyzer = EmotionAnalyzer()
except Exception as e:
    print(f"Warning: Model failed to load. Provide text to see error. {e}")
    analyzer = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json()
    text = data.get("text", "").strip()
    voice_name = data.get("voice", "en-US-AriaNeural")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    if not analyzer:
        return jsonify({"error": "AI Model not initialized"}), 500

    # 1. Analyze text mapping to 7 emotions + intensity scalar
    analysis = analyzer.analyze(text)
    
    # 2. Map emotion and intensity to prosody traits
    top_emotion = analysis["top_emotion"]
    intensity = analysis["intensity"]
    
    if voice_name == "auto":
        voice_name = get_dynamic_voice(top_emotion)
        
    text = apply_lexical_padding(text, top_emotion, intensity)
    
    params = map_params(top_emotion, intensity)
    
    # 3. Build literal SSML XML payload
    ssml = build_ssml(text, params, voice_name=voice_name)
    
    # 4. Generate TTS via engine consuming exactly the SSML text
    static_dir = os.path.join(app.root_path, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    import glob
    for old_file in glob.glob(os.path.join(static_dir, "output_*.mp3")):
        try:
            os.remove(old_file)
        except:
            pass
            
    filename = f"output_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(static_dir, filename)
    
    try:
        generate_mp3_from_ssml(ssml, filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status": "success",
        "analysis": analysis,
        "vocal_parameters": params,
        "ssml_payload": ssml,
        "audio_url": url_for('static', filename=filename)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
