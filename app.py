from flask import Flask, render_template, abort, request, make_response
from utils.loader import get_all_posts, get_post_by_slug
from utils.parser import render_markdown

app = Flask(__name__)

# Security Headers Middleware
@app.after_request
def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self'"
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:;"
    )
    return response

@app.route('/')
def home():
    posts = get_all_posts(parse_body=False)
    # Mengumpulkan semua tag unik untuk ditampilkan di sidebar/header
    all_tags = sorted(list({tag for p in posts for tag in p.get('tags', [])}))
    return render_template('home.html', posts=posts, tag=all_tags)

@app.route('/posts/<slug>')
def post_detail(slug):
    post = get_post_by_slug(slug)
    if not post:
        abort(404)

    post['html_content'] = render_markdown(post['content'])
    return render_template('post.html', post=post)

@app.route('/tag/<tag>')
def tag_posts(tag):
    all_posts = get_all_posts(parse_body=False)
    filtered_posts = [p for p in all_posts if tag.lower() in [t.lower() for t in p.get('tags', [])]]
    return render_template('tag.html', tag=tag, posts=filtered_posts)

@app.route('/archive')
def archive():
    posts = get_all_posts(parse_body=False)
    return render_template('archive.html', posts=posts)

@app.route('/search')
def search():
    posts = get_all_posts(parse_body=False)
    return render_template('search.html', posts= posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)