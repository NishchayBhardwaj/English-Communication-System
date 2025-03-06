from collections import Counter
from textblob import TextBlob
import spacy
from nltk.corpus import wordnet
import numpy as np

class VocabularyAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        
    def analyze_vocabulary(self, text):
        """Analyze vocabulary richness and appropriateness"""
        doc = self.nlp(text)
        
        # Analyze lexical diversity
        words = [token.text.lower() for token in doc if token.is_alpha]
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Analyze vocabulary sophistication
        sophistication_score = self._calculate_sophistication(doc)
        
        # Analyze context appropriateness
        context_score = self._analyze_context(doc)
        
        return {
            "lexical_diversity": lexical_diversity,
            "sophistication": sophistication_score,
            "context_appropriateness": context_score,
            "unique_words": len(unique_words),
            "total_words": len(words)
        }
    
    def _calculate_sophistication(self, doc):
        """Calculate vocabulary sophistication based on word frequency"""
        sophistication_scores = []
        for token in doc:
            if token.is_alpha and not token.is_stop:
                # Use log frequency as a proxy for word complexity
                frequency = token.rank if hasattr(token, 'rank') else 0
                sophistication_scores.append(1 / (1 + np.log(frequency + 1)))
        return np.mean(sophistication_scores) if sophistication_scores else 0
    
    def _analyze_context(self, doc):
        """Analyze if words are used in appropriate context"""
        context_scores = []
        for sent in doc.sents:
            for token in sent:
                if token.has_vector:
                    # Compare word similarity with surrounding context
                    context_vector = sum(w.vector for w in sent if w.has_vector)
                    similarity = token.vector.dot(context_vector)
                    context_scores.append(similarity)
        return np.mean(context_scores) if context_scores else 0 