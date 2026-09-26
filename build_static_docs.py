import os
import shutil
import urllib.request
import re

def build_docs():
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # 1. Fetch Main Page
    print("Fetching main page from http://127.0.0.1:8000/ ...")
    req = urllib.request.Request('http://127.0.0.1:8000/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        main_html = response.read().decode('utf-8')

    # 2. Fetch Gallery Page
    print("Fetching gallery page from http://127.0.0.1:8000/gallery/ ...")
    req_gal = urllib.request.Request('http://127.0.0.1:8000/gallery/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_gal) as response:
        gallery_html = response.read().decode('utf-8')

    # 2.1 Fetch Materials Page
    print("Fetching materials page from http://127.0.0.1:8000/materials/ ...")
    req_mat = urllib.request.Request('http://127.0.0.1:8000/materials/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_mat) as response:
        materials_html = response.read().decode('utf-8')

    # 3. Copy static folder to docs/static
    docs_static = os.path.join(docs_dir, 'static')
    if os.path.exists(docs_static):
        shutil.rmtree(docs_static)
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), docs_static)
    print("Static assets copied to docs/static")

    # 4. Patch static/js/main.js for GitHub Pages demo mode (mock API success)
    main_js_path = os.path.join(docs_static, 'js', 'main.js')
    if os.path.exists(main_js_path):
        with open(main_js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()

        # In GitHub Pages environment, bypass fetch failure and show instant success screen
        mock_handler = """
        // GitHub Pages Demo Mode: Return simulated success if on static host
        if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
            await new Promise(r => setTimeout(r, 600));
            res = { success: true };
        } else {
        """
        # Patch quiz submit fetch
        js_code = js_code.replace(
            "const response = await fetch('/api/quiz-lead/', {",
            mock_handler + "\n            const response = await fetch('/api/quiz-lead/', {"
        )
        js_code = js_code.replace(
            "const res = await response.json();",
            "const res = await response.json();\n        }"
        )

        # Patch sample box submit fetch
        js_code = js_code.replace(
            "const response = await fetch('/api/sample-box/', {",
            mock_handler + "\n            const response = await fetch('/api/sample-box/', {"
        )

        with open(main_js_path, 'w', encoding='utf-8') as f:
            f.write(js_code)
        print("Patched docs/static/js/main.js for demo mode")

    # 5. Transform URLs in HTML for GitHub Pages relative paths
    def transform_html(html, page_type='main'):
        # Replace /static/ with static/
        html = html.replace('href="/static/', 'href="static/')
        html = html.replace('src="/static/', 'src="static/')
        html = html.replace("url('/static/", "url('static/")
        html = html.replace('url("/static/', 'url("static/')

        # Replace internal links
        html = html.replace('href="/materials/"', 'href="materials.html"')
        html = html.replace('href="/gallery/"', 'href="gallery.html"')
        if page_type == 'main':
            html = html.replace('href="/#', 'href="#')
            html = html.replace('href="/"', 'href="index.html"')
        else:
            html = html.replace('href="/#', 'href="index.html#')
            html = html.replace('href="/"', 'href="index.html"')

        return html

    main_html_clean = transform_html(main_html, page_type='main')
    gallery_html_clean = transform_html(gallery_html, page_type='gallery')
    materials_html_clean = transform_html(materials_html, page_type='materials')

    # 6. Write docs/index.html, docs/gallery.html and docs/materials.html
    with open(os.path.join(docs_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(main_html_clean)

    with open(os.path.join(docs_dir, 'gallery.html'), 'w', encoding='utf-8') as f:
        f.write(gallery_html_clean)

    with open(os.path.join(docs_dir, 'materials.html'), 'w', encoding='utf-8') as f:
        f.write(materials_html_clean)

    # Add .nojekyll so GitHub Pages doesn't ignore anything
    with open(os.path.join(docs_dir, '.nojekyll'), 'w', encoding='utf-8') as f:
        f.write('')

    print("docs/index.html, docs/gallery.html and docs/.nojekyll generated successfully!")

if __name__ == '__main__':
    build_docs()
