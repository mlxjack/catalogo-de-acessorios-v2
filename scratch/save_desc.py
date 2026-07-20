import json

with open('D:/chumbada-catalogo-v2/assets/js/data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
products = json.loads(parts[1].rsplit(';', 1)[0])

with open('D:/chumbada-catalogo-v2/scratch/desc.txt', 'w', encoding='utf-8') as f:
    for p in products:
        specs = p.get('specs', {})
        if not specs or len(specs) < 2:
            f.write(f"=== {p['name']} ===\n")
            f.write(f"Desc: {p.get('description', '')}\n\n")

print("Saved to scratch/desc.txt")
