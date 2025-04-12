import gradio as gr
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sklearn.tree import export_text
from model.speech_processor import SpeechProcessor
# from model.vocabulary_analyzer import VocabularyAnalyzer
# from model.pronunciation_analyzer import PronunciationAnalyzer
# from utils.report_generator import ReportGenerator
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import logging
import base64
from io import BytesIO
import base64
import tempfile
from pymongo import MongoClient
import matplotlib

matplotlib.use('Agg')

# Connect to MongoDB
MONGO_URI = "mongodb+srv://vaibhav22210180:gMnJlkXIweLe9AA1@cluster0.wye6h.mongodb.net/"

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
            "process_speech": "/api/process-speech"
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
        # self.vocabulary_analyzer = VocabularyAnalyzer()
        # self.pronunciation_analyzer = PronunciationAnalyzer()
        # self.report_generator = ReportGenerator()

    def create_radar_chart(self, scores_dict):
        """Create fast radar chart and return base64-encoded image for HTML embedding, with score labels shown."""
        categories = ['Grammar', 'Vocabulary', 'Fluency', 'Coherence']
        values = [
            scores_dict.get('Grammar', 0),
            scores_dict.get('Vocabulary', 0),
            scores_dict.get('Fluency', 0),
            scores_dict.get('Coherence', 0)
        ]

        values += values[:1]  # loop back to start
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        ax.plot(angles, values, linewidth=2, linestyle='solid', color='blue')
        ax.fill(angles, values, color='skyblue', alpha=0.4)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10, color='white')

        ax.set_yticklabels([])  # hide radial labels
        ax.set_ylim(0, 1)

        # Add score labels at each point
        for angle, value in zip(angles, values):
            ax.text(
                angle,
                value + 0.05,  # slightly offset from the point
                f"{value:.2f}",
                ha='center',
                va='center',
                fontsize=9,
                color='white',
                fontweight='bold'
            )

        buf = BytesIO()
        plt.tight_layout()
        fig.patch.set_facecolor('#1f2937')  # match Tailwind's bg-gray-900
        ax.set_facecolor('#1f2937')
        plt.savefig(buf, format='jpeg', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    def create_vocab_chart(self, vocab_data):
        """Create interactive bar chart for vocabulary metrics using matplotlib"""
        metrics = ['Lexical Diversity', 'Sophistication', 'Context Score']
        values = [
            vocab_data['lexical_diversity'],
            vocab_data['sophistication'],
            vocab_data['context_appropriateness']
        ]

        # Create a bar chart with matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(metrics, values, color='skyblue')
        
        # Adding score values on top of the bars
        for i, value in enumerate(values):
            ax.text(i, value + 0.02, f'{value:.2f}', ha='center', va='bottom', fontsize=12)

        ax.set_title("Vocabulary Analysis")
        ax.set_xlabel("Metrics")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1)

        # Convert the plot to a base64-encoded image for HTML embedding
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        vocab_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return vocab_base64

#     def process_input(self, audio_file):
#         MONGO_URI = "mongodb+srv://vaibhav22210180:gMnJlkXIweLe9AA1@cluster0.wye6h.mongodb.net/"  # Update with your MongoDB URI if hosted remotely
#         client = MongoClient(MONGO_URI)
#         db = client["communication_assessment"]  # Database Name
#         collection = db["queries"]  # Collection Name

#         """Process audio input and return comprehensive analysis"""
#         if audio_file is None:
#             return [("Grammar Analysis:", "Please provide an audio input."), 
#                    ("Grammar Score:", "0.00")], [("", "")], None, None, None, ""

#         try:
#             # Get transcribed text and initial feedback (optimized with async)
#             chat_history = self.speech_processor.process_audio(audio_file)
#             transcribed_text = chat_history[0][1]

#             # Parallel processing of analyses
#             vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(transcribed_text)
#             pron_analysis = self.pronunciation_analyzer.analyze_pronunciation(audio_file)

