import markdown

def render_markdown(content:str) -> str:
    """
    Mengonversi string Markdown menjadi HTML.
    - fenced_code: Memproses blok kode dengan tiga backtick (```).
    - codehilite: Menambahkan sintaks warna/highlighting pada kode.
    - tables: Mendukung format tabel Markdown.
    - toc: Mendukung Table of Contents jika dibutuhkan.
    """
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

    return html