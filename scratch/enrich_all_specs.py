import json

data_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'

with open(data_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

parts = js_content.split('window.PRODUCTS = ')
header = parts[0]
products = json.loads(parts[1].rsplit(';', 1)[0])

# Dicionário de especificações ricas
specs_enrichment = {
    "clip vara": {
        "Material": "Borracha flexível de alta qualidade",
        "Conteúdo": "1 Clip Vara e Fita Dupla Face 3M de alta aderência",
        "Fixação": "Adesiva (Paredes, barcos, caiaques, bancadas)",
        "Indicação": "Organização e apoio seguro para varas de pesca (evita riscos)"
    },
    "atrativo comum": {
        "Material": "EVA Floating macio e flexível",
        "Conteúdo": "5 filetes com 10 unidades cada (Total de 50 atrativos por pacote)",
        "Função": "Flutuabilidade da isca, atração visual por cor/movimento e exposição do anzol",
        "Indicação": "Montagem de chicotes para pesca de praia (surfcasting) e costão"
    },
    "atrativo holográfico": {
        "Material": "EVA Floating macio e flexível com brilho holográfico",
        "Conteúdo": "5 filetes com 10 unidades cada (Total de 50 atrativos por pacote)",
        "Função": "Flutuabilidade da isca, atração visual por cor/movimento e exposição do anzol",
        "Indicação": "Montagem de chicotes para pesca de praia (surfcasting) e costão"
    },
    "mini atrativo comum": {
        "Material": "EVA Floating de altíssima flutuabilidade",
        "Conteúdo": "Pacote com atrativos mini",
        "Função": "Alta atração visual, leveza na isca e flutuação próxima ao anzol",
        "Indicação": "Pescaria de praia e costão com anzóis menores"
    },
    "mini atrativo holográfico": {
        "Material": "EVA Floating com reflexo holográfico brilhante",
        "Conteúdo": "Pacote com atrativos mini holográficos",
        "Função": "Máxima visibilidade em águas claras ou escuras, flutuabilidade no anzol",
        "Indicação": "Pescaria de praia (surfcasting) e costão"
    },
    "cabeça de cobra": {
        "Material": "Aço carbono e latão niquelado",
        "Conteúdo": "8 unidades por embalagem",
        "Tamanhos": "P (Chicotes até 0,40mm / Pernadas 0,20 a 0,28mm) | G (Chicotes até 0,62mm / Pernadas 0,28 a 0,42mm)",
        "Função": "Troca rápida de pernadas sem nós e rotação anti-torção"
    },
    "snap universal": {
        "Material": "Snap em aço inox e protetor Cobrenó em borracha termoplástica",
        "Indicação": "Conexão rápida entre chumbada e chicote de pesca",
        "Função": "Facilitar a troca de chumbadas e proteger o nó contra enroscos e sujeira"
    },
    "stopper oliva": {
        "Material": "Borracha macia de alta qualidade (Alta aderência)",
        "Função": "Limitador/Stopper móvel ajustável, regulagem de pernadas/boias e fusível de impacto na linha",
        "Indicação": "Chicotes de pesca de praia, costão e montagens Down Shot"
    },
    "stopper cilíndrico": {
        "Material": "Borracha de alta aderência com cabo de aço de transferência",
        "Conteúdo": "Kit com 2 fardos contendo 10 unidades cada (Total 20 stoppers)",
        "Diferencial": "Fixação ultra firme com pega anatômica e cabo de aço colado",
        "Indicação": "Travas seguras em linhas de chicote para pesca pesada ou praia"
    },
    "rotor de engate rápido v": {
        "Material": "Aço inox de alta tração",
        "Tamanhos": "Micro (Pernada 0,13 a 0,18mm) | P (0,20 a 0,26mm) | M (0,26 a 0,31mm) | G (0,31 a 0,45mm)",
        "Função": "Engate ultra rápido e livre rotação para pernadas de chicotes de pesca"
    },
    "destorcedores": {
        "Material": "Aço Inoxidável de alta resistência",
        "Capacidades": "7mm (4Kg) | 11mm (19Kg) | 15mm (35Kg) | 25mm (75Kg)",
        "Função": "Evitar a torção da linha de pesca, garantindo melhor sensibilidade e durabilidade",
        "Indicação": "Montagem de chicotes, líderes e pescaria de praia, rio e mar"
    },
    "destorcedor triplo": {
        "Material": "Aço Inoxidável reforçado",
        "Função": "Evitar a torção de linhas em montagens do tipo Down Shot ou esperas",
        "Indicação": "Pescarias de espera de peixes ariscos (como piapara e piauçu) e pesca de praia"
    },
    "snap single": {
        "Material": "Aço inoxidável de alta resistência",
        "Conteúdo": "Um pacote",
        "Função": "Troca rápida e prática de chicotes, líderes ou chumbadas",
        "Diferencial": "Design compacto e reforçado de abertura única"
    },
    "snap double": {
        "Material": "Aço inoxidável de alta resistência",
        "Conteúdo": "Um pacote",
        "Função": "Troca rápida e prática de acessórios sem a necessidade de cortar a linha",
        "Diferencial": "Formato único com duas aberturas independentes"
    },
    "snap gota": {
        "Material": "Aço inoxidável de alta resistência",
        "Conteúdo": "Um pacote",
        "Função": "Conexão de chumbadas no chicote com livre articulação",
        "Diferencial": "Ponta arredondada em gota que facilita o movimento"
    },
    "snap francês": {
        "Material": "Aço inoxidável de alta resistência",
        "Conteúdo": "Um pacote",
        "Função": "Troca ultra rápida de chicotes, líderes e montagens",
        "Indicação": "Pescarias dinâmicas de praia ou costão (potencializado em conjunto com o Cobrenó)"
    },
    "régua cantoneira": {
        "Material": "Cantoneira plástica especial resistente e adesivo de alta aderência",
        "Dimensões": "15cm de largura (Medidas extremamente precisas e aferidas individualmente)",
        "Diferenciais": "Cantos arredondados, raio antiqueda para transporte e cola à prova d'água"
    },
    "nano pipe": {
        "Material": "Borracha de alta qualidade (Não gruda e não trinca)",
        "Compatibilidade": "Canos de esgoto de 2 polegadas (50 milímetros)",
        "Funções": "Apoio seguro sem riscar, suportes para saca anzol, iscador, tesoura, pano e chicotes"
    },
    "apoio para barco com elástico": {
        "Material": "Borracha macia soft flexível (Proteção contra trincas/arranhões)",
        "Encaixe": "Cantoneira para cantos de 90 graus (Dispensa furos, parafusos ou cola)",
        "Indicação": "Transporte seguro de varas de pesca em barcos de alumínio"
    },
    "kit suporte carretilha": {
        "Material": "Plástico de engenharia de alta densidade",
        "Conteúdo": "Kit com 4 peças (Acompanha 4 parafusos e 4 buchas)",
        "Instalação": "Vertical (Perfeito para economizar espaço em paredes e garagens)"
    },
    "adaptador de vara para suporte": {
        "Material": "Alumínio de alta resistência e borracha especial UV (Não degrada no sol/chuva)",
        "Diferencial": "Apoio traseiro para iscagem ou troca de chicotes com as mãos livres",
        "Regulagem": "Altura sob pressão sem necessidade de parafusos ou travas"
    },
    "copo organizador": {
        "Material": "Plástico rígido de alta durabilidade",
        "Conteúdo": "Kit com tamanhos P, M e G",
        "Indicação": "Organizar stoppers, chumbadas, dedeiras (P/M) e carretéis de chicotes (G)"
    },
    "copo para carretel g": {
        "Material": "Plástico rígido de alta durabilidade com tampa segura",
        "Capacidade": "Comporta 5 carretéis de chicotes (Até 25 chicotes guardados)",
        "Indicação": "Proteção e organização rápida de chicotes e pernadas de pesca de praia"
    },
    "porta elastricot": {
        "Material": "Polietileno leve e resistente (Não incomoda no pescoço)",
        "Diferencial": "Ausência de furos (Sem necessidade de soprar a linha ou usar agulhas)",
        "Uso": "Fácil manuseio com as mãos, ideal para pescarias noturnas"
    },
    "porta isca e chumbada": {
        "Material": "Plástico de engenharia com tampa de rosca de alta segurança",
        "Funções": "Organizar chumbadas na caixa de pesca ou armazenar iscas naturais na beira da água",
        "Diferenciais": "Alça de engate rápido e tampa com furos de ventilação para iscas"
    },
    "porta pernada compacto": {
        "Capacidade": "Armazena até 68 anzóis em 34 divisórias (Design de baixa espessura)",
        "Compatibilidade de Linhas": "Trava pernadas com linhas de 0,10mm a 0,60mm",
        "Indicação": "Organização segura e compacta de pernadas e chicotes de pesca"
    },
    "suporte para molinetes": {
        "Material": "Estrutura plástica robusta e durável",
        "Capacidade": "Acomoda até 3 molinetes grandes ou 4 molinetes pequenos",
        "Conteúdo": "Acompanha 2 buchas e 2 parafusos para fixação na parede"
    },
    "protetor de bobina p e g": {
        "Material": "Elástico de alta densidade com costura reforçada",
        "Funções": "Proteger a linha contra sol, chuva e atritos, e fixar o snap do arranque sem usar a unha do carretel",
        "Indicação": "Bobinas de molinetes de diversos tamanhos"
    },
    "dedeira": {
        "Material": "Neoprene soft / Couro sintético reforçado",
        "Variações": "Soft (Sensibilidade) | Hard (Proteção em arremesso pesado) | Ultrasoft (Conforto)",
        "Função": "Proteger o dedo indicador durante arremessos de alta potência"
    },
    "apoio de borracha": {
        "Material": "Borracha premium de alta densidade",
        "Compatibilidade": "Peça sobressalente de reposição para o suporte de vara Slim",
        "Função": "Apoio seguro anti-risco para a vara"
    },
    "copo de borracha": {
        "Material": "Borracha premium de alta densidade",
        "Compatibilidade": "Peça sobressalente de reposição para o suporte de vara Slim",
        "Função": "Apoio inferior de encaixe do pé da vara"
    },
    "apoio para anzol": {
        "Material": "Plástico rígido de engenharia leve e resistente",
        "Função": "Retirar anzóis profundos de forma rápida e segura sem machucar o peixe",
        "Tamanhos": "Disponível em P, M, G ou no Kit Completo com os 3 tamanhos"
    },
    "adaptador de carretilha": {
        "Material": "Polímero rígido resistente",
        "Conteúdo": "Kit com 4 unidades (Permite organizar até 3 carretilhas no Suporte de Molinetes)",
        "Função": "Adaptação de apoio de manivelas para armazenamento vertical no suporte padrão"
    },
    "bastão luminoso": {
        "Conteúdo": "1 unidade por embalagem química",
        "Indicação": "Pescaria noturna em conjunto com o Star Light Sinker (Chumbada Luminosa)",
        "Duração": "Alta visibilidade por várias horas consecutivas"
    },
    "cobrenó": {
        "Material": "Borracha termoplástica flexível",
        "Função": "Proteger o nó da montagem contra enroscos de anzol, acúmulo de sujeira e permitir ponta de nó maior",
        "Indicação": "Conexões de snaps, destorcedores e líderes"
    },
    "elastricot 150m": {
        "Material": "Elastômero elástico ultra fino de alta elasticidade",
        "Metragem": "150 metros",
        "Função": "Fixar e amarrar iscas moles (corrupto, camarão, lula) sem a necessidade de nós finais"
    },
    "elastricot 100m": {
        "Material": "Elastômero elástico ultra fino de alta elasticidade",
        "Metragem": "100 metros",
        "Função": "Fixar e amarrar iscas moles (corrupto, camarão, lula) sem a necessidade de nós finais"
    },
    "iscador preto ou cristal": {
        "Material": "Inox rígido de alta durabilidade e cabo anatômico",
        "Aplicação": "Iscagem prática e profissional de corrupto e camarão",
        "Indicação": "Pesca de praia e costão"
    },
    "iscador agulhão": {
        "Material": "Inox rígido de alta rigidez (não entorta) e cabo termoplástico de engenharia",
        "Uso": "Iscagem de sardinhas inteiras, em pedaços, ou lulas",
        "Diferenciais": "Ponta altamente penetrante para iscas congeladas, agulha fixa de alta durabilidade"
    },
    "iscador duplo": {
        "Material": "Inox rígido duplo e cabo anatômico",
        "Aplicação": "Iscagem prática e profissional de corrupto e camarão",
        "Diferencial": "Hastes duplas que auxiliam na sustentação da isca mole"
    },
    "micro snap": {
        "Material": "Aço inoxidável de alta resistência e protetor Cobrenó termoplástico",
        "Indicação": "Conexão rápida de chumbadas leves com proteção de nó",
        "Função": "Troca de chumbada rápida e proteção contra algas e sujeiras"
    },
    "pipa kit com 2": {
        "Material": "Plástico leve de alta flutuabilidade e asas aerodinâmicas",
        "Função": "Fazer a chumbada flutuar acima do fundo durante o recolhimento rápido, evitando enroscos",
        "Conteúdo": "Kit com 2 pipas de flutuação"
    },
    "saca anzol / desembuchador": {
        "Material": "Plástico rígido de engenharia leve e resistente",
        "Tamanhos": "Disponível em P, M, G ou no Kit Completo com os 3 tamanhos",
        "Função": "Retirar anzóis profundos de forma rápida e segura sem machucar o peixe ou perder a linha"
    },
    "agulha de tarrafa": {
        "Material": "Plástico especial flexível de alta resistência",
        "Diferencial": "Desenho que segura o nylon firmemente sem escorregar em movimentos bruscos",
        "Indicação": "Confecção e reparos artesanais de tarrafas e redes de pesca"
    },
    "alicate de pesca": {
        "Material": "Liga metálica de alta resistência revestida e pegada plástica",
        "Cor": "Laranja vibrante (Fácil localização à beira d'água)",
        "Função": "Remoção segura de garateias e anzóis de iscas artificiais ou naturais, protegendo as mãos"
    },
    "imã fix": {
        "Material": "Borracha macia protetora contra riscos na lataria e 2 superímãs de neodímio",
        "Função": "Fixação magnética instantânea na lataria do veículo para apoiar varas de pesca inclinadas",
        "Diferencial": "Protege a pintura do veículo e evita quedas ou danos nas varas"
    },
    "mini secretária": {
        "Material": "Polietileno de alta resistência contra raios UV e impactos",
        "Funções": "Bandeja de apoio compacta para tesoura, saca-anzol, iscas e preparo rápido de montagens na praia",
        "Compatibilidade": "Encaixe em suportes de vara Slim, Premium ou canos de 2 polegadas"
    },
    "tela de espremer iscas": {
        "Material": "Tela plástica de alta densidade e resistência",
        "Função": "Escoamento de líquidos e prensagem rápida de iscas moídas",
        "Indicação": "Preparo de iscas e engodos para competições ou pesca de praia"
    },
    "avental chumbada": {
        "Material": "Tecido impermeável de fácil limpeza",
        "Diferenciais": "2 bolsos frontais estratégicos para acessórios rápidos (saca-anzol, tesoura, iscador)",
        "Função": "Proteção corporal e agilidade durante o manuseio de peixes e iscas"
    },
    "boné chumbada": {
        "Material": "Algodão e Poliéster respirável",
        "Proteção": "Aba curva para máxima proteção solar UV contra raios solares",
        "Ajuste": "Fivela traseira regulável confortável"
    },
    "chapéu de palha": {
        "Material": "Palha natural de alta qualidade",
        "Aba": "Aba larga para excelente sombra de rosto e pescoço",
        "Ajuste": "Fita regulável sob o queixo para encaixe seguro"
    },
    "tubeneck tradicional": {
        "Material": "Microfibra técnica respirável de altíssima qualidade",
        "Proteção Solar": "FPS 50+ contra raios UV",
        "Diferenciais": "Formato anatômico, secagem ultra rápida e regulação térmica"
    },
    "tubeneck premium": {
        "Material": "Microfibra técnica respirável de altíssima qualidade",
        "Proteção Solar": "FPS 50+ contra raios UV",
        "Diferenciais": "Furos feitos a laser na posição da boca para evitar embaçar óculos, secagem ultra rápida, formato anatômico"
    },
    "calça corta vento esporte": {
        "Material": "Tecido técnico inteligente (bloqueia vento e respingos)",
        "Diferenciais": "Design esportivo, caimento ergonômico, ótima respirabilidade e secagem rápida",
        "Indicação": "Treinos e pescarias em condições de ventania ou chuva leve"
    },
    "calça elastic comfort": {
        "Material": "Tecido técnico elástico de alta performance",
        "Diferenciais": "Flexibilidade total de movimentos, respirabilidade e resistência a rasgos",
        "Indicação": "Vestuário esportivo para pescadores e atletas exigentes"
    },
    "blusa corta vento comfort": {
        "Material": "Tecido técnico leve corta-vento (Semi-impermeável)",
        "Diferenciais": "Design ultraleve e compacto (não ocupa espaço na mochila), estilo versátil para uso diário",
        "Proteção": "Bloqueio eficiente contra vento frio e respingos d'água"
    },
    "blusa corta vento esporte": {
        "Material": "Tecido técnico leve corta-vento (Semi-impermeável)",
        "Diferenciais": "Design ultraleve e compacto, ótimo caimento para prática esportiva dinâmica",
        "Proteção": "Bloqueio eficiente contra vento frio e respingos d'água"
    },
    "blusa corta vento presa viva": {
        "Material": "Tecido técnico leve corta-vento (Semi-impermeável) especial Presa Viva",
        "Diferenciais": "Design ultraleve, alta durabilidade e costuras elásticas reforçadas",
        "Proteção": "Bloqueio de vento e conforto térmico excepcional na beira da água"
    }
}

# Atualizar specs
count = 0
for p in products:
    name_lower = p['name'].lower()
    
    # Buscar correspondência no dicionário
    matched_specs = None
    for key, val in specs_enrichment.items():
        if key in name_lower:
            matched_specs = val
            break
            
    if matched_specs:
        p['specs'] = matched_specs
        count += 1

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(header + 'window.PRODUCTS = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\n')

print(f"Especificações atualizadas com sucesso para {count} produtos!")
