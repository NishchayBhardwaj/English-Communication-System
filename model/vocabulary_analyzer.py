from collections import Counter
from textblob import TextBlob
import spacy
from nltk.corpus import wordnet, cmudict
import numpy as np
from nltk.corpus import brown, gutenberg
from nltk.probability import FreqDist
import nltk

class VocabularyAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        # Initialize NLTK resources
        try:
            self.cmu = cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            self.cmu = cmudict.dict()
        
        # Create frequency distributions from standard corpora
        self.freq_dist = self._initialize_frequency_dist()
        # Create word ranks dictionary
        self.word_ranks = self._create_word_ranks()
        
        # CEFR level approximations based on frequency ranks
        self.cefr_thresholds = {
            'A1': 1000,    # Most common words
            'A2': 2000,
            'B1': 3500,
            'B2': 5000,
            'C1': 7000,
            'C2': float('inf')  # Beyond common usage
        }
    
    def _initialize_frequency_dist(self):
        """Initialize frequency distribution from standard corpora"""
        try:
            words = []
            # Use Brown corpus (standard American English)
            words.extend(brown.words())
            # Use Gutenberg corpus (classic literature)
            words.extend(gutenberg.words())
            return FreqDist(word.lower() for word in words)
        except LookupError:
            nltk.download('brown')
            nltk.download('gutenberg')
            words = []
            words.extend(brown.words())
            words.extend(gutenberg.words())
            return FreqDist(word.lower() for word in words)

    def _create_word_ranks(self):
        """Create a dictionary of word ranks based on frequency"""
        words_by_freq = sorted(self.freq_dist.items(), key=lambda x: x[1], reverse=True)
        return {word: rank for rank, (word, _) in enumerate(words_by_freq, 1)}
    
    def _get_word_complexity(self, word):
        """Calculate word complexity based on multiple factors"""
        complexity_scores = []
        
        # 1. Length complexity
        length_score = min(len(word) / 12, 1.0)  # Normalize by max expected length
        complexity_scores.append(length_score)
        
        # 2. Syllable complexity
        try:
            syllables = len(self._count_syllables(word))
            syllable_score = min(syllables / 5, 1.0)  # Normalize by max expected syllables
            complexity_scores.append(syllable_score)
        except (KeyError, IndexError):
            syllable_score = 0.5  # Default if word not found
            complexity_scores.append(syllable_score)
        
        # 3. Frequency-based complexity
        freq_rank = self._get_frequency_rank(word)
        freq_score = min(freq_rank / 10000, 1.0)  # Normalize by rank
        complexity_scores.append(freq_score)
        
        # 4. Semantic complexity (number of meanings)
        try:
            meanings = len(wordnet.synsets(word))
            semantic_score = min(meanings / 10, 1.0)  # Normalize by max expected meanings
            complexity_scores.append(semantic_score)
        except LookupError:
            nltk.download('wordnet')
            meanings = len(wordnet.synsets(word))
            semantic_score = min(meanings / 10, 1.0)
            complexity_scores.append(semantic_score)
        
        return np.mean(complexity_scores)
    
    def _count_syllables(self, word):
        """Count syllables using CMU pronouncing dictionary"""
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu[word.lower()]]
        except KeyError:
            # Fallback syllable counting if word not in CMU dict
            return [len(''.join(c for c in word if c.lower() in 'aeiou'))]
    
    def _get_frequency_rank(self, word):
        """Get word frequency rank"""
        word = word.lower()
        return self.word_ranks.get(word, len(self.word_ranks))
    
    def _get_cefr_level(self, word):
        """Determine CEFR level based on frequency rank"""
        rank = self._get_frequency_rank(word)
        for level, threshold in sorted(self.cefr_thresholds.items()):
            if rank <= threshold:
                return level
        return 'C2'
    
    def analyze_vocabulary(self, text):
        """Analyze vocabulary richness and appropriateness"""
        try:
            doc = self.nlp(text)
            
            # Analyze lexical diversity
            words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
            if not words:
                return {
                    "lexical_diversity": 0,
                    "sophistication": 0,
                    "context_appropriateness": 0,
                    "unique_words": [],
                    "total_words": 0,
                    "cefr_levels": {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0},
                    "complex_words": []
                }
            
            # Analyze word complexity and CEFR levels
            word_complexities = {}
            cefr_levels = {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0}
            
            for word in words:
                try:
                    complexity = self._get_word_complexity(word)
                    word_complexities[word] = complexity
                    cefr_level = self._get_cefr_level(word)
                    cefr_levels[cefr_level] += 1
                except Exception as e:
                    print(f"Error processing word '{word}': {str(e)}")
                    continue
            
            # Get complex words (above B1 level with high complexity)
            complex_words = [
                {
                    'word': word,
                    'complexity': score,
                    'cefr_level': self._get_cefr_level(word)
                }
                for word, score in word_complexities.items()
                if score > 0.6  # Threshold for complex words
            ]
            
            # Sort complex words by complexity
            complex_words.sort(key=lambda x: x['complexity'], reverse=True)
            
            return {
                "lexical_diversity": len(set(words)) / len(words),
                "sophistication": np.mean(list(word_complexities.values())) if word_complexities else 0,
                "context_appropriateness": self._analyze_context(doc),
                "unique_words": list(set(words)),
                "total_words": len(words),
                "cefr_levels": cefr_levels,
                "complex_words": complex_words[:10]  # Top 10 most complex words
            }
        except Exception as e:
            print(f"Error in analyze_vocabulary: {str(e)}")
            return {
                "lexical_diversity": 0,
                "sophistication": 0,
                "context_appropriateness": 0,
                "unique_words": [],
                "total_words": 0,
                "cefr_levels": {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0},
                "complex_words": []
            }
    
    def _analyze_context(self, doc):
        """Analyze if words are used in appropriate context"""
        try:
            context_scores = []
            for sent in doc.sents:
                sent_vectors = [w.vector for w in sent if w.has_vector]
                if sent_vectors:
                    context_vector = np.mean(sent_vectors, axis=0)
                    for token in sent:
                        if token.has_vector:
                            similarity = np.dot(token.vector, context_vector) / (
                                np.linalg.norm(token.vector) * np.linalg.norm(context_vector)
                            )
                            context_scores.append(similarity)
            return np.mean(context_scores) if context_scores else 0
        except Exception as e:
            print(f"Error in context analysis: {str(e)}")
            return 0 