#             # Calculate grammar score more accurately
#             grammar_issues = chat_history[1][1]
#             grammar_corrections = chat_history[2][1]
            
#             # Force a non-zero grammar score based on the corrections
#             if "No major issues found" in grammar_issues:
#                 grammar_score = 0.95  # High score for no issues
#                 issue_count = 0
#             else:
#                 # Count issues by splitting on commas
#                 issue_list = [issue.strip() for issue in grammar_issues.split(',') if issue.strip()]
#                 issue_count = len(issue_list)
                
#                 # Calculate score based on issue count and text length
#                 words_count = len(transcribed_text.split())
#                 if words_count > 0:
#                     # Normalize by text length (longer text can have more issues)
#                     normalized_issues = min(issue_count / (words_count / 10), 1.0)
#                     grammar_score = max(0.1, 1.0 - normalized_issues)
#                 else:
#                     grammar_score = 0.1  # Minimum score
            
#             # Calculate overall scores
#             scores = [
#                 pron_analysis['pronunciation_score'],
#                 grammar_score,  # Improved grammar score
#                 vocab_analysis['lexical_diversity'],
#                 pron_analysis['fluency_score']
#             ]

#             # Create visualizations
#             radar_chart = self.create_radar_chart(scores)
#             vocab_chart = self.create_vocabulary_chart(vocab_analysis)

#             # Format the complete response - split into two parts for UI
#             # Remove transcription from language analysis
#             language_analysis = [
#                 ("Grammar Analysis:", chat_history[2][1]),
#                 ("Grammar Score:", f"{grammar_score:.2f}")
#             ]
            
#             performance_analysis = [
#                 ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nHigh-Quality Complex Words: {', '.join(vocab_analysis['unique_words']) if vocab_analysis['unique_words'] else 'None detected'}"),
#                 ("Pronunciation Score:", f"{pron_analysis['pronunciation_score']:.2f}"),
#                 ("Improvement Suggestion:", chat_history[3][1])
#             ]

#             # Create a formatted report for the report_box
#             report_text = f"""Communication Assessment Report
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# OVERALL SCORES
# Pronunciation: {pron_analysis['pronunciation_score']:.2f}
# Grammar: {grammar_score:.2f}
# Vocabulary: {vocab_analysis['lexical_diversity']:.2f}
# Fluency: {pron_analysis['fluency_score']:.2f}

# KEY FINDINGS
# • Grammar: {issue_count} issues found
# • Complex Words Used: {len(vocab_analysis['unique_words'])}
# • Pronunciation Quality: {'Excellent' if pron_analysis['pronunciation_score'] > 0.8 else 'Good' if pron_analysis['pronunciation_score'] > 0.6 else 'Needs Improvement'}
# • Speech Fluency: {'Excellent' if pron_analysis['fluency_score'] > 0.8 else 'Good' if pron_analysis['fluency_score'] > 0.6 else 'Needs Improvement'}
# """

#             # Save the analysis to MongoDB 
#             query_data = {
#                 "timestamp": datetime.now().isoformat(),
#                 "transcribed_text": transcribed_text,
#                 "scores": {
#                     "pronunciation": pron_analysis['pronunciation_score'],
#                     "grammar": grammar_score,
#                     "vocabulary": vocab_analysis['lexical_diversity'],
#                     "fluency": pron_analysis['fluency_score']
#                 },
#                 "grammar_issues": grammar_issues,
#                 "vocab_analysis": vocab_analysis,
#                 "pronunciation_analysis": pron_analysis,
#                 "report": report_text
#             }

#             collection.insert_one(query_data)  # Store data in MongoDB

#             return language_analysis, performance_analysis, radar_chart, vocab_chart, transcribed_text, report_text

#         except Exception as e:
#             print(f"Error in process_input: {str(e)}")
#             return [("Grammar Analysis:", "Error occurred"), 
#                    ("Grammar Score:", "0.00")], [("Error:", "Analysis failed")], None, None, None, "Error generating report"

