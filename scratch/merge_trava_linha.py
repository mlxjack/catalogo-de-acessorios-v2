import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

trava = None
porta_idx = -1

for i, p in enumerate(products):
    if p['name'] == 'Trava Linha':
        trava = p
    if p['name'] == 'Porta Pernada Cano':
        porta_idx = i

if trava and porta_idx != -1:
    porta = products[porta_idx]
    
    # Add to vars
    porta['vars'].append(["Trava Linha (Reposição)", trava['price']])
    
    # Add to varImages
    porta['varImages']["Trava Linha (Reposição)"] = trava['img']
    
    # Add img to images if not present
    if trava['img'] not in porta['images']:
        porta['images'].append(trava['img'])
        
    # Remove Trava Linha from products
    products = [p for p in products if p['name'] != 'Trava Linha']
    
    with open(data_path, 'w', encoding='utf-8') as f:
        f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
    print("Merged Trava Linha into Porta Pernada Cano and removed it as standalone.")
else:
    print("Could not find Trava Linha or Porta Pernada Cano")
