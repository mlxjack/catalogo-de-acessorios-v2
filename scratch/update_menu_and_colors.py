import json
import os
import shutil

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
img_dest_dir = 'D:/chumbada-catalogo-v2/assets/img/shopify'
source_dir = 'D:/Chumbada/Cores utilizadas nas iscas'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

# TAREFA 1: Fix capitalization of categories
for p in products:
    cat = p.get('category', '')
    if cat.isupper():
        p['category'] = cat.title().replace(' E ', ' e ')

# TAREFA 2: Lançamentos
# Only "Linha Multi Verax 4X 300m", "Clip Vara (com fita dupla face)" and "Kit Atrativo Cônico..."
lancamentos_names = ['linha multi verax', 'clip vara', 'kit atrativo cônico']
for p in products:
    name_lower = p['name'].lower()
    is_lan = any(l in name_lower for l in lancamentos_names)
    
    if is_lan:
        p['section'] = 'Lançamentos'
    else:
        if p.get('section') == 'Lançamentos':
            # Remove from lancamentos
            # if category is defined, fallback to category, else use 'Geral'
            p['section'] = p.get('category', 'Geral')

# TAREFA 3: Atrativos Holográficos
# Get all files in source_dir
new_colors = []
for f_name in os.listdir(source_dir):
    if f_name.endswith(('.jpg', '.png', '.jpeg')):
        name = os.path.splitext(f_name)[0].replace('-', ' ').title()
        
        src = os.path.join(source_dir, f_name)
        dst_name = 'holografico-' + f_name.replace(' ', '-').lower()
        dst = os.path.join(img_dest_dir, dst_name)
        shutil.copy2(src, dst)
        
        img_url = f"assets/img/shopify/{dst_name}"
        bg_style = f"url({img_url}) center/cover"
        new_colors.append((name, bg_style, img_url))

for p in products:
    if p['name'] in ['Atrativo Holográfico', 'Mini Atrativo Holográfico']:
        # Clear existing swatches and add the new ones
        p['swatches'] = [[c[0], c[1]] for c in new_colors]
        # Clear existing vars and add the new ones (assuming they cost the same as base price or Sob Consulta)
        price = p.get('price', 'Sob Consulta')
        p['vars'] = [[c[0], price] for c in new_colors]
        # Append all these new images to the product's image gallery
        for c in new_colors:
            if c[2] not in p['images']:
                p['images'].append(c[2])

# Reorder products: Lançamentos first, Vestuário last
lan_prods = []
vest_prods = []
other_prods = []

for p in products:
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

print("Dados e categorias atualizados com sucesso!")
