
from flask import Flask, jsonify, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session support

# Raw articles
RAW_ARTICLES = [
    {
        "id": 1,
        "author": "Alice",
        "title": "Flask Tips",
        "content": "Learn Flask step by step.",
        "date": "2026-01-12"
    },
    {
        "id": 2,
        "author": "Bob",
        "title": "Python Tricks",
        "content": "Cool Python tricks for developers.",
        "date": "2026-01-11"
    },
    {
        "id": 3,
        "author": "Carol",
        "title": "APIs 101",
        "content": "Introduction to building APIs.",
        "date": "2026-01-10"
    },
]

# Helper to enrich articles with 'preview' and 'minutes_to_read'
def enrich_article(article):
    enriched = article.copy()  # Copy to keep original fields like 'date'
    enriched["preview"] = enriched["content"][:15] + "..." if len(enriched["content"]) > 15 else enriched["content"]
    words = len(enriched["content"].split())
    enriched["minutes_to_read"] = max(1, words // 200)  # minimum 1 minute
    return enriched

# Dictionary of articles by ID
ARTICLES = {a["id"]: enrich_article(a) for a in RAW_ARTICLES}

# Route to show an article
@app.route('/articles/<int:id>')
def show_article(id):
    # Increment or initialize page views
    session['page_views'] = session.get('page_views', 0) + 1

    # Check pageview limit
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Fetch article
    article = ARTICLES.get(id)
    if not article:
        return jsonify({"message": "Article not found"}), 404

    return jsonify(article)

# Route to clear session
@app.route('/clear')
def clear_session():
    session.clear()
    return jsonify({"message": "Session cleared"})

if __name__ == "__main__":
    app.run(debug=True)
