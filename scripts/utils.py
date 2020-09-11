import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()

support_queries = [
    'mondego',
    'machine',
    'learning',
    'software',
    'engineering',
    'security',
    'students',
    'affairs',
    'graduate',
    'courses',
    'informatics',
    'REST',
    'computer',
    'games',
    'information',
    'retrieval',
    'PhD',
    'program',
    'artificial',
    'intelligence',
    'informatics',
    'science',
]

SUPPORTED_QUERIES = set([LEMMATIZER.lemmatize(token.lower()) for token in support_queries])



def load_pickled_file(file_path) -> {str: [dict]}:
    with open(file_path, 'rb') as read_file:
        return pickle.load(read_file)


def load_json_file(file_path) -> {str: str}:
    with open(file_path, 'r') as read_file:
        return json.load(read_file)


def process_query(raw_query: str) -> [str]:
    """
    tokenize query for further processing
    """
    query_tokens = word_tokenize(raw_query)

    return [LEMMATIZER.lemmatize(token.lower()) for token in query_tokens
            if LEMMATIZER.lemmatize(token.lower()) not in STOP_WORDS]
