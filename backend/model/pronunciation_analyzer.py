# import torch
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# import librosa
# import numpy as np
# from config.settings import PRONUNCIATION_MODEL, SAMPLE_RATE
# from scipy.signal import find_peaks
# import librosa.effects

# class PronunciationAnalyzer:
#     def __init__(self):
#         self.processor = Wav2Vec2Processor.from_pretrained(PRONUNCIATION_MODEL)
#         self.model = Wav2Vec2ForCTC.from_pretrained(PRONUNCIATION_MODEL)
        
#     def analyze_pronunciation(self, audio_path):
#         """Analyze pronunciation quality from audio"""
#         # Load and preprocess audio
#         waveform, _ = librosa.load(audio_path, sr=SAMPLE_RATE)
        
#         # Speed up processing by trimming silence
#         waveform, _ = librosa.effects.trim(waveform, top_db=20)
        
#         # Process shorter segments in parallel if audio is long
#         if len(waveform) > SAMPLE_RATE * 10:  # If longer than 10 seconds
#             segments = self._split_audio(waveform)
#             results = []
#             for segment in segments:
#                 results.append(self._process_segment(segment))
            
#             # Aggregate results
#             confidence_scores = np.mean([r['confidence'] for r in results])
#             stress_patterns = np.mean([r['stress'] for r in results])
#             fluency_score = self._calculate_fluency(waveform)
#         else:
#             result = self._process_segment(waveform)
#             confidence_scores = result['confidence']
#             stress_patterns = result['stress']
#             fluency_score = self._calculate_fluency(waveform)
        
#         return {
#             "confidence_scores": confidence_scores,
#             "stress_patterns": stress_patterns,
#             "pronunciation_score": self._calculate_overall_score(confidence_scores, stress_patterns),
#             "fluency_score": fluency_score
#         }
    
#     def _analyze_stress_patterns(self, waveform):
#         """Analyze speech rhythm and stress patterns"""
#         # Calculate energy envelope
#         energy = librosa.feature.rms(y=waveform)[0]
        
#         # Find peaks in energy (stressed syllables)
#         peaks = librosa.util.peak_pick(
#             energy,
#             pre_max=3,
#             post_max=3,
#             pre_avg=3,
#             post_avg=3,
#             delta=0.1,
#             wait=10
#         )
        
#         return len(peaks) / len(energy)  # Rhythm regularity score
    
#     def _calculate_overall_score(self, confidence, stress_score):
#         """Calculate overall pronunciation score"""
#         return 0.7 * confidence + 0.3 * stress_score 

#     def _calculate_fluency(self, waveform):
#         """Calculate fluency score based on speech rate and pauses"""
#         # Calculate speech rate
#         speech_rate = self._calculate_speech_rate(waveform)
        
#         # Analyze pauses
#         pause_score = self._analyze_pauses(waveform)
        
#         # Combine scores
#         fluency_score = 0.6 * speech_rate + 0.4 * pause_score
#         return min(max(fluency_score, 0), 1)  # Normalize between 0 and 1

#     def _calculate_speech_rate(self, waveform):
#         """Calculate speech rate score"""
#         # Get speech envelope
#         envelope = np.abs(waveform)
        
#         # Find peaks in envelope (syllables)
#         peaks, _ = find_peaks(envelope, distance=int(SAMPLE_RATE * 0.1))
        
#         # Calculate speech rate (syllables per second)
#         speech_rate = len(peaks) / (len(waveform) / SAMPLE_RATE)
        
#         # Normalize speech rate (typical speech is 2-5 syllables/second)
#         return min(max((speech_rate - 2) / 3, 0), 1)

#     def _analyze_pauses(self, waveform):
#         """Analyze pauses in speech"""
#         # Calculate energy in small windows
#         frame_length = int(SAMPLE_RATE * 0.03)  # 30ms windows
#         hop_length = frame_length // 2
        
#         energy = librosa.feature.rms(y=waveform, frame_length=frame_length, hop_length=hop_length)[0]
        
#         # Find pauses (low energy segments)
#         pause_threshold = np.mean(energy) * 0.1
#         pauses = energy < pause_threshold
        
#         # Calculate pause score (penalize too many or too few pauses)
#         pause_ratio = np.mean(pauses)
#         return 1 - abs(pause_ratio - 0.15) * 2  # Optimal pause ratio around 15%

#     def _split_audio(self, waveform):
#         """Split audio into smaller segments for parallel processing"""
#         segment_length = SAMPLE_RATE * 5  # 5-second segments
#         return [waveform[i:i + segment_length] for i in range(0, len(waveform), segment_length)]

#     def _process_segment(self, waveform):
#         """Process a single audio segment"""
#         inputs = self.processor(
#             waveform, 
#             sampling_rate=SAMPLE_RATE, 
#             return_tensors="pt"
#         )
        
#         # Get model predictions
#         with torch.no_grad():
#             logits = self.model(inputs.input_values).logits
            
#         # Calculate pronunciation confidence scores
#         probs = torch.nn.functional.softmax(logits, dim=-1)
#         confidence_scores = torch.max(probs, dim=-1)[0]
        
#         # Analyze rhythm and stress patterns
#         stress_patterns = self._analyze_stress_patterns(waveform)
        
#         return {
#             "confidence": confidence_scores.mean().item(),
#             "stress": stress_patterns
#         } 