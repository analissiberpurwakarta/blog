import os
import shutil
from app import app
from utils.loader import get_all_posts

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

# Jika di-deploy ke GitHub Pages dengan repo bernama 'blog', isi BASE_URL = '/blog'
# Jika repo di-rename menjadi 'analissiberpurwakarta.github.io', isi BASE_URL = ''
BASE_URL = os.getenv('BASE_URL', '/blog')

def clean_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

def copy_static_files():
    static_src = os.path.join(os.path.dirname(__file__), 'static')
    static_dst = os.path.join(OUTPUT_DIR, 'static')
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)

def save_html(path: str, content: str):
    clean_path = path.lstrip('/')
    
    if not clean_path:
        target_file = os.path.join(OUTPUT_DIR, 'index.html')
    else:
        if not clean_path.endswith('.html'):
            target_file = os.path.join(OUTPUT_DIR, f"{clean_path}.html")
        else:
            target_file = os.path.join(OUTPUT_DIR, clean_path)

    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [+] Generated: {os.path.relpath(target_file, OUTPUT_DIR)}")

def build_static_site():
    print("[*] Starting static site generation...")
    clean_output_dir()
    copy_static_files()

    # Pass base_url ke Jinja2 context global
    app.jinja_env.globals['base_url'] = BASE_URL

    with app.test_client() as client:
        # 1. Home
        res = client.get('/')
        save_html('/', res.get_data(as_text=True))

        # 2. Archive
        res = client.get('/archive')
        save_html('/archive', res.get_data(as_text=True))

        # 3. Search
        res = client.get('/search')
        save_html('/search', res.get_data(as_text=True))

        # 4. Posts & Tags
        posts = get_all_posts(parse_body=False)
        all_tags = set()

        for post in posts:
            slug = post['slug']
            res = client.get(f'/posts/{slug}')
            if res.status_code == 200:
                save_html(f'/posts/{slug}', res.get_data(as_text=True))
            
            for tag in post.get('tags', []):
                all_tags.add(tag)

        # 5. Tag pages
        for tag in all_tags:
            res = client.get(f'/tag/{tag}')
            if res.status_code == 200:
                save_html(f'/tag/{tag}', res.get_data(as_text=True))

    print("\n[✔] Build complete! Static files generated in 'output/' directory.")

if __name__ == '__main__':
    build_static_site()