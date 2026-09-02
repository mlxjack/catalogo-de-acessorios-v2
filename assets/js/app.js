// Catálogo de Acessórios V2 - Chumbada Oficial
// Controlador principal da SPA (Single Page Application)

const PRODUCTS = window.PRODUCTS;
const CONFIG = window.CONFIG;
const PRODUCT_INDICATORS = window.PRODUCT_INDICATORS || {};

// Estado global simples para persistir filtros ao voltar de um produto
const state = {
  searchQuery: '',
  selectedCategory: 'Todos',
  selectedColor: {},     // Salva cor selecionada por id de produto: { [productId]: colorName }
  selectedVariation: {}, // Salva variação selecionada por id de produto: { [productId]: varIndex }
};

// Elementos estáticos do DOM
const appContainer = document.getElementById('app');
const logoNav = document.getElementById('logo-nav');

// Inicialização da aplicação
function init() {
  try {
    router();
    window.addEventListener('hashchange', router);
  } catch (err) {
    console.error("Erro na inicialização do roteador:", err);
  }
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Reset de busca ao clicar no logotipo
if (logoNav) {
  logoNav.addEventListener('click', () => {
    state.searchQuery = '';
    state.selectedCategory = 'Todos';
  });
}

// Roteador SPA baseado em Hash
function router() {
  const hash = window.location.hash || '#/';
  
  // Rolar para o topo ao mudar de rota de forma compatível e segura
  try {
    window.scrollTo({ top: 0, behavior: 'auto' });
  } catch (e) {
    window.scrollTo(0, 0);
  }

  // Rota do Produto: #/produto/slug-do-produto
  const productMatch = hash.match(/^#\/produto\/([\w-]+)$/);
  
  if (productMatch) {
    const slug = productMatch[1];
    const product = PRODUCTS.find(p => p.slug === slug);
    if (product) {
      renderProductDetail(product);
      updateSEOMeta(product.name, product.description);
    } else {
      // Produto não encontrado -> volta para catálogo
      window.location.hash = '#/';
    }
  } else {
    // Rota padrão (Catálogo / Home)
    renderCatalog();
    updateSEOMeta(
      "Catálogo de Acessórios | Chumbada Oficial",
      "Explore o catálogo completo de acessórios premium da Chumbada Oficial. Linhas, vestuário técnico, suportes e montagens de alta performance esportiva."
    );
  }
}

// Atualizar títulos e metadados SEO dinamicamente
function updateSEOMeta(title, description) {
  document.title = title;
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) {
    metaDesc.setAttribute('content', description.substring(0, 160));
  }
}

// Função auxiliar para escapar caracteres HTML e evitar XSS
function escapeHTML(str) {
  if (!str) return '';
  return String(str).replace(/[&<>'"]/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[c]));
}

// Função auxiliar para normalizar textos para pesquisa (remover acentos)
function normalizeText(str) {
  return String(str)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

// Verifica se o nome do arquivo de uma imagem "casa" com um texto de varia\u00e7\u00e3o/cor
function imageMatchesText(imgSrc, text) {
  if (!text || !imgSrc) return false;
  const parts = imgSrc.split('/');
  const filename = parts[parts.length - 1];
  const normFile = normalizeText(filename);
  const normalizedText = normalizeText(text).replace(/\s+/g, '-');
  const normalizedTextNoSpace = normalizeText(text).replace(/\s+/g, '');
  return normFile.includes(normalizedText) || normFile.includes(normalizedTextNoSpace) || normalizedTextNoSpace.includes(normFile.replace(/\.[\w]+$/, '').replace(/-/g, ''));
}

// ==========================================
// Indicadores visuais por foto (badge no canto inferior esquerdo)
// Usa window.PRODUCT_INDICATORS (definido em data.js) para saber, produto a
// produto e imagem a imagem, o que desenhar. Produtos sem entrada no mapa
// n\u00e3o s\u00e3o afetados \u2014 a fun\u00e7\u00e3o simplesmente retorna null e nada \u00e9 renderizado.
// ==========================================

// Barra de "capacidade de carga": funciona como um medidor de bateria/sinal \u2014
// quanto mais cheia (e mais vermelha), maior a capacidade. Cinza (Finesse,
// mais leve) at\u00e9 vermelho (Fundo, mais pesado), em vez de 4 cores arbitr\u00e1rias
// sem rela\u00e7\u00e3o entre si.
const CHICOTE_TYPE_STYLE = {
  'Finesse':   { color: '#777D84', tier: 1 },
  'Beira':     { color: '#9B5C66', tier: 2 },
  'Meia \u00c1gua': { color: '#BF3C49', tier: 3 },
  'Fundo':     { color: '#E31B2B', tier: 4 },
};

// Duas escalas: miniatura (thumb) e foto principal (main). Mesma l\u00f3gica de
// desenho para as duas, s\u00f3 muda o preset de tamanhos/posi\u00e7\u00f5es. Layout em 3
// linhas: barra de capacidade (acima) \u2192 linha+pontas+componente \u2192 medida.
const INDICATOR_PRESETS = {
  thumb: {
    w: 60, h: 26,
    barX1: 20, barX2: 50, barY: 4, barH: 4, barRadius: 2,
    lineX1: 20, lineX2: 50, lineY: 15, strokeW: 1.6,
    endRX: 1.9, endRY: 1.2, diagLen: 3,
    vSize: 1.9, beadR: 1.7,
    textY: 24, fontSize: 7.5,
  },
  main: {
    w: 150, h: 44,
    barX1: 42, barX2: 108, barY: 8, barH: 8, barRadius: 4,
    lineX1: 42, lineX2: 108, lineY: 27, strokeW: 3,
    endRX: 4.2, endRY: 2.8, diagLen: 6.5,
    vSize: 4.3, beadR: 3.7,
    textY: 40, fontSize: 12,
  },
};

// Busca a ficha do indicador (tipo/medida/linha/pontas/componente) para uma
// imagem espec\u00edfica de um produto. Associa\u00e7\u00e3o \u00e9 pelo NOME do arquivo, nunca
// pela posi\u00e7\u00e3o na galeria \u2014 se o produto ou a imagem n\u00e3o tiverem entrada no
// mapa, retorna null (nenhum indicador \u00e9 desenhado).
function getIndicatorMeta(p, imgSrc) {
  if (!imgSrc) return null;
  const map = PRODUCT_INDICATORS[p.slug];
  if (!map) return null;
  const basename = imgSrc.split('/').pop();
  return map[basename] || null;
}

// Desenha o badge SVG (bolinhas de tipo, linha, acabamento das pontas,
// componente central e texto da medida) para uma ficha de indicador.
function buildIndicatorSVG(meta, variant) {
  const P = INDICATOR_PRESETS[variant];
  const typeStyle = CHICOTE_TYPE_STYLE[meta.tipo];
  if (!P || !typeStyle) return '';

  // Barra de capacidade de carga: trilho cinza-claro + preenchimento
  // proporcional ao "tier" do tipo (1/4 a 4/4), na cor daquele tier.
  const barW = P.barX2 - P.barX1;
  const barFillW = barW * (typeStyle.tier / 4);
  const bar = `<rect x="${P.barX1}" y="${P.barY}" width="${barW}" height="${P.barH}" rx="${P.barRadius}" fill="#EDEDED" stroke="#D8D8D8" stroke-width="0.75"/>` +
    `<rect x="${P.barX1}" y="${P.barY}" width="${barFillW}" height="${P.barH}" rx="${P.barRadius}" fill="${typeStyle.color}"/>`;

  const lineColor = meta.linha === 'vermelha' ? '#E31B2B' : '#C9CED4';
  const line = `<line x1="${P.lineX1}" y1="${P.lineY}" x2="${P.lineX2}" y2="${P.lineY}" stroke="${lineColor}" stroke-width="${P.strokeW}" stroke-linecap="round"/>`;

  // Acabamento das pontas: stopper (bolinha oval preta) ou n\u00f3 de correr
  // (risco diagonal vermelho) \u2014 nunca os dois juntos.
  let ends;
  if (meta.pontas === 'stopper') {
    ends = `<ellipse cx="${P.lineX1}" cy="${P.lineY}" rx="${P.endRX}" ry="${P.endRY}" fill="#111111"/>` +
           `<ellipse cx="${P.lineX2}" cy="${P.lineY}" rx="${P.endRX}" ry="${P.endRY}" fill="#111111"/>`;
  } else {
    const d = P.diagLen;
    ends = `<line x1="${P.lineX1 - d / 2}" y1="${P.lineY - d / 2}" x2="${P.lineX1 + d / 2}" y2="${P.lineY + d / 2}" stroke="#E31B2B" stroke-width="${P.strokeW * 0.75}" stroke-linecap="round"/>` +
           `<line x1="${P.lineX2 - d / 2}" y1="${P.lineY - d / 2}" x2="${P.lineX2 + d / 2}" y2="${P.lineY + d / 2}" stroke="#E31B2B" stroke-width="${P.strokeW * 0.75}" stroke-linecap="round"/>`;
  }

  // Componente central: rotor de engate r\u00e1pido ("V" duplo preto) ou mi\u00e7anga
  // rotor (2 c\u00edrculos furados: centro branco, contorno preto).
  const midX = (P.lineX1 + P.lineX2) / 2;
  const gap = (P.lineX2 - P.lineX1) * 0.22;
  let center = '';
  if (meta.componente === 'engate') {
    const vs = P.vSize;
    [midX - gap, midX + gap].forEach(cx => {
      center += `<path d="M ${cx - vs} ${P.lineY - vs} L ${cx} ${P.lineY + vs * 0.5} L ${cx + vs} ${P.lineY - vs}" fill="none" stroke="#111111" stroke-width="${P.strokeW * 0.6}" stroke-linecap="round" stroke-linejoin="round"/>`;
    });
  } else {
    [midX - gap, midX + gap].forEach(cx => {
      center += `<circle cx="${cx}" cy="${P.lineY}" r="${P.beadR}" fill="#ffffff" stroke="#111111" stroke-width="1"/>`;
    });
  }

  const text = `<text x="${P.w / 2}" y="${P.textY}" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="${P.fontSize}" font-weight="700" fill="#111111">${escapeHTML(meta.medida)}</text>`;

  return `<svg class="prod-indicator prod-indicator--${variant}" viewBox="0 0 ${P.w} ${P.h}" width="${P.w}" height="${P.h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" style="display:block;pointer-events:none;">
    <rect x="0.5" y="0.5" width="${P.w - 1}" height="${P.h - 1}" rx="4" fill="rgba(255,255,255,0.85)" stroke="rgba(17,17,17,0.08)"/>
    ${bar}${line}${ends}${center}${text}
  </svg>`;
}

// Monta o HTML do slot posicionado (canto inferior esquerdo, pointer-events:none)
// que envolve o SVG do indicador \u2014 usado tanto nas miniaturas quanto na foto principal.
function buildIndicatorSlotHTML(meta, variant, extraStyle) {
  if (!meta) return '';
  const svg = buildIndicatorSVG(meta, variant);
  if (!svg) return '';
  return `<span class="prod-indicator-slot" style="position:absolute;left:3px;bottom:3px;pointer-events:none;line-height:0;z-index:3;${extraStyle || ''}">${svg}</span>`;
}

// Em produtos com muitas varia\u00e7\u00f5es/cores, mostra s\u00f3 as fotos gen\u00e9ricas + as da op\u00e7\u00e3o
// selecionada, escondendo o restante at\u00e9 o cliente clicar na varia\u00e7\u00e3o correspondente.
// O v\u00eddeo do produto (se houver) nunca \u00e9 afetado por esse filtro.
function getComboImage(p, colorName, varName) {
  if (!p.variantImageMap) return null;
  return p.variantImageMap[`${varName}::${colorName}`] || p.variantImageMap[varName] || null;
}

function getVisibleGalleryImages(p, colorName, varName) {
  if (!p.images) return [];

  // Modo estrito: produto com mapa exato foto -> variação (não mantém fotos genéricas
  // sempre visíveis; só mostra a foto da combinação de cor/variação ativa no momento)
  if (p.variantImageMap) {
    const comboImg = getComboImage(p, colorName, varName);
    return comboImg ? [comboImg] : (p.img ? [p.img] : p.images.slice(0, 1));
  }

  const varLabels = p.vars ? p.vars.map(v => v[0]) : [];
  const colorLabels = p.swatches ? p.swatches.map(s => s[0]) : [];
  if (varLabels.length + colorLabels.length <= 1) return p.images.slice();

  const allLabels = [...varLabels, ...colorLabels];
  const isVariantSpecific = img => allLabels.some(label => imageMatchesText(img, label));
  const matchesActive = img => imageMatchesText(img, colorName) || imageMatchesText(img, varName);

  const filtered = p.images.filter(img => !isVariantSpecific(img) || matchesActive(img));
  return filtered.length > 0 ? filtered : p.images.slice();
}

// Monta o HTML das miniaturas da galeria (imagens filtradas + bot\u00e3o de v\u00eddeo, sempre vis\u00edvel)
function buildGalleryThumbsHTML(p, images) {
  return `
    ${images.map((img, i) => `
      <button class="thumb-btn ${i === 0 ? 'active' : ''}" data-type="image" data-src="${img}" type="button" aria-label="Ver imagem ${i + 1}">
        <img src="${img}" alt="" onerror="this.src='assets/images/chumbada-oficial-27c01352.png'">
        ${buildIndicatorSlotHTML(getIndicatorMeta(p, img), 'thumb')}
      </button>
    `).join('')}
    ${p.video ? `
      <button class="thumb-btn thumb-video-btn" data-type="video" data-video-src="${p.video}" type="button" aria-label="Ver v\u00eddeo do produto">
        <div class="play-icon-overlay">
          <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
        <img src="${p.img}" alt="Previa do v\u00eddeo">
      </button>
    ` : ''}
  `;
}

// ==========================================
// 1. RENDERIZAÇÃO DA PÁGINA DE CATÁLOGO (HOME)
// ==========================================

function renderCatalog() {
  // Destacar menu
  const navHome = document.getElementById('nav-home');
  if (navHome) navHome.classList.add('active');

  // Encontrar o produto em destaque (featured: true) ou o primeiro produto
  const featuredProduct = PRODUCTS.find(p => p.featured) || PRODUCTS[0];

  // Estrutura HTML da home (Hero + Seção de Filtros + Grid de Produtos)
  appContainer.innerHTML = `
    <div class="view-fade">
      <!-- Seção Hero Esportiva -->
      <section class="hero" aria-label="Apresentação do Catálogo">
        <div class="hero-container">
          <div class="hero-content">
            <span class="badge-tag">Edição Oficial 2026</span>
            <h1 class="hero-title">Equipamentos de <span>Alta Performance</span></h1>
            <p class="hero-desc">
              Explore o novo Catálogo V2 da Chumbada Oficial. Desenvolvido no padrão das grandes marcas mundiais, trazendo riqueza de detalhes, fotos e as especificações técnicas completas dos acessórios de pesca que dominam o mercado.
            </p>
            <div class="hero-actions">
              <a href="#catalogo-secao" class="btn btn-primary">Ver Catálogo</a>
              <a href="https://chumbadas.com.br" target="_blank" rel="noopener" class="btn btn-secondary">Visitar Loja</a>
            </div>
          </div>
          
          <!-- Card de Destaque -->
          <div class="hero-card" aria-label="Destaque">
            <a href="#/produto/${featuredProduct.slug}">
              <div class="hero-card-media">
                <img src="${featuredProduct.img}" alt="${escapeHTML(featuredProduct.name)}">
              </div>
            </a>
            <div class="hero-card-body">
              <div class="hero-card-info">
                <h3>${escapeHTML(featuredProduct.name)}</h3>
                <p>${escapeHTML(featuredProduct.category)}</p>
              </div>
              <span class="hero-card-badge">Destaque</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Seção de Busca, Filtros e Grid -->
      <main class="main-wrap" id="catalogo-secao">
        <!-- Painel de Busca & Filtros (Sticky) -->
        <section class="panel" aria-label="Painel de Busca e Filtros">
          <div class="tools">
            <div class="search-wrapper">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input id="search-input" type="search" class="search-input" placeholder="O que você está procurando?" autocomplete="off" value="${escapeHTML(state.searchQuery)}">
            </div>
            
            <div class="menu-dropdown-wrapper">
              <button class="hamburger-menu-btn" id="hamburger-menu-btn" type="button" aria-expanded="false" aria-label="Menu de Categorias">
                <svg class="hamburger-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="3" y1="12" x2="21" y2="12"></line>
                  <line x1="3" y1="6" x2="21" y2="6"></line>
                  <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
                <span id="active-category-label">Todos</span>
                <svg class="chevron-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="margin-left:auto; transition: transform 0.2s;">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
              <div class="categories-dropdown" id="categories-dropdown">
                <!-- Filtros serão inseridos por JS -->
              </div>
            </div>
          </div>
        </section>

        <!-- Barra de Status / Resultados -->
        <div class="summary-bar">
          <div class="summary-title">
            <h2>Nossos Produtos</h2>
            <p>Selecione um produto para ver tamanhos, cores disponíveis, fotos detalhadas e solicitar orçamento.</p>
          </div>
          <div class="summary-count" id="products-count">Carregando...</div>
        </div>

        <!-- Grid de Produtos -->
        <div class="products-grid" id="products-grid" aria-live="polite">
          <!-- Cards serão inseridos por JS -->
        </div>
      </main>
    </div>
  `;

  // Iniciar componentes do catálogo
  setupFilters();
  setupSearch();
  renderGrid();
}

// Configurar chips de filtros
// Configurar chips de filtros (Menu Hamburger Dropdown)
function setupFilters() {
  const dropdown = document.getElementById('categories-dropdown');
  const btn = document.getElementById('hamburger-menu-btn');
  const activeLabel = document.getElementById('active-category-label');
  if (!dropdown || !btn || !activeLabel) return;

  // Extrair categorias únicas de PRODUCTS
  const categories = ['Todos', ...Array.from(new Set(PRODUCTS.map(p => p.category))).sort((a,b) => a.localeCompare(b, 'pt-BR'))];

  // Definir categoria ativa inicial
  activeLabel.textContent = state.selectedCategory;

  dropdown.innerHTML = categories.map(cat => `
    <button class="dropdown-item ${state.selectedCategory === cat ? 'active' : ''}" type="button" data-category="${escapeHTML(cat)}">
      ${escapeHTML(cat)}
    </button>
  `).join('');

  // Toggle dropdown
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const isExpanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', !isExpanded);
    dropdown.classList.toggle('active', !isExpanded);
    
    // Rotate chevron
    const chevron = btn.querySelector('.chevron-icon');
    if (chevron) {
      chevron.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
    }
  });

  // Fechar ao clicar fora
  document.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', 'false');
    dropdown.classList.remove('active');
    const chevron = btn.querySelector('.chevron-icon');
    if (chevron) chevron.style.transform = 'rotate(0deg)';
  });

  // Evento de clique na categoria
  dropdown.addEventListener('click', e => {
    const item = e.target.closest('.dropdown-item');
    if (!item) return;

    state.selectedCategory = item.dataset.category;
    activeLabel.textContent = state.selectedCategory;
    
    // Atualizar classe ativa
    dropdown.querySelectorAll('.dropdown-item').forEach(c => {
      c.classList.toggle('active', c === item);
    });

    renderGrid();
  });
}

