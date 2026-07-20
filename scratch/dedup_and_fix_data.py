import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

# 1. Names to remove completely (duplicates or variations merged into parents)
names_to_remove = {
    # Duplicates from CSV matching existing items
    "Alicate Chumbada",
    "Apoio Barco de Borracha com Elástico",
    "Cobre Nó (Pacote com 40)",
    "Copo Para Carretel de Chicotes",
    "Kit Adaptador de Carretilha",
    "Kit Suporte Para Carretilha e Molinete Individual",
    "Miçanga de Vidro",
    "Kit Nó de Correr",
    "Pipa",
    "Protetor de Bobina Chumbada",
    "Saca Anzol Competição Nano",
    "Stopper Modelo Cilíndrico",
    "Stopper Modelo Oliva",
    "Tela de Espremer Isca Chumbada",
    "Toalha Chumbada",
    
    # Newly added individual chicotes (will be merged into "Chicotes Montados (3 unidades)")
    "Chicote - BEIRA 1,00m - 3 Unidades",
    "Chicote - MEIA ÁGUA 1,15m - 3 Unidades",
    "Chicote - FUNDO 1,30m - 3 Unidades",
    "Chicote - FUNDO 1,80m - 3 Unidades",
    "Chicote FINESSE- 85cm",
    
    # Old Porta Pernadas e Chicotes (newly added version) to keep only the updated ID 73
    "Porta Pernadas e Chicotes"
}

# Filter out the removed products
filtered_products = []
id_73_prod = None
id_32_prod = None

for p in products:
    if p['name'] in names_to_remove:
        continue
    
    if p.get('id') == 73:
        id_73_prod = p
    elif p.get('id') == 32:
        id_32_prod = p
    else:
        filtered_products.append(p)

# 2. Fix flat board product (originally ID 73, was named "Chicotes Montados (3 unidades)")
if id_73_prod:
    id_73_prod['name'] = "Porta Pernadas e Chicotes"
    id_73_prod['slug'] = "porta-pernadas-e-chicotes"
    id_73_prod['category'] = "Organização"
    id_73_prod['section'] = "Organização"
    id_73_prod['price'] = "R$ 29,90"
    id_73_prod['img'] = "assets/img/shopify/sedalha-areia-capa.png"
    id_73_prod['images'] = [
        "assets/img/shopify/sedalha-areia-capa.png",
        "assets/img/shopify/sedalha-areia.png",
        "assets/img/shopify/sedalha-azul.png",
        "assets/img/shopify/sedalha-azul-claro.png",
        "assets/img/shopify/sedalha-rosa.png",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_branco.jpg?v=1738591758",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_preto.jpg?v=1738591758"
    ]
    id_73_prod['swatches'] = [
        ["Azul", "#2563eb"],
        ["Branco", "#ffffff"],
        ["Rosa", "#ec4899"],
        ["Areia", "#ece0ca"],
        ["Preto", "#111827"]
    ]
    id_73_prod['colorImages'] = {
        "Azul": "assets/img/shopify/sedalha-azul.png",
        "Branco": "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_branco.jpg?v=1738591758",
        "Rosa": "assets/img/shopify/sedalha-rosa.png",
        "Areia": "assets/img/shopify/sedalha-areia.png",
        "Preto": "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/porta_pernada_e_chicotes_preto.jpg?v=1738591758"
    }
    id_73_prod['vars'] = None
    id_73_prod['sizes'] = None
    id_73_prod['description'] = "<p>Este produto contém 30 canais superiores e 30 canais inferiores. Nele é possível acomodar pernadas (anzóis empatados), chicotes com pernadas. A vantagem do porta pernada e chicote é que o mesmo causa menos memória nas linhas usadas por mantê-las esticadas, outra vantagem é seu formato plano comprido que ocupa pouco espaço em sua caixa de pesca.</p><p>Medida: 32 x 8,5 cm</p>"
    id_73_prod['specs'] = {
        "Comprimento/Medida": "8,5 CM",
        "Dimensões": "32X8,5CM",
        "Capacidade": "60 Canais (30 Sup. / 30 Inf.)",
        "Indicação": "Acomodar pernadas (anzóis empatados)"
    }
    filtered_products.append(id_73_prod)
    print("Reconfigured flat Porta Pernadas e Chicotes (ID 73)")

