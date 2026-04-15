# The Empathy Engine 🎙️🧠

Giving AI a Human Voice. \
The Empathy Engine is a responsive, emotionally-intelligent Text-to-Speech (TTS) pipeline designed to bridge the uncanny valley. Instead of robotic, monolithic speech, this service analyzes the granular emotion and intensity of text to dynamically manipulate vocal prosody (pitch, rate, and volume)—producing highly expressive, human-like audio.

## 🌟 Key Features (The "Wow" Factors)
* **7-Class Emotion Model**: Uses `j-hartmann/emotion-english-distilroberta-base` locally to detect joy, anger, fear, disgust, sadness, surprise, and neutral (far beyond simple positive/negative analysis).
* **Continuous Intensity Interpolation**: It does not just switch between a "happy" or "sad" voice. By feeding the text through VADER sentiment analysis, combined with punctuation and capitalization heuristics, it calculates a 0.0 to 1.0 multiplier. "This is nice" gets a slight pitch shift; "THIS IS INCREDIBLE!!!" receives massive modulation.
* **SSML Prosody Control**: The engine crafts strict, dynamic XML Speech Synthesis Markup Language (SSML) payload strings that dictate how the Edge-TTS neural voices pronounce the text.
* **Real-time UI Visualization**: A Flask-served web UI leveraging Chart.js allows users to see exactly how confident the model is across all 7 emotions side-by-side with the synthesized audio player.

---

## 🏗️ Design Choices: Emotion to Voice Mapping

To ensure realistic emotional resonance, vocal parameter changes were mapped scientifically:

1. **Emotion Detection**: The text is evaluated, and a `top_emotion` is identified along with its respective confidence scores.
2. **Intensity Calculation**: VADER sentiment compound score computes absolute magnitude. Additional heuristics (All-caps strings over 3 characters, volume of exclamation points) are added to reach an `intensity` scalar of 0.0 to 1.0.
3. **The Voice Mapping Lexicon**:
    * **Joy**: Bound to faster rate, higher pitch, louder volume.
    * **Sadness**: Bound to much slower rate, lower pitch, softer volume.
    * **Fear**: Bound to significantly faster rate, higher pitch, but heavily reduced volume.
    * **Anger**: Bound to fast rate, high pitch, and massively boosted volume.
4. **Interpolation Math**: If Anger's base maximum rate is `+25%`, and the VADER intensity scores `0.6` (moderately angry), the system scales the parameter: `25 * 0.6 = +15% rate`. This avoids awkward jumps and preserves natural human boundaries.

---

## 🚀 Setup & Execution

Everything runs 100% locally and free. No API keys are required.

### 1. Prerequisites
Make sure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/ShresthChandel/Empathy-Engine.git
cd Empathy-Engine

# It is recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Running the Engine
Start up the Flask server:
```bash
python app.py
```
After the server boots, visit exactly **`http://127.0.0.1:5000`** in your browser to interact with the engine.

> **Note**: On the very first input, the HuggingFace zero-shot classification model (~320mb) will automatically download locally to your machine. This might take 10-15 seconds. All subsequent syntheses will be practically instantaneous!
