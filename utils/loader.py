import os
import glob
import frontmatter
from werkzeug.utils import secure_filename

POST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts')

def _is_safe_slug(slug: str) -> bool:
    """ 
    Validasi kemanan slug untuk mencegah Path Traversal
    Memeriksa apakah slug yang dibersihkan sama dengan slug asli
    dan memastikan file tetap berada di dalam POST_DIR 
    """
    cleaned_slug = secure_filename(slug)
    if not cleaned_slug or cleaned_slug != slug:
        return False

    # Verifikasi path agar tidak keluar dari directory POSTS_DIR
    target_path = os.path.abspath(os.path.join(POST_DIR, f"{slug}.md"))
    return target_path.startswith(os.path.abspath(POST_DIR))

def get_all_posts(parse_body: bool = False) -> list[dict]:
    """ 
    Mengambil semua artikel dari folder posts/
    - Jika parse_body=False: Hanya membaca metadata (cocok untuk Home / Archive / Tag page).
    - Menambahkan fallback 'slug' dari nama file jika tidak diisi di front matter.
    - Mengurutkan artikel dari tanggal terbaru ke terlama. 
    """
    posts = []
    pattern = os.path.join(POST_DIR, '*.md')
    files = glob.glob(pattern)

    print(f"\n[DEBUG] Path folder posts: {POST_DIR}")
    print(f"[DEBUG] File .md yang ditemukan: {files}")

    for filepath in glob.glob(pattern):
        try:
            post = frontmatter.load(filepath)
            metadata = post.metadata

            # Fallback slug dari nama file tanpa ekstensi .md
            filename_slug = os.path.splitext(os.path.basename(filepath))[0]
            slug = metadata.get('slug', filename_slug)

            item = {
                'title': metadata.get('title', 'Untitled'),
                'slug': slug,
                'date': str(metadata.get('date', '')),
                'tags': metadata.get('tags', []),
                'summary': metadata.get('summary', '')
            }

            if parse_body:
                item['content'] = post.content

            posts.append(item)
        except Exception as e:
            # Mengabaikan file yang gagal di-unggah/corrupt
            continue

    posts.sort(key=lambda x: x['date'], reverse = True)
    return posts

def get_post_by_slug(slug: str) -> dict | None:
    """
    Mengambil satu artikel berdasarkan slug.
    Mengembalikan dict berisi metadata + raw markdown content, atau None jika tidak ditemukan.
    """
    if not _is_safe_slug(slug):
        return None

    filepath = os.path.join(POST_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        return None

    try:
        post = frontmatter.load(filepath)
        metadata = post.metadata
        
        return {
            'title': metadata.get('title', 'Untitled'),
            'slug': metadata.get('slug', slug),
            'date': str(metadata.get('date', '')),
            'tags': metadata.get('tags', []),
            'summary': metadata.get('summary', ''),
            'content': post.content  # Raw markdown
        }
    except Exception:
        return None