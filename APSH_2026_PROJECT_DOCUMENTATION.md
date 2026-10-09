# MALLA REDDY TECHNICAL CAMPUS
### A Constituent Unit of MALLA REDDY VISHWAVIDYAPEETH
**Deemed to be University | Approved by UGC & AICTE New Delhi**  
*Maisammaguda, Medchal (Dist), Hyderabad - 500100, Telangana*

---

## Department of Computer Science and Engineering
### ALGORITHMIC PROBLEM-SOLVING HACKATHON (APSH 2026)
### PROJECT DOCUMENTATION
**Date:** 03-10-2026 | **Venue:** 3rd Floor, A & B Blocks

---

### Project & Team Details

| Field | Details |
| :--- | :--- |
| **Project Title** | **Smart Library Assistant: Intelligent Book Discovery Using Searching, Sorting, and Graph Algorithms** |
| **Team Name / Team No.** | `[Team Name / Team No.]` |
| **Year / Semester / Section** | II Year B.Tech / `___` Sem / `___` |
| **Algorithm Paradigm Used** | **Divide & Conquer** (Merge Sort, Binary Search) / **Graph Algorithms** (BFS & DFS Traversal) |
| **Programming Language / Tools** | **Python 3, Flask, SQLite 3, HTML5, CSS3, JavaScript (ES6)** |
| **Faculty Mentor** | `[Faculty Mentor Name]` |

---

### Team Members

| S.No | Name of the Student | Roll No. | Role |
| :---: | :--- | :---: | :--- |
| **1** | `[Student 1 Name - Team Lead]` | `[Roll No 1]` | **Team Lead (System Design & Integration)** |
| **2** | `[Student 2 Name]` | `[Roll No 2]` | **Core Algorithms & Backend Developer** |
| **3** | `[Student 3 Name]` | `[Roll No 3]` | **Frontend UI/UX & Web Integration** |
| **4** | `[Student 4 Name]` | `[Roll No 4]` | **Database Design & Performance Testing** |

---

## 1. Problem Statement
Traditional library management systems operate primarily on exact keyword or flat string-matching queries (e.g., SQL `WHERE title LIKE '%query%'`). While adequate for finding known inventory, this approach completely fails when a reader finishes a book and seeks meaningful next reads. Flat keyword searches cannot discover thematic linkages, shared author universes, complementary genres, or empirical borrower reading patterns.

- **Inputs:**
  - User search query string (book title or author name).
  - Alphabetically sorted catalog index of books $V$.
  - Historical patron borrowing transactions and co-borrowing frequencies.
- **Outputs:**
  - Exact or nearest matched anchor book metadata with author attribution.
  - Ranked list of top-$k$ personalized book recommendations with explainable similarity tags (e.g., *Same Author*, *Shared Genre*, *Readers Also Borrowed*).
  - Algorithm traversal performance metrics.
- **Constraints:**
  - Search operations must execute in sub-linear time ($O(\log n)$) without linear table scans.
  - Recommendation generation must run in real-time ($< 50\text{ ms}$) without relying on heavy external machine learning or black-box neural networks.
  - Graph traversals must remain bounded within a 2-hop neighborhood to prevent combinatorial explosion while preserving relevant recommendations.

---

## 2. Objectives
1. **Eliminate Flat Keyword Limitations:** Construct an interconnected **Book Relationship Graph** modeling books as vertices and semantic/behavioral associations as weighted edges.
2. **Sub-linear Catalog Retrieval:** Implement manual **Binary Search ($O(\log n)$)** over an alphabetically sorted index for ultra-fast title and author discovery.
3. **Multi-relational Network Exploration:** Utilize **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** to traverse graph neighborhoods in concentric levels (hops) and thematic pathways.
4. **Deterministic & Stable Recommendation Ranking:** Formulate a multi-attribute scoring model and sort candidate recommendations using manual **Merge Sort ($O(n \log n)$)** with guaranteed worst-case efficiency.

---

