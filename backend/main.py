import gradio as gr
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model.speech_processor import SpeechProcessor
from model.vocabulary_analyzer import VocabularyAnalyzer
from model.pronunciation_analyzer import PronunciationAnalyzer
from utils.report_generator import ReportGenerator
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import logging
from pydub import AudioSegment
import io
import subprocess
import base64

app = Flask(__name__)
CORS(app)

# Add root route
@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Communication Assessment API is running",
        "endpoints": {
            "process_text": "/api/process-text",
            "process_audio": "/api/process-audio"
        }
    })

# Add error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not found",
        "message": "The requested resource does not exist"
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500

class CommunicationAssessmentApp:
    def __init__(self):
        self.speech_processor = SpeechProcessor()
        self.vocabulary_analyzer = VocabularyAnalyzer()
        self.pronunciation_analyzer = PronunciationAnalyzer()
        self.report_generator = ReportGenerator()

    def create_radar_chart(self, scores):
        """Create interactive radar chart using plotly"""
        categories = ['Pronunciation', 'Grammar', 'Vocabulary', 'Fluency']
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Skills Assessment'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Communication Skills Assessment"
        )
        return fig

    def create_vocabulary_chart(self, vocab_data):
        """Create interactive bar chart for vocabulary metrics"""
        metrics = ['Lexical Diversity', 'Sophistication', 'Context Score']
        values = [
            vocab_data['lexical_diversity'],
            vocab_data['sophistication'],
            vocab_data['context_appropriateness']
        ]
        
        fig = px.bar(
            x=metrics,
            y=values,
            title="Vocabulary Analysis",
            labels={'x': 'Metrics', 'y': 'Score'},
            color=values,
            color_continuous_scale='viridis'
        )
        return fig

    def process_input(self, audio_file):
        """Process audio input and return comprehensive analysis"""
        if audio_file is None:
            return [("Grammar Analysis:", "Please provide an audio input."), 
                   ("Grammar Score:", "0.00")], [("", "")], None, None, None, ""

        try:
            # Get transcribed text and initial feedback (optimized with async)
            chat_history = self.speech_processor.process_audio(audio_file)
            transcribed_text = chat_history[0][1]

            # Parallel processing of analyses
            vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(transcribed_text)
            pron_analysis = self.pronunciation_analyzer.analyze_pronunciation(audio_file)

            # Calculate grammar score more accurately
            grammar_issues = chat_history[1][1]
            grammar_corrections = chat_history[2][1]
            
            # Force a non-zero grammar score based on the corrections
            if "No major issues found" in grammar_issues:
                grammar_score = 0.95  # High score for no issues
                issue_count = 0
            else:
                # Count issues by splitting on commas
                issue_list = [issue.strip() for issue in grammar_issues.split(',') if issue.strip()]
                issue_count = len(issue_list)
                
                # Calculate score based on issue count and text length
                words_count = len(transcribed_text.split())
                if words_count > 0:
                    # Normalize by text length (longer text can have more issues)
                    normalized_issues = min(issue_count / (words_count / 10), 1.0)
                    grammar_score = max(0.1, 1.0 - normalized_issues)
                else:
                    grammar_score = 0.1  # Minimum score
            
            # Calculate overall scores
            scores = [
                pron_analysis['pronunciation_score'],
                grammar_score,  # Improved grammar score
                vocab_analysis['lexical_diversity'],
                pron_analysis['fluency_score']
            ]

            # Create visualizations
            radar_chart = self.create_radar_chart(scores)
            vocab_chart = self.create_vocabulary_chart(vocab_analysis)

            # Format the complete response - split into two parts for UI
            # Remove transcription from language analysis
            language_analysis = [
                ("Grammar Analysis:", chat_history[2][1]),
                ("Grammar Score:", f"{grammar_score:.2f}")
            ]
            
            performance_analysis = [
                ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nHigh-Quality Complex Words: {', '.join(vocab_analysis['unique_words']) if vocab_analysis['unique_words'] else 'None detected'}"),
                ("Pronunciation Score:", f"{pron_analysis['pronunciation_score']:.2f}"),
                ("Improvement Suggestion:", chat_history[3][1])
            ]

            # Create a formatted report for the report_box
            report_text = f"""Communication Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL SCORES
Pronunciation: {pron_analysis['pronunciation_score']:.2f}
Grammar: {grammar_score:.2f}
Vocabulary: {vocab_analysis['lexical_diversity']:.2f}
Fluency: {pron_analysis['fluency_score']:.2f}

KEY FINDINGS
• Grammar: {issue_count} issues found
• Complex Words Used: {len(vocab_analysis['unique_words'])}
• Pronunciation Quality: {'Excellent' if pron_analysis['pronunciation_score'] > 0.8 else 'Good' if pron_analysis['pronunciation_score'] > 0.6 else 'Needs Improvement'}
• Speech Fluency: {'Excellent' if pron_analysis['fluency_score'] > 0.8 else 'Good' if pron_analysis['fluency_score'] > 0.6 else 'Needs Improvement'}
"""

            return language_analysis, performance_analysis, radar_chart, vocab_chart, transcribed_text, report_text

        except Exception as e:
            print(f"Error in process_input: {str(e)}")
            return [("Grammar Analysis:", "Error occurred"), 
                   ("Grammar Score:", "0.00")], [("Error:", "Analysis failed")], None, None, None, "Error generating report"

    def process_text(self, text):
        """Process text input and return analysis"""
        try:
            # Get initial feedback
            chat_history = self.speech_processor.process_text(text)
            
            # Parallel processing of analyses
            vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(text)
            
            # Calculate grammar score
            grammar_issues = chat_history[1][1]
            grammar_corrections = chat_history[2][1]
            
            if "No major issues found" in grammar_issues:
                grammar_score = 0.95
                issue_count = 0
            else:
                issue_list = [issue.strip() for issue in grammar_issues.split(',') if issue.strip()]
                issue_count = len(issue_list)
                words_count = len(text.split())
                if words_count > 0:
                    normalized_issues = min(issue_count / (words_count / 10), 1.0)
                    grammar_score = max(0.1, 1.0 - normalized_issues)
                else:
                    grammar_score = 0.1
            
            # Calculate overall scores
            scores = [
                0.0,  # No pronunciation score for text
                grammar_score,
                vocab_analysis['lexical_diversity'],
                0.0   # No fluency score for text
            ]

            # Create visualizations
            radar_chart = self.create_radar_chart(scores)
            vocab_chart = self.create_vocabulary_chart(vocab_analysis)

            return {
                'language_analysis': [
                    ("Grammar Analysis:", chat_history[2][1]),
                    ("Grammar Score:", f"{grammar_score:.2f}")
                ],
                'performance_analysis': [
                    ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nHigh-Quality Complex Words: {', '.join(vocab_analysis['unique_words']) if vocab_analysis['unique_words'] else 'None detected'}"),
                    ("Improvement Suggestion:", chat_history[3][1])
                ],
                'transcribed_text': text,
                'report': f"""Communication Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL SCORES
Grammar: {grammar_score:.2f}
Vocabulary: {vocab_analysis['lexical_diversity']:.2f}

KEY FINDINGS
• Grammar: {issue_count} issues found
• Complex Words Used: {len(vocab_analysis['unique_words'])}
""",
                'charts': {
                    'radar': radar_chart.to_json() if radar_chart else None,
                    'vocabulary': vocab_chart.to_json() if vocab_chart else None
                }
            }
        except Exception as e:
            print(f"Error in process_text: {str(e)}")
            raise

    def create_interface(self):
        """Create and return the Gradio interface"""
        interface = gr.Blocks(title="Communication Assessment Tool", theme="soft")

        with interface:
            gr.Markdown("# 🎯 Communication Assessment Tool")
            gr.Markdown("Upload an audio file or record your speech for comprehensive analysis")

            with gr.Row():
                with gr.Column(scale=1):
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Audio Input"
                    )
                    transcription = gr.Textbox(
                        label="Transcribed Text",
                        interactive=False
                    )

            with gr.Row():
                with gr.Column(scale=1):
                    language_chatbot = gr.Chatbot(
                        label="Language Analysis",
                        height=500
                    )
                    performance_chatbot = gr.Chatbot(
                        label="Performance Analysis",
                        height=500
                    )
                with gr.Column(scale=1):
                    radar_plot = gr.Plot(label="Skills Assessment")
                    vocab_plot = gr.Plot(label="Vocabulary Analysis")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Hide the Communication Assessment Report title since it's already in the content
                    report_box = gr.Textbox(
                        label="Assessment Summary",
                        interactive=False,
                        lines=15
                    )

            audio_input.change(
                fn=self.process_input,
                inputs=[audio_input],
                outputs=[language_chatbot, performance_chatbot, radar_plot, vocab_plot, transcription, report_box]
            )

        return interface

    @app.route('/api/process-text', methods=['POST', 'OPTIONS'])
    def process_text_api():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response

        try:
            print("Received request data:", request.data)
            data = request.get_json()
            print("Parsed JSON data:", data)
            
            if not data or 'text' not in data:
                print("Missing text in request")
                return jsonify({'error': 'No text provided'}), 400

            text = data.get('text')
            if not text or not isinstance(text, str):
                print(f"Invalid text format: {type(text)}")
                return jsonify({'error': 'Invalid text format'}), 400

            assessment_app = CommunicationAssessmentApp()
            result = assessment_app.process_text(text)
            print("Processing result:", result)  # Add this debug line
            return jsonify(result)

        except Exception as e:
            import traceback
            print(f"Error in process_text_api: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    @app.route('/api/process-speech', methods=['POST', 'OPTIONS'])
    def process_speech_api():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response

        webm_path = None
        wav_path = None

        try:
            if 'audio' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio']
            if not audio_file:
                return jsonify({'error': 'Empty file'}), 400

            # Save the file temporarily
            temp_path = 'temp_audio'
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)
            
            # Save original WebM file
            webm_path = os.path.join(temp_path, 'temp_audio.webm')
            wav_path = os.path.join(temp_path, 'temp_audio.wav')
            
            audio_file.save(webm_path)
            
            try:
                # Convert WebM to WAV using ffmpeg
                command = [
                    'ffmpeg',
                    '-i', webm_path,
                    '-acodec', 'pcm_s16le',
                    '-ar', '16000',
                    '-ac', '1',
                    '-y',  # Overwrite output file if it exists
                    wav_path
                ]
                
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    print(f"FFmpeg error: {stderr.decode()}")
                    raise ValueError("Failed to convert audio format")

                if not os.path.exists(wav_path):
                    raise ValueError("WAV file was not created")

                # Process the audio
                assessment_app = CommunicationAssessmentApp()
                chat_history = assessment_app.speech_processor.process_audio(wav_path)
                
                if not chat_history or len(chat_history) < 4:
                    raise ValueError("Invalid speech processing result")

                transcribed_text = chat_history[0][1]  # Get transcribed text
                
                # Get vocabulary analysis
                vocab_analysis = assessment_app.vocabulary_analyzer.analyze_vocabulary(transcribed_text)
                
                # Calculate grammar score
                grammar_issues = chat_history[1][1]
                if "No major issues found" in grammar_issues:
                    grammar_score = 0.95
                    issue_count = 0
                else:
                    issue_list = [issue.strip() for issue in grammar_issues.split(',') if issue.strip()]
                    issue_count = len(issue_list)
                    words_count = len(transcribed_text.split())
                    if words_count > 0:
                        normalized_issues = min(issue_count / (words_count / 10), 1.0)
                        grammar_score = max(0.1, 1.0 - normalized_issues)
                    else:
                        grammar_score = 0.1

                # Create visualizations
                scores = [
                    0.7,  # Placeholder pronunciation score
                    grammar_score,
                    vocab_analysis['lexical_diversity'],
                    0.8,  # Placeholder fluency score
                ]

                radar_chart = assessment_app.create_radar_chart(scores)
                vocab_chart = assessment_app.create_vocabulary_chart(vocab_analysis)

                # Convert charts to base64
                try:
                    # Radar chart
                    radar_buffer = io.BytesIO()
                    radar_chart.write_image(radar_buffer, format='png')
                    radar_base64 = base64.b64encode(radar_buffer.getvalue()).decode('utf-8')
                    radar_buffer.close()

                    # Vocabulary chart
                    vocab_buffer = io.BytesIO()
                    vocab_chart.write_image(vocab_buffer, format='png')
                    vocab_base64 = base64.b64encode(vocab_buffer.getvalue()).decode('utf-8')
                    vocab_buffer.close()
                except Exception as e:
                    print(f"Error converting charts to base64: {str(e)}")
                    radar_base64 = None
                    vocab_base64 = None

                result = {
                    'language_analysis': [
                        ("Grammar Analysis:", chat_history[2][1]),
                        ("Grammar Score:", f"{grammar_score:.2f}")
                    ],
                    'performance_analysis': [
                        ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nHigh-Quality Complex Words: {', '.join(vocab_analysis['unique_words']) if vocab_analysis['unique_words'] else 'None detected'}"),
                        ("Improvement Suggestion:", chat_history[3][1])
                    ],
                    'transcribed_text': transcribed_text,
                    'report': f"""Communication Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TRANSCRIPTION:
{transcribed_text}

OVERALL SCORES
Grammar: {grammar_score:.2f}
Vocabulary: {vocab_analysis['lexical_diversity']:.2f}

KEY FINDINGS
• Grammar: {issue_count} issues found
• Complex Words Used: {len(vocab_analysis['unique_words'])}
""",
                    'charts': {
                        'radar': radar_base64,
                        'vocabulary': vocab_base64
                    }
                }

            except Exception as e:
                print(f"Error processing audio: {str(e)}")
                raise

        except Exception as e:
            import traceback
            print(f"Error in process_speech_api: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

        finally:
            # Clean up temp files
            try:
                if webm_path and os.path.exists(webm_path):
                    os.remove(webm_path)
                if wav_path and os.path.exists(wav_path):
                    os.remove(wav_path)
            except Exception as e:
                print(f"Error cleaning up temp files: {str(e)}")

        return jsonify(result)

def main():
    multiprocessing.freeze_support()
    # Add more detailed logging
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main() 