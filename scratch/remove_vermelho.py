import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if p['name'] == 'Suporte de Vara Slim':
        # Remove from swatches
        if 'swatches' in p:
            p['swatches'] = [s for s in p['swatches'] if s[0] != 'Vermelho']
            
        # Remove from images
        if 'images' in p:
            p['images'] = [img for img in p['images'] if 'vermelho' not in img.lower()]
            
        print("Removed Vermelho from Suporte de Vara Slim")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
