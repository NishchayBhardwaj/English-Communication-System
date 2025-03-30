from textblob import TextBlob
import spacy
import numpy as np
from collections import Counter

class ScoringAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_md')
        
    def analyze_text(self, text):
        """Comprehensive text analysis returning multiple scores"""
        doc = self.nlp(text)
        blob = TextBlob(text)
        
        # Grammar and syntax analysis
        grammar_score = self._calculate_grammar_score(doc, blob)
        
        # Vocabulary analysis
        vocab_score = self._calculate_vocabulary_score(doc)
        
        # Fluency analysis for speech
        fluency_score = self._calculate_fluency_score(doc)
        
        # Coherence analysis
        coherence_score = self._calculate_coherence_score(doc)
        
        return {
            'grammar_score': grammar_score,
            'vocabulary_score': vocab_score,
            'fluency_score': fluency_score,
            'coherence_score': coherence_score,
            'overall_score': np.mean([grammar_score, vocab_score, fluency_score, coherence_score]),
            'detailed_feedback': self._generate_detailed_feedback(doc, blob)
        }
    
    def _calculate_grammar_score(self, doc, blob):
        """Calculate grammar score based on multiple factors"""
        # Check sentence structure
        sent_scores = []
        for sent in doc.sents:
            has_subject = False
            has_verb = False
            for token in sent:
                if token.dep_ in ['nsubj', 'nsubjpass']:
                    has_subject = True
                if token.pos_ == 'VERB':
                    has_verb = True
            sent_scores.append(1.0 if has_subject and has_verb else 0.5)
        
        # Calculate base grammar score (0-1 range)
        base_score = np.mean(sent_scores) if sent_scores else 0.5
        
        # Consider spelling and normalize to 0-1 range
        misspelled = len(blob.correct().split()) - len(blob.string.split())
        total_words = len(blob.string.split())
        spelling_score = 1.0 - (min(misspelled, total_words) / (total_words + 1))
        
        # Calculate grammar complexity score
        complexity_indicators = 0
        for token in doc:
            if token.dep_ in ['ccomp', 'xcomp', 'advcl', 'acl']:  # Complex clauses
                complexity_indicators += 1
            if token.dep_ in ['mark', 'cc', 'prep']:  # Connectors and prepositions
                complexity_indicators += 0.5
        
        complexity_score = min(1.0, complexity_indicators / (len(doc) / 5))
        
        # Combine scores with weights
        final_score = (
            0.4 * base_score +
            0.3 * spelling_score +
            0.3 * complexity_score
        )
        
        # Ensure score is between 0 and 1
        return max(0.1, min(1.0, final_score))
    
    def _calculate_vocabulary_score(self, doc):
        """Calculate vocabulary sophistication score"""
        # Count unique lemmas
        lemmas = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        unique_lemmas = set(lemmas)
        
        # Calculate lexical diversity (0-1 range)
        diversity = len(unique_lemmas) / (len(lemmas) + 1)
        
        # Calculate sophistication based on word length and frequency
        avg_word_length = np.mean([len(word) for word in unique_lemmas]) if unique_lemmas else 0
        sophistication = min(1.0, avg_word_length / 12)  # Normalize by max expected length
        
        # Combine scores
        return min(1.0, max(0.1, (diversity + sophistication) / 2))
    
    def _calculate_fluency_score(self, doc):
        """Calculate fluency score based on text structure"""
        # Analyze sentence length variation
        sent_lengths = [len(sent) for sent in doc.sents]
        if not sent_lengths:
            return 0.5
            
        # Calculate normalized sentence length variation (0-1 range)
        avg_len = np.mean(sent_lengths)
        length_variation = 1.0 - min(1.0, np.std(sent_lengths) / (avg_len + 1))
        
        # Analyze conjunction and punctuation usage
        connectors = len([token for token in doc if token.pos_ in ['CCONJ', 'SCONJ']])
        connector_ratio = min(1.0, connectors / (len(doc) / 10))
        
        # Combine scores
        return min(1.0, max(0.1, (length_variation + connector_ratio) / 2))
    
    def _calculate_coherence_score(self, doc):
        """Calculate text coherence score"""
        # Analyze sentence similarity
        sents = list(doc.sents)
        if len(sents) < 2:
            return 0.7
            
        # Calculate semantic similarity between adjacent sentences
        similarities = []
        for i in range(len(sents) - 1):
            similarity = sents[i].similarity(sents[i + 1])
            similarities.append(similarity)
        
        # Normalize to 0-1 range
        coherence_score = np.mean(similarities) if similarities else 0.5
        return min(1.0, max(0.1, coherence_score))
    
    def _generate_detailed_feedback(self, doc, blob):
        """Generate detailed feedback based on analysis"""
        feedback = []
        
        # Grammar feedback
        grammar_issues = []
        for sent in doc.sents:
            if not any(token.dep_ in ['nsubj', 'nsubjpass'] for token in sent):
                grammar_issues.append("Missing subject")
            if not any(token.pos_ == 'VERB' for token in sent):
                grammar_issues.append("Missing verb")
                
        if grammar_issues:
            feedback.append(f"Grammar issues found: {', '.join(grammar_issues)}")
            
        # Vocabulary feedback
        sophisticated_words = [token.text for token in doc if len(token.text) > 7 and token.is_alpha]
        if sophisticated_words:
            feedback.append(f"Good use of sophisticated words: {', '.join(sophisticated_words[:3])}")
            
        return feedback 