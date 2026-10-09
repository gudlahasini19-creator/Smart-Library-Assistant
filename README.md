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
- 📄 **[Official Hackathon Documentation (APSH 2026)](./APSH_2026_PROJECT_DOCUMENTATION.md)**
- 📄 **[View DAA Project Report (PDF)](./Report.pdf)**
- 📊 **[Download Presentation Slides (PPTX)](./library%20management.pptx)**

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
├── APSH_2026_PROJECT_DOCUMENTATION.md  # Official 3-Page Hackathon Documentation
├── Report.pdf                  # Full DAA Project Report (PDF)
├── library management.pptx     # Hackathon Presentation Slides (PPTX)
├── app.py                      # Flask REST API server & web routes
├── database.py                 # SQLite database schema, initialization & connection
├── seed_data.py                # Database seeder (105 curated books & 1,728 graph edges)
├── requirements.txt            # Minimal dependencies (Flask)
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

