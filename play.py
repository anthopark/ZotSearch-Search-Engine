import pickle
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
from bs4.element import Comment
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



def load_inverted_index(file_path: str) -> {str: [dict]}:
    with open(file_path, 'rb') as read_file:
        return pickle.load(read_file)


ii = load_inverted_index('./scripts/inverted_index')
ii_small = dict()

for term in SUPPORTED_QUERIES:
    ii_small[term] = ii[term]

with open('./inverted_index_shrinked.pickle', 'wb') as write_file:
    pickle.dump(ii_small, write_file, protocol=pickle.HIGHEST_PROTOCOL)

# print(len(ii))
# print(ii['intelligence'], len(ii['intelligence']))
# print()
# print(ii['artificial'], len(ii['artificial']))
# print()
# print(ii['computer'], len(ii['computer']))


def _compute_term_freq(web_page) -> {'str': int}:
    result = defaultdict(int)
    with open(web_page, mode='r') as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')

        text_content = " ".join(t.strip() for t in filter(
            _is_visible_tag, soup.findAll(text=True)) if t.strip() != '')
        tokens = word_tokenize(text_content)
        lemmatized_tokens = [LEMMATIZER.lemmatize(token.lower()) for token in tokens
                            if (len(token) > 1) and not (token.isdigit() and (len(token) <= 2 or len(token) >= 5))]
        final_tokens = [token for token in lemmatized_tokens if token in SUPPORTED_QUERIES]

        for term in final_tokens:
            result[term] += 1
    return dict(result)    



def _is_visible_tag(elem):
    if elem.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(elem, Comment):
        return False
    return True


def build_document_term_freq_dict() -> {'doc_id': {str: int}}:

    result = defaultdict(dict)

    web_pages_dir = Path('./WEBPAGES_RAW')
    assert web_pages_dir.exists() and web_pages_dir.is_dir(), "Corpus Dir Error"
    web_page_list = sorted([corp_dir for corp_dir in web_pages_dir.iterdir()
                            if corp_dir.is_dir()], key=(lambda x: int(x.name)))

    for sub_dir in web_page_list:
        for web_page in sorted(sub_dir.iterdir(), key=(lambda x: int(x.name))):
            doc_id = sub_dir.name + "/" + web_page.name

            result[doc_id] = _compute_term_freq(web_page)

    return dict(result)


if __name__ == "__main__":
    pass
    document_term_freq_dict = build_document_term_freq_dict()

    with open('./document_termfreq_shrinked.pickle', 'wb') as write_file:
        pickle.dump(document_term_freq_dict, write_file, protocol=pickle.HIGHEST_PROTOCOL)


