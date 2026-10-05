import os
import shutil
import re
import django

def build_docs():
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from django.test import Client

    client = Client()
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # 1. Fetch Pages via Django Client (reliable, zero external server needed)
    pages = {
        'index': ('/', 'main'),
        'gallery': ('/gallery/', 'gallery'),
        'materials': ('/materials/', 'materials'),
        'projects': ('/projects/', 'projects'),
        'fonts': ('/fonts/', 'fonts'),
        'partners': ('/partners/', 'partners'),
        'portal': ('/portal/', 'portal'),
        'contacts': ('/contacts/', 'contacts'),
    }

    raw_htmls = {}
    for key, (path, page_type) in pages.items():
        print(f"Rendering {path} via Django Client...")
        res = client.get(path)
        if res.status_code != 200:
            raise RuntimeError(f"Failed to render {path}: HTTP {res.status_code}")
        raw_htmls[key] = res.content.decode('utf-8')

    # 2. Copy static folder to docs/static
    docs_static = os.path.join(docs_dir, 'static')
    if os.path.exists(docs_static):
        shutil.rmtree(docs_static)
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), docs_static)
    print("Static assets copied to docs/static")

    # 3. Static assets are ready (main.js natively includes demo mode checks)
    print("Static assets verified in docs/static")

    # 4. Transform URLs in HTML for GitHub Pages relative paths
    def transform_html(html, page_type='main'):
        # Replace /static/ with static/
        html = html.replace('href="/static/', 'href="static/')
        html = html.replace('src="/static/', 'src="static/')
        html = html.replace("url('/static/", "url('static/")
        html = html.replace('url("/static/', 'url("static/')

        # Replace internal links
        html = html.replace('href="/materials/#', 'href="materials.html#')
        html = html.replace('href="/materials/"', 'href="materials.html"')
        html = html.replace('href="/materials"', 'href="materials.html"')
        html = html.replace('href="/projects/#', 'href="projects.html#')
        html = html.replace('href="/projects/"', 'href="projects.html"')
        html = html.replace('href="/projects"', 'href="projects.html"')
        html = html.replace('href="/gallery/#', 'href="gallery.html#')
        html = html.replace('href="/gallery/"', 'href="gallery.html"')
        html = html.replace('href="/gallery"', 'href="gallery.html"')
        html = html.replace('href="/fonts/#', 'href="fonts.html#')
        html = html.replace('href="/fonts/"', 'href="fonts.html"')
        html = html.replace('href="/fonts"', 'href="fonts.html"')
        html = html.replace('href="/partners/#', 'href="partners.html#')
        html = html.replace('href="/partners/"', 'href="partners.html"')
        html = html.replace('href="/partners"', 'href="partners.html"')
        html = html.replace('href="/portal/#', 'href="portal.html#')
        html = html.replace('href="/portal/"', 'href="portal.html"')
        html = html.replace('href="/portal"', 'href="portal.html"')
        html = html.replace('href="/contacts/#', 'href="contacts.html#')
        html = html.replace('href="/contacts/"', 'href="contacts.html"')
        html = html.replace('href="/contacts"', 'href="contacts.html"')

        if page_type == 'main':
            html = html.replace('href="/#', 'href="#')
            html = html.replace('href="/"', 'href="index.html"')
        else:
            html = html.replace('href="/#', 'href="index.html#')
            html = html.replace('href="/"', 'href="index.html"')

        return html

    root_dir = os.path.dirname(__file__)
    for key, (path, page_type) in pages.items():
        clean_html = transform_html(raw_htmls[key], page_type=page_type)
        out_file = os.path.join(docs_dir, f"{key}.html")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(clean_html)
        root_file = os.path.join(root_dir, f"{key}.html")
        with open(root_file, 'w', encoding='utf-8') as f:
            f.write(clean_html)
        print(f"Saved {out_file} and {root_file}")

    # Add .nojekyll so GitHub Pages doesn't ignore anything
    with open(os.path.join(docs_dir, '.nojekyll'), 'w', encoding='utf-8') as f:
        f.write('')
    with open(os.path.join(root_dir, '.nojekyll'), 'w', encoding='utf-8') as f:
        f.write('')

    print("All pages (index, gallery, materials, projects, fonts) generated successfully in root and docs!")

if __name__ == '__main__':
    build_docs()
