import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'premium' in p['name'].lower():
        print(f"=== NAME: {p['name']} ===")
        print(f"  id: {p.get('id')}")
        print(f"  vars: {p.get('vars')}")
        print(f"  images: {p.get('images')}")
        print()
