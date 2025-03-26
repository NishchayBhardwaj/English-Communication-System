import gradio as gr
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

def main():
    multiprocessing.freeze_support()
    app = CommunicationAssessmentApp()
    interface = app.create_interface()
    interface.launch(share=False, server_port=7860)

if __name__ == "__main__":
    main() 