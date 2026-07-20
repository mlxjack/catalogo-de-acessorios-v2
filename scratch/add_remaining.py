import csv
import json
import re
import unicodedata

def normalize(s):
    if not isinstance(s, str): return ''
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'[^a-z0-9]', '', s)

# Load data.js
data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_js = json.loads(parts[1].rsplit(';', 1)[0])
already_in_js = set(normalize(p['name']) for p in products_js)

# Load CSV
csv_path = 'D:/Dowloads HD 1T/products_export_acessorios_completo.csv'
with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    rows_by_handle = {}
    for row in reader:
        h = row.get('Handle')
        if h:
            if h not in rows_by_handle:
                rows_by_handle[h] = []
            rows_by_handle[h].append(dict(row))

def map_section(title):
    t = title.lower()
    if 'chicote' in t or 'linha' in t:
        return 'Montagem'
    if 'camiseta' in t or 'jaqueta' in t or 'calca' in t or 'blusa' in t or 'bone' in t or 'chapeu' in t or 'tube' in t or 'avental' in t:
        return 'Vestuário'
    if 'stopper' in t or 'cobre no' in t or 'cobren' in t or 'snap' in t or 'destorcedor' in t or 'rotor' in t:
        return 'Montagem'
    if 'atrativo' in t or 'isca' in t:
        return 'Atrativos'
    if 'suporte' in t or 'copo' in t or 'porta' in t or 'varal' in t or 'cano' in t:
        return 'Suportes'
    if 'dedeira' in t or 'protetor' in t:
        return 'Proteção'
    return 'Acessórios'

def get_variations_from_rows(rows):
    opt1_name = rows[0].get('Option1 Name', '') if rows else ''
    sizes = []
    colors = []
    images = []
    color_images = {}
    main_image = ''
    
    for r in rows:
        img = r.get('Image Src', '')
        var_img = r.get('Variant Image', '')
        opt1v = r.get('Option1 Value', '').strip()
        
        if img and not main_image:
            main_image = img
        if img and img not in images:
            images.append(img)
        
        if opt1v:
            if opt1_name.lower() in ['cor', 'color', 'colour']:
                if opt1v not in [c[0] for c in colors]:
                    colors.append([opt1v, '#888888'])
                if var_img and opt1v:
                    color_images[opt1v] = var_img
            elif opt1_name.lower() in ['tamanho', 'size', 'modelo', 'tipo de rotor']:
                if opt1v not in sizes:
                    sizes.append(opt1v)
    
    return main_image, images, colors, sizes, color_images

# Remaining missing handles with correct CSV handles
remaining_handles = [
    'micangas-de-vidro-pacote-com-500',
    'copo-para-suporte-de-vara',
    'ferradura-para-suporte-de-vara',
    'copo-g-chumbada',  # Copo Para Carretel
    'kit-destorcedor-triplo',  # Already in as Kit Destorcedor Triplo?
    'kit-suporte-para-carretilha-e-molinete-indivudual',
    'apoio-barco-de-borracha',
]

added = 0
for handle in remaining_handles:
    rows = rows_by_handle.get(handle)
    if not rows:
        print(f"Handle not found: {handle}")
        continue
    
    title = rows[0].get('Title', '').strip()
    status = rows[0].get('Status', 'active').strip().lower()
    if status != 'active':
        print(f"Inactive: {title}")
        continue
    
    norm_title = normalize(title)
    if any(norm_title in jn or jn in norm_title for jn in already_in_js if len(norm_title) >= 5 and len(jn) >= 5):
        print(f"Already in data.js: {title}")
        continue
    
    body = rows[0].get('Body (HTML)', '')
    price = rows[0].get('Variant Price', '')
    main_image, images, colors, sizes, color_images = get_variations_from_rows(rows)
    section = map_section(title)
    
    new_product = {
        'name': title,
        'desc': body,
        'specs': {},
        'price': price,
        'category': section,
        'section': section,
        'colors': colors,
        'colorImages': color_images,
        'sizes': sizes,
        'rating': 5.0,
        'reviews': 0,
        'image': main_image,
        'images': images,
    }
    products_js.append(new_product)
    already_in_js.add(norm_title)
    added += 1
    print(f"Added: {title} -> section={section}")

print(f"\nAdded: {added} | Total: {len(products_js)}")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products_js, indent=2, ensure_ascii=False) + ';\n')

print("Done!")
