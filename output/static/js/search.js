document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('searchInput');
    const resultsDiv = document.getElementById('searchResults');
    const dataScript = document.getElementById('search-data');
    const scriptTag = document.querySelector('script[src*="search.js"]');

    if (!input || !resultsDiv || !dataScript) {
        return;
    }

    // 1. Ambil data JSON posts
    const searchData = JSON.parse(dataScript.textContent || '[]');

    // 2. Ambil base_url secara otomatis dari path script tag
    let baseUrl = '';
    if (scriptTag) {
        const src = scriptTag.getAttribute('src');
        // Mengambil prefix sebelum '/static/js/search.js'
        baseUrl = src.replace(/\/static\/js\/search\.js.*$/, '');
    }

    // Fungsi Render Card Artikel
    function render(items) {
        if (items.length === 0) {
            resultsDiv.innerHTML = '<p class="post-summary" style="margin-top: 1rem;">Artikel tidak ditemukan.</p>';
            return;
        }

        resultsDiv.innerHTML = items.map(p => `
            <article class="post-card">
                <h2 class="post-title">
                    <a href="${baseUrl}/posts/${p.slug}.html">${p.title}</a>
                </h2>
                <div class="post-meta">${p.date || ''}</div>
                <p class="post-summary">${p.summary || ''}</p>
                ${p.tags && p.tags.length > 0 ? `
                    <div class="tags" style="margin-top: 0.5rem;">
                        ${p.tags.map(t => `<a href="${baseUrl}/tag/${t}.html" class="tag-badge">#${t}</a>`).join(' ')}
                    </div>
                ` : ''}
            </article>
        `).join('');
    }

    // Render awal seluruh artikel saat halaman dibuka
    render(searchData);

    // Filter Pencarian secara Live
    input.addEventListener('input', (e) => {
        const q = e.target.value.toLowerCase().trim();
        
        if (!q) {
            render(searchData);
            return;
        }

        const filtered = searchData.filter(p => {
            const titleMatch = p.title && p.title.toLowerCase().includes(q);
            const summaryMatch = p.summary && p.summary.toLowerCase().includes(q);
            const tagMatch = p.tags && p.tags.some(t => t.toLowerCase().includes(q));
            
            return titleMatch || summaryMatch || tagMatch;
        });

        render(filtered);
    });
});