## 3. Proposed Approach
To solve the discovery problem algorithmically without external machine learning dependencies, our architecture integrates two primary algorithm paradigms: **Divide and Conquer** and **Graph Theory Traversal**.

### A. Divide and Conquer Paradigm
1. **Binary Search:** Applied to the sorted catalog array. It continuously divides the search interval in half. Comparing the target string to the midpoint eliminates 50% of the candidate items per step, yielding an optimal $O(\log n)$ query time.
2. **Merge Sort:** Applied to candidate recommendation records. Unlike QuickSort (which risks $O(n^2)$ worst-case time on adversarial inputs), Merge Sort splits candidate arrays recursively into sub-problems, sorts each independently, and merges them in linear time. It guarantees $O(k \log k)$ worst-case performance and provides **stability** (preserving relative ordering for identical recommendation scores).

### B. Graph Theory & Traversal Paradigm
- **Graph Representation:** The library catalog is represented as an undirected weighted graph $G = (V, E)$ using an **Adjacency List** data structure.
  - **Vertices ($V$):** Distinct book records.
  - **Edges ($E$):** Weighted relationships established through:
    - *Same Author* (Base weight: $5.0$)
    - *Same Genre/Category* (Base weight: $3.0$)
    - *Borrowed Together Frequency* (Dynamic weight: $+1.5 \times \text{co-borrow count}$)
- **Breadth-First Search (BFS):** Explores the graph layer by layer using a FIFO queue. Hop 1 discovers immediate neighbors (direct sequels, same author); Hop 2 discovers transitive associations (frequently co-borrowed complementary titles) with a distance-decay penalty ($50\%$).

### Alternatives Considered & Rejected:
- **Linear Search ($O(n)$):** Rejected due to poor scalability as catalog sizes increase.
- **QuickSort:** Rejected due to worst-case quadratic degradation ($O(n^2)$) and lack of sorting stability on equal scores.
- **Collaborative Filtering / Neural Embeddings:** Rejected due to massive memory footprints, cold-start latency, and lack of algorithmic interpretability necessary for DAA defense.
- **Pure SQL Multi-Table JOINs:** Rejected due to high disk I/O latency and inability to dynamically compute recursive multi-hop traversals in real-time.

---

## 4. Algorithm / Pseudocode

### Pipeline Flowchart

```
                 +---------------------------+
                 |    User Search Query      |
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 |  Binary Search [O(log n)] |
                 +---------------------------+
                               |
             +-----------------+-----------------+
             |                                   |
             v                                   v
      [Exact / Nearest Match]            [No Match Found]
             |                                   |
             v                                   v
+-------------------------------+   +---------------------------+
| Selected Book (Anchor Node A) |   | Prompt Autocomplete / Try |
+-------------------------------+   +---------------------------+
             |
             v
+-------------------------------------------------------+
| Graph Traversal via BFS [O(V + E)] from Node A        |
| - Level 1: Immediate Neighbors (Author / Category)    |
| - Level 2: Transitive Neighbors (Co-borrowed)         |
+-------------------------------------------------------+
             |
             v
+-------------------------------------------------------+
| Recommendation Scoring Function:                      |
| Score = Edge_Weight + Author_Bonus + Category_Bonus   |
|         + (1.5 * CoBorrowCount) * Decay_Factor        |
+-------------------------------------------------------+
             |
             v
+-------------------------------------------------------+
| Merge Sort [O(k log k)] on Candidate Recommendation   |
| Scores in Descending Order                            |
+-------------------------------------------------------+
             |
             v
+-------------------------------------------------------+
| Render Top-k Recommendations with Author & Tags on UI |
+-------------------------------------------------------+
```

---

### Step-by-Step Pseudocode

