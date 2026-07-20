import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

cleaned = []

for p in products:
    name = p['name']
    
    if name == "Camiseta de Pesca Masculina":
        print(f"Removing: {name}")
        continue
        
    if name == "Jaqueta de Pesca":
        p['img'] = p.get('image')
        print("Fixed Jaqueta de Pesca: copied 'image' to 'img'")
        
    cleaned.append(p)

# Sorting: Lançamentos first, then Acessórios, then others
def sort_key(p):
    sec = p.get('section')
    cat = p.get('category')
    
    sec_order = 0 if sec == 'Lançamentos' else 1
    
    cat_order = {
        "Acessórios": 1,
        "Montagem": 2,
        "Atrativos": 3,
        "Suportes": 4,
        "Organização": 5,
        "Proteção": 6,
        "Vestuário": 7
    }.get(cat, 99)
    
    return (sec_order, cat_order)

sorted_products = sorted(cleaned, key=sort_key)

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(sorted_products, indent=2, ensure_ascii=False) + ';\n')

print(f"Data.js cleanup and resort complete. Total products: {len(sorted_products)}")
