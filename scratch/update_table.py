import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products_json = parts[1].rsplit(';', 1)[0]
products = json.loads(products_json)

table_html = """
<h4>Tabela de Medidas</h4>
<table class="size-table">
  <thead>
    <tr>
      <th>Tamanho</th>
      <th>P</th>
      <th>M</th>
      <th>G</th>
      <th>GG</th>
      <th>EXG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Largura</td>
      <td>56</td>
      <td>58</td>
      <td>60</td>
      <td>62</td>
      <td>68</td>
    </tr>
    <tr>
      <td>Altura</td>
      <td>65</td>
      <td>67</td>
      <td>70</td>
      <td>72</td>
      <td>80</td>
    </tr>
  </tbody>
</table>
"""

for p in products:
    if 'blusa corta vento' in p['name'].lower():
        desc = p['description']
        # Remove a imagem original da tabela
        desc = desc.replace('<img alt="" src="assets/img/shopify/Tabela-de-tamanhos-corta-vento_2.png">', '')
        # Se houver outras variações da tag img, tentar limpar via replace simples:
        desc = desc.replace('<img alt="" src="assets/img/shopify/Tabela-de-tamanhos-corta-vento_2.png" />', '')
        
        # Anexa a tabela de medidas no final ou inicio da desc? A imagem ficava no começo. Vamos colocar no final que fica melhor.
        p['description'] = desc + table_html

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')
print("Tabelas de medidas adicionadas com sucesso nas blusas corta vento!")
