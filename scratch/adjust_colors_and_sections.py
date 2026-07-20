import json
import os
import shutil
import unicodedata

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
img_dest_dir = 'D:/chumbada-catalogo-v2/assets/img/shopify'
source_dir = 'D:/Chumbada/Cores utilizadas nas iscas'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

files_in_dir = os.listdir(source_dir)

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def find_file_fuzzy(color_name):
    norm_color = strip_accents(color_name.lower().replace(' ', '').replace('estelar', 'estrelnar'))
    for f in files_in_dir:
        norm_f = strip_accents(f.lower().replace('-', '').replace(' ', '').split('.')[0])
        if norm_color in norm_f or norm_f in norm_color:
            return f
    return None

# Cores especificadas pelo usuário
holo_colors_list = [
    "Beijo da Sombra", "Capim Rubi", "Chá", "Luz Laranja",
    "Roxo Estelar", "Rubi Dourado", "Salmão Radiante",
    "Verde Cósmico", "Vermelho Holográfico", "Véu da Noite"
]

conico_colors_list = [
    "Amarelo Neon", "Branco Pérola", "Laranja Neon",
    "Preto Brilhante", "Vermelho Holográfico", "Verde Neon"
]

# Preparar swatches para holograficos
holo_swatches = []
for color in holo_colors_list:
    f_name = find_file_fuzzy(color)
    if f_name:
        dst_name = 'holografico-' + f_name.replace(' ', '-').lower()
        src = os.path.join(source_dir, f_name)
        dst = os.path.join(img_dest_dir, dst_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        img_url = f"assets/img/shopify/{dst_name}"
        holo_swatches.append((color, f"url({img_url}) center/cover", img_url))

# Preparar swatches para conico
conico_swatches = []
for color in conico_colors_list:
    f_name = find_file_fuzzy(color)
    if f_name:
        dst_name = 'conico-' + f_name.replace(' ', '-').lower()
        src = os.path.join(source_dir, f_name)
        dst = os.path.join(img_dest_dir, dst_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        img_url = f"assets/img/shopify/{dst_name}"
        conico_swatches.append((color, f"url({img_url}) center/cover", img_url))

# Atualizar atrativos holográficos no data.js
for p in products:
    name = p['name']
    if name in ['Atrativo Holográfico', 'Mini Atrativo Holográfico']:
        p['swatches'] = [[c[0], c[1]] for c in holo_swatches]
        price = p.get('price', 'Sob Consulta')
        p['vars'] = [[c[0], price] for c in holo_swatches]
        original_img = p['images'][0] if p['images'] else p['img']
        p['img'] = original_img
        p['images'] = [original_img] + [c[2] for c in holo_swatches]
        print(f"Atualizado {name} com {len(holo_swatches)} cores.")

    if 'kit atrativo cônico' in name.lower():
        p['swatches'] = [[c[0], c[1]] for c in conico_swatches]
        price = p.get('price', 'Sob Consulta')
        p['vars'] = [[c[0], price] for c in conico_swatches]
        original_img = p['images'][0] if p['images'] else p['img']
        p['img'] = original_img
        p['images'] = [original_img] + [c[2] for c in conico_swatches]
        print(f"Atualizado {name} com {len(conico_swatches)} cores.")

# Garantir separação de Lançamentos
for p in products:
    pSection = p.get('section')
    if pSection == 'Lançamentos':
        pass
    else:
        if p.get('category') == 'Vestuário':
            p['section'] = 'Vestuário'
        else:
            p['section'] = p.get('category', 'Outros')

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')

print("Fim da execução!")
