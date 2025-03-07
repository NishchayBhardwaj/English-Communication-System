# import speech_recognition as sr
# import time
# import os
# import gradio as gr
# from groq import Groq
# from transformers import pipeline
# from textblob import TextBlob
# from termcolor import colored
# from dotenv import load_dotenv
# import multiprocessing

# load_dotenv()

# groq_api_key=os.environ.get("GROQ_API_KEY")

# # Set up Groq API client
# client = Groq(api_key=groq_api_key)

# def initialize_model():
#     """Initialize the grammar checker model"""
#     return pipeline("text2text-generation", 
#                    model="prithivida/grammar_error_correcter_v1",
#                    device="cpu")

# # Initialize NLP model for grammar and fluency analysis
# grammar_checker = None

# def get_groq_feedback(text):
#     """Send user speech to Groq chatbot for better phrasing suggestions"""
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": "Provide real-time speaking improvement suggestions. Instead of 'I would like to say', use 'I prefer to'. Keep responses concise."},
#             {"role": "user", "content": text}
#         ],
#         temperature=0.5,
#         max_completion_tokens=1024,
#         top_p=1,
#         stop=None,
#         stream=False
#     )
#     return response.choices[0].message.content

# def analyze_text(text):
#     """Analyze text for grammar mistakes and spelling errors"""
#     global grammar_checker
#     if grammar_checker is None:
#         grammar_checker = initialize_model()
        
#     corrected_text = grammar_checker(text, max_length=100)[0]["generated_text"]
    
#     # Highlight grammar/spelling mistakes using TextBlob
#     blob = TextBlob(text)
#     mistakes = []
#     for word, tag in blob.tags:
#         if tag in ["NN", "VB", "JJ"] and word.lower() not in corrected_text.lower():
#             mistakes.append(word)

#     return mistakes, corrected_text

# def process_audio(audio_file):
#     """Process audio file and return analysis results"""
#     if audio_file is None:
#         return [("Please provide an audio input.", "")]
    
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.AudioFile(audio_file) as source:
#             audio = recognizer.record(source)
#             text = recognizer.recognize_google(audio)
            
#             # Get all analyses
#             chatbot_feedback = get_groq_feedback(text)
#             mistakes, grammar_feedback = analyze_text(text)
            
#             # Format the response for the chatbot
#             chat_history = [
#                 ("You said:", text),
#                 ("Grammar Issues:", f"Potential mistakes in: {', '.join(mistakes) if mistakes else 'No major issues found'}"),
#                 ("Corrected Version:", grammar_feedback),
#                 ("Improvement Suggestion:", chatbot_feedback)
#             ]
            
#             return chat_history
            
#     except Exception as e:
#         return [("Error processing audio:", str(e))]

# def create_gradio_interface():
#     """Create and launch the Gradio interface"""
#     with gr.Blocks(title="Speech Analysis Assistant") as interface:
#         gr.Markdown("# Speech Analysis Assistant")
#         gr.Markdown("Upload an audio file or record your speech for analysis")
        
#         with gr.Row():
#             audio_input = gr.Audio(
#                 sources=["microphone", "upload"],
#                 type="filepath",
#                 label="Audio Input"
#             )
        
#         with gr.Row():
#             chatbot = gr.Chatbot(
#                 label="Analysis Results",
#                 height=400
#             )
        
#         audio_input.change(
#             fn=process_audio,
#             inputs=[audio_input],
#             outputs=[chatbot]
#         )
    
#     return interface

# if __name__ == "__main__":
#     # Add multiprocessing support for Windows
#     multiprocessing.freeze_support()
    
#     # Initialize the model at startup
#     grammar_checker = initialize_model()
    
#     # Create and launch the interface
#     interface = create_gradio_interface()
#     interface.launch(share=False, server_port=7860)
