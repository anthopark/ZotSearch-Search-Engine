from flask import Flask, request, jsonify, render_template, url_for

from scripts import utils, retrieval

app = Flask(__name__)

inverted_index = utils.load_pickled_file('./scripts/inverted_index_shrinked.pickle')
document_term_freq = utils.load_pickled_file('./scripts/document_termfreq_shrinked.pickle')
url_bookkeeper = utils.load_json_file('./scripts/bookkeeping.json')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/search')
def get_search_result():

    if not request.args['query']:
        return jsonify({"results": []})

    tokenized_query = utils.process_query(request.args['query'])

    for token in tokenized_query:
        if token not in utils.SUPPORTED_QUERIES:
            return jsonify({"results": []})
    
    ranked_result = retrieval.retrieve_results(tokenized_query, inverted_index, document_term_freq)
    search_result = retrieval.map_result_to_url(ranked_result, url_bookkeeper)

    return jsonify(search_result)


if __name__ == '__main__':
    app.run(debug=True)