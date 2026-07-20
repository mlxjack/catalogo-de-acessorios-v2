import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'mini secretária' in p['name'].lower() or 'mini secretaria' in p['name'].lower():
        p['section'] = 'Lançamentos'
        print("Updated Mini Secretária section to Lançamentos")

# Reordenar para colocar todos os Lançamentos no topo
lan_prods = []
other_prods = []

for p in products:
    if p.get('section') == 'Lançamentos':
        lan_prods.append(p)
    else:
        other_prods.append(p)

final_products = lan_prods + other_prods

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(final_products, indent=2, ensure_ascii=False) + ';\n')

print("Regrupado com sucesso!")
