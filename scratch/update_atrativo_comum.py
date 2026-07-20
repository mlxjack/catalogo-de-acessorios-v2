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

target_url = 'https://cdn.shopify.com/s/files/1/0454/5845/6736/files/cap-atrativo.png?v=1725023875'
local_img = download_img(target_url)

for p in products:
    if p['name'] == 'Atrativo Comum':
        p['img'] = local_img
        if local_img not in p['images']:
            p['images'].insert(0, local_img)
        print("Updated Atrativo Comum image.")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')

print("Fim do processo!")
