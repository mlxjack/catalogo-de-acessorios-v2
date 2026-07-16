import csv
import json
import os
import urllib.parse
import urllib.request

csv_path = "D:/Dowloads HD 1T/products_export (3).csv"
data_js_path = "D:/chumbada-catalogo-v2/assets/js/data.js"
img_dir = "D:/chumbada-catalogo-v2/assets/img/shopify"

def get_local_path(url):
    if not url or "shopify.com" not in url:
        return url
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return url
    return f"assets/img/shopify/{filename}"

def download_img(url):
    if not url or "shopify.com" not in url:
        return
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return
    local_full_path = os.path.join(img_dir, filename)
    if not os.path.exists(local_full_path):
        print(f"Baixando {filename}...")
        try:
            urllib.request.urlretrieve(url, local_full_path)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

# Lendo CSV 3 (roupas)
blouse_data = {}
with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        handle = row.get("Handle")
        title = row.get("Title")
        body = row.get("Body (HTML)", "")
        img = row.get("Image Src", "")
        
        if not handle:
            continue
            
        if handle not in blouse_data:
            blouse_data[handle] = {
                "title": title or "",
                "description": body or "",
                "images": []
            }
        
        if not blouse_data[handle]["title"] and title:
            blouse_data[handle]["title"] = title
            
        if not blouse_data[handle]["description"] and body:
            blouse_data[handle]["description"] = body
            
        if img:
            download_img(img)
            blouse_data[handle]["images"].append(get_local_path(img))

print("Dados do CSV 3 lidos:")
for handle, data in blouse_data.items():
    print(f" - {data['title']}: {len(data['images'])} imagens")

# Atualizando data.js
with open(data_js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_json = parts[1].rsplit(';', 1)[0]
products = json.loads(products_json)

for p in products:
    name_lower = p['name'].lower()
    # Procurar correspondência no blouse_data
    best_match = None
    for handle, data in blouse_data.items():
        title_lower = data['title'].lower()
        if not title_lower:
            continue
        # Check if they match
        if title_lower in name_lower or name_lower in title_lower:
            best_match = data
            break
            
    if best_match:
        if best_match["images"]:
            p["img"] = best_match["images"][0]
            # Replace images list keeping old ones if they are not shopify?
            # actually better to just replace
            p["images"] = best_match["images"]
        if best_match["description"]:
            p["description"] = best_match["description"]
        print(f"Produto atualizado: {p['name']}")

with open(data_js_path, "w", encoding="utf-8") as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
print("data.js atualizado com sucesso!")
