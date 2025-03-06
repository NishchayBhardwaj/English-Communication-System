import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base project settings
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model Settings
GRAMMAR_MODEL = "prithivida/grammar_error_correcter_v1"
PRONUNCIATION_MODEL = "facebook/wav2vec2-large-960h"
ACCENT_MODEL = "facebook/wav2vec2-large-xlsr-53"

# Scoring Parameters
FLUENCY_WEIGHT = 0.3
PRONUNCIATION_WEIGHT = 0.25
GRAMMAR_WEIGHT = 0.25
VOCABULARY_WEIGHT = 0.2

# Audio Settings
SAMPLE_RATE = 16000
MAX_AUDIO_LENGTH = 300  # seconds 