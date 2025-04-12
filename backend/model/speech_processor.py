import torch
from transformers import pipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from groq import Groq
from textblob import TextBlob
from dotenv import load_dotenv
import os
import re
from concurrent.futures import ThreadPoolExecutor
from .scoring_analyzer import ScoringAnalyzer

load_dotenv()

class SpeechProcessor:
    def __init__(self):
        # Use Faster-Whisper instead of regular Whisper
        try:
            from faster_whisper import WhisperModel
            # Use tiny model for faster processing
            self.speech_recognizer = WhisperModel("tiny", device="cpu", compute_type="int8")
        except ImportError:
            # Fallback to regular whisper with tiny model if faster-whisper not installed
            self.speech_recognizer = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-tiny",
                chunk_length_s=30
            )
            
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.grammar_checker = self._initialize_grammar_model()
        self.scoring_analyzer = ScoringAnalyzer()

    def _initialize_grammar_model(self):
        """Initialize a better grammar checker model"""
        try:
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
            return None

    def transcribe_audio(self, audio_file):
        """Transcribe audio using Faster-Whisper"""
        try:
            if hasattr(self.speech_recognizer, 'transcribe'):
                # Using Faster-Whisper
                segments, _ = self.speech_recognizer.transcribe(
                    audio_file,
                    language="en",
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500)
                )
                return " ".join([seg.text for seg in segments])
            else:
                # Using regular Whisper
                result = self.speech_recognizer(
                    audio_file,
                    language="en",
                    return_timestamps=False
                )
                return result["text"]
                
        except Exception as e:
            print(f"Error in transcribe_audio: {str(e)}")
            return ""

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
        """Process audio input and return comprehensive analysis"""
        try:
            if not audio_file:
                return [("Error:", "No audio file provided")]

            # Get transcription
            text = self.transcribe_audio(audio_file)
            
            if not text:
                return [("Error:", "Could not transcribe audio")]

            return self._process_input(text)

        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            return [("Error:", "An error occurred while processing the audio")]

    def process_text(self, text):
        """Process text input and return comprehensive analysis"""
        try:
            if not text:
                return [("Error:", "No text provided")]
            
            return self._process_input(text)
        
        except Exception as e:
            print(f"Error in process_text: {str(e)}")
            return [("Error:", "An error occurred while processing the text")]

    def _process_input(self, text):
        """Common processing logic for both text and speech input"""
        try:
            # Get comprehensive analysis
            scores = self.scoring_analyzer.analyze_text(text)
            mistakes, grammar_feedback = self.analyze_text(text)
            chatbot_feedback = self.get_groq_feedback(text)
            interview_questions = self.generate_interview_questions(text)

            # Extract vocabulary data from the analysis (passed from analyze_text)
            vocab_data = scores.get('vocab_data', {})

            # Debug print
            print("Scores generated:", scores)
            print("Detailed feedback:", scores['detailed_feedback'])

            # Format detailed feedback
            detailed_feedback = scores['detailed_feedback']
            if mistakes:
                detailed_feedback.append(f"Specific issues: {', '.join(mistakes)}")

            # Build the final result (include vocabulary scores and metrics)
            result = [
                ("Input:", text),
                ("Grammar Analysis:", grammar_feedback),
                ("Corrected Version:", self.grammar_checker(text)[0]['generated_text'] if self.grammar_checker else text),
                ("Scores:", f"""Grammar: {scores['grammar_score']:.2f}
    Vocabulary: {scores['vocabulary_score']:.2f}
    Fluency: {scores['fluency_score']:.2f}
    Coherence: {scores['coherence_score']:.2f}
    Overall: {scores['overall_score']:.2f}"""),
                ("Detailed Feedback:", "\n".join(detailed_feedback)),
                ("Improvement Suggestion:", chatbot_feedback),
                ("Interview Questions:", "\n".join(f"{i+1}. {q}" for i, q in enumerate(interview_questions))),
                ("Vocabulary Analysis:", vocab_data)
            ]

            # Debug print
            print("Final formatted result:", result)
            return result

        except Exception as e:
            print(f"Error in _process_input: {str(e)}")
            return [
                ("Input:", text),
                ("Error:", "Analysis failed"),
                ("Corrected Version:", text),
                ("Scores:", "Unable to calculate scores"),
                ("Detailed Feedback:", "Analysis failed"),
                ("Improvement Suggestion:", "Unable to generate suggestions"),
                ("Interview Questions:", "Unable to generate questions")
            ]

    def generate_interview_questions(self, text):
        """Generate one contextual follow-up question based on the input"""
        try:
            prompt = f"""Based on this statement: "{text}"
            
            Act as an expert interviewer. Using chain-of-thought:
            1. First, identify the key topics and expertise mentioned
            2. Then, consider what deeper knowledge should be tested
            3. Finally, generate 1 intelligent follow-up question that:
               - Tests both knowledge and practical application
               - Encourages a detailed response
               - Stays relevant to the context
               - Focuses on the most important aspect mentioned
            
            Format: Return only the question, no other text.
            """

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer who generates one insightful, context-aware question."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_completion_tokens=256,
                top_p=1,
                stream=False
            )
            
            # Extract and format the question
            question = response.choices[0].message.content.strip()
            # Clean up any numbering or extra spaces
            question = question.lstrip('0123456789.)-] ')
            
            return [question]  # Return as list for consistency with existing code

        except Exception as e:
            print(f"Error generating interview question: {str(e)}")
            return ["Unable to generate a follow-up question at this time."] 