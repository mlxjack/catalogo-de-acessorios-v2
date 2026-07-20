import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

# Vamos definir o mapeamento de seção para cada produto
# Se o produto for lançamentos (conforme verificado), mantemos.
# Caso contrário, vamos mapear cada categoria diretamente como sua seção para simplificar e garantir harmonia
for p in products:
    if p.get('section') == 'Lançamentos':
        continue
    # Usar a categoria como seção para ficar tudo bem agrupado
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

# Agrupar produtos
grouped_products = {sec: [] for sec in section_order}
# Se houver alguma seção que não esteja na lista, criamos um fallback
other_sec_products = []

for p in products:
    sec = p.get('section', 'Outros')
    if sec in grouped_products:
        grouped_products[sec].append(p)
    else:
        # Se for alguma variação de string por causa de acentos, tentamos mapear
        mapped = False
        for s_order in section_order:
            if s_order.lower() in sec.lower() or sec.lower() in s_order.lower():
                grouped_products[s_order].append(p)
                mapped = True
                break
        if not mapped:
            other_sec_products.append(p)

# Montar a lista final contígua
final_products = []
for sec in section_order:
    final_products.extend(grouped_products[sec])
final_products.extend(other_sec_products)

# Verificar se não perdemos nenhum produto no caminho
print(f"Total original: {len(products)}")
print(f"Total agrupado: {len(final_products)}")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(final_products, indent=2, ensure_ascii=False) + ';\n')

print("Produtos agrupados por seção com sucesso!")
