import csv
import json
import re
import unicodedata

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

# Load CSV products
csv_path = 'D:/Dowloads HD 1T/products_export_acessórios.csv'
csv_titles = set()

# detect delimiter and encoding
import chardet
with open(csv_path, 'rb') as f:
    result = chardet.detect(f.read(100000))
    encoding = result['encoding'] or 'utf-8'

with open(csv_path, 'r', encoding=encoding) as f:
    # try comma and then semicolon
    sample = f.read(1024)
    f.seek(0)
    dialect = csv.Sniffer().sniff(sample)
    reader = csv.DictReader(f, dialect=dialect)
    
    title_col = None
    for col in reader.fieldnames:
        if col and ('title' in col.lower() or 'nome' in col.lower()):
            title_col = col
            break
            
    if not title_col:
        print(f"Column for Title not found. Columns: {reader.fieldnames}")
    else:
        for row in reader:
            title = row.get(title_col)
            if title:
                csv_titles.add(title.strip())

# Compare
missing_in_js = []
for title in csv_titles:
    norm_title = normalize(title)
    if not any(norm_title in jn or jn in norm_title for jn in js_names_normalized):
        missing_in_js.append(title)

print(f"Found {len(missing_in_js)} products in CSV not in data.js:")
for m in sorted(missing_in_js):
    print(" - " + m)
