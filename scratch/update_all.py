import json
import csv
import urllib.request
import urllib.parse
import os

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
img_dir = 'D:/chumbada-catalogo-v2/assets/img/shopify'

def get_local_path(url):
    if not url: return ''
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    return f"assets/img/shopify/{filename}" if filename else ''

def download_img(url):
    if not url: return
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename: return
    local_path = os.path.join(img_dir, filename)
    if not os.path.exists(local_path):
        try:
            print(f"Baixando {filename}...")
            urllib.request.urlretrieve(url, local_path)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

# Lendo data.js
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_json = parts[1].rsplit(';', 1)[0]
products = json.loads(products_json)

# TAREFA 1: Boné
bone_url = 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/bone-chumbada.png?v=1784560274'
download_img(bone_url)
bone_img_path = get_local_path(bone_url)
for p in products:
    if 'bon' in p['name'].lower() and 'chumbada' in p['name'].lower():
        p['img'] = bone_img_path
        if bone_img_path not in p['images']:
            p['images'].insert(0, bone_img_path)

# TAREFA 2: Remover span
for p in products:
    if 'span' in p:
        del p['span']

# TAREFA 3: Unificar Dedeiras
# Vamos achar o ID para a nova dedeira (usar um id max + 1)
max_id = max(p['id'] for p in products) if products else 0
# Remover dedeiras antigas
products = [p for p in products if 'dedeira' not in p['name'].lower()]

# Adicionar nova dedeira
dedeira_url = 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/dedeira.png?v=1784561288'
download_img(dedeira_url)
dedeira_img_path = get_local_path(dedeira_url)

nova_dedeira = {
    "id": max_id + 1,
    "slug": "dedeira-chumbada",
    "category": "Acessórios",
    "name": "Dedeira",
    "price": "Sob Consulta",
    "img": dedeira_img_path,
    "link": "https://chumbadas.com.br",
    "vars": [
        ["Soft", "Sob Consulta"],
        ["Hard", "Sob Consulta"],
        ["Ultrasoft", "Sob Consulta"]
    ],
    "description": "<p>A Dedeira da Chumbada Oficial é o acessório ideal para proteger os dedos durante os arremessos. Disponível nas variações Soft, Hard e Ultrasoft para se adequar a sua pescaria.</p>",
    "images": [dedeira_img_path],
    "video": "",
    "specs": {}
}
products.append(nova_dedeira)

# TAREFA 4: Blusas Corta-vento (usando o CSV)
csv_path = r'D:\Dowloads HD 1T\blusas corta vento.csv'
blouse_data = {}
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row.get('Title')
        img = row.get('Image Src')
        if title:
            current_title = title
            if current_title not in blouse_data:
                blouse_data[current_title] = []
        if img and current_title:
            blouse_data[current_title].append(img)
            download_img(img)

# Atualizar as blusas
for p in products:
    name = p['name']
    best_match = None
    for b_title, b_imgs in blouse_data.items():
        if b_title.lower() in name.lower() or name.lower() in b_title.lower():
            best_match = b_imgs
            break
    if best_match:
        local_imgs = [get_local_path(url) for url in best_match]
        if local_imgs:
            p['img'] = local_imgs[0]
            p['images'] = local_imgs

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
print("Tudo atualizado com sucesso!")
