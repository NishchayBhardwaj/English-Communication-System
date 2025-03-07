#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy's English model
python -m spacy download en_core_web_md

# Download required NLTK data
python -c "import nltk; nltk.download('brown'); nltk.download('gutenberg'); nltk.download('wordnet'); nltk.download('cmudict'); nltk.download('averaged_perceptron_tagger')"