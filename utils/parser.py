import markdown
import nh3
from bs4 import BeautifulSoup

ALLOWED_TAGS = {
    "p", "br", "hr",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "em", "b", "i", "u", "s", "del",
    "a", "img",
    "ul", "ol", "li",
    "blockquote",
    "code", "pre", "span",
    "table", "thead", "tbody", "tr", "th", "td",
    "div",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title", "target", "rel"},
    "img": {"src", "alt", "title", "width", "height"},
    # codehilite/pygments butuh class buat syntax highlighting
    "code": {"class"},
    "pre": {"class"},
    "span": {"class"},
    "div": {"class"},
    "table": {"class"},
    "th": {"class"},
    "td": {"class"},
}

def _harden_external_links(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        is_internal = (
            href.startswith('/') or href.startswith('#')
            or 'analissiberpurwakarta.github.io' in href
            or '127.0.0.1' in href
        )
        if not is_internal:
            a['target'] = '_blank'
            a['rel'] = 'noopener noreferrer'
    return str(soup)

def render_markdown(content:str) -> str:
    if not content:
        return ""

    extensions = [
        'fenced_code',
        'codehilite',
        'tables',
        'toc'
    ]

    extensions_configs = {
        'codehilite': {
            'css_class': 'highlight',
            'linenums': False,
            'use_pygments': True
        }
    }

    html = markdown.markdown(
        content,
        extensions=extensions,
        extension_configs=extensions_configs
    )

    hardened_html = _harden_external_links(html)

    clean_html = nh3.clean(
        hardened_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        link_rel=None
    )

    return clean_html