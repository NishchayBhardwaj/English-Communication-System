#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_md

# Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"