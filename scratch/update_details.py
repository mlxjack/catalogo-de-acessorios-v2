import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_json = parts[1].rsplit(';', 1)[0]
products = json.loads(products_json)

for p in products:
    name_lower = p['name'].lower()
    
    if 'adaptador da secret' in name_lower:
        desc = p['description']
        desc = desc.replace('a parte superior do Varal', 'a parte superior do <a href="#/produto/varal-chumbada">Varal</a>')
        desc = desc.replace('onde o Varal', 'onde o <a href="#/produto/varal-chumbada">Varal</a>')
        p['description'] = desc
        print('Updated adaptador link')
        
    if 'suporte de vara slim' in name_lower:
        p['specs'] = {
            'Material': 'Estrutura em alumínio com peças em borracha e plástico premium',
            'Tamanhos Disponíveis': '40cm, 60cm, 85cm, 1m, 1,20m',
            'Itens Avulsos (Reposição)': 'Apoio de Borracha, Copo de Borracha, e Cano (podem ser adquiridos separadamente)'
        }
        print('Updated suporte slim specs')

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
