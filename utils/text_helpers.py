"""
Helper functions for text preprocessing
"""
import nltk
from nltk.corpus import stopwords

def _nltk_prep():
    """
    Check if tokens and stopwords are already on local machine
    If not, download

    :return:
    """
    try:
        nltk.word_tokenize('')
    except LookupError:
        nltk.download('punkt')
    try:
        [word for word in '' if word not in stopwords.words('english')]
    except LookupError:
        nltk.download('stopwords')
