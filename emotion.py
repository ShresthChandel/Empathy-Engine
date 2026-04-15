from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EmotionAnalyzer:
    def __init__(self):
        print("Loading 7-class emotion model (j-hartmann/emotion-english-distilroberta-base)...")
        # top_k=None returns all 7 classes with confidence scores
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
        self.vader = SentimentIntensityAnalyzer()
        print("Model loaded successfully")

    def analyze(self, text: str):
        # Form: [[{'label': 'joy', 'score': 0.8}, ...]]
        hf_results = self.classifier(text)[0]
        
        # Dictionary formatting
        emotions_dict = {item['label']: item['score'] for item in hf_results}
        top_emotion = max(emotions_dict, key=emotions_dict.get)
        
        # Intensity Interpolation (VADER + Punctuation)
        vader_scores = self.vader.polarity_scores(text)
        compound = abs(vader_scores['compound']) 
        
        # Bonus features logic
        exclamation_boost = min(text.count('!') * 0.15, 0.4)
        caps_boost = 0.2 if text.isupper() and len(text) > 3 else 0.0
        
        intensity = min(compound + exclamation_boost + caps_boost, 1.0)
        
        return {
            "top_emotion": top_emotion,
            "intensity": intensity,
            "all_scores": emotions_dict
        }
