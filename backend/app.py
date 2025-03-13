from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import random
import re
import os

app = Flask(__name__)
CORS(app)

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class TextHumanizer:
    def __init__(self):
        # Common typing errors
        self.common_errors = {
            'th': 'ht',  # common reversal
            'ie': 'ei',  # common misspelling
            'er': 're',  # common reversal
            'you': 'u',  # casual typing
            'your': 'ur',  # casual typing
            'their': 'there',  # common confusion
        }
        
        # Common filler words
        self.fillers = [
            'like', 'you know', 'I mean', 'sort of', 
            'kind of', 'basically', 'actually'
        ]

    def add_typos(self, text, error_rate=0.1):
        words = word_tokenize(text)
        modified_words = []
        
        for word in words:
            if random.random() < error_rate:
                # Apply random error type
                error_type = random.choice(['swap', 'double', 'common'])
                
                if error_type == 'swap' and len(word) > 3:
                    # Swap two adjacent letters
                    pos = random.randint(0, len(word)-2)
                    word_list = list(word)
                    word_list[pos], word_list[pos+1] = word_list[pos+1], word_list[pos]
                    word = ''.join(word_list)
                    
                elif error_type == 'double' and len(word) > 2:
                    # Double a letter
                    pos = random.randint(0, len(word)-1)
                    word = word[:pos] + word[pos] + word[pos:]
                    
                elif error_type == 'common':
                    # Apply common error if available
                    for pattern, replacement in self.common_errors.items():
                        if pattern in word.lower():
                            word = word.lower().replace(pattern, replacement)
                            break
            
            modified_words.append(word)
        
        return ' '.join(modified_words)

    def adjust_formality(self, text, keep_professional=True):
        sentences = sent_tokenize(text)
        modified_sentences = []
        
        for sentence in sentences:
            if keep_professional:
                # Remove casual language and maintain formality
                sentence = re.sub(r'\b(gonna|wanna|gotta)\b', lambda m: {
                    'gonna': 'going to',
                    'wanna': 'want to',
                    'gotta': 'have to'
                }[m.group()], sentence, flags=re.IGNORECASE)
                
                # Remove multiple punctuation
                sentence = re.sub(r'([!?.]){2,}', r'\1', sentence)
                
            else:
                # Add casual elements
                if random.random() < 0.2:
                    sentence = random.choice(self.fillers) + ', ' + sentence
                    
            modified_sentences.append(sentence)
            
        return ' '.join(modified_sentences)

    def adjust_vocabulary(self, text, grade_level):
        words = word_tokenize(text)
        modified_words = []
        
        for word in words:
            if len(word) > 4 and random.random() < 0.2:
                # Attempt to find synonyms
                synsets = wordnet.synsets(word)
                if synsets:
                    # Get all lemmas from all synsets
                    lemmas = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
                    if lemmas:
                        # Choose a random synonym
                        new_word = random.choice(lemmas).replace('_', ' ')
                        if grade_level < 10 and len(new_word) > 8:
                            # For lower grade levels, prefer shorter words
                            continue
                        word = new_word
                        
            modified_words.append(word)
            
        return ' '.join(modified_words)

    def humanize_text(self, text, style="casual", creativity=0.7):
        # Tokenize the text
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)

        # Apply style-specific transformations
        if style == "casual":
            # Add contractions
            text = re.sub(r"(\w+) (am|are|is|have|has|had|will|would)", r"\1'\2", text)
            text = re.sub(r"(cannot)", r"can't", text)
            
            # Add casual markers
            casual_markers = ["well,", "you know,", "like,", "basically,"]
            if random.random() < creativity:
                text = random.choice(casual_markers) + " " + text.lower()
        
        elif style == "formal":
            # Remove contractions
            text = re.sub(r"'ve", " have", text)
            text = re.sub(r"'re", " are", text)
            text = re.sub(r"'m", " am", text)
            text = re.sub(r"'ll", " will", text)
            text = re.sub(r"n't", " not", text)
            
            # Ensure proper capitalization
            sentences = sent_tokenize(text)
            text = ' '.join([s.capitalize() for s in sentences])

        # Add natural variations based on creativity level
        if creativity > 0.5:
            # Add filler words
            fillers = ["actually", "basically", "literally", "seriously"]
            if random.random() < creativity:
                idx = random.randint(0, len(sentences)-1)
                sentences[idx] = random.choice(fillers) + ", " + sentences[idx].lower()
            
            # Add emphasis
            emphasis = ["really", "very", "quite", "absolutely"]
            if random.random() < creativity:
                for i, (word, tag) in enumerate(pos_tags):
                    if tag.startswith('JJ') and random.random() < 0.3:  # 30% chance for adjectives
                        words[i] = random.choice(emphasis) + " " + word

        # Reconstruct text with variations
        humanized_text = ' '.join(sentences)
        
        # Calculate metrics
        naturalness_score = min(1.0, 0.5 + creativity)
        semantic_similarity = 0.8 + random.random() * 0.2  # Simplified similarity score

        return {
            "humanized_text": humanized_text,
            "original_text": text,
            "metrics": {
                "naturalness_score": naturalness_score,
                "semantic_similarity": semantic_similarity
            }
        }

humanizer = TextHumanizer()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/process-text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data['text']
        options = data['options']
        
        # Process the text with the humanizer
        modified_text = text
        
        # Adjust vocabulary based on grade level
        modified_text = humanizer.adjust_vocabulary(
            modified_text, 
            int(options['vocabularyLevel'])
        )
        
        # Add human-like errors if requested
        if options['addErrors']:
            modified_text = humanizer.add_typos(modified_text)
        
        # Adjust formality
        modified_text = humanizer.adjust_formality(
            modified_text, 
            options['keepProfessional']
        )
        
        # Humanize text
        humanized_text = humanizer.humanize_text(
            modified_text, 
            options['style'], 
            float(options['creativity'])
        )
        
        return jsonify({
            'success': True,
            'modifiedText': humanized_text['humanized_text'],
            'metrics': humanized_text['metrics']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)