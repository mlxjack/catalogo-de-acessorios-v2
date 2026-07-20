import json

with open('D:/chumbada-catalogo-v2/scratch/missing_products.json', 'r', encoding='utf-8') as f:
    missing_csv = json.load(f)
    
new_products = []
for p in missing_csv:
    # Build standard data.js object
    obj = {
        "name": p['title'],
        "desc": p['body'],
        "specs": {},
        "price": p['price'],
        "category": p['type'] if p['type'] else "Outros",
        "section": p['type'] if p['type'] else "Outros",
        "colors": [],
        "sizes": [],
        "rating": 5.0,
        "reviews": 0,
        "image": p['image']
    }
    new_products.append(obj)

with open('D:/chumbada-catalogo-v2/scratch/to_add.json', 'w', encoding='utf-8') as f:
    json.dump(new_products, f, indent=2, ensure_ascii=False)
