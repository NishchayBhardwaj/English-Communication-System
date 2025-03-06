import speech_recognition as sr
from groq import Groq
from transformers import pipeline
from textblob import TextBlob
from dotenv import load_dotenv
import os

load_dotenv()

class SpeechProcessor:
    def __init__(self):
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.grammar_checker = self._initialize_model()
        self.recognizer = sr.Recognizer()

    def _initialize_model(self):
        """Initialize the grammar checker model"""
        return pipeline("text2text-generation", 
                      model="prithivida/grammar_error_correcter_v1",
                      device="cpu")

    def get_groq_feedback(self, text):
        """Send user speech to Groq chatbot for better phrasing suggestions"""
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Provide real-time speaking improvement suggestions. Instead of 'I would like to say', use 'I prefer to'. Keep responses concise."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False
        )
        return response.choices[0].message.content

    def analyze_text(self, text):
        """Analyze text for grammar mistakes and spelling errors"""
        corrected_text = self.grammar_checker(text, max_length=100)[0]["generated_text"]
        
        # Highlight grammar/spelling mistakes using TextBlob
        blob = TextBlob(text)
        mistakes = []
        for word, tag in blob.tags:
            if tag in ["NN", "VB", "JJ"] and word.lower() not in corrected_text.lower():
                mistakes.append(word)

        return mistakes, corrected_text

    def process_audio(self, audio_file):
        """Process audio file and return analysis results"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                
                # Get all analyses
                chatbot_feedback = self.get_groq_feedback(text)
                mistakes, grammar_feedback = self.analyze_text(text)
                
                # Format the response
                chat_history = [
                    ("You said:", text),
                    ("Grammar Issues:", f"Potential mistakes in: {', '.join(mistakes) if mistakes else 'No major issues found'}"),
                    ("Corrected Version:", grammar_feedback),
                    ("Improvement Suggestion:", chatbot_feedback)
                ]
                
                return chat_history
                
        except Exception as e:
            return [("Error processing audio:", str(e))] 