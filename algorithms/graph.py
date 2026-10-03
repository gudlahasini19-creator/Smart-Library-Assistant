"""
Algorithm: Book Relationship Graph, BFS & DFS Traversal
Time Complexity: 
  - BFS Traversal: O(V + E)
  - DFS Traversal: O(V + E)
Space Complexity: O(V) for visited set, queue/recursion stack

Purpose:
Manual graph data structure representing books as nodes and relationships as weighted edges.
Implements Breadth-First Search (BFS) and Depth-First Search (DFS) from scratch.
"""

from collections import deque
import sqlite3
from database import get_connection

class BookGraph:
    """
    Graph representation using an Adjacency List.
    No external libraries (NetworkX, etc.) used. Pure Python dictionaries and lists.
    
    Structure:
    self.adj = {
        book_id: [
            {"target": neighbor_id, "type": relationship_type, "strength": weight}
        ]
    }
    """
    def __init__(self):
        self.adj = {}       # book_id -> list of edge dicts
        self.books = {}     # book_id -> book dict info

    def add_node(self, book_id, book_info):
        """Adds a book node to the graph."""
        if book_id not in self.adj:
            self.adj[book_id] = []
        self.books[book_id] = book_info

    def add_edge(self, u, v, rel_type, strength):
        """
        Adds or combines a weighted relationship edge between book u and book v.
        If an edge already exists, strengthens the connection.
        """
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        # Check if an edge of this type already exists
        for edge in self.adj[u]:
            if edge["target"] == v and edge["type"] == rel_type:
                edge["strength"] = max(edge["strength"], strength)
                return

        self.adj[u].append({
            "target": v,
            "type": rel_type,
            "strength": strength
        })

    def get_neighbors(self, book_id):
        """Returns sorted neighbors of book_id by relationship strength descending."""
        neighbors = self.adj.get(book_id, [])
        return sorted(neighbors, key=lambda e: e["strength"], reverse=True)

    # =========================================================================
    # Breadth-First Search (BFS)
    # Time Complexity: O(V + E)
    # Explores book relationships level by level (concentric rings)
    # =========================================================================
    def bfs(self, start_book_id, max_depth=2):
        """
        Performs Breadth-First Search starting from start_book_id.
        
        Parameters:
            start_book_id (int): Center book to explore outward from.
            max_depth (int): Maximum hop distance (default 2 hops).
            
        Returns:
            dict: {
                "traversal_order": list of book IDs in visited sequence,
                "levels": dict of book_id -> hop level,
                "traversal_edges": list of edges traversed during BFS,
                "steps": list of detailed step logs for DAA judge explanation
            }
        """
        if start_book_id not in self.adj:
            return {"traversal_order": [], "levels": {}, "traversal_edges": [], "steps": []}

        visited = {start_book_id}
        queue = deque([(start_book_id, 0)])  # Queue stores tuples of (book_id, depth)
        levels = {start_book_id: 0}
        traversal_order = []
        traversal_edges = []
        steps = []

        step_counter = 0

        while queue:
            curr_id, depth = queue.popleft()
            traversal_order.append(curr_id)
            curr_title = self.books.get(curr_id, {}).get("title", f"Book #{curr_id}")

            step_counter += 1
            steps.append({
                "step": step_counter,
                "algorithm": "BFS",
                "action": "VISIT_NODE",
                "book_id": curr_id,
                "title": curr_title,
                "depth": depth,
                "queue_size": len(queue),
                "explanation": f"Popped '{curr_title}' from queue at Level/Hop {depth}."
            })

            # If reached max depth, do not explore further descendants
            if depth >= max_depth:
                continue

            # Explore neighbors sorted by edge strength
            for edge in self.get_neighbors(curr_id):
                neighbor_id = edge["target"]
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    levels[neighbor_id] = depth + 1
                    queue.append((neighbor_id, depth + 1))

                    edge_record = {
                        "source": curr_id,
                        "target": neighbor_id,
                        "type": edge["type"],
                        "strength": edge["strength"]
                    }
                    traversal_edges.append(edge_record)

                    neighbor_title = self.books.get(neighbor_id, {}).get("title", f"Book #{neighbor_id}")
                    steps.append({
                        "step": step_counter,
                        "algorithm": "BFS",
                        "action": "ENQUEUE_NEIGHBOR",
                        "from_title": curr_title,
                        "to_title": neighbor_title,
                        "relation": edge["type"],
                        "strength": edge["strength"],
                        "explanation": f"Discovered edge: '{curr_title}' -> '{neighbor_title}' via [{edge['type']}, strength={edge['strength']}]. Added to queue for Level {depth + 1}."
                    })

        return {
            "traversal_order": traversal_order,
            "levels": levels,
            "traversal_edges": traversal_edges,
            "steps": steps
        }

    # =========================================================================
    # Depth-First Search (DFS)
    # Time Complexity: O(V + E)
    # Explores book connections deeply along branches before backtracking
    # =========================================================================
    def dfs(self, start_book_id, max_depth=3):
        """
        Performs Depth-First Search starting from start_book_id using explicit recursion.
        
        Parameters:
            start_book_id (int): Center book to explore deep thematic branches from.
            max_depth (int): Maximum depth limit.
            
        Returns:
            dict: {
                "traversal_order": list of book IDs visited,
                "levels": dict of book_id -> hop level,
                "traversal_edges": list of edges traversed during DFS,
                "steps": list of detailed step logs
            }
        """
        if start_book_id not in self.adj:
            return {"traversal_order": [], "levels": {}, "traversal_edges": [], "steps": []}

        visited = set()
        traversal_order = []
        traversal_edges = []
        levels = {}
        steps = []
        step_counter = [0]

        def _dfs_recursive(curr_id, depth):
            if depth > max_depth or curr_id in visited:
                return

            visited.add(curr_id)
            levels[curr_id] = depth
            traversal_order.append(curr_id)
            step_counter[0] += 1

            curr_title = self.books.get(curr_id, {}).get("title", f"Book #{curr_id}")
            steps.append({
                "step": step_counter[0],
                "algorithm": "DFS",
                "action": "DFS_VISIT",
                "book_id": curr_id,
                "title": curr_title,
                "depth": depth,
                "explanation": f"Visiting deeper branch: '{curr_title}' at Depth {depth}."
            })

            # Recurse through neighbors
            for edge in self.get_neighbors(curr_id):
                neighbor_id = edge["target"]
                if neighbor_id not in visited:
                    traversal_edges.append({
                        "source": curr_id,
                        "target": neighbor_id,
                        "type": edge["type"],
                        "strength": edge["strength"]
                    })
                    _dfs_recursive(neighbor_id, depth + 1)

        _dfs_recursive(start_book_id, 0)

        return {
            "traversal_order": traversal_order,
            "levels": levels,
            "traversal_edges": traversal_edges,
            "steps": steps
        }


def build_graph_from_db():
    """
    Constructs the BookGraph by querying the SQLite database.
    Loads nodes from `books` and edges from `book_relationships`.
    """
    conn = get_connection()
    cur = conn.cursor()

    graph = BookGraph()

    # 1. Load all books as nodes
    cur.execute("SELECT id, title, author, category, year, description FROM books")
    for row in cur.fetchall():
        graph.add_node(row["id"], dict(row))

    # 2. Load all relationships as weighted edges
    cur.execute("SELECT book_id_1, book_id_2, relationship_type, strength FROM book_relationships")
    for row in cur.fetchall():
        graph.add_edge(row["book_id_1"], row["book_id_2"], row["relationship_type"], row["strength"])

    conn.close()
    return graph
