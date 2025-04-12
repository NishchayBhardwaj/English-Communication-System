import language_tool_python
from lexicalrichness import LexicalRichness
import textstat
import spacy
from sentence_transformers import SentenceTransformer, util
import numpy as np
from textblob import TextBlob
from transformers import BertTokenizer, BertModel
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from collections import Counter
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

class ScoringAnalyzer:
    def __init__(self):
        # Initialize LanguageTool, spaCy, and Sentence-BERT
        self.coherence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        self.tool = language_tool_python.LanguageTool('en-US')
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize GPT2 for perplexity-based fluency check
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

    def analyze_text(self, text):
        doc = self.nlp(text)
        blob = TextBlob(text)

        grammar_score = self._calculate_grammar_score(text)
        vocab_data = self._calculate_vocabulary_score(text)
        fluency_score = self._calculate_fluency_score(text)
        coherence_score = self._calculate_coherence_score(text)

        return {
            'grammar_score': grammar_score,
            'vocabulary_score': np.mean([vocab_data['lexical_diversity'], vocab_data['sophistication'], vocab_data['context_appropriateness']]),  # Use average of vocab metrics as the score
            'fluency_score': fluency_score,
            'coherence_score': coherence_score,
            'overall_score': np.mean([grammar_score, np.mean([vocab_data['lexical_diversity'], vocab_data['sophistication'], vocab_data['context_appropriateness']]), fluency_score, coherence_score]),
            'detailed_feedback': self._generate_detailed_feedback(text),
            'vocab_data': vocab_data
        }

    def _calculate_grammar_score(self, text):
        """Use LanguageTool and BERT-based model for grammar checking."""
        matches = self.tool.check(text)
        words = len(text.split()) + 1
        grammar_score = 1 - min(len(matches) / words, 1)
        
        # BERT-based approach for more contextual errors
        blob = TextBlob(text)
        bert_grammar_score = 1 if len(blob.correct()) == len(text) else 0.7
        
        # Average the scores
        final_score = (grammar_score + bert_grammar_score) / 2
        return max(0.1, round(final_score, 3))

    def _calculate_vocabulary_score(self, text):
        """Use LexicalRichness and word frequency analysis for vocabulary scoring."""
        lex = LexicalRichness(text)
        diversity = lex.ttr  # Type-Token Ratio
        words = [word for word in text.split() if word.isalpha()]
        avg_word_length = np.mean([len(w) for w in words]) if words else 0
        sophistication = min(1.0, avg_word_length / 12)
        
        # Calculate word frequency using Counter and stopwords
        word_count = Counter(words)
        total_words = sum(word_count.values())
        common_words = set(stopwords.words('english'))
        freq_penalty = 0

        for word, count in word_count.items():
            if word.lower() not in common_words:  # Exclude common stopwords
                word_freq = count / total_words
                if word_freq > 0.1:  # Penalize overly frequent words
                    freq_penalty += word_freq
        
        # Context appropriateness could be a simple function of sophistication and frequency
        # Example: Higher sophistication and lower word frequency would be more appropriate contextually
        context_appropriateness = max(0, (sophistication - min(freq_penalty, 1.0)) / 2)
        
        # Return the vocabulary analysis data in a dictionary
        vocab_data = {
            'lexical_diversity': round(diversity, 3),
            'sophistication': round(sophistication, 3),
            'context_appropriateness': round(context_appropriateness, 3)
        }

        return vocab_data

    def _calculate_fluency_score(self, text):
        """Use Flesch readability score and GPT perplexity for fluency estimation."""
        try:
            ease = textstat.flesch_reading_ease(text)
            normalized = 1 - min(ease / 100, 1)
        except:
            normalized = 0.5
        
        # GPT-2 Perplexity for fluency
        inputs = self.tokenizer.encode(text, return_tensors="pt")
        loss = self.gpt2_model(inputs, labels=inputs).loss
        perplexity = torch.exp(loss).item()
        gpt_fluency = 1 / (1 + perplexity / 1000)  # Normalize perplexity
        
        # Combine the two scores
        fluency_score = (normalized + gpt_fluency) / 2
        return max(0.1, round(fluency_score, 3))

    def _calculate_coherence_score(self, text):
        """Use Sentence-BERT for semantic similarity and BERT for sentence transitions coherence analysis."""
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 1]
        if len(sentences) < 2:
            return 0.7

        # Sentence-BERT for semantic similarity
        embeddings = self.coherence_model.encode(sentences, convert_to_tensor=True)
        sims = util.pytorch_cos_sim(embeddings[:-1], embeddings[1:]).cpu().numpy().flatten()
        avg_sim = np.mean(sims) if len(sims) else 0.5

        # Additional BERT-based coherence (sentence-to-sentence transitions)
        coherence_score_bert = self._calculate_bert_coherence(sentences)
        
        # Combine Sentence-BERT and BERT coherence
        coherence_score = (avg_sim + coherence_score_bert) / 2
        return max(0.1, round(coherence_score, 3))

    def _calculate_bert_coherence(self, sentences):
        """Calculate coherence using BERT-based sentence embeddings."""
        # Tokenize the sentences for BERT
        inputs = self.bert_tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        
        # Use the [CLS] token embeddings for each sentence
        sentence_embeddings = outputs.last_hidden_state[:, 0, :]
        
        # Compute cosine similarity between consecutive sentences
        sims = []
        for i in range(len(sentence_embeddings) - 1):
            cos_sim = torch.nn.functional.cosine_similarity(sentence_embeddings[i], sentence_embeddings[i + 1], dim=0)
            sims.append(cos_sim.item())
        
        return np.mean(sims) if sims else 0.5

    def _generate_detailed_feedback(self, text):
        """Generate detailed feedback on grammar and vocabulary."""
        feedback = []
        matches = self.tool.check(text)
        if matches:
            grammar_msgs = list(set([match.message for match in matches[:3]]))
            feedback.append(f"Grammar suggestions: {', '.join(grammar_msgs)}")

        # Vocabulary feedback
        words = [word for word in text.split() if word.isalpha()]
        long_words = [w for w in words if len(w) > 7]
        if long_words:
            feedback.append(f"Nice use of advanced vocabulary: {', '.join(long_words[:3])}")

        return feedback