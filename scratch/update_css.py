with open('D:/chumbada-catalogo-v2/assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remover a seção adicionada no final anteriormente
css_parts = css.split('/* Melhorias no Layout do Menu de Categorias */')
css = css_parts[0]

# Estilos do menu dropdown
dropdown_styles = """
.menu-dropdown-wrapper {
  position: relative;
  width: 100%;
}
.hamburger-menu-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--color-text-secondary);
  padding: 12px 18px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.hamburger-menu-btn:hover {
  border-color: var(--color-text-muted);
  color: var(--color-text-primary);
  background-color: #e2e8f0;
}
.categories-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 100%;
  background-color: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: none;
  flex-direction: column;
  z-index: 100;
  overflow: hidden;
}
.categories-dropdown.active {
  display: flex;
}
.dropdown-item {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-transform: capitalize;
}
.dropdown-item:hover {
  background-color: #f1f5f9;
  color: var(--color-text-primary);
}
.dropdown-item.active {
  background-color: var(--color-brand);
  color: #ffffff;
}
"""

# Substituir o bloco antigo de filtros pelo novo
old_filters_block = """.filters-wrapper {
  overflow: hidden;
}
.filters-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none; /* Firefox */
  padding-bottom: 2px;
}
.filters-scroll::-webkit-scrollbar {
  display: none; /* Safari & Chrome */
}
.chip {
  white-space: nowrap;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--color-text-secondary);
  padding: 8px 18px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.chip:hover {
  border-color: var(--color-text-muted);
  color: var(--color-text-primary);
  background-color: #e2e8f0;
}
.chip.active {
  background-color: var(--color-brand);
  color: #ffffff;
  border-color: var(--color-brand);
  box-shadow: var(--shadow-glow);
}"""

if old_filters_block in css:
    css = css.replace(old_filters_block, dropdown_styles)
    print("CSS replaced successfully!")
else:
    # Caso haja pequenas diferenças de espaçamento no arquivo original, vamos tentar substituir uma parte menor
    print("Block not found. Appending dropdown styles instead...")
    css += dropdown_styles

with open('D:/chumbada-catalogo-v2/assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
