import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    name_lower = p['name'].lower()
    
    # 1. Rotor de Engate Rápido Cabeça de Cobra para Montagem
    if 'cabeça de cobra' in name_lower:
        p['category'] = 'Montagem'
        print("Updated Cabeça de Cobra category to Montagem")
        
    # 2. Linha Verax para Montagem
    if 'verax' in name_lower:
        p['category'] = 'Montagem'
        print("Updated Verax category to Montagem")
        
    # 3. Dedeira para Proteção
    if 'dedeira' in name_lower:
        p['category'] = 'Proteção'
        print("Updated Dedeira category to Proteção")

# Refazer o agrupamento
for p in products:
    if p.get('section') == 'Lançamentos':
        continue
    p['section'] = p['category']

# Ordem desejada para as seções na home
section_order = [
    'Lançamentos',
    'Atrativos',
    'Linhas',
    'Linha Terminal e Kits',
    'Montagem',
    'Medição',
    'Suportes',
    'Organização',
    'Proteção',
    'Peças',
    'Acessórios',
    'Vestuário'
]

grouped_products = {sec: [] for sec in section_order}
other_sec_products = []

for p in products:
    sec = p.get('section', 'Outros')
    if sec in grouped_products:
        grouped_products[sec].append(p)
    else:
        mapped = False
        for s_order in section_order:
            if s_order.lower() in sec.lower() or sec.lower() in s_order.lower():
                grouped_products[s_order].append(p)
                mapped = True
                break
        if not mapped:
            other_sec_products.append(p)

final_products = []
for sec in section_order:
    final_products.extend(grouped_products[sec])
final_products.extend(other_sec_products)

# Remover seções vazias de final_products (por exemplo, se Linhas ou Linha Terminal e Kits estiverem vazias por causa da mudança de categoria)
# Na verdade, o python map mantém itens vazios na lista, mas final_products só estende se houver produtos nela. Então está correto.

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(final_products, indent=2, ensure_ascii=False) + ';\n')

print("Dados reorganizados com sucesso!")