#     def process_text(self, text):
        

#         """Process text input and return analysis"""
#         try:
#             # Get initial feedback
#             chat_history = self.speech_processor.process_text(text)
            
#             # Parallel processing of analyses
#             vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(text)
            
#             # Calculate grammar score
#             grammar_issues = chat_history[1][1]
#             grammar_corrections = chat_history[2][1]
            
#             if "No major issues found" in grammar_issues:
#                 grammar_score = 0.95
#                 issue_count = 0
#             else:
#                 issue_list = [issue.strip() for issue in grammar_issues.split(',') if issue.strip()]
#                 issue_count = len(issue_list)
#                 words_count = len(text.split())
#                 if words_count > 0:
#                     normalized_issues = min(issue_count / (words_count / 10), 1.0)
#                     grammar_score = max(0.1, 1.0 - normalized_issues)
#                 else:
#                     grammar_score = 0.1
            
#             # Calculate overall scores
#             scores = [
#                 0.0,  # No pronunciation score for text
#                 grammar_score,
#                 vocab_analysis['lexical_diversity'],
#                 0.0   # No fluency score for text
#             ]

#             # Create visualizations
#             radar_chart = self.create_radar_chart(scores)
#             vocab_chart = self.create_vocabulary_chart(vocab_analysis)

#             report_text = f"""Communication Assessment Report
#                 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#                 OVERALL SCORES
#                 Grammar: {grammar_score:.2f}
#                 Vocabulary: {vocab_analysis['lexical_diversity']:.2f}

#                 KEY FINDINGS
#                 • Grammar: {issue_count} issues found
#                 • Complex Words Used: {len(vocab_analysis['unique_words'])}
#             """

            

