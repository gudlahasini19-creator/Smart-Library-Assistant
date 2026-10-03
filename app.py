"""
Smart Library Assistant - Flask Application Server
College DAA Hackathon Project: Intelligent Book Discovery Using Searching, Sorting, and Graph Algorithms.
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import webbrowser

from database import init_db, is_database_seeded, get_connection
from seed_data import seed_database
from algorithms.binary_search import binary_search_books, binary_search_authors
from algorithms.sorting import merge_sort, sort_books_by
from algorithms.graph import build_graph_from_db
from algorithms.recommendation import get_recommendations

app = Flask(__name__)

# Disable all browser caching so updates are ALWAYS immediately visible!
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Global in-memory graph cache
GRAPH_INSTANCE = None

def get_graph():
    global GRAPH_INSTANCE
    if GRAPH_INSTANCE is None:
        GRAPH_INSTANCE = build_graph_from_db()
    return GRAPH_INSTANCE

def reload_graph():
    global GRAPH_INSTANCE
    GRAPH_INSTANCE = build_graph_from_db()
    return GRAPH_INSTANCE

# =========================================================================
# WEB ROUTES
# =========================================================================
@app.route("/")
def index():
    return render_template("index.html")

# =========================================================================
# API ENDPOINTS
# =========================================================================
@app.route("/api/books", methods=["GET"])
def api_get_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, category, year, description FROM books ORDER BY title ASC")
    books = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify({"books": books, "count": len(books)})


@app.route("/api/book/<int:book_id>", methods=["GET"])
def api_get_book(book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, category, year, description FROM books WHERE id = ?", (book_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": f"Book with ID {book_id} not found."}), 404
    book = dict(row)
    return jsonify(book)


@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": [], "count": 0}), 200

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, category, year, description FROM books")
    all_books = [dict(row) for row in cur.fetchall()]
    conn.close()

    # Search title and author using binary search
    title_matches, _ = binary_search_books(all_books, query)
    author_matches, _ = binary_search_authors(all_books, query)

    # Combine unique results
    combined_dict = {}
    for b in title_matches:
        combined_dict[b["id"]] = b
    for b in author_matches:
        combined_dict[b["id"]] = b

    results = list(combined_dict.values())
    return jsonify({"query": query, "count": len(results), "results": results})


@app.route("/api/recommend/<int:book_id>", methods=["GET"])
def api_recommend(book_id):
    traversal_mode = request.args.get("mode", "bfs").strip().lower()
    sort_by = request.args.get("sort_by", "relevance").strip().lower()
    top_n = request.args.get("top_n", 6, type=int)

    graph = get_graph()
    if book_id not in graph.books:
        return jsonify({"error": f"Book with ID {book_id} not found."}), 404

    data = get_recommendations(graph, book_id, traversal_mode=traversal_mode, top_n=top_n)
    if sort_by != "relevance" and data.get("recommendations"):
        data["recommendations"] = sort_books_by(data["recommendations"], criteria=sort_by)

    return jsonify(data)


@app.route("/api/graph/<int:book_id>", methods=["GET"])
def api_graph(book_id):
    traversal_mode = request.args.get("mode", "bfs").strip().lower()
    graph = get_graph()
    if book_id not in graph.books:
        return jsonify({"error": "Book not found."}), 404

    trav = graph.bfs(book_id, max_depth=2) if traversal_mode == "bfs" else graph.dfs(book_id, max_depth=3)
    visited_nodes = trav["traversal_order"]
    levels = trav["levels"]

    nodes = []
    for bid in visited_nodes:
        b = graph.books[bid]
        nodes.append({
            "id": bid,
            "title": b["title"],
            "author": b["author"],
            "category": b["category"],
            "year": b["year"],
            "level": levels.get(bid, 0),
            "is_center": (bid == book_id)
        })

    visited_set = set(visited_nodes)
    edges = []
    seen_edges = set()

    for u in visited_nodes:
        for edge in graph.adj.get(u, []):
            v = edge["target"]
            if v in visited_set:
                edge_key = tuple(sorted([u, v])) + (edge["type"],)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "source": u,
                        "target": v,
                        "type": edge["type"],
                        "strength": edge["strength"]
                    })

    return jsonify({
        "center_book": graph.books[book_id],
        "nodes": nodes,
        "edges": edges
    })


@app.route("/api/stats", methods=["GET"])
def api_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM books")
    book_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT category) FROM books")
    category_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM borrow_history")
    borrow_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM book_relationships")
    relationship_count = cur.fetchone()[0]
    conn.close()

    graph = get_graph()
    return jsonify({
        "books_count": book_count,
        "graph_nodes": len(graph.books),
        "relationships_count": relationship_count,
        "borrow_records": borrow_count,
        "categories_count": category_count
    })


# =========================================================================
# APPLICATION LAUNCHER
# =========================================================================
def run_app():
    init_db()
    if not is_database_seeded():
        print("[*] Seeding database...")
        seed_database()

    reload_graph()
    port = 5000
    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print("  SMART LIBRARY ASSISTANT")
    print(f"[*] Running at: {url}")
    print("[*] Press Ctrl+C to stop.")
    print("=" * 60)

    if "--no-browser" not in sys.argv:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    app.run(host="127.0.0.1", port=port, debug=False)

if __name__ == "__main__":
    run_app()
