import csv
import json
import re
import unicodedata
import chardet

def normalize(s):
    if not isinstance(s, str): return ''
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'[^a-z0-9]', '', s)

# Load data.js products
data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
parts = js_content.split('window.PRODUCTS = ')
products_js = json.loads(parts[1].rsplit(';', 1)[0])
js_names_normalized = set(normalize(p['name']) for p in products_js)
js_names = [p['name'] for p in products_js]

print(f"Current products in data.js: {len(products_js)}")
print()

csv_path = 'D:/Dowloads HD 1T/products_export_acessorios_completo.csv'
with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    csv_products = {}
    for row in reader:
        handle = row.get('Handle')
        title = row.get('Title')
        if not handle: continue
        if handle not in csv_products:
            if title:
                csv_products[handle] = {
                    'title': title.strip(),
                    'status': row.get('Status','active').strip().lower(),
                    'image': row.get('Image Src',''),
                    'body': row.get('Body (HTML)',''),
                    'type': row.get('Type',''),
                    'price': row.get('Variant Price',''),
                    'tags': row.get('Tags',''),
                }

active = {k: v for k,v in csv_products.items() if v['status'] == 'active'}
print(f"Active products in new CSV: {len(active)}")
print()

# Find missing
missing = []
for handle, data in active.items():
    norm = normalize(data['title'])
    found = False
    for jn in js_names_normalized:
        # fuzzy: check if one is contained in the other (at least 5 chars)
        if len(norm) >= 5 and len(jn) >= 5:
            if norm in jn or jn in norm:
                found = True
                break
        elif norm == jn:
            found = True
            break
    if not found:
        missing.append(data)

with open('D:/chumbada-catalogo-v2/scratch/missing_complete.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, indent=2, ensure_ascii=False)

print(f"Missing products ({len(missing)}):")
for p in missing:
    print(f"  - {p['title']}")

print()
print("=== ALL CSV titles for reference ===")
for h, v in active.items():
    norm = normalize(v['title'])
    matched = any((norm in jn or jn in norm) and len(norm) >= 5 and len(jn) >= 5 for jn in js_names_normalized)
    marker = "  OK" if matched else "MISSING"
    print(f"  [{marker}] {v['title']}")
