import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

cleaned_products = []

# Identificar produtos para fusão/remoção
varal_chumbada = None
suporte_slim = None
porta_pernada_cano = None  # ID 32 "Porta Pernada e Chicote"

for p in products:
    name = p['name']
    if name == "Varal Chumbada":
        varal_chumbada = p
    elif name == "Suporte de Vara Slim":
        suporte_slim = p
    elif name == "Porta Pernada e Chicote":
        porta_pernada_cano = p

# Listas de remoção
to_remove_names = {
    # 1. Anzóis e Kits de Anzóis
    "Anzol 50656 (Pct com 15)",
    "Anzol 53117 (Pct com 15)",
    "Anzol A1 Kisu Premium QUIMIPOINT (Pct com 15)",
    "Anzol A4 Kisu Premium Quimipoint (Pct com 15)",
    "Anzol A5 Kisu Premium Quimipoint (Pct com 15)",
    "Anzol Aji Sendou Premium",
    "Anzol Akita Kitsune Premium (Pct com 15)",
    "Anzol Akita Kitsune Premium QUIMIPOINT (Pct com 15)",
    "Anzol Akita Sode Premium (Pct com 15)",
    "Anzol Akitasune (Pct com 15)",
    "Anzol Atleta Kisu Premium QUIMIPOINT",
    "Anzol Chinu (Pct com 15)",
    "Anzol First Kisu Premium (Pct com 15)",
    "Anzol Fune Karei Premium QUIMIPOINT",
    "Anzol Iseama (Pct com 15)",
    "Anzol Izumezina (Pct com 15)",
    "Anzol Keiryu (Pct com 15)",
    "Anzol Kisu Libero Premium QUIMIPOINT (Pct com 15)",
    "Anzol Kitsune (Pct com 15)",
    "Anzol Maruseigo XC (Pct com 15)",
    "Anzol Sode (Pct com 15)",
    "Anzol Yamame Premium QUIMIPOINT",
    "Kit Anzol 60° - 10 unidades",
    "Kit Anzol 60° com Mola - 10 unidades",
    "Kit Anzol 90° - 10 unidades",
    "Kit Anzol EWG - 10 unidades",
    "Apoio Anzol Cano",
    "Apoio para Anzol",
    
    # 2. Produtos fundidos em outros
    "Kit Parte Superior do Varal para Chicotes - Com Tubo de Alumínio Incluído - Chumbada Oficial",
    "Apoio de Borracha",
    "Copo de Borracha",
    
    # 3. Iscas Artificiais e Outros itens de pesca do lago/pesqueiro que não pertencem a acessórios
    "Kit Anteninha Átomo 11mm - 2 Unidades",
    "Kit Isca Artificial Camarão Offset Articulado",
    "Kit Isca Artificial Batelouca",
    "Isca Artificial Boom Paddle",
    "Isca Artificial AjiTwin",
    "Isca Artificial AjiStingV",
    "Kit Isca Artificial AjiNeedle",
    "Kit Isca Artificial AjiBall",
    "Isca Artificial AjiBeast",
    "Jig Head AJI",
    "Isca Artificial AjiMizu",
    "Isca Artificial AjiRing",
    "Isca Artificial AjiSho",
    "Kit Isca Artificial AjiKaze",
    "Kit Isca Artificial AjiFukura",
    "Kit Isca Artificial AjiNagare",
    "Isca Artificial AjiHane",
    "Miçanga Micro Tubo",
    "Linha de Pesca"
}

# Realizar fusões
# A. Kit Parte Superior do Varal para Chicotes => Varal Chumbada
if varal_chumbada:
    # Garantir que a imagem do Kit Superior está na galeria do Varal
    kit_img = "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/varal-01_2.png?v=1739457551"
    if kit_img not in varal_chumbada['images']:
        varal_chumbada['images'].append(kit_img)
    
    # Associar a varImage correspondente
    if 'varImages' not in varal_chumbada or not varal_chumbada['varImages']:
        varal_chumbada['varImages'] = {}
    varal_chumbada['varImages']['Superior com tubo'] = kit_img
    print("Merged Varal Kit into Varal Chumbada")

# B. Apoio de Borracha e Copo de Borracha => Suporte de Vara Slim
if suporte_slim:
    # Adicionar variações de reposição
    if 'vars' not in suporte_slim or not suporte_slim['vars']:
        suporte_slim['vars'] = []
    
    # Adicionar se não existirem
    var_names = [v[0] for v in suporte_slim['vars']]
    if 'Apoio de Borracha (Reposição)' not in var_names:
        suporte_slim['vars'].append(['Apoio de Borracha (Reposição)', 'R$ 4,00'])
    if 'Copo de Borracha (Reposição)' not in var_names:
        suporte_slim['vars'].append(['Copo de Borracha (Reposição)', 'R$ 5,00'])
        
    # Adicionar imagens na galeria
    apoio_img = "assets/img/shopify/apoio_borracha.jpg"
    copo_img = "assets/img/shopify/Copo_borracha.jpg"
    copo_img2 = "assets/img/shopify/Copo_borracha1.png"
    
    for img in [apoio_img, copo_img, copo_img2]:
        if img not in suporte_slim['images']:
            suporte_slim['images'].append(img)
            
    # Mapear varImages
    if 'varImages' not in suporte_slim or not suporte_slim['varImages']:
        suporte_slim['varImages'] = {}
    suporte_slim['varImages']['Apoio de Borracha (Reposição)'] = apoio_img
    suporte_slim['varImages']['Copo de Borracha (Reposição)'] = copo_img
    print("Merged Apoio & Copo de Borracha into Suporte Slim")

# C. Apoio para Anzol e Apoio Anzol Cano => Porta Pernada e Chicote (ID 32)
if porta_pernada_cano:
    # Adicionar variação
    if 'vars' not in porta_pernada_cano or not porta_pernada_cano['vars']:
        porta_pernada_cano['vars'] = []
        
    var_names = [v[0] for v in porta_pernada_cano['vars']]
    if 'Apoio de Anzol (Reposição)' not in var_names:
        porta_pernada_cano['vars'].append(['Apoio de Anzol (Reposição)', 'R$ 2,69'])
        
    # Adicionar imagens reais
    apoio_real_img = "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/apoio.png?v=1725024070"
    suporte_img = "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/suporte-3_49d86944-6027-4fee-a41f-89707bb55c86.png?v=1725024074"
    
    for img in [apoio_real_img, suporte_img]:
        if img not in porta_pernada_cano['images']:
            porta_pernada_cano['images'].append(img)
            
    # Mapear varImages
    if 'varImages' not in porta_pernada_cano or not porta_pernada_cano['varImages']:
        porta_pernada_cano['varImages'] = {}
    porta_pernada_cano['varImages']['Apoio de Anzol (Reposição)'] = apoio_real_img
    print("Merged Apoio para Anzol & Apoio Anzol Cano into Porta Pernada e Chicote")

# Filtrar e reordenar
for p in products:
    name = p['name']
    if name in to_remove_names:
        print(f"Removing: {name}")
        continue
    
    # Corrigir a jaqueta de pesca para Vestuário
    if name == "Jaqueta de Pesca":
        p['category'] = "Vestuário"
        p['section'] = "Vestuário"
        print("Moved Jaqueta de Pesca to Vestuário")
        
    cleaned_products.append(p)

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(cleaned_products, indent=2, ensure_ascii=False) + ';\n')

print(f"Done! Cleaned products size: {len(cleaned_products)}")
