import re
from bs4 import BeautifulSoup
import spacy
from textblob import TextBlob
import unicodedata

# Download English language model for spaCy
nlp = spacy.load("en_core_web_sm")

def get_clean(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ')
    x = remove_hash_tags(x)
    x = cont_exp(x)
    x = remove_emails(x)
    x = remove_urls(x)
    x = remove_html_tags(x)
    x = remove_accented_chars(x)
    x = remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    return x

def remove_hash_tags(x):
    # Remove hash tags
    return re.sub(r'@\w+|#\w+', ' ', x)
def cont_exp(x):
    # Replace contractions
    x = re.sub(r"\'ll", " will", x)
    x = re.sub(r"\'ve", " have", x)
    x = re.sub(r"n\'t", " not", x)
    x = re.sub(r"\'re", " are", x)
    x = re.sub(r"\'d", " would", x)
    x = re.sub(r"\'re", " are", x)
    x = re.sub(r"\'s", " is", x)
    x = re.sub(r"\'t", " not", x)
    x = re.sub(r"\'m", " am", x)
    return x

def remove_emails(x):
    # Remove email addresses
    return re.sub(r'\S*@\S*\s?', '', x)

def remove_urls(x):
    # Remove URLs
    return re.sub(r'http?:\S+|https?:\S+', '', x)

def remove_html_tags(x):
    # Remove HTML tags
    soup = BeautifulSoup(x, 'html.parser')
    return soup.get_text()

def remove_accented_chars(x):
    # Remove accented characters
    return unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_special_chars(x):
    # Remove special characters
    return re.sub(r'[^a-zA-Z0-9\s]', '', x)

def make_base(x):
    # Lemmatize words
    doc = nlp(x)
    return ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc])

def spelling_correction(x):
    # Correct spelling
    blob = TextBlob(x)
    return blob.correct()
