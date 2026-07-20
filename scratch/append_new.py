import json

with open('D:/chumbada-catalogo-v2/scratch/to_add.json', 'r', encoding='utf-8') as f:
    to_add = json.load(f)

# Hardcoded duplicates / variations to SKIP
skip_list = [
    "Cobre Nó (Pacote com 40)", # Already in as Cobrenó
    "Protetor de Bobina Chumbada", # Already in as Protetor de Bobina P e G
    "Porta Pernadas e Chicotes", # Already in as Porta Pernada Compacto
    "Suporte de Vara Premium Chumbada Oficial", # Already in as Suporte Premium
    "Copo Para Carretel de Chicotes", # Already in as Copo para Carretel G
    "Kit Destorcedor", # Already in as Destorcedores / Kit? No, Destorcedores is there, maybe keep Kit
    "Stopper Modelo Cilíndrico", # Already in as Stopper Cilíndrico P, M, G
    "Kit Nó de Correr", # Already in as Nó de Correr
    "Kit Adaptador de Carretilha", # Already in as Adaptador de Carretilha
    "Apoio Barco de Borracha", # Already in as Apoio para Barco com Elástico
    "Kit Suporte Para Carretilha e Molinete Individual", # Already in as Kit Suporte Carretilha e Molinete Individual
]

filtered = [p for p in to_add if p['name'] not in skip_list]

print(f"Adding {len(filtered)} new products...")

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_js = json.loads(parts[1].rsplit(';', 1)[0])

products_js.extend(filtered)

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products_js, indent=2, ensure_ascii=False) + ';\n')

print("Products added to data.js successfully.")
