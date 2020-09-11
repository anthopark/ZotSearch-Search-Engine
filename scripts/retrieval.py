import numpy as np
from collections import defaultdict
from math import log, sqrt


def map_result_to_url(results: [('doc_id', float)], url_bookkeeper) -> [[int, str]]:
    """
    map ranked search result to urls using document id
    """
    rank_url_pairs = []

    for rank, tup in enumerate(results, start=1):
        rank_url_pairs.append((rank, url_bookkeeper[tup[0]]))

    return rank_url_pairs[:10]


def retrieve_results(query: [str], i_index: {str: [dict]},
                     doc_tf_dict: {'doc_id': {'term': int}}) -> [('doc_id', float)]:
    """
    compute cosine similarity score for ranking the result of search query
    """

    query_vec = _compute_query_vector(query, i_index)
    doc_vectors = _get_doc_vectors(query, i_index, doc_tf_dict)

    # [(doc_id, scores)]
    cosine_scores = []

    for doc_id, doc_vec in doc_vectors.items():
        cosine_scores.append((doc_id, np.dot(query_vec, doc_vec)))

    cosine_scores = sorted(cosine_scores, key=(lambda x: x[1]), reverse=True)

    return cosine_scores


def _compute_query_vector(query: [str], inverted_index: {str: [dict]}) -> np.array:
    """
    For the query vector, used logarithmically weighted term freq and idf.
    The normalization is not applied.
    """
    query_vec = np.zeros(len(query))

    query_tf_dict = defaultdict(int)
    query_df_dict = defaultdict(int)

    for t in query:
        query_tf_dict[t] += 1

        try:
            query_df_dict[t] = len(inverted_index[t])
        except KeyError:
            query_df_dict[t] = 0

    for i in range(len(query)):
        term = query[i]
        weighted_tf = 1 + log(query_tf_dict[term], 10)
        idf = log(37497/query_df_dict[term], 10) \
            if query_df_dict[term] != 0 else 0
        query_vec[i] = weighted_tf * idf

    return query_vec


def _get_doc_vectors(query: [str], inverted_index: {str: [dict]},
                     doc_tf_dict: {str: {str: int}}) -> {str: np.array}:
    """
    returns doc_id paired with a corresponding document vector
    """
    doc_vectors = dict()

    # [docid1, docid2, ...]
    retrieved_pages = []

    for t in query:
        for i in range(50):
            try:
                retrieved_pages.append(inverted_index[t][i]['id'])
            except (KeyError, IndexError):
                break

    for doc_id in retrieved_pages:

        doc_vectors[doc_id] = _compute_doc_vector(query, doc_tf_dict[doc_id])

    return doc_vectors


def _compute_doc_vector(query: [str], page_tf_dict: {str: int}) -> np.array:
    """

    :param query:
    :param page_tf_dict: doc_id page specific term freq map
    :return: np.array
    """

    doc_vec = np.zeros(len(query))

    query_tf_dict = defaultdict(int)

    for t in query:
        try:
            query_tf_dict[t] = page_tf_dict[t]
        except KeyError:
            query_tf_dict[t] = 0

    for i in range(len(query)):
        term = query[i]
        doc_vec[i] = 1 + log(query_tf_dict[term], 10) \
            if query_tf_dict[term] != 0 else 0

    # normalize
    sqrt_sum_sq = sqrt(sum([pow(val, 2) for val in doc_vec]))

    if sqrt_sum_sq != 0:
        for i in range(len(doc_vec)):
            doc_vec[i] /= sqrt_sum_sq
    else:
        # all 0s in vector
        pass

    return doc_vec