# 3. Fix cylindrical cano product (ID 32, "Porta Pernada e Chicote")
if id_32_prod:
    id_32_prod['name'] = "Porta Pernada e Chicote"
    id_32_prod['swatches'] = [
        ["Azul", "#2563eb"],
        ["Branco", "#ffffff"],
        ["Marrom", "#8a5a36"]
    ]
    id_32_prod['colorImages'] = {
        "Azul": "assets/img/shopify/SomenteCanoAzul_9e637403-fc0c-41ff-ad30-463aac2483d6.jpg",
        "Branco": "assets/img/shopify/SomenteCanoBranco_edf334b2-400f-4657-b93d-32b34b7b5256.jpg",
        "Marrom": "assets/img/shopify/30cm-marrom_4aa55bbc-ab4f-44e0-9c37-d56b04cf00f8.png"
    }
    id_32_prod['vars'] = [
        ["30cm", "R$ 30,00"],
        ["40cm", "R$ 32,00"],
        ["50cm", "R$ 34,00"],
        ["60cm", "R$ 36,00"],
        ["70cm", "R$ 38,00"],
        ["80cm", "R$ 40,00"],
        ["100cm", "R$ 44,00"]
    ]
    id_32_prod['varImages'] = {
        "30cm": "assets/img/shopify/somente-cano-30cm_e136635e-c403-47ce-a25a-524284107c07.png",
        "40cm": "assets/img/shopify/somente-cano-40cm_e6bca2ec-d0b2-4b79-b6cf-30cf21387706.png",
        "50cm": "assets/img/shopify/somente-cano-50cm_6e62cfdb-4e63-492e-8e19-f6db40bd566a.png",
        "60cm": "assets/img/shopify/somente-cano-60cm_f8423987-a950-424a-9d80-679e41447737.png",
        "70cm": "assets/img/shopify/somente-cano-70cm_bcfbc84d-03ad-489d-87fa-50f969953709.png",
        "80cm": "assets/img/shopify/somente-cano-80cm_78f92977-f490-467b-92c2-d9fa9b1067dd.png",
        "100cm": "assets/img/shopify/somente-cano-100cm_a52c9c44-de3c-40a3-990c-bda2fabe13dd.png"
    }
    filtered_products.append(id_32_prod)
    print("Reconfigured cylindrical Porta Pernada e Chicote (ID 32)")

