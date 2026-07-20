import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'slim' in p['name'].lower() or 'apoio de borracha' in p['name'].lower() or 'copo de borracha' in p['name'].lower():
        print(f"=== NAME: {p['name']} ===")
        print(f"  id: {p.get('id')}")
        print(f"  slug: {p.get('slug')}")
        print(f"  price: {p.get('price')}")
        print(f"  img/image: {p.get('img') or p.get('image')}")
        print(f"  images: {p.get('images')}")
        print(f"  vars: {p.get('vars')}")
        print("-" * 30)