#             return {
#                 'language_analysis': [
#                     ("Grammar Analysis:", chat_history[2][1]),
#                     ("Grammar Score:", f"{grammar_score:.2f}")
#                 ],
#                 'performance_analysis': [
#                     ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nHigh-Quality Complex Words: {', '.join(vocab_analysis['unique_words']) if vocab_analysis['unique_words'] else 'None detected'}"),
#                     ("Improvement Suggestion:", chat_history[3][1])
#                 ],
#                 'transcribed_text': text,
#                 'report': report_text,
#                 'charts': {
#                     'radar': radar_chart.to_json() if radar_chart else None,
#                     'vocabulary': vocab_chart.to_json() if vocab_chart else None
#                 }
#             }
#         except Exception as e:
#             print(f"Error in process_text: {str(e)}")
#             raise

    @app.route('/api/process-text', methods=['POST'])
    def process_text_api():
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({'error': 'No text provided'}), 400

            assessment_app = CommunicationAssessmentApp()
            chat_history = assessment_app.speech_processor.process_text(data['text'])
            
            # Debugging: Print the structure of chat_history
            print(f"Chat History: {chat_history}")
            
            if not chat_history or len(chat_history) < 1:
                raise ValueError("Invalid text processing result")
            
            # Check the structure of chat_history
            if isinstance(chat_history[0], tuple):  # If it's a list of tuples
                input_text = chat_history[0][1]      # Input text
                grammar_analysis = chat_history[1][1] # Grammar analysis
                corrected_text = chat_history[2][1]   # Corrected version
                scores_text = chat_history[3][1]      # All scores
                detailed_feedback = chat_history[4][1] # Detailed feedback
                improvement = chat_history[5][1]      # Improvement suggestion
                questions = chat_history[6][1]        # Interview questions

                # Extract vocabulary data from the analysis
                vocab_data = chat_history[7][1] if len(chat_history) > 7 else {}
            else:
                # If chat_history is not in the expected tuple format, handle accordingly
                return jsonify({'error': 'Unexpected structure of chat_history'}), 400

            # Parse scores
            scores = {}
            for line in scores_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':')
                    scores[key.strip()] = float(value.strip())
            
            # Radar chart as base64 image
            radar_base64 = assessment_app.create_radar_chart(scores)
            
            # Vocabulary chart (base64 image)
            vocab_chart_base64 = assessment_app.create_vocab_chart(vocab_data)

            # Generate the report with the new vocabulary chart
            report = f"""
    <h2 style="margin-top: 30px;">Communication Assessment Report</h2>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h3 style="margin-top: 20px;">Input Text</h3>
    <p>{input_text}</p>

    <h3 style="margin-top: 20px;">Analysis</h3>
    <pre style="white-space: pre-wrap; font-size: 14px;">{scores_text}</pre>

    <h3 style="margin-top: 20px;">Radar Chart</h3>
    <img src="data:image/png;base64,{radar_base64}" alt="Radar Chart" width="500" style="margin: 10px 0;" />

    <h3 style="margin-top: 20px;">Vocabulary Chart</h3>
    <img src="data:image/png;base64,{vocab_chart_base64}" alt="Vocabulary Chart" width="500" style="margin: 10px 0;" />

    <h3 style="margin-top: 20px;">Detailed Feedback</h3>
    <p>{detailed_feedback}</p>

    <h3 style="margin-top: 20px;">Suggestions</h3>
    <p>{improvement}</p>

    <h3 style="margin-top: 20px;">Follow-up Questions</h3>
    <p>{questions}</p>
    """

            result = {
                'language_analysis': [
                    ("Grammar Analysis:", grammar_analysis),
                    ("Corrected Version:", corrected_text)
                ],
                'performance_analysis': [
                    ("Scores:", scores_text),
                    ("Detailed Feedback:", detailed_feedback),
                    ("Improvement Suggestion:", improvement)
                ],
                'input_text': input_text,
                'interview_questions': questions,
                'report': report
            }

            # Save to MongoDB
            client = MongoClient(MONGO_URI)
            db = client["communication_assessment"]
            collection = db["queries"]

            query_data = {
                "timestamp": datetime.now().isoformat(),
                "input_text": input_text,
                "scores": scores_text,
                "feedback": detailed_feedback,
                "Suggestions": improvement,
                "Follow-up Questions": questions,
                "report": report
            }

            collection.insert_one(query_data)

            return jsonify(result)

        except Exception as e:
            print(f"Error in process_text_api: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/process-speech', methods=['POST', 'OPTIONS'])
    def process_speech_api():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response

        temp_dir = None
        try:
            if 'audio' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio']
            if not audio_file:
                return jsonify({'error': 'Empty file'}), 400

            temp_dir = tempfile.mkdtemp()
            audio_path = os.path.join(temp_dir, 'temp_audio.wav')
            audio_file.save(audio_path)

            assessment_app = CommunicationAssessmentApp()

            # Get speech analysis
            chat_history = assessment_app.speech_processor.process_audio(audio_path)
            if not chat_history or len(chat_history) < 1:
                raise ValueError("Invalid speech processing result")

            # Extract data from chat_history
            transcribed_text = chat_history[0][1]  # Input text
            grammar_analysis = chat_history[1][1]  # Grammar analysis
            corrected_text = chat_history[2][1]    # Corrected version
            scores_text = chat_history[3][1]       # All scores
            detailed_feedback = chat_history[4][1]  # Detailed feedback
            improvement = chat_history[5][1]        # Improvement suggestion
            questions = chat_history[6][1] if len(chat_history) > 6 else "No questions generated"

            # Extract vocabulary data from the analysis
            vocab_data = chat_history[7][1] if len(chat_history) > 7 else {}

            # Parse scores
            scores = {}
            for line in scores_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':')
                    scores[key.strip()] = float(value.strip())

            # Radar chart as base64 image
            radar_base64 = assessment_app.create_radar_chart(scores)
            
            # Vocabulary chart (base64 image)
            vocab_chart_base64 = assessment_app.create_vocab_chart(vocab_data)

            # Generate the report with the new vocabulary chart
            report = f"""
    <h2 style="margin-top: 30px;">Communication Assessment Report</h2>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h3 style="margin-top: 20px;">Transcribed Text</h3>
    <p>{transcribed_text}</p>

    <h3 style="margin-top: 20px;">Analysis</h3>
    <pre style="white-space: pre-wrap; font-size: 14px;">{scores_text}</pre>

    <h3 style="margin-top: 20px;">Radar Chart</h3>
    <img src="data:image/png;base64,{radar_base64}" alt="Radar Chart" width="500" style="margin: 10px 0;" />

    <h3 style="margin-top: 20px;">Vocabulary Chart</h3>
    <img src="data:image/png;base64,{vocab_chart_base64}" alt="Vocabulary Chart" width="500" style="margin: 10px 0;" />

    <h3 style="margin-top: 20px;">Detailed Feedback</h3>
    <p>{detailed_feedback}</p>

    <h3 style="margin-top: 20px;">Suggestions</h3>
    <p>{improvement}</p>

    <h3 style="margin-top: 20px;">Follow-up Questions</h3>
    <p>{questions}</p>
    """

            result = {
                'language_analysis': [
                    ("Grammar Analysis:", grammar_analysis),
                    ("Corrected Version:", corrected_text)
                ],
                'performance_analysis': [
                    ("Scores:", scores_text),
                    ("Detailed Feedback:", detailed_feedback),
                    ("Improvement Suggestion:", improvement)
                ],
                'transcribed_text': transcribed_text,
                'interview_questions': questions,
                'report': report
            }

            # Save to MongoDB
            client = MongoClient(MONGO_URI)
            db = client["communication_assessment"]
            collection = db["queries"]

            query_data = {
                "timestamp": datetime.now().isoformat(),
                "input_text": transcribed_text,
                "scores": scores_text,
                "feedback": detailed_feedback,
                "Suggestions": improvement,
                "Follow-up Questions": questions,
                "report": report
            }

            collection.insert_one(query_data)

            return jsonify(result)

        except Exception as e:
            print(f"Error in process_speech_api: {str(e)}")
            return jsonify({'error': str(e)}), 500
        finally:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)

    @app.route('/api/chat-histories', methods=['GET'])
    def get_chat_histories():
        try:
            client = MongoClient(MONGO_URI)
            db = client["communication_assessment"]
            collection = db["queries"]
            
            # Get all chat histories, sorted by timestamp
            histories = list(collection.find({}, {
                'timestamp': 1,
                'transcribed_text': 1,
                'input_text': 1,
                'scores': 1
            }).sort('timestamp', -1))
            
            # Convert ObjectId to string for JSON serialization
            for history in histories:
                history['_id'] = str(history['_id'])
            
            return jsonify(histories)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/chat-histories/<chat_id>', methods=['GET'])
    def get_chat_history(chat_id):
        try:
            client = MongoClient(MONGO_URI)
            db = client["communication_assessment"]
            collection = db["queries"]
            
            # Convert string ID to ObjectId
            from bson.objectid import ObjectId
            chat = collection.find_one({'_id': ObjectId(chat_id)})
            
            if not chat:
                return jsonify({'error': 'Chat not found'}), 404
            
            chat['_id'] = str(chat['_id'])
            return jsonify(chat)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/chat-histories/<chat_id>', methods=['DELETE'])
    def delete_chat_history(chat_id):
        try:
            client = MongoClient(MONGO_URI)
            db = client["communication_assessment"]
            collection = db["queries"]
            
            # Convert string ID to ObjectId
            from bson.objectid import ObjectId
            result = collection.delete_one({'_id': ObjectId(chat_id)})
            
            if result.deleted_count == 0:
                return jsonify({'error': 'Chat not found'}), 404
            
            return jsonify({'message': 'Chat deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def main():
    multiprocessing.freeze_support()
    # Add more detailed logging
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == "__main__":
    main() 