// Configurar campo de pesquisa
function setupSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  searchInput.addEventListener('input', e => {
    state.searchQuery = e.target.value;
    renderGrid();
  });
}

// Renderizar o grid de produtos filtrado
function renderGrid() {
  const grid = document.getElementById('products-grid');
  const countLabel = document.getElementById('products-count');
  if (!grid || !countLabel) return;

  const queryNorm = normalizeText(state.searchQuery);

  // Filtrar produtos com base no estado de busca e categoria
  const filtered = PRODUCTS.filter(p => {
    const matchesCategory = state.selectedCategory === 'Todos' || p.category === state.selectedCategory;
    
    let matchesSearch = true;
    if (queryNorm) {
      const nameNorm = normalizeText(p.name);
      const catNorm = normalizeText(p.category);
      const sectionNorm = normalizeText(p.section || '');
      const varNamesNorm = p.vars ? p.vars.map(v => normalizeText(v[0])).join(' ') : '';
      const swatchNamesNorm = p.swatches ? p.swatches.map(s => normalizeText(s[0])).join(' ') : '';
      
      matchesSearch = nameNorm.includes(queryNorm) || 
                      catNorm.includes(queryNorm) || 
                      sectionNorm.includes(queryNorm) ||
                      varNamesNorm.includes(queryNorm) ||
                      swatchNamesNorm.includes(queryNorm);
    }

    return matchesCategory && matchesSearch;
  });

  // Atualizar contador de resultados
  countLabel.textContent = `${filtered.length} produto${filtered.length === 1 ? '' : 's'}`;

  // Se nenhum for encontrado, exibir estado vazio
  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-results">
        <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3>Nenhum produto encontrado</h3>
        <p>Tente buscar por termos diferentes ou selecione outra categoria.</p>
      </div>
    `;
    return;
  }

  // Mapear produtos para HTML
  let lastSection = '';
  grid.innerHTML = filtered.map(p => {
    const pSection = p.section || p.category || 'Outros';
    let sectionBreak = '';
    
    // Separador visual de seções se estiver visualizando todos sem busca ativa
    if (state.selectedCategory === 'Todos' && !state.searchQuery && pSection !== lastSection) {
      lastSection = pSection;
      sectionBreak = `<div class="section-break"><h3>${escapeHTML(pSection)}</h3></div>`;
    }

    // Configurar spans e classes de layout
    let spanClass = '';

    // Previews de Cores
    const swatchesHtml = p.swatches ? `
      <div class="card-swatches" aria-label="Cores disponíveis">
        ${p.swatches.map(s => `<span class="card-swatch" style="background: ${escapeHTML(s[1])}" title="${escapeHTML(s[0])}"></span>`).join('')}
      </div>
    ` : '';

    // Previews de Variações
    const varsCountHtml = p.vars ? `
      <div class="card-vars-count">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="9" x2="15" y2="9"></line>
          <line x1="9" y1="13" x2="15" y2="13"></line>
          <line x1="9" y1="17" x2="11" y2="17"></line>
        </svg>
        <span>${p.vars.length} variação${p.vars.length === 1 ? '' : 'ões'}</span>
      </div>
    ` : '';

    const showPrice = CONFIG.showPrices && p.price;
    const priceHtml = showPrice ? `<span class="product-card-price">${escapeHTML(p.price)}</span>` : '';
    const btnStyle = showPrice ? '' : 'width: 100%; text-align: center; justify-content: center;';

    return `
      ${sectionBreak}
      <article class="product-card ${spanClass}">
        <div class="product-card-media">
          ${p.video ? `<span class="video-badge">
            <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14" style="margin-right: 4px; vertical-align: middle;">
              <path d="M8 5v14l11-7z"/>
            </svg>
            Vídeo
          </span>` : ''}
          <img loading="lazy" src="${p.img}" alt="${escapeHTML(p.name)}" onerror="this.src='assets/images/chumbada-oficial-27c01352.png'">
        </div>
        <div class="product-card-content">
          <span class="product-card-cat">${escapeHTML(p.category)}</span>
          <h3 class="product-card-title">${escapeHTML(p.name)}</h3>
          
          <div class="product-card-previews">
            ${swatchesHtml}
            ${varsCountHtml}
          </div>
          
          <div class="product-card-footer">
            ${priceHtml}
            <a href="#/produto/${p.slug}" class="product-card-action" style="${btnStyle}">Ver Detalhes</a>
          </div>
        </div>
      </article>
    `;
  }).join('');
}


// ==========================================
// 2. RENDERIZAÇÃO DA PÁGINA DE DETALHES DO PRODUTO
// ==========================================

function renderProductDetail(p) {
  // Desmarcar menu ativo para focar no produto
  const navHome = document.getElementById('nav-home');
  if (navHome) navHome.classList.remove('active');

  // Inicializar estado do produto
  if (state.selectedColor[p.id] === undefined) {
    state.selectedColor[p.id] = p.swatches && p.swatches.length > 0 ? p.swatches[0][0] : '';
  }
  if (state.selectedVariation[p.id] === undefined) {
    state.selectedVariation[p.id] = 0; // Primeira variação por padrão
  }

  // Preço da variação ativa ou geral
  const currentVarIndex = state.selectedVariation[p.id];
  let priceText = 'Sob Consulta';
  if (CONFIG.showPrices) {
    if (p.vars && p.vars[currentVarIndex] && p.vars[currentVarIndex][1]) {
      priceText = p.vars[currentVarIndex][1];
    } else if (p.price) {
      priceText = p.price;
    }
  }

  // Galeria: em produtos com muitas variações/cores, mostra inicialmente só as fotos
  // genéricas + as da opção já selecionada por padrão (o restante aparece ao trocar a opção)
  const initialVarText = p.vars && p.vars[currentVarIndex] ? p.vars[currentVarIndex][0] : '';
  const initialColorText = state.selectedColor[p.id] || '';
  const visibleGalleryImages = getVisibleGalleryImages(p, initialColorText, initialVarText);

  // Montagem da Tabela de Especificações Técnicas (Misturando estáticas e dinâmicas do produto)
  let specsRows = `
    <tr>
      <td class="specs-label">Marca</td>
      <td class="specs-val">Chumbada Oficial</td>
    </tr>
    <tr>
      <td class="specs-label">Categoria</td>
      <td class="specs-val">${escapeHTML(p.category)}</td>
    </tr>
  `;

  // Mesclar especificações personalizadas do produto (specs: {"Material": "Inox", ...})
  if (p.specs && typeof p.specs === 'object') {
    for (const [key, value] of Object.entries(p.specs)) {
      if (value) {
        specsRows += `
          <tr>
            <td class="specs-label">${escapeHTML(key)}</td>
            <td class="specs-val">${escapeHTML(value)}</td>
          </tr>
        `;
      }
    }
  }

  specsRows += `
    <tr>
      <td class="specs-label">Disponibilidade</td>
      <td class="specs-val" style="color: var(--color-success)">Disponível</td>
    </tr>
    <tr>
      <td class="specs-label">Código de Referência</td>
      <td class="specs-val">#${String(p.id).padStart(4, '0')}</td>
    </tr>
  `;

  // Renderizar a estrutura de detalhes
  appContainer.innerHTML = `
    <div class="view-fade">
      <main class="main-wrap detail-view">
        <!-- Breadcrumb para navegação -->
        <nav class="breadcrumb" aria-label="Navegação de trilha">
          <a href="#/">Home</a>
          <span class="breadcrumb-separator">/</span>
          <a href="#/" onclick="state.selectedCategory = '${escapeHTML(p.category)}'">${escapeHTML(p.category)}</a>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current" aria-current="page">${escapeHTML(p.name)}</span>
        </nav>

        <div class="detail-grid">
          <!-- Coluna da Esquerda: Galeria Interativa com fotos e vídeo -->
          <section class="detail-gallery" aria-label="Imagens do Produto">
            <div class="gallery-main" id="gallery-main-container">
              <img id="main-product-img" src="${visibleGalleryImages[0] || p.img}" alt="${escapeHTML(p.name)}" onerror="this.src='assets/images/chumbada-oficial-27c01352.png'">
              <div id="main-product-video" class="gallery-video-wrapper" style="display: none;"></div>
              <div id="main-product-indicator">${buildIndicatorSlotHTML(getIndicatorMeta(p, visibleGalleryImages[0] || p.img), 'main')}</div>
            </div>
            
            ${(visibleGalleryImages.length > 1) || p.video ? `
              <div class="gallery-thumbs${p.slug === 'chicotes-montados-3-unidades' ? ' gallery-thumbs--grid4' : ''}" id="gallery-thumbs">
                ${buildGalleryThumbsHTML(p, visibleGalleryImages)}
              </div>
            ` : ''}
          </section>

          <!-- Coluna da Direita: Informações detalhadas -->
          <section class="detail-info" aria-label="Informações do Produto">
            <div class="info-header">
              <span class="info-cat">${escapeHTML(p.category)}</span>
              <h1 class="info-title">${escapeHTML(p.name)}</h1>
              
              ${CONFIG.showPrices && priceText !== 'Sob Consulta' ? `
                <div class="info-price-wrapper">
                  <span class="info-price-label">Preço de Referência:</span>
                  <span class="info-price" id="detail-price-display">${escapeHTML(priceText)}</span>
                </div>
              ` : ''}
            </div>

            <!-- Tabela de Especificações Técnicas -->
            <div class="info-section">
              <h2 class="info-section-title">Especificações Técnicas</h2>
              <table class="specs-table">
                <tbody>
                  ${specsRows}
                </tbody>
              </table>
            </div>

            <!-- Seletor de Cores -->
            ${p.swatches ? `
              <div class="info-section" id="section-colors">
                <h2 class="info-section-title">
                  Cor: <span class="info-section-value" id="selected-color-label">${escapeHTML(state.selectedColor[p.id])}</span>
                </h2>
                <div class="swatches-selector" role="radiogroup" aria-label="Seleção de Cor">
                  ${p.swatches.map(s => `
                    <button class="swatch-btn ${state.selectedColor[p.id] === s[0] ? 'active' : ''}" 
                            style="background: ${escapeHTML(s[1])}" 
                            data-color-name="${escapeHTML(s[0])}" 
                            data-title="${escapeHTML(s[0])}" 
                            type="button"
                            role="radio"
                            aria-checked="${state.selectedColor[p.id] === s[0] ? 'true' : 'false'}">
                    </button>
                  `).join('')}
                </div>
              </div>
            ` : ''}

            <!-- Seletor de Tamanhos / Variações -->
            ${p.vars ? `
              <div class="info-section" id="section-vars">
                <h2 class="info-section-title">Opções / Variações</h2>
                <div class="vars-selector" role="radiogroup" aria-label="Seleção de Variação">
                  ${p.vars.map((v, index) => {
                    const hasPrice = CONFIG.showPrices && v[1];
                    const activeClass = currentVarIndex === index ? 'active' : '';
                    return `
                      <button class="var-btn ${activeClass}" 
                              data-var-index="${index}" 
                              type="button"
                              role="radio"
                              aria-checked="${currentVarIndex === index ? 'true' : 'false'}">
                        <span class="var-name">${escapeHTML(v[0])}</span>
                        ${hasPrice ? `<span class="var-price">${escapeHTML(v[1])}</span>` : ''}
                      </button>
                    `;
                  }).join('')}
                </div>
              </div>
            ` : ''}

            <!-- Descrição Técnica Premium -->
            <div class="info-section">
              <h2 class="info-section-title">Descrição</h2>
              <div class="info-desc">${p.description}</div>
            </div>

            <!-- Ações Principais -->
            <div class="detail-actions">
              <!-- Botão do WhatsApp (Atendimento/Orçamento) -->
              <button class="btn btn-primary btn-whatsapp" id="btn-order-whatsapp" type="button">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.513 2.262 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.724-1.458L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436.002 9.858-4.417 9.86-9.86.001-2.638-1.024-5.117-2.884-6.979C16.59 1.905 14.113.882 11.48.882c-5.441 0-9.863 4.42-9.865 9.861 0 1.682.454 3.32 1.317 4.757l-.988 3.605 3.702-.971zm11.367-7.252c-.3-.149-1.777-.875-2.05-.974-.274-.1-.474-.149-.674.15-.2.299-.774.974-.949 1.173-.174.199-.349.224-.648.075-.3-.15-1.263-.465-2.403-1.482-.888-.793-1.488-1.77-1.663-2.069-.175-.299-.019-.461.13-.61.135-.134.3-.349.449-.523.149-.174.199-.299.299-.498.1-.2.05-.374-.025-.523-.075-.15-.674-1.62-.924-2.22-.243-.585-.49-.507-.674-.516-.174-.008-.374-.01-.574-.01-.2 0-.524.075-.798.374-.274.299-1.048 1.022-1.048 2.492 0 1.47 1.073 2.89 1.223 3.089.15.2 2.11 3.22 5.111 4.516.713.308 1.27.493 1.704.63.716.228 1.368.196 1.883.119.574-.085 1.777-.726 2.025-1.42.249-.696.249-1.293.174-1.418-.075-.125-.274-.199-.573-.349z"/>
                </svg>
                Solicitar via WhatsApp
              </button>

              <div class="action-row">
                <!-- Botão do Link Oficial (Shopify) se existir -->
                ${p.link && p.link !== '#' ? `
                  <a href="${p.link}" target="_blank" rel="noopener" class="btn btn-secondary">
                    Comprar no Site
                  </a>
                ` : `
                  <button class="btn btn-secondary" style="opacity: 0.5; cursor: not-allowed;" disabled>
                    Indisponível no Site
                  </button>
                `}
                
                <!-- Botão Voltar -->
                <a href="#/" class="btn btn-secondary">
                  Voltar ao Catálogo
                </a>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  `;

  // Inicializar os seletores interativos
  initDetailSelectors(p);
}

// Configurar comportamento dinâmico nos seletores da página de produto
function initDetailSelectors(p) {
  const sectionColors = document.getElementById('section-colors');
  const sectionVars = document.getElementById('section-vars');
  const colorLabel = document.getElementById('selected-color-label');
  const priceDisplay = document.getElementById('detail-price-display');
  const btnWhatsapp = document.getElementById('btn-order-whatsapp');
  
  const galleryThumbs = document.getElementById('gallery-thumbs');
  const mainImg = document.getElementById('main-product-img');
  const mainVideoContainer = document.getElementById('main-product-video');
  const mainIndicator = document.getElementById('main-product-indicator');

  // Controle da Galeria de Imagens e Vídeo
  if (galleryThumbs && mainImg && mainVideoContainer) {
    galleryThumbs.addEventListener('click', e => {
      const btn = e.target.closest('.thumb-btn');
      if (!btn) return;

      // Atualizar classe ativa do botão selecionado
      galleryThumbs.querySelectorAll('.thumb-btn').forEach(b => b.classList.toggle('active', b === btn));

      const type = btn.dataset.type;

      if (type === 'image') {
        mainVideoContainer.style.display = 'none';
        mainVideoContainer.innerHTML = '';
        mainImg.style.display = 'block';
        mainImg.src = btn.dataset.src;
        if (mainIndicator) mainIndicator.innerHTML = buildIndicatorSlotHTML(getIndicatorMeta(p, btn.dataset.src), 'main');
      } else if (type === 'video') {
        mainImg.style.display = 'none';
        mainVideoContainer.style.display = 'flex';
        if (mainIndicator) mainIndicator.innerHTML = '';

        const videoSrc = btn.dataset.videoSrc;
        if (videoSrc.includes('youtube.com') || videoSrc.includes('youtu.be') || videoSrc.includes('embed')) {
          let embedUrl = videoSrc;
          if (videoSrc.includes('watch?v=')) {
            embedUrl = videoSrc.replace('watch?v=', 'embed/');
          }
          mainVideoContainer.innerHTML = `
            <iframe src="${embedUrl}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          `;
        } else {
          mainVideoContainer.innerHTML = `
            <video src="${videoSrc}" controls autoplay muted></video>
          `;
        }
      }
    });
  }

  // Função para reconstruir o link do WhatsApp com os dados selecionados
  function updateWhatsappLink() {
    const selectedColor = state.selectedColor[p.id];
    const varIndex = state.selectedVariation[p.id];
    const selectedVar = p.vars && p.vars[varIndex] ? p.vars[varIndex][0] : 'Nenhum';
    
    // Substituir tokens na mensagem
    let message = CONFIG.whatsappMessageTemplate
      .replace('{productName}', p.name)
      .replace('{category}', p.category)
      .replace('{variation}', selectedVar)
      .replace('{color}', selectedColor || 'Nenhum');
      
    const url = `https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(message)}`;
    
    // Associar ação de clique ao botão
    btnWhatsapp.onclick = () => {
      window.open(url, '_blank', 'noopener');
    };
  }

  // Seletor de Cores
  if (sectionColors) {
    sectionColors.addEventListener('click', e => {
      const btn = e.target.closest('.swatch-btn');
      if (!btn) return;

      const colorName = btn.dataset.colorName;
      state.selectedColor[p.id] = colorName;

      // Atualizar classe ativa
      sectionColors.querySelectorAll('.swatch-btn').forEach(b => {
        const isActive = b === btn;
        b.classList.toggle('active', isActive);
        b.setAttribute('aria-checked', isActive ? 'true' : 'false');
      });

      // Atualizar texto do label de cor
      if (colorLabel) colorLabel.textContent = colorName;

      // Atualizar galeria (revela as fotos da cor selecionada e troca a foto principal)
      refreshGallery(colorName);

      updateWhatsappLink();
    });
  }

  // Seletor de Variações
  if (sectionVars) {
    sectionVars.addEventListener('click', e => {
      const btn = e.target.closest('.var-btn');
      if (!btn) return;

      const varIndex = parseInt(btn.dataset.varIndex, 10);
      state.selectedVariation[p.id] = varIndex;

      // Atualizar classe ativa
      sectionVars.querySelectorAll('.var-btn').forEach((b, index) => {
        const isActive = index === varIndex;
        b.classList.toggle('active', isActive);
        b.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      });

      // Atualizar exibição de preço para a variação ativa
      if (CONFIG.showPrices && priceDisplay && p.vars && p.vars[varIndex]) {
        const varPrice = p.vars[varIndex][1] || p.price || 'Sob Consulta';
        priceDisplay.textContent = varPrice;
        priceDisplay.classList.toggle('empty', varPrice === 'Sob Consulta');
      }

      // Atualizar galeria (revela as fotos da variação selecionada e troca a foto principal)
      if (p.vars && p.vars[varIndex]) {
        refreshGallery(p.vars[varIndex][0]);
      }

      updateWhatsappLink();
    });
  }

  // Reconstrói as miniaturas da galeria mostrando as fotos genéricas + as da opção ativa
  // (cor e variação), e troca a foto principal para a que combina com o texto recém-selecionado.
  // O vídeo (se houver) permanece sempre visível, nunca é escondido pelo filtro.
  function refreshGallery(activeText) {
    if (!p.images || !galleryThumbs) return;

    const colorName = state.selectedColor[p.id] || '';
    const varIndex = state.selectedVariation[p.id];
    const varName = p.vars && p.vars[varIndex] ? p.vars[varIndex][0] : '';

    const visibleImages = getVisibleGalleryImages(p, colorName, varName);
    galleryThumbs.innerHTML = buildGalleryThumbsHTML(p, visibleImages);

    // 1. Tentar correspondência exata por URL mapeada em colorImages ou varImages
    let targetSrc = '';
    if (p.colorImages && p.colorImages[activeText] && visibleImages.includes(p.colorImages[activeText])) {
      targetSrc = p.colorImages[activeText];
    } else if (p.varImages && p.varImages[activeText] && visibleImages.includes(p.varImages[activeText])) {
      targetSrc = p.varImages[activeText];
    }

    // 2. Fallback: correspondência por nome de arquivo dentro das imagens visíveis
    if (!targetSrc) {
      const matchIndex = visibleImages.findIndex(img => imageMatchesText(img, activeText));
      targetSrc = matchIndex !== -1 ? visibleImages[matchIndex] : visibleImages[0];
    }

    if (targetSrc) {
      mainVideoContainer.style.display = 'none';
      mainVideoContainer.innerHTML = '';
      mainImg.style.display = 'block';
      mainImg.src = targetSrc;
      if (mainIndicator) mainIndicator.innerHTML = buildIndicatorSlotHTML(getIndicatorMeta(p, targetSrc), 'main');

      const thumbBtns = galleryThumbs.querySelectorAll('.thumb-btn[data-type="image"]');
      thumbBtns.forEach(b => b.classList.toggle('active', b.dataset.src === targetSrc));
      const activeBtn = Array.from(thumbBtns).find(b => b.dataset.src === targetSrc);
      if (activeBtn) activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  // Inicializar link pela primeira vez
  updateWhatsappLink();
}
