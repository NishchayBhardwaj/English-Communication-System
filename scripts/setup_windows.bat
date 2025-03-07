pip install -r requirements.txt

python -m spacy download en_core_web_md

python -c "import nltk; nltk.download('brown'); nltk.download('gutenberg'); nltk.download('wordnet'); nltk.download('cmudict'); nltk.download('averaged_perceptron_tagger')"

python -m textblob.download_corpora