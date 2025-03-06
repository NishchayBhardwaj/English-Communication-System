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
            return [("Please provide an audio input.", "")], None, None, None, None

        try:
            # Get transcribed text and initial feedback (optimized with async)
            chat_history = self.speech_processor.process_audio(audio_file)
            transcribed_text = chat_history[0][1]

            # Parallel processing of analyses
            vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(transcribed_text)
            pron_analysis = self.pronunciation_analyzer.analyze_pronunciation(audio_file)

            # Calculate overall scores
            scores = [
                pron_analysis['pronunciation_score'],
                float(len(chat_history[1][1].split(',')) == 0),  # Grammar score
                vocab_analysis['lexical_diversity'],
                pron_analysis['fluency_score']  # New fluency score
            ]

            # Create visualizations
            radar_chart = self.create_radar_chart(scores)
            vocab_chart = self.create_vocabulary_chart(vocab_analysis)

            # Format the complete response
            complete_analysis = [
                ("Transcription:", transcribed_text),
                ("Grammar Analysis:", chat_history[2][1]),
                ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nUnique Words: {vocab_analysis['unique_words']}"),
                ("Pronunciation Score:", f"{pron_analysis['pronunciation_score']:.2f}"),
                ("Improvement Suggestion:", chat_history[3][1])
            ]

            # Create detailed analysis text
            detailed_analysis = f"""
            ## Communication Assessment Report
            Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            ### Overall Scores
            - Pronunciation: {pron_analysis['pronunciation_score']:.2f}
            - Grammar: {float(len(chat_history[1][1].split(',')) == 0):.2f}
            - Vocabulary: {vocab_analysis['lexical_diversity']:.2f}
            - Fluency: {pron_analysis['fluency_score']:.2f}

            ### Detailed Analysis
            1. Grammar Corrections:
            {chat_history[2][1]}

            2. Vocabulary Usage:
            - Unique words: {vocab_analysis['unique_words']}
            - Lexical diversity: {vocab_analysis['lexical_diversity']:.2f}
            - Sophistication: {vocab_analysis['sophistication']:.2f}
            - Context appropriateness: {vocab_analysis['context_appropriateness']:.2f}

            3. Pronunciation Details:
            - Confidence score: {pron_analysis['confidence_scores']:.2f}
            - Stress pattern score: {pron_analysis['stress_patterns']:.2f}
            - Fluency score: {pron_analysis['fluency_score']:.2f}
            """

            return complete_analysis, radar_chart, vocab_chart, detailed_analysis, transcribed_text

        except Exception as e:
            return [("Error processing input:", str(e))], None, None, None, None

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
                    chatbot = gr.Chatbot(
                        label="Quick Analysis",
                        height=400
                    )
                with gr.Column(scale=1):
                    radar_plot = gr.Plot(label="Skills Assessment")
                    vocab_plot = gr.Plot(label="Vocabulary Analysis")
            
            with gr.Row():
                detailed_report = gr.Markdown(label="Detailed Report")

            audio_input.change(
                fn=self.process_input,
                inputs=[audio_input],
                outputs=[chatbot, radar_plot, vocab_plot, detailed_report, transcription]
            )

        return interface

def main():
    multiprocessing.freeze_support()
    app = CommunicationAssessmentApp()
    interface = app.create_interface()
    interface.launch(share=False, server_port=7860)

if __name__ == "__main__":
    main() 