import json
import urllib.request
import urllib.parse
import os

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
img_dir = 'D:/chumbada-catalogo-v2/assets/img/shopify'

def download_img(url):
    if not url: return ''
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename: return ''
    local_path = os.path.join(img_dir, filename)
    if not os.path.exists(local_path):
        try:
            print(f"Baixando {filename}...")
            urllib.request.urlretrieve(url, local_path)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
    return f"assets/img/shopify/{filename}"

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

camisa_prod = None
clip_prod = None

# Update Snap specs and collect Camisa and Clip
for p in products:
    name_lower = p['name'].lower()
    if 'snap' in name_lower and 'specs' in p:
        for k, v in p['specs'].items():
            if '1 unidade' in v.lower():
                p['specs'][k] = 'Um pacote'
    
    if 'camise' in name_lower and 'pesca' in name_lower:
        camisa_prod = p
    elif 'clip' in name_lower and 'vara' in name_lower:
        clip_prod = p

# Modify Camisa
if camisa_prod:
    camisa_prod['name'] = 'Camisa de Pesca'
    camisa_prod['section'] = 'Vestuário'
    camisa_img = download_img('https://cdn.shopify.com/s/files/1/0454/5845/6736/files/camisa.png?v=1784562308')
    camisa_prod['img'] = camisa_img
    if camisa_img not in camisa_prod['images']:
        camisa_prod['images'].insert(0, camisa_img)

# Modify Clip Vara
if clip_prod:
    clip_prod['section'] = 'Lançamentos'

# Reorder products
# Put all 'Lançamentos' first, then the rest, and 'Vestuário' at the end.
lan_prods = []
vest_prods = []
other_prods = []

for p in products:
    # Ensure section property consistency
    sec = p.get('section')
    if sec == 'Lançamentos':
        lan_prods.append(p)
    elif sec == 'Vestuário' or p.get('category') == 'Vestuário':
        p['section'] = 'Vestuário'
        vest_prods.append(p)
    else:
        other_prods.append(p)

final_products = lan_prods + other_prods + vest_prods

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(final_products, indent=2, ensure_ascii=False) + ';\n')

print("Dados reorganizados com sucesso!")
