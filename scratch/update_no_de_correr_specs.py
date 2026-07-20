import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'nó de correr' in p['name'].lower() or 'no de correr' in p['name'].lower():
        p['specs'] = {
            "Material": "Linha multifilamento especial de alta resistência e guias plásticos",
            "Conteúdo": "4 suportes plásticos guia com 3 nós cada (Total de 12 nós de correr por pacote)",
            "Indicação": "Montagem de chicotes de pesca, pernadas reguláveis e ajuste de altura de boias",
            "Função": "Atuar como trava/stopper móvel ajustável sem danificar ou marcar a linha principal"
        }
        print("Updated specs for Nó de Correr.")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')

print("Fim do processo!")
