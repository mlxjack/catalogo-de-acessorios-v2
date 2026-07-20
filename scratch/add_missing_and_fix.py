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
js_names_normalized = set(normalize(p['name']) for p in products_js)

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

# === FIX 1: Corrigir Porta Pernadas e Chicotes - adicionar foto e cores ===
for p in products_js:
    if 'porta pernadas e chicotes' in p['name'].lower() or 'porta pernadas e chicote' in p['name'].lower():
        p['image'] = 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/sedalha-areia-capa.png?v=1725025532'
        p['images'] = [
            'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/sedalha-areia-capa.png?v=1725025532',
            'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_branco.jpg?v=1738591758',
            'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_preto.jpg?v=1738591758',
        ]
        p['colors'] = [
            ['Azul', '#3b82f6'],
            ['Branco', '#f1f5f9'],
            ['Rosa', '#f9a8d4'],
            ['Areia', '#d4a87a'],
            ['Preto', '#1a1a1a'],
        ]
        p['colorImages'] = {
            'Azul': 'https://cdn.shopify.com/s/files/1/0454/5845/6736/products/sedalha-azul.png?v=1725025534',
            'Branco': 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_branco.jpg?v=1738591758',
            'Rosa': 'https://cdn.shopify.com/s/files/1/0454/5845/6736/products/sedalha-rosa.png?v=1725025534',
            'Areia': 'https://cdn.shopify.com/s/files/1/0454/5845/6736/products/sedalha-areia.png?v=1725025534',
            'Preto': 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_preto.jpg?v=1738591758',
        }
        print(f"Fixed: {p['name']}")
        break

# === FIX 2: Corrigir Chicotes Montados já existentes - add image if needed ===
# Also find and update if they're already there with wrong images

# === ADD: New products from CSV ===
# Products missing from data.js (from check_complete_csv output)
products_to_add_handles = [
    'porta-pernadas-e-chicotes',  # New product (different from Porta Pernada Compacto)
    'camiseta-de-pesca-masculina',
    'pipa',
    'stopper-modelo-oliva',
    'miangas-de-vidro-pacote-com-500',
    'cobre-no-pacote-com-40',
    'apoio-anzol-cano',
    'copo-para-suporte-de-vara-premium',
    'ferradura-para-suporte-de-vara-premium',
    'chicote-pesca-de-beira-1-00m',
    'chicote-pesca-de-meia-agua-1-15m',
    'chicote-pesca-no-fundo-1-30m',
    'chicote-pesca-no-fundo-1-80m',
    'copo-para-carretel-de-chicotes',
    'kit-destorcedor',
    'protetor-de-bobina-chumbada',
    'stopper-modelo-cilindrico',
    'alicate-chumbada',
    'kit-no-de-correr',
    'chicote-finesse-85cm',
    'kit-adaptador-de-carretilha',
    'tela-de-espremer-isca-chumbada',
    'kit-parte-superior-do-varal-para-chicotes-com-tubo-de-aluminio-incluido-chumbada-oficial',
    'kit-suporte-para-carretilha-e-molinete-individual',
    'apoio-barco-de-borracha-com-elastico',
    'linha-de-pesca',
]

# category mapping from product type or name
def map_section(title, ptype):
    t = title.lower()
    if 'chicote' in t or 'linha' in t:
        return 'Montagem'
    if 'camiseta' in t or 'jaqueta' in t or 'calca' in t or 'blusa' in t or 'bone' in t or 'chapeu' in t or 'tube' in t or 'avental' in t:
        return 'Vestuário'
    if 'stopper' in t or 'cobre no' in t or 'cobren' in t or 'snap' in t or 'destorcedor' in t or 'destorcedor' in t or 'rotor' in t:
        return 'Montagem'
    if 'atrativo' in t or 'isca' in t:
        return 'Atrativos'
    if 'suporte' in t or 'copo' in t or 'porta' in t or 'varal' in t or 'cano' in t or 'nano pipe' in t:
        return 'Suportes'
    if 'dedeira' in t or 'protetor' in t or 'tube' in t:
        return 'Proteção'
    return 'Acessórios'

def get_variations_from_rows(rows):
    """Extract size/color variations from CSV rows"""
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
        if img:
            if img not in images:
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

# Products already in data.js that should NOT be re-added
skip_if_similar = {
    'porta-pernadas-e-chicotes': 'porta pernadas',  # this one IS missing, add it
}

already_in_js = set()
for p in products_js:
    already_in_js.add(normalize(p['name']))

added_count = 0
for handle in products_to_add_handles:
    # find matching rows in CSV
    rows = None
    for h, r in rows_by_handle.items():
        if h == handle or normalize(h) == normalize(handle):
            rows = r
            break
    
    if not rows:
        print(f"Handle not found in CSV: {handle}")
        continue
    
    title = rows[0].get('Title', '').strip()
    status = rows[0].get('Status', 'active').strip().lower()
    
    if status != 'active':
        print(f"Skipping inactive: {title}")
        continue
    
    # Check if already in data.js
    norm_title = normalize(title)
    if any(norm_title in jn or jn in norm_title for jn in already_in_js if len(norm_title) >= 5 and len(jn) >= 5):
        print(f"Already in data.js: {title}")
        continue
    
    body = rows[0].get('Body (HTML)', '')
    ptype = rows[0].get('Type', '')
    price = rows[0].get('Variant Price', '')
    tags = rows[0].get('Tags', '')
    
    main_image, images, colors, sizes, color_images = get_variations_from_rows(rows)
    section = map_section(title, ptype)
    
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
    added_count += 1
    print(f"Added: {title} -> section={section}, colors={len(colors)}, sizes={len(sizes)}")

# === FIX 3: Update Chicotes Montados image (if exists in data.js) ===
for p in products_js:
    name = p['name'].lower()
    # Update chicotes with correct images from CSV
    for handle, rows in rows_by_handle.items():
        if not rows: continue
        csv_title = rows[0].get('Title', '').strip()
        if normalize(csv_title) == normalize(p['name']):
            main_image, images, colors, sizes, color_images = get_variations_from_rows(rows)
            if main_image and (not p.get('image') or 'placeholder' in p.get('image', '').lower()):
                p['image'] = main_image
                p['images'] = images
                if colors:
                    p['colors'] = colors
                if color_images:
                    p['colorImages'] = color_images
                if sizes:
                    p['sizes'] = sizes
                print(f"Updated image for: {p['name']}")
            break

print()
print(f"Total added: {added_count}")
print(f"Total in data.js: {len(products_js)}")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products_js, indent=2, ensure_ascii=False) + ';\n')

print("Done!")