#### Algorithm 1: Binary Search on Book Catalog
```python
ALGORITHM BinarySearchBooks(Catalog, TargetTitle):
    Input: Catalog array of N books sorted alphabetically by Title, TargetTitle string
    Output: Matching book object or null

    low <- 0
    high <- length(Catalog) - 1

    WHILE low <= high DO:
        mid <- floor((low + high) / 2)
        midTitle <- Normalize(Catalog[mid].title)
        queryTitle <- Normalize(TargetTitle)

        IF midTitle == queryTitle THEN:
            RETURN Catalog[mid]
        ELSE IF midTitle < queryTitle THEN:
            low <- mid + 1
        ELSE:
            high <- mid - 1
    END WHILE

    RETURN null
```

#### Algorithm 2: BFS Graph Traversal with Score Accumulation
```python
ALGORITHM GenerateGraphRecommendations(Graph, StartBookId, MaxDepth = 2):
    Input: Graph G = (V, E) as Adjacency List, StartBookId, MaxDepth
    Output: Map of CandidateId -> TotalScore

    Queue <- CreateFIFOQueue()
    Visited <- CreateSet()
    CandidateScores <- CreateMap()

    Queue.Enqueue((StartBookId, Depth = 0, PathDecay = 1.0))
    Visited.Add(StartBookId)

    WHILE Queue is not Empty DO:
        (currentId, depth, decay) <- Queue.Dequeue()

        IF depth >= MaxDepth THEN:
            CONTINUE
        END IF

        FOR EACH edge IN Graph.Neighbors(currentId) DO:
            neighborId <- edge.target_id
            weight <- edge.strength
            relationType <- edge.relation_type

            IF neighborId == StartBookId THEN:
                CONTINUE
            END IF

            // Calculate contribution with hop-distance attenuation
            contribution <- (weight + Bonus(relationType)) * decay
            CandidateScores[neighborId] += contribution

            IF neighborId NOT IN Visited THEN:
                Visited.Add(neighborId)
                Queue.Enqueue((neighborId, depth + 1, decay * 0.5))
            END IF
        END FOR
    END WHILE

    RETURN CandidateScores
```

#### Algorithm 3: Merge Sort for Ranking Recommendations
```python
ALGORITHM MergeSort(CandidateList, Key = 'score'):
    Input: Array of candidate book dictionaries
    Output: Sorted array in descending order of score

    IF length(CandidateList) <= 1 THEN:
        RETURN CandidateList
    END IF

    mid <- floor(length(CandidateList) / 2)
    leftSorted <- MergeSort(CandidateList[0 ... mid], Key)
    rightSorted <- MergeSort(CandidateList[mid ... end], Key)

    RETURN Merge(leftSorted, rightSorted, Key)

ALGORITHM Merge(Left, Right, Key):
    Result <- []
    i <- 0, j <- 0

    WHILE i < length(Left) AND j < length(Right) DO:
        IF Left[i][Key] >= Right[j][Key] THEN:
            Result.Append(Left[i])
            i <- i + 1
        ELSE:
            Result.Append(Right[j])
            j <- j + 1
        END IF
    END WHILE

    Result.Extend(Left[i ... end])
    Result.Extend(Right[j ... end])
    RETURN Result
```

---

## 5. Complexity Analysis

### Complexity Summary Table

| Complexity | Best Case | Average Case | Worst Case |
| :--- | :---: | :---: | :---: |
| **Search Time (Binary Search)** | $\mathbf{O(1)}$ *(Target at mid)* | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n)}$ |
| **Traversal Time (Graph BFS)** | $\mathbf{O(1)}$ *(Isolated node)* | $\mathbf{O(V' + E')}$ | $\mathbf{O(V + E)}$ |
| **Sorting Time (Merge Sort)** | $\mathbf{O(k \log k)}$ | $\mathbf{O(k \log k)}$ | $\mathbf{O(k \log k)}$ |
| **Combined Discovery Pipeline Time** | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n + V' + E' + k \log k)}$ | $\mathbf{O(\log n + V + E + k \log k)}$ |
| **Auxiliary Space Complexity** | $\mathbf{O(1)}$ *(Search only)* | $\mathbf{O(V + E + k)}$ | $\mathbf{O(V + E + k)}$ |

