import csv
import json
import re
import unicodedata
import chardet
import io

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

js_names = [p['name'] for p in products_js]
js_names_normalized = set(normalize(n) for n in js_names)

csv_path = 'D:/Dowloads HD 1T/products_export_acessórios.csv'
with open(csv_path, 'rb') as f:
    e = chardet.detect(f.read(100000))['encoding']

with open(csv_path, 'r', encoding=e) as f:
    reader = csv.DictReader(f)
    
    csv_products = {} # handle -> dict
    for row in reader:
        handle = row.get('Handle')
        title = row.get('Title')
        status = row.get('Status')
        
        if not handle or not title: continue
        
        # Shopify only repeats the title on the first row of the product
        if handle not in csv_products:
            csv_products[handle] = {
                'title': title.strip(),
                'status': status.strip().lower() if status else 'active',
                'body': row.get('Body (HTML)', ''),
                'image': row.get('Image Src', ''),
                'price': row.get('Variant Price', ''),
                'type': row.get('Type', ''),
                'tags': row.get('Tags', '')
            }

missing_products = []
for handle, data in csv_products.items():
    if data['status'] != 'active': continue
    
    norm_title = normalize(data['title'])
    
    # Check if normalized title is in any JS name or vice versa
    found = False
    for jn in js_names_normalized:
        if norm_title in jn or jn in norm_title:
            found = True
            break
            
    # Some special matches, e.g. "Alicate Chumbada" vs "Alicate de Pesca"
    if "alicate" in norm_title and any("alicate" in j for j in js_names_normalized):
        found = True
    if "verax" in norm_title and any("verax" in j for j in js_names_normalized):
        found = True
        
    if not found:
        missing_products.append(data)

with open('D:/chumbada-catalogo-v2/scratch/missing_products.json', 'w', encoding='utf-8') as f:
    json.dump(missing_products, f, indent=2, ensure_ascii=False)

print(f"Found {len(missing_products)} missing active products. Saved to missing_products.json")
for p in missing_products:
    print(f"- {p['title']}")
