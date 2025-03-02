from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route("/search", methods=["GET"])
def search_emails():
    query = request.args.get("q", "")

    if not query:
        return jsonify({"error": "Please provide a search query"}), 400

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["from", "subject"]
            }
        }
    }

    results = es.search(index="emails", body=search_body)
    return jsonify(results["hits"]["hits"])

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)

@app.route("/")  # This defines the homepage route
def home():
    return "Flask is running successfully!"

if __name__ == "__main__":
    app.run(debug=True)
