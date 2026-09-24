# ANALIS SIBER PURWAKARTA TECHNICAL WRITE BLOG
Blog bagian dari Analis Siber Purwakarta yang memiliki fokus pada technical content cyber security khususnya Red Team, dan Penetration Testing

## Riwayat Pengembangan (Changelog)

### v0.0.2 - 2026-09-24
**Perbaikan bug:** Penambahan sanitasi HTML menggunakan nh3 (whitelist tags & attribute) setelah proses markdown.markdown(), sebelum di-render lewat {{ post.html_content|safe }}. Event handler (onerror, onclick, dll), <script>, dan javascript: URI sekarang ke-strip otomatis pada parser.py .