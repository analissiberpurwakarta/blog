import os
import glob
import frontmatter
import re
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

POST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts')

logger = logging.getLogger(__name__)

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
    try:
        from pathlib import Path
        Path(target_path).relative_to(os.path.abspath(POST_DIR))
    except ValueError:
        return False
    return True
    
def _secure_extenal_links(content: str) -> str:
    if not content:
        return content

    def replace_link(match):
        full_tag = match.group(0)
        href = match.group(1)

        if href.startswith('/') or href.startswith('#') or 'analissiberpurwakarta.github.io' in href or '127.0.0.1' in href:
            return full_tag

        new_tag = full_tag
        if 'target=' not in new_tag:
            new_tag = new_tag.replace('<a ', '<a target="_blank" ')
        if 'rel=' not in new_tag:
            new_tag = new_tag.replace('<a ', '<a rel="noopener noreferrer" ')

        return new_tag

    pattern = r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>'
    return re.sub(pattern, replace_link, content, flags=re.IGNORECASE)

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
                item['content'] = _secure_extenal_links(post.content)

            posts.append(item)
        except Exception as e:
            # Mengabaikan file yang gagal di-unggah/corrupt
            logger.warning(f"Gagal load post '{filepath}': {e}")

    posts.sort(key=lambda x: _parse_date(x.get('date', '')), reverse = True)
    return posts

def get_post_by_slug(slug: str) -> dict | None:
    if not _is_safe_slug(slug):
        return None

    filepath = os.path.join(POST_DIR, f"{slug}.md")
    if os.path.exists(filepath):
        try:
            post = frontmatter.load(filepath)
            metadata = post.metadata
            return {
                'title':metadata.get('title', 'Untitled'),
                'slug':metadata.get('slug', slug),
                'date':str(metadata.get('date', '')),
                'tags': metadata.get('tags', []),
                'summary': metadata.get('summary', ''),
                'content': _secure_extenal_links(post.content)
            }
        except Exception as e:
            logger.warning(f"Gagal load post dengan slug '{slug}': {e}")
            return None

    posts = get_all_posts(parse_body=True)
    for post in posts:
        if post.get('slug') == slug:
            return post

    return None