import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'varal' in p['name'].lower():
        print(f"=== NAME: {p['name']} ===")
        print(f"  slug: {p.get('slug')}")
        print(f"  price: {p.get('price')}")
        print(f"  img: {p.get('img') or p.get('image')}")
        print(f"  images: {p.get('images')}")
        print(f"  vars: {p.get('vars')}")
        print()
