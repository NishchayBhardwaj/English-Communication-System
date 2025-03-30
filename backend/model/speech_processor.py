import speech_recognition as sr
from groq import Groq
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from textblob import TextBlob
from dotenv import load_dotenv
import os
import re

load_dotenv()

class SpeechProcessor:
    def __init__(self):
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.grammar_checker = self._initialize_grammar_model()
        self.recognizer = sr.Recognizer()

    def _initialize_grammar_model(self):
        """Initialize a better grammar checker model"""
        try:
            # Use T5-based grammar correction model instead
            model_name = "vennify/t5-base-grammar-correction"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            return pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=512
            )
        except Exception as e:
            print(f"Error initializing grammar model: {str(e)}")
            # Fallback to the original model if the new one fails
            try:
                return pipeline("text2text-generation", 
                              model="prithivida/grammar_error_correcter_v1",
                              device="cpu")
            except:
                return None

    def get_groq_feedback(self, text):
        """Send user speech to Groq chatbot for better phrasing suggestions"""
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert English language coach specializing in sophisticated grammar and vocabulary. Analyze the provided speech for grammar issues and suggest more elegant, complex phrasing where appropriate. Focus on transforming basic expressions into more sophisticated ones. Keep responses concise and actionable."},
                    {"role": "user", "content": text}
                ],
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting Groq feedback: {str(e)}")
            return "Unable to generate feedback at this time."

    def analyze_text(self, text):
        """Analyze text for grammar mistakes and spelling errors"""
        try:
            if self.grammar_checker is None:
                return [], text

            # Generate corrected text
            corrected_text = self.grammar_checker(text, max_length=512)[0]["generated_text"]
            
            # Find specific grammar errors by comparing original and corrected text
            original_sentences = self._split_into_sentences(text)
            corrected_sentences = self._split_into_sentences(corrected_text)
            
            # Identify specific grammar issues
            mistakes = []
            for i, (orig, corr) in enumerate(zip(original_sentences, corrected_sentences)):
                if orig.strip().lower() != corr.strip().lower():
                    # Find specific differences
                    orig_words = orig.split()
                    corr_words = corr.split()
                    
                    # Check for word-level differences
                    for j, (o_word, c_word) in enumerate(zip(orig_words, corr_words)):
                        if o_word.lower() != c_word.lower():
                            context = " ".join(orig_words[max(0, j-2):min(len(orig_words), j+3)])
                            mistakes.append(f"'{o_word}' → '{c_word}' in '{context}'")
                    
                    # If no specific word differences found but sentences differ
                    if not any(m for m in mistakes if f"in '{orig}'" in m):
                        mistakes.append(f"Sentence structure: '{orig}' → '{corr}'")
            
            # If no specific issues found but text was corrected
            if not mistakes and text.lower() != corrected_text.lower():
                mistakes.append("General grammar and structure improvements")
                
            return mistakes, corrected_text
        except Exception as e:
            print(f"Error analyzing text: {str(e)}")
            return [], text
    
    def _split_into_sentences(self, text):
        """Split text into sentences more accurately"""
        # Simple sentence splitting - can be improved
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return sentences

    def process_audio(self, audio_file):
        """Process audio file and return analysis results"""
        try:
            if not audio_file:
                return [("Error:", "No audio file provided")]

            with sr.AudioFile(audio_file) as source:
                # Adjust for longer audio files
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                
                if not text:
                    return [("Error:", "Could not transcribe audio")]

                # Initialize default responses
                chat_history = [
                    ("You said:", text),
                    ("Grammar Issues:", "Analyzing..."),
                    ("Corrected Version:", "Processing..."),
                    ("Improvement Suggestion:", "Generating...")
                ]

                # Get analyses
                mistakes, grammar_feedback = self.analyze_text(text)
                chatbot_feedback = self.get_groq_feedback(text)
                
                # Update chat history with actual results
                chat_history = [
                    ("You said:", text),
                    ("Grammar Issues:", f"{', '.join(mistakes) if mistakes else 'No major issues found'}"),
                    ("Corrected Version:", grammar_feedback),
                    ("Improvement Suggestion:", chatbot_feedback)
                ]
                
                return chat_history
                
        except sr.UnknownValueError:
            return [("Error:", "Could not understand the audio")]
        except sr.RequestError as e:
            return [("Error:", f"Could not process audio; {str(e)}")]
        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            return [("Error:", "An error occurred while processing the audio")]

    def process_text(self, text):
        """Process text input and return feedback"""
        try:
            # Get grammar analysis
            mistakes, corrected_text = self.analyze_text(text)
            
            # Get improvement suggestions from Groq
            chatbot_feedback = self.get_groq_feedback(text)
            
            return [
                ("Transcription:", text),
                ("Grammar Issues:", ", ".join(mistakes) if mistakes else "No major issues found"),
                ("Corrected Version:", corrected_text),
                ("Improvement Suggestion:", chatbot_feedback)
            ]
        except Exception as e:
            print(f"Error in process_text: {str(e)}")
            return [
                ("Transcription:", text),
                ("Grammar Issues:", "Error analyzing grammar"),
                ("Corrected Version:", text),
                ("Improvement Suggestion:", "Unable to generate suggestions")
            ] 