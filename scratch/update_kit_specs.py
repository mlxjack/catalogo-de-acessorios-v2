import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

for p in products:
    if 'kit atrativo cônico' in p['name'].lower():
        p['specs'] = {
            "Material": "EVA Floating de altíssima flutuabilidade",
            "Conteúdo": "5 filetes com 10 unidades cada (Total de 50 atrativos por pacote)",
            "Indicação": "Pesca de praia (surfcasting), costão e montagens com iscas naturais",
            "Função": "Elevar a isca da areia, aumentar o movimento natural e expor melhor o anzol"
        }
        print("Updated specs for Kit Atrativo Cônico.")

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')

print("Fim do processo!")
