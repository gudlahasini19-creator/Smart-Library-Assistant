// Smart Library Assistant - Simple & Clean Discovery Controller

let currentBookId = 5;
let catalogBooks = [];

window.addEventListener('DOMContentLoaded', () => {
  fetchCatalog();
  loadBook(5); // Default initial view: Harry Potter (ID 5)
});

// 1. Fetch Book Catalog for Autocomplete
async function fetchCatalog() {
  try {
    const res = await fetch('/api/books');
    const data = await res.json();
    catalogBooks = data.books || [];
  } catch (err) {
    console.error("Failed to load catalog", err);
  }
}

// 2. Search Autocomplete
const searchInput = document.getElementById('searchInput');
const dropdown = document.getElementById('autocompleteDropdown');

searchInput.addEventListener('input', (e) => {
  const query = e.target.value.trim().toLowerCase();
  if (!query) {
    dropdown.style.display = 'none';
    return;
  }

  const matches = catalogBooks.filter(b => 
    b.title.toLowerCase().includes(query) || b.author.toLowerCase().includes(query)
  ).slice(0, 6);

  if (matches.length === 0) {
    dropdown.innerHTML = '<div class="drop-item" style="color: #94a3b8;">No matching books or authors found</div>';
  } else {
    dropdown.innerHTML = matches.map(b => `
      <div class="drop-item" onclick="selectBook(${b.id}, '${escapeQuote(b.title)}')">
        <strong>${escapeHtml(b.title)}</strong>
        <div style="font-size: 0.78rem; color: #a5b4fc; margin-top: 2px;">
          ✍️ ${escapeHtml(b.author)} • <span style="color: #cbd5e1;">${escapeHtml(b.category)}</span>
        </div>
      </div>
    `).join('');
  }
  dropdown.style.display = 'block';
});

// Close autocomplete when clicking outside
document.addEventListener('click', (e) => {
  if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
    dropdown.style.display = 'none';
  }
});

function selectBook(id, title) {
  searchInput.value = title;
  dropdown.style.display = 'none';
  closeMatches();
  loadBook(id);
}

// 3. Trigger Search & Display Matches with Author
async function triggerSearch() {
  const query = searchInput.value.trim();
  if (!query) return;
  dropdown.style.display = 'none';

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    const results = data.results || [];

    if (results.length > 0) {
      renderSearchMatches(results, query);
      // Immediately load the first match
      loadBook(results[0].id);
    } else {
      document.getElementById('searchMatchesContainer').style.display = 'none';
    }
  } catch (err) {
    console.error("Search failed", err);
  }
}

function renderSearchMatches(books, query) {
  const container = document.getElementById('searchMatchesContainer');
  const list = document.getElementById('searchMatchesList');
  const countText = document.getElementById('matchesCountText');

  countText.innerText = `Found ${books.length} book(s) for "${query}":`;
  list.innerHTML = books.map(b => `
    <div class="match-item" onclick="loadBook(${b.id}); closeMatches();">
      <div class="match-title">${escapeHtml(b.title)}</div>
      <div class="match-author">✍️ Author: <strong>${escapeHtml(b.author)}</strong> • ${escapeHtml(b.category)}</div>
    </div>
  `).join('');

  container.style.display = 'block';
}

function closeMatches() {
  const container = document.getElementById('searchMatchesContainer');
  if (container) container.style.display = 'none';
}

// 4. Instant 1-Click Quick Select
function quickSelect(bookId, title, btn) {
  document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  searchInput.value = title;
  closeMatches();
  loadBook(bookId);
}

// 5. Load Book Details & Personalized Recommendations
async function loadBook(bookId) {
  currentBookId = bookId;

  try {
    const recRes = await fetch(`/api/recommend/${bookId}?top_n=6`);
    const recData = await recRes.json();
    const center = recData.start_book;
    const recs = recData.recommendations || [];

    // Prominently update Currently Selected Book Card with Title AND Author
    document.getElementById('bookTitle').innerText = center.title;
    document.getElementById('bookAuthor').innerText = center.author;
    document.getElementById('bookCategory').innerText = center.category;
    document.getElementById('bookYear').innerText = center.year;
    document.getElementById('bookDesc').innerText = center.description || 'A timeless library classic.';

    // Render "Recommended for You" cards (with authors)
    renderRecommendations(recs);

  } catch (e) {
    console.error("Discovery error", e);
  }
}

function renderRecommendations(recs) {
  const container = document.getElementById('recommendationsList');
  container.innerHTML = '';

  if (!recs || recs.length === 0) {
    container.innerHTML = '<div style="color: #94a3b8; font-size: 0.9rem; padding: 16px;">No related recommendations found for this title.</div>';
    document.getElementById('recsCount').innerText = '0 recommendations';
    return;
  }

  document.getElementById('recsCount').innerText = `${recs.length} recommended titles`;

  recs.forEach(r => {
    const card = document.createElement('div');
    card.className = 'rec-card';
    card.onclick = () => {
      loadBook(r.id);
      window.scrollTo({ top: 120, behavior: 'smooth' });
    };

    // Clean human-friendly connection tags (strip any technical weight labels)
    const reasonsList = r.reasons || [];
    const tagHtml = reasonsList.slice(0, 2).map(reason => {
      const cleanText = String(reason).replace(/\(\+[\d\.]+\)/g, '').trim();
      return `<span class="rec-tag-pill">✓ ${escapeHtml(cleanText)}</span>`;
    }).join('');

    card.innerHTML = `
      <div>
        <div class="rec-top-row">
          <div class="rec-book-name">${escapeHtml(r.title)}</div>
        </div>
        <div class="rec-author-line">✍️ Author: <strong>${escapeHtml(r.author)}</strong> • ${escapeHtml(r.category)} (${r.year})</div>
        <div class="rec-tags">${tagHtml}</div>
      </div>
      <div class="rec-card-footer">
        <span>Click to view recommendations</span> →
      </div>
    `;
    container.appendChild(card);
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeQuote(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'");
}
