import os
import glob
import frontmatter
from werkzeug.utils import secure_filename
from datetime import datetime

POST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts')

def _parse_date(date_str: str) -> datetime:
    if not date_str:
        return datetime.min

    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        pass

    return datetime.min

def _is_safe_slug(slug: str) -> bool:
    cleaned_slug = secure_filename(slug)
    if not cleaned_slug or cleaned_slug != slug:
        return False

    # Verifikasi path agar tidak keluar dari directory POSTS_DIR
    target_path = os.path.abspath(os.path.join(POST_DIR, f"{slug}.md"))
    return target_path.startswith(os.path.abspath(POST_DIR))

def get_all_posts(parse_body: bool = False) -> list[dict]:
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

    posts.sort(key=lambda x: _parse_date(x.get('date', '')), reverse = True)
    return posts

def get_post_by_slug(slug: str) -> dict | None:
    # 1. Coba cari berdasarkan nama file langsung
    filepath = os.path.join(POST_DIR, f"{slug}.md")
    if os.path.exists(filepath):
        try:
            post = frontmatter.load(filepath)
            metadata = post.metadata
            return {
                'title': metadata.get('title', 'Untitled'),
                'slug': metadata.get('slug', slug),
                'date': str(metadata.get('date', '')),
                'tags': metadata.get('tags', []),
                'summary': metadata.get('summary', ''),
                'content': post.content
            }
        except Exception:
            return None

    # 2. Jika nama file berbeda dengan custom slug, cari dari daftar artikel
    posts = get_all_posts(parse_body=True)
    for post in posts:
        if post.get('slug') == slug:
            return post

    return None