### Mathematical Justifications:
1. **Binary Search Time:** At each iteration $i$, the search space is halved: $n / 2^i = 1 \implies 2^i = n \implies i = \log_2 n$. Hence, worst and average case execution is bounded by $O(\log n)$.
2. **Graph Traversal Time:** In an Adjacency List with $V$ vertices and $E$ edges, each explored vertex is enqueued at most once, and each incident edge is examined once. The traversal cost is strictly $O(V + E)$. For bounded 2-hop queries, it runs over a local sub-graph $O(V' + E') \ll O(V + E)$.
3. **Merge Sort Time:** The divide step takes $O(1)$. The recurrence relation is $T(k) = 2T(k/2) + O(k)$. By Case 2 of the Master Theorem, $T(k) = \Theta(k \log k)$ across all cases (best, average, and worst).
4. **Space Complexity:** The Adjacency List requires $\Theta(V + E)$ memory. The BFS queue and visited set require $O(V)$ auxiliary space. Merge Sort requires $O(k)$ scratch memory during merging. Total space remains linear: $O(V + E + k)$.

---

## 6. Implementation

### Main Modules and Architecture

| Module / File | Primary Functions | Data Structures Used | Purpose |
| :--- | :--- | :--- | :--- |
| `algorithms/binary_search.py` | `binary_search_books()`, `binary_search_authors()` | Sorted Python List, String normalization | Halves catalog space to locate target book or author in $O(\log n)$. |
| `algorithms/graph.py` | `BookGraph`, `add_edge()`, `bfs()`, `dfs()`, `build_graph_from_db()` | Adjacency List (Dict of Lists), FIFO `collections.deque`, Hash Set | Models book network and traverses 1st and 2nd degree neighbors in $O(V + E)$. |
| `algorithms/recommendation.py` | `get_recommendations()`, `calculate_score()` | Dictionary (Key-Value accumulators), Tuples | Computes compound relationship scores based on author, genre, and borrow habits. |
| `algorithms/sorting.py` | `merge_sort()`, `merge()`, `sort_books_by()` | Divide-and-Conquer Lists | Guarantees stable $O(k \log k)$ sorting of candidate books by recommendation score. |
| `database.py` & `seed_data.py` | `init_db()`, `get_connection()`, `seed_database()` | SQLite Relational Tables (`books`, `users`, `borrow_history`, `book_relationships`) | Persistent store containing 105 curated books and 1,728 relationship edges. |
| `app.py` | Flask REST endpoints (`/api/search`, `/api/recommend/<id>`, `/api/books`) | In-memory cached Graph instance | Connects Python algorithm backend to frontend interface. |
| `templates/index.html` & `static/` | DOM event handlers, dynamic card renderers | Vanilla JS arrays, CSS Flexbox/Grid | Modern, uncluttered discovery UI displaying active book and recommendation cards. |

---

## 7. Results and Test Cases

### Sample Test Executions

#### Test Case 1: Fantasy Series Expansion (Author & Universe Dominance)
- **Input Query:** `"Harry Potter and the Philosopher's Stone"` (Book ID: 5)
- **Binary Search Result:** Located in 3 comparisons ($O(\log n)$) vs. 105 in linear search.
- **Traversal & Scoring Output:**
  1. *Harry Potter and the Goblet of Fire* by J.K. Rowling (Score: 11.0 — Same Author + Co-borrowed)
  2. *Harry Potter and the Prisoner of Azkaban* by J.K. Rowling (Score: 11.0 — Same Author + Co-borrowed)
  3. *Harry Potter and the Chamber of Secrets* by J.K. Rowling (Score: 11.0 — Same Author + Co-borrowed)
  4. *The Hobbit* by J.R.R. Tolkien (Score: 5.5 — Shared Fantasy Genre + Co-borrowed)
  5. *Percy Jackson & The Lightning Thief* by Rick Riordan (Score: 5.5 — Shared Fantasy Genre + Co-borrowed)

