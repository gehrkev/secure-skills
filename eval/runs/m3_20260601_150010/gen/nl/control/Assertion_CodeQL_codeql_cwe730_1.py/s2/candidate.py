from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('query', '')

    if 'www.example.com/' in query or 'beta.example.com/' in query:
        return f'Search results for: {query}'
    else:
        return f'No results found for: {query}'

if __name__ == '__main__':
    app.run(debug=True)
