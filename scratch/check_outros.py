import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
products = json.loads(parts[1].rsplit(';', 1)[0])

print("=== PRODUCTS IN OUTROS CATEGORY OR SECTION ===")
for p in products:
    cat = p.get('category')
    sec = p.get('section')
    if cat == 'Outros' or sec == 'Outros':
        print(f"Name: {p['name']}")
        print(f"  Category: {cat} | Section: {sec}")
        print(f"  Image: {p.get('image')}")
        print(f"  Images: {p.get('images')}")
        print("-" * 30)
