import json
import re
import os
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

project_dir = 'D:/chumbada-catalogo-v2'
data_js_path = os.path.join(project_dir, 'assets/js/data.js')
img_dir = os.path.join(project_dir, 'assets/img/shopify')
video_dir = os.path.join(project_dir, 'assets/video/shopify')

os.makedirs(img_dir, exist_ok=True)
os.makedirs(video_dir, exist_ok=True)

with open(data_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Parse JSON
match = re.search(r"window\.PRODUCTS = (\[.*?\]);", js_content, re.DOTALL)
if not match:
    print("Could not find window.PRODUCTS in data.js")
    exit(1)
products = json.loads(match.group(1))

# Parse CONFIG
config_match = re.search(r"(window\.CONFIG = \{.*?\};)", js_content, re.DOTALL)
config_str = config_match.group(1) if config_match else ""

url_mapping = {}

def get_local_path(url, is_video=False):
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return None
    # Removendo query params da URL (como ?v=123)
    if is_video or url.endswith('.mp4') or url.endswith('.mov'):
        return f"assets/video/shopify/{filename}"
    return f"assets/img/shopify/{filename}"

def download_file(url, local_path):
    full_local_path = os.path.join(project_dir, local_path)
    if os.path.exists(full_local_path):
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(full_local_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Encontrar todas as URLs e preparar o mapeamento
for p in products:
    img = p.get('img', '')
    if img and 'shopify.com' in img:
        local = get_local_path(img)
        url_mapping[img] = local
        p['img'] = local
        
    for i, image in enumerate(p.get('images', [])):
        if 'shopify.com' in image:
            local = get_local_path(image)
            url_mapping[image] = local
            p['images'][i] = local
            
    video = p.get('video', '')
    if video and 'shopify.com' in video:
        local = get_local_path(video, True)
        url_mapping[video] = local
        p['video'] = local
        
    # Processar descrição
    desc = p.get('description', '')
    if desc:
        desc_urls = set(re.findall(r'(https://cdn\.shopify\.com/[^\"\'\>\s]+)', desc))
        for d_url in desc_urls:
            # limpar query strings temporariamente se elas causarem bugs na extensão
            clean_url = d_url.split('?')[0]
            is_vid = clean_url.endswith('.mp4') or clean_url.endswith('.mov')
            local = get_local_path(d_url, is_vid)
            url_mapping[d_url] = local
            desc = desc.replace(d_url, local)
        p['description'] = desc

    # Processar variations e swatches
    if p.get('vars'):
        for v in p['vars']:
            if len(v) > 2 and v[2] and 'shopify.com' in v[2]:
                local = get_local_path(v[2])
                url_mapping[v[2]] = local
                v[2] = local
                
    if p.get('swatches'):
        for s in p['swatches']:
            if len(s) > 1 and 'shopify.com' in s[1]:
                # As vezes o swatch não é url, é cor em hex, mas se for imagem a gente baixa
                if 'http' in s[1]:
                    local = get_local_path(s[1])
                    url_mapping[s[1]] = local
                    s[1] = f"url('{local}')"

print(f"Encontrados {len(url_mapping)} arquivos para baixar...")

# Fazer o download multithreaded
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for remote, local in url_mapping.items():
        if local:
            futures.append(executor.submit(download_file, remote, local))
            
    for future in futures:
        future.result()

print("Downloads finalizados. Reescrevendo data.js...")

new_js_content = f"""// Catálogo de Acessórios V2 - Chumbada Oficial
// Base de dados gerada dinamicamente com informações de produtos e variações

{config_str}

window.PRODUCTS = {json.dumps(products, indent=2, ensure_ascii=False)};
"""

with open(data_js_path, "w", encoding="utf-8") as f:
    f.write(new_js_content)

print("data.js atualizado localmente com sucesso!")
