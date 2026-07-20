import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

cleaned = []

to_remove = {
    "Kit destorcedor",
    "Camiseta de Pesca Chumbada Oficial",
    "Miçangas de Vidro (Pacote com 500)",
    "Copo para Suporte de Vara Premium",
    "Ferradura para Suporte de Vara Premium"
}

suporte_premium = None

for p in products:
    name = p['name']
    
    if name in to_remove:
        print(f"Removing duplicate/unwanted: {name}")
        continue
        
    if name == "Suporte de Vara Premium Completo":
        suporte_premium = p
        
    cleaned.append(p)

# Merge Ferradura and Copo images into Suporte de Vara Premium Completo if needed
if suporte_premium:
    copo_img = "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/copo-capa.png?v=1725026399"
    ferradura_img = "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/ferradura-preta.png?v=1757939203"
    
    for img in [copo_img, ferradura_img]:
        if img not in suporte_premium['images']:
            suporte_premium['images'].append(img)
            
    if 'varImages' not in suporte_premium or not suporte_premium['varImages']:
        suporte_premium['varImages'] = {}
    suporte_premium['varImages']['Somente copo'] = copo_img
    suporte_premium['varImages']['Somente ferradura'] = ferradura_img
    print("Ensured Suporte de Vara Premium Completo has variation images mapped.")

# Apply other corrections
for p in cleaned:
    name = p['name']
    
    # Jaqueta de Pesca photo fix
    if name == "Jaqueta de Pesca":
        p['image'] = "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/jaqueta-frente.png?v=1724697596"
        p['images'] = [
            "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/jaqueta-frente.png?v=1724697596",
            "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/costas.png?v=1724697597",
            "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/lateral-02.jpg?v=1724697596",
            "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/lateral-01.jpg?v=1724697597"
        ]
        print("Fixed Jaqueta de Pesca photos")

    # Rename Porta Pernada e Chicote to Porta Pernada Cano
    if name == "Porta Pernada e Chicote":
        p['name'] = "Porta Pernada Cano"
        p['slug'] = "porta-pernada-cano"
        print("Renamed Porta Pernada e Chicote to Porta Pernada Cano")

    # Linha Verax category change
    if name == "Linha Multi Verax 4X 300m":
        p['category'] = "Acessórios"
        # We keep the section as Lançamentos since it should stay there
        print("Moved Linha Multi Verax to category Acessórios")

# Group products contiguously by their category/section
# To make sure "Chicotes Montados (3 unidades)" is grouped contiguously with other Montagem products
# Let's inspect the categories of all products and group them

# We will sort products by:
# 1. Section (Lançamentos first)
# 2. Category (to keep Montagem, Organização, Suportes, etc., grouped)
def sort_key(p):
    sec = p.get('section')
    cat = p.get('category')
    
    # Lançamentos section should be first
    sec_order = 0 if sec == 'Lançamentos' else 1
    
    # Group by category order
    cat_order = {
        "Montagem": 1,
        "Atrativos": 2,
        "Suportes": 3,
        "Organização": 4,
        "Proteção": 5,
        "Vestuário": 6,
        "Acessórios": 7
    }.get(cat, 99)
    
    return (sec_order, cat_order)

sorted_products = sorted(cleaned, key=sort_key)

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(sorted_products, indent=2, ensure_ascii=False) + ';\n')

print(f"Data.js reorganization complete. Total products: {len(sorted_products)}")
