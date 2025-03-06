import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import numpy as np
from config.settings import PRONUNCIATION_MODEL, SAMPLE_RATE

class PronunciationAnalyzer:
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained(PRONUNCIATION_MODEL)
        self.model = Wav2Vec2ForCTC.from_pretrained(PRONUNCIATION_MODEL)
        
    def analyze_pronunciation(self, audio_path):
        """Analyze pronunciation quality from audio"""
        # Load and preprocess audio
        waveform, _ = librosa.load(audio_path, sr=SAMPLE_RATE)
        inputs = self.processor(
            waveform, 
            sampling_rate=SAMPLE_RATE, 
            return_tensors="pt"
        )
        
        # Get model predictions
        with torch.no_grad():
            logits = self.model(inputs.input_values).logits
            
        # Calculate pronunciation confidence scores
        probs = torch.nn.functional.softmax(logits, dim=-1)
        confidence_scores = torch.max(probs, dim=-1)[0]
        
        # Analyze rhythm and stress patterns
        stress_patterns = self._analyze_stress_patterns(waveform)
        
        return {
            "confidence_scores": confidence_scores.mean().item(),
            "stress_patterns": stress_patterns,
            "pronunciation_score": self._calculate_overall_score(
                confidence_scores.mean().item(),
                stress_patterns
            )
        }
    
    def _analyze_stress_patterns(self, waveform):
        """Analyze speech rhythm and stress patterns"""
        # Calculate energy envelope
        energy = librosa.feature.rms(y=waveform)[0]
        
        # Find peaks in energy (stressed syllables)
        peaks = librosa.util.peak_pick(
            energy,
            pre_max=3,
            post_max=3,
            pre_avg=3,
            post_avg=3,
            delta=0.1,
            wait=10
        )
        
        return len(peaks) / len(energy)  # Rhythm regularity score
    
    def _calculate_overall_score(self, confidence, stress_score):
        """Calculate overall pronunciation score"""
        return 0.7 * confidence + 0.3 * stress_score 