from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/search')
def get_search_result():
    search_query = request.args['query']
    print(search_query)

    dummy = {
        "result": "search result"
    }

    return jsonify(dummy)


if __name__ == '__main__':
    app.run(debug=True)