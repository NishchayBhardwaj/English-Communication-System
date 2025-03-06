import gradio as gr
from model.speech_processor import SpeechProcessor
from model.vocabulary_analyzer import VocabularyAnalyzer
from model.pronunciation_analyzer import PronunciationAnalyzer
from utils.report_generator import ReportGenerator
import multiprocessing

class CommunicationAssessmentApp:
    def __init__(self):
        self.speech_processor = SpeechProcessor()
        self.vocabulary_analyzer = VocabularyAnalyzer()
        self.pronunciation_analyzer = PronunciationAnalyzer()
        self.report_generator = ReportGenerator()

    def process_input(self, audio_file):
        """Process audio input and return comprehensive analysis"""
        if audio_file is None:
            return [("Please provide an audio input.", "")]

        try:
            # Get transcribed text and initial feedback
            chat_history = self.speech_processor.process_audio(audio_file)
            transcribed_text = chat_history[0][1]  # Get the transcribed text

            # Analyze vocabulary
            vocab_analysis = self.vocabulary_analyzer.analyze_vocabulary(transcribed_text)

            # Analyze pronunciation
            pron_analysis = self.pronunciation_analyzer.analyze_pronunciation(audio_file)

            # Generate report
            analysis_results = {
                "transcription": transcribed_text,
                "grammar_feedback": chat_history[2][1],  # Get grammar feedback
                "vocabulary_analysis": vocab_analysis,
                "pronunciation_analysis": pron_analysis,
                "improvement_suggestion": chat_history[3][1]  # Get improvement suggestion
            }

            report_path = self.report_generator.generate_report(analysis_results)

            # Format the complete response
            complete_analysis = [
                ("Transcription:", transcribed_text),
                ("Grammar Analysis:", chat_history[2][1]),
                ("Vocabulary Analysis:", f"Lexical Diversity: {vocab_analysis['lexical_diversity']:.2f}\nUnique Words: {vocab_analysis['unique_words']}"),
                ("Pronunciation Score:", f"{pron_analysis['pronunciation_score']:.2f}"),
                ("Improvement Suggestion:", chat_history[3][1]),
                ("Report Generated:", str(report_path))
            ]

            return complete_analysis

        except Exception as e:
            return [("Error processing input:", str(e))]

    def create_interface(self):
        """Create and return the Gradio interface"""
        interface = gr.Blocks(title="Communication Assessment Tool")

        with interface:
            gr.Markdown("# Communication Assessment Tool")
            gr.Markdown("Upload an audio file or record your speech for comprehensive analysis")

            with gr.Row():
                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="Audio Input"
                )

            with gr.Row():
                chatbot = gr.Chatbot(
                    label="Analysis Results",
                    height=400
                )

            audio_input.change(
                fn=self.process_input,
                inputs=[audio_input],
                outputs=[chatbot]
            )

        return interface

def main():
    # Add multiprocessing support for Windows
    multiprocessing.freeze_support()
    
    # Create and launch the application
    app = CommunicationAssessmentApp()
    interface = app.create_interface()
    interface.launch(share=False, server_port=7860)

if __name__ == "__main__":
    main() 