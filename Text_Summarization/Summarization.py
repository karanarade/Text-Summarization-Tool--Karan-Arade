import nltk
import heapq
import re
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3):
    # Clean the text
    cleaned_text = BeautifulSoup(text, "html.parser").text
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Tokenize into sentences
    sentence_list = nltk.sent_tokenize(cleaned_text)

    # Create a frequency table for words
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(cleaned_text.lower()):
        if word not in stopwords and word.isalpha():
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Score sentences
    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    # Select top N sentences
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)