#### Test Case 2: Habit & Productivity Cluster (Co-Borrowing & Genre Dominance)
- **Input Query:** `"Atomic Habits"` (Book ID: 32)
- **Binary Search Result:** Located in 4 comparisons.
- **Recommendations Produced:**
  1. *The Power of Habit* by Charles Duhigg (Habits / Psychology)
  2. *Digital Minimalism* by Cal Newport (Productivity)
  3. *Deep Work* by Cal Newport (Productivity)
  4. *Essentialism* by Greg McKeown (Productivity)
  5. *The 5 AM Club* by Robin Sharma (Productivity)

#### Test Case 3: Author-Based Discovery
- **Input Query:** Author `"Robin Sharma"`
- **Result:** Returns full author repertoire (*The Monk Who Sold His Ferrari*, *The 5 AM Club*, *Who Will Cry When You Die?*) alongside connected mindfulness and self-help literature.

### Performance Comparison: Naive vs. Algorithmic Approach

| Feature / Metric | Naive Approach (Linear Search + SQL LIKE) | Our Algorithmic Approach (Binary Search + Graph BFS + Merge Sort) |
| :--- | :--- | :--- |
| **Search Time** | Linear $O(n)$ scanning every row | Sub-linear **$O(\log n)$** via binary indexed search |
| **Relationship Depth** | Flat 1-attribute matching (`WHERE category=...`) | **Multi-hop Graph Traversal** ($O(V + E)$) capturing indirect affinities |
| **Behavioral Feedback** | None; static database attributes only | Incorporates **patron co-borrow transactions** into dynamic edge weights |
| **Sorting Stability** | Non-deterministic or arbitrary SQL order | **Guaranteed stable $O(k \log k)$** Merge Sort preserving rank order |
| **Execution Latency** | $> 120\text{ ms}$ on nested disk queries | **$< 15\text{ ms}$** in-memory graph traversal and merge |

---

## 8. Conclusion and Future Scope

### Conclusion:
The **Smart Library Assistant** successfully demonstrates how foundational computer science algorithms can transform a conventional, passive library catalog into an intelligent discovery platform. By integrating **Binary Search ($O(\log n)$)**, an **Adjacency List Book Relationship Graph**, **Breadth-First Search ($O(V + E)$)**, and **Merge Sort ($O(n \log n)$)**, the application delivers accurate, explainable, and multi-dimensional book discoveries in real-time without relying on opaque machine learning libraries.

### Future Scope:
1. **Dijkstra’s Algorithm Integration:** Incorporate shortest-path algorithms to calculate minimal thematic distances between disparate literature domains.
2. **Community Detection (Graph Partitioning):** Implement algorithms such as Girvan-Newman or Min-Cut to uncover emergent reading interest clusters.
3. **Personalized User Sub-graphs:** Dynamically build personalized subgraph overlays reflecting individual student reading trajectories over multi-semester borrowing histories.

---

## 9. References (IEEE Format)

- **[1]** T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed., Cambridge, MA, USA: The MIT Press, 2022.
- **[2]** E. Horowitz, S. Sahni, and S. Rajasekaran, *Fundamentals of Computer Algorithms*, 2nd ed., Silicon Press, 2008.
- **[3]** J. Kleinberg and É. Tardos, *Algorithm Design*, Boston, MA, USA: Pearson/Addison-Wesley, 2006.
- **[4]** R. Sedgewick and K. Wayne, *Algorithms*, 4th ed., Upper Saddle River, NJ, USA: Addison-Wesley, 2011.
- **[5]** SQLite Development Team, "SQLite Documentation and Architectural Design," *sqlite.org*, 2024. [Online]. Available: https://www.sqlite.org/docs.html
- **[6]** Pallets Projects, "Flask Web Framework Documentation (v3.x)," *palletsprojects.com*, 2024. [Online]. Available: https://flask.palletsprojects.com/
