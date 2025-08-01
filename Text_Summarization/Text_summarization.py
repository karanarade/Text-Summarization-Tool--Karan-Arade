# text_summarizer.py

import nltk
nltk.download('punkt_tab')
import re
import heapq
from bs4 import BeautifulSoup

# Download required resources
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

def summarize_text(text, max_sentences=3):
    # Clean text
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Normalize frequencies
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_freq

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(' ')) < 30:  # Filter long sentences
                    if sent not in sentence_scores:
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Select top sentences
    summary_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary
