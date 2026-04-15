from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid
from emotion import EmotionAnalyzer
from voice_mapper import map_params
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
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    if not analyzer:
        return jsonify({"error": "AI Model not initialized"}), 500

    # 1. Analyze text mapping to 7 emotions + intensity scalar
    analysis = analyzer.analyze(text)
    
    # 2. Map emotion and intensity to prosody traits
    params = map_params(analysis["top_emotion"], analysis["intensity"])
    
    # 3. Build literal SSML XML payload
    ssml = build_ssml(text, params)
    
    # 4. Generate TTS via engine consuming exactly the SSML text
    os.makedirs(os.path.join(app.root_path, "static"), exist_ok=True)
    filename = f"output_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(app.root_path, "static", filename)
    
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