# 4. Create the actual "Chicotes Montados (3 unidades)" parent product
chicotes_montados_parent = {
    "id": 730,
    "slug": "chicotes-montados-3-unidades",
    "category": "Montagem",
    "name": "Chicotes Montados (3 unidades)",
    "price": "a partir de R$ 28,60",
    "img": "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/fundo-capa.webp?v=1737636375",
    "link": "https://chumbadas.com.br/collections/chicotes-montados",
    "description": "<p>Chicotes montados prontos para uso, fabricados com linhas de excelente qualidade e equipados com rotores de engate rápido com stopper.</p><ul><li><b>Beira:</b> Ideal para pesca abaixo de 40m. Linha vermelha 0.32mm.</li><li><b>Meia Água:</b> Ideal para pesca entre 40m e 100m. Linha vermelha 0.42mm.</li><li><b>Fundo:</b> Ideal para pesca acima de 100m. Linha vermelha 0.62mm.</li><li><b>Finesse:</b> Desenvolvido para capturas sutis com rotor micro V.</li></ul>",
    "images": [
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/fundo-capa.webp?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/capa-beira_p.jpg?v=1737636486",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/meia-agua-capa_1_76b66870-2364-4e10-b85c-486a4c29f38f.webp?v=1737637449",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/fundo_capa.webp?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/chicote-finesse-capa.webp?v=1737637378",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-13_9199f71d-b95c-4d72-b1b0-16fb351fcf0c.png?v=1737636486",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-14_d5202550-ffd9-43cf-95ae-3c796c3b4b63.png?v=1737636486",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-09_4abfa100-cd27-470b-85a7-eb51806ef1f3.png?v=1737637449",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-10_698c8c9b-51b5-4cae-aaeb-45cdeb2baa40.png?v=1737637449",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-11_2746424b-ff6c-48ad-9fe2-57969ea201c4.png?v=1737637449",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-12_6b0c46f0-c752-46a6-b59b-68879349053a.png?v=1737637449",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-01_0687d65a-ff2c-4c55-bbac-f497a0217c6b.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-02_f11db813-2538-41a9-ae54-140dcf0e107f.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-03_5b05a6b5-da11-4f4e-89cc-68d94747e16b.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-04_5eac5caa-0e32-40ed-993c-bc826855adb9.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-17_42f1ff77-58eb-4f62-8111-c3521ea8566e.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-18_60bd0fae-18fc-4833-8608-e9e7aaebccb1.png?v=1737636375",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-05_2a35b456-ea1f-4c96-a08e-7f1fc759c71d.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-06_eb775414-8375-477e-8a2c-294a0f142218.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-07_db0d0216-b8ce-44ba-8762-4cdabc72bff3.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-08_41a4da33-8559-469e-9ffa-6ce1cadaf1fa.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-153_f237610c-46e0-4309-984d-51f34858faf3.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-16_ded8a465-57af-4eec-8e09-425e61590955.png?v=1737636782",
        "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/chicote-finesse.png?v=1737637378"
    ],
    "video": "",
    "specs": {
        "Material": "Monofilamento / Fluorocarbono",
        "Quantidade": "3 unidades por pacote",
        "Rotores": "Equipado com Rotores de Engate Rápido e Stopper"
    },
    "vars": [
        ["Beira - Modelo 13", "R$ 28,60"],
        ["Beira - Modelo 14", "R$ 28,60"],
        ["Meia Água - Modelo 9", "R$ 28,60"],
        ["Meia Água - Modelo 10", "R$ 28,60"],
        ["Meia Água - Modelo 11", "R$ 28,60"],
        ["Meia Água - Modelo 12", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 1", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 2", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 3", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 4", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 17", "R$ 28,60"],
        ["Fundo 1,30m - Modelo 18", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 5", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 6", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 7", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 8", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 15", "R$ 28,60"],
        ["Fundo 1,80m - Modelo 16", "R$ 28,60"],
        ["Finesse 85cm - Rotor Micro V", "R$ 33,80"]
    ],
    "varImages": {
        "Beira - Modelo 13": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-13_9199f71d-b95c-4d72-b1b0-16fb351fcf0c.png?v=1737636486",
        "Beira - Modelo 14": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-14_d5202550-ffd9-43cf-95ae-3c796c3b4b63.png?v=1737636486",
        "Meia Água - Modelo 9": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-09_4abfa100-cd27-470b-85a7-eb51806ef1f3.png?v=1737637449",
        "Meia Água - Modelo 10": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-10_698c8c9b-51b5-4cae-aaeb-45cdeb2baa40.png?v=1737637449",
        "Meia Água - Modelo 11": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-11_2746424b-ff6c-48ad-9fe2-57969ea201c4.png?v=1737637449",
        "Meia Água - Modelo 12": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-12_6b0c46f0-c752-46a6-b59b-68879349053a.png?v=1737637449",
        "Fundo 1,30m - Modelo 1": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-01_0687d65a-ff2c-4c55-bbac-f497a0217c6b.png?v=1737636375",
        "Fundo 1,30m - Modelo 2": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-02_f11db813-2538-41a9-ae54-140dcf0e107f.png?v=1737636375",
        "Fundo 1,30m - Modelo 3": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-03_5b05a6b5-da11-4f4e-89cc-68d94747e16b.png?v=1737636375",
        "Fundo 1,30m - Modelo 4": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-04_5eac5caa-0e32-40ed-993c-bc826855adb9.png?v=1737636375",
        "Fundo 1,30m - Modelo 17": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-17_42f1ff77-58eb-4f62-8111-c3521ea8566e.png?v=1737636375",
        "Fundo 1,30m - Modelo 18": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-18_60bd0fae-18fc-4833-8608-e9e7aaebccb1.png?v=1737636375",
        "Fundo 1,80m - Modelo 5": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-05_2a35b456-ea1f-4c96-a08e-7f1fc759c71d.png?v=1737636782",
        "Fundo 1,80m - Modelo 6": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-06_eb775414-8375-477e-8a2c-294a0f142218.png?v=1737636782",
        "Fundo 1,80m - Modelo 7": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-07_db0d0216-b8ce-44ba-8762-4cdabc72bff3.png?v=1737636782",
        "Fundo 1,80m - Modelo 8": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-08_41a4da33-8559-469e-9ffa-6ce1cadaf1fa.png?v=1737636782",
        "Fundo 1,80m - Modelo 15": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-153_f237610c-46e0-4309-984d-51f34858faf3.png?v=1737636782",
        "Fundo 1,80m - Modelo 16": "https://cdn.shopify.com/s/files/1/0454/5845/6736/products/modelo-16_ded8a465-57af-4eec-8e09-425e61590955.png?v=1737636782",
        "Finesse 85cm - Rotor Micro V": "https://cdn.shopify.com/s/files/1/0454/5845/6736/files/chicote-finesse.png?v=1737637378"
    },
    "section": "Montagem"
}

filtered_products.append(chicotes_montados_parent)
print("Added single parent Chicotes Montados (3 unidades) product")

# Output path and save
with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(filtered_products, indent=2, ensure_ascii=False) + ';\n')

print(f"Data.js cleanup completed. Total products: {len(filtered_products)}")
