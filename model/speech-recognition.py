import speech_recognition as sr
import time
import os
from groq import Groq
from transformers import pipeline
from textblob import TextBlob
from termcolor import colored
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.environ.get("GROQ_API_KEY")

# Set up Groq API client
client = Groq(api_key=groq_api_key)

# Initialize NLP model for grammar and fluency analysis
grammar_checker = pipeline("text2text-generation", model="facebook/bart-large-cnn")

def get_groq_feedback(text):
    """Send user speech to Groq chatbot for better phrasing suggestions"""
    response = client.chat.completions.create(
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

def analyze_text(text):
    """Analyze text for grammar mistakes and spelling errors"""
    corrected_text = grammar_checker(text, max_length=100)[0]["generated_text"]
    
    # Highlight grammar/spelling mistakes using TextBlob
    blob = TextBlob(text)
    highlighted_text = ""
    for word, tag in blob.tags:
        if tag in ["NN", "VB", "JJ"] and word.lower() not in corrected_text.lower():
            highlighted_text += colored(word, "red") + " "
        else:
            highlighted_text += word + " "

    return highlighted_text.strip(), corrected_text

def recognize_speech():
    """Continuously recognize speech and provide feedback"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Start speaking about a topic... (Press Ctrl+C to stop)")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("\nListening for 10 seconds... Speak now.")
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

                # Get chatbot's improvement feedback
                chatbot_feedback = get_groq_feedback(text)
                print(colored(f"Chatbot Suggestion: {chatbot_feedback}", "yellow"))

                # Get NLP-based grammar feedback
                highlighted_text, grammar_feedback = analyze_text(text)
                print(colored(f"Grammar Issues: {highlighted_text}", "red"))
                print(colored(f"Corrected Version: {grammar_feedback}", "green"))

            except sr.UnknownValueError:
                print(colored("Sorry, I couldn't understand.", "cyan"))
            except sr.RequestError as e:
                print(colored(f"Error with speech recognition: {e}", "cyan"))
            except sr.WaitTimeoutError:
                input(colored("No speech detected. Press Enter to activate listening again...", "cyan"))
            except KeyboardInterrupt:
                print(colored("Stopping...", "cyan"))
                break

if __name__ == "__main__":
    recognize_speech()
