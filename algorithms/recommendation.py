"""
Algorithm: Recommendation Scoring & Ranking
Time Complexity: 
  - Graph neighborhood discovery: O(V + E)
  - Merge Sort Ranking: O(k log k) where k is number of candidate recommendations
Space Complexity: O(k)

Purpose:
Aggregates multi-edge graph weights, bonuses for shared author/category and real borrowing
history, then applies Merge Sort to present the top ranked recommendations.
"""

from .sorting import merge_sort

def get_recommendations(graph, start_book_id, traversal_mode="bfs", top_n=6):
    """
    Computes and ranks book recommendations starting from a searched book.
    
    Parameters:
        graph (BookGraph): The book relationship graph instance.
        start_book_id (int): The target book node.
        traversal_mode (str): 'bfs' (level-by-level) or 'dfs' (deep chain).
        top_n (int): Number of top recommendations to return.
        
    Returns:
        dict: Contains start book details, traversal summary, and Merge-Sorted recommendations.
    """
    if start_book_id not in graph.books:
        return {"error": "Book not found", "recommendations": []}

    start_book = graph.books[start_book_id]

    # 1. Run Graph Traversal (BFS or DFS)
    if traversal_mode.lower() == "dfs":
        traversal_result = graph.dfs(start_book_id, max_depth=3)
    else:
        traversal_result = graph.bfs(start_book_id, max_depth=2)

    visited_ids = traversal_result["traversal_order"]
    levels = traversal_result["levels"]

    # 2. Multi-Edge Recommendation Scoring
    # score = relationship_strength + same_category_bonus + same_author_bonus + borrowing_bonus
    candidates = {}

    # Gather direct edge relationships
    for edge in graph.adj.get(start_book_id, []):
        neighbor_id = edge["target"]
        if neighbor_id == start_book_id:
            continue

        if neighbor_id not in candidates:
            candidates[neighbor_id] = {
                "base_strength": 0.0,
                "author_bonus": 0.0,
                "category_bonus": 0.0,
                "borrowing_bonus": 0.0,
                "reasons": []
            }

        rel_type = edge["type"]
        strength = edge["strength"]

        if rel_type == "same_author":
            candidates[neighbor_id]["author_bonus"] += 5.0
            candidates[neighbor_id]["reasons"].append(f"Same Author: {start_book['author']} (+5)")
        elif rel_type == "same_category":
            candidates[neighbor_id]["category_bonus"] += 3.0
            candidates[neighbor_id]["reasons"].append(f"Same Category: {start_book['category']} (+3)")
        elif rel_type == "borrowed_together":
            candidates[neighbor_id]["borrowing_bonus"] += strength
            candidates[neighbor_id]["reasons"].append(f"Frequently borrowed together (+{strength})")
        elif rel_type == "similar_book":
            candidates[neighbor_id]["base_strength"] += strength
            candidates[neighbor_id]["reasons"].append("Thematic literary connection (+2)")

    # 3. Consider multi-hop graph neighbors discovered during traversal (Hop 2 decay)
    for edge in traversal_result["traversal_edges"]:
        u = edge["source"]
        v = edge["target"]
        # If v is a 2-hop neighbor connected through u
        if u != start_book_id and v != start_book_id:
            if v not in candidates:
                candidates[v] = {
                    "base_strength": 0.0,
                    "author_bonus": 0.0,
                    "category_bonus": 0.0,
                    "borrowing_bonus": 0.0,
                    "reasons": []
                }
            # Indirect graph connection weight (decayed by 50%)
            decayed_strength = round(edge["strength"] * 0.5, 1)
            candidates[v]["base_strength"] += decayed_strength
            via_title = graph.books.get(u, {}).get("title", f"Book #{u}")
            candidates[v]["reasons"].append(f"Connected through '{via_title}' (+{decayed_strength})")

    # 4. Compute total composite recommendation score
    candidate_list = []
    for book_id, data in candidates.items():
        if book_id == start_book_id or book_id not in graph.books:
            continue

        book_info = dict(graph.books[book_id])
        
        # Check explicit category & author matches if not already captured
        if book_info["author"].lower() == start_book["author"].lower() and data["author_bonus"] == 0:
            data["author_bonus"] = 5.0
            data["reasons"].append(f"Same Author: {start_book['author']} (+5)")
        if book_info["category"].lower() == start_book["category"].lower() and data["category_bonus"] == 0:
            data["category_bonus"] = 3.0
            data["reasons"].append(f"Same Category: {start_book['category']} (+3)")

        total_score = round(
            data["base_strength"] + data["author_bonus"] + data["category_bonus"] + data["borrowing_bonus"], 
            1
        )

        book_info["score"] = total_score
        book_info["hop_level"] = levels.get(book_id, 1)
        # Deduplicate reasons list
        book_info["reasons"] = list(dict.fromkeys(data["reasons"]))
        candidate_list.append(book_info)

    # 5. SORTING ALGORITHM: Merge Sort
    # Time Complexity: O(k log k)
    # Sorts candidates strictly descending by recommendation score
    sorted_recommendations = merge_sort(
        candidate_list, 
        key_func=lambda b: (b["score"], b.get("year", 0)), 
        reverse=True
    )

    return {
        "start_book": start_book,
        "traversal_mode": traversal_mode.upper(),
        "traversal_order": visited_ids,
        "traversal_steps": traversal_result["steps"],
        "recommendations": sorted_recommendations[:top_n]
    }
