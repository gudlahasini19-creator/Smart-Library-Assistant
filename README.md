# 📚 Smart Library Assistant
### Intelligent Book Discovery Using Searching, Sorting, and Graph Algorithms
**College DAA (Design and Analysis of Algorithms) Hackathon Project**

---

## 1. Project Overview & Problem Statement

### The Problem
Traditional library search systems only support exact keyword lookups by title or author. When readers discover or finish a book, flat keyword search cannot help them discover meaningful thematic connections, shared authors, or related reading patterns.

### The Solution: Smart Library Assistant
Our system implements a complete algorithm-driven discovery engine:
1. **Binary Search ($O(\log n)$):** Fast indexed catalog lookups by title or author.
2. **Book Relationship Graph:** Models books as vertices ($V$) and relationships (author, genre, borrowing history) as weighted edges ($E$).
3. **Graph Traversal (BFS & DFS - $O(V + E)$):** Explores connected titles level-by-level (BFS) or follows deep thematic pathways (DFS).
4. **Merge Sort ($O(n \log n)$):** Ranks candidate recommendations by composite relationship score.

---

## 📑 Project Presentation & Documentation
- 📄 **[View DAA Project Report (PDF)](./PPT%20and%20DOCUMENTATION/Report.pdf)**
- 📊 **[Download Presentation Slides (PPTX)](./PPT%20and%20DOCUMENTATION/library%20management.pptx)**

---

## 2. Core Architecture & Pipeline

```
USER SEARCH
      ↓
BINARY SEARCH [O(log n)]
      ↓
MATCHING BOOK (Anchor Node)
      ↓
BOOK RELATIONSHIP GRAPH (Adjacency List)
      ↓
BFS / DFS TRAVERSAL [O(V + E)]
      ↓
MULTI-EDGE RECOMMENDATION SCORING
      ↓
MERGE SORT [O(n log n)]
      ↓
RECOMMENDATIONS ("Recommended for You")
```

---

## 3. Technology Stack

- **Backend:** Python 3, Flask (REST API)
- **Database:** SQLite 3 (Stores 105+ books, users, borrow history, and 1,700+ graph edges)
- **Frontend:** HTML5, CSS3, Modern Vanilla JavaScript (Fast, responsive, zero external frameworks)
- **Algorithms:** Custom Python implementations from scratch (No external ML or black-box libraries)

---

## 4. Project Structure

```
DAA HACK/
│
├── PPT and DOCUMENTATION/      # Project Report & Presentation Slides
│   ├── Report.pdf              # Full DAA Project Report
│   └── library management.pptx # Hackathon Presentation Slides
│
├── app.py                      # Flask REST API server & web routes
├── database.py                 # SQLite database schema, initialization & connection
├── seed_data.py                # Database seeder (105 curated books & 1,728 graph edges)
├── run.bat                     # 1-Click launcher (checks & installs Flask automatically)
├── README.md                   # Documentation, presentation guide & viva Q&A
│
├── algorithms/                 # Pure CS algorithm implementations
│   ├── __init__.py             # Python package marker
│   ├── binary_search.py        # Manual Binary Search O(log n) with step tracking
│   ├── sorting.py              # Manual Merge Sort O(n log n) with custom comparator
│   ├── graph.py                # BookGraph adjacency list, BFS & DFS O(V + E)
│   └── recommendation.py       # Multi-edge score aggregation & recommendation ranking
│
├── data/
│   └── library.db              # SQLite database (pre-seeded with 105 books)
│
├── templates/
│   └── index.html              # Clean, modern book discovery dashboard
│
└── static/
    ├── style.css               # Clean styling and responsive layout
    └── script.js               # Frontend controller (search, autocomplete, recommendations)
```

---

## 5. Core Algorithms & Complexity Analysis

| Algorithm | Role in Project | Time Complexity | Space Complexity | Implementation File |
| :--- | :--- | :--- | :--- | :--- |
| **Binary Search** | Title & author lookups | **$O(\log n)$** | $O(1)$ | `algorithms/binary_search.py` |
| **Merge Sort** | Ranking recommendation candidates | **$O(n \log n)$** | $O(n)$ | `algorithms/sorting.py` |
| **Breadth-First Search (BFS)** | Level-by-level neighbor discovery | **$O(V + E)$** | $O(V)$ | `algorithms/graph.py` |
| **Depth-First Search (DFS)** | Deep thematic path discovery | **$O(V + E)$** | $O(V)$ | `algorithms/graph.py` |
| **Adjacency List** | Graph representation | $O(1)$ edge insert | $O(V + E)$ | `algorithms/graph.py` |

---

## 6. How the Recommendation Score is Calculated

For any candidate book $B$ connected to the target book $A$:

$$\text{Score} = \text{BaseStrength} + \text{AuthorBonus} + \text{CategoryBonus} + \text{BorrowingBonus}$$

- **Same Author Bonus:** $+5.0$ points (e.g., J.K. Rowling sequels)
- **Same Category Bonus:** $+3.0$ points (e.g., Fantasy / Productivity)
- **Co-Borrowing Bonus:** $+1.5 \times \text{co\_borrow\_count}$ (from actual library transactions)
- **Thematic Link Bonus:** $+2.0$ points
- **Multi-Hop Decay:** Indirect connections (2-hop neighbors) receive a $50\%$ decay factor.

---

## 7. How to Run the Application

### Option A: 1-Click Launch (Windows)
Double-click **`run.bat`** in the folder. It will launch the Flask server automatically!

### Option B: Command Line

1. **Install Flask (if not already installed):**
   ```bash
   pip install flask
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 8. Hackathon Presentation & Viva Q&A Guide

**Q1: Why use Binary Search instead of standard linear search?**  
*Answer:* Linear search checks elements one-by-one taking $O(n)$ time. By pre-sorting our catalog in $O(n \log n)$, Binary Search finds any book or author in $O(\log n)$ time, cutting the search space in half with every comparison.

**Q2: Why use a Graph with BFS instead of simple SQL filtering?**  
*Answer:* Standard SQL `WHERE category = '...'` only matches single attributes. A Graph connects books through multiple relationship types simultaneously (author, genre, and co-borrowing history). BFS explores these relationships hop-by-hop ($O(V + E)$) to discover non-obvious cross-category recommendations.

**Q3: Why did you implement Merge Sort instead of QuickSort?**  
*Answer:* Merge Sort guarantees a worst-case time complexity of $O(n \log n)$ under all conditions, whereas QuickSort can degrade to $O(n^2)$ with adversarial or poor pivot choices. Merge Sort is also stable, preserving the relative order of books when recommendation scores are tied.

**Q4: How does borrowing history affect recommendations?**  
*Answer:* The SQLite database records user borrow transactions. When multiple users borrow both Book A and Book B, an aggregation calculates their co-borrowing frequency and dynamically creates or strengthens weighted edges in the Book Graph.
