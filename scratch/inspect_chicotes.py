import csv
import json

csv_path = 'D:/Dowloads HD 1T/products_export_acessorios_completo.csv'
with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    rows_by_handle = {}
    for row in reader:
        h = row.get('Handle')
        if h:
            if h not in rows_by_handle:
                rows_by_handle[h] = []
            rows_by_handle[h].append(dict(row))

targets = ['chicote', 'porta-pernadas', 'porta-pernada']
for handle, rows in rows_by_handle.items():
    match = any(t in handle for t in targets)
    if match:
        title = rows[0].get('Title', '')
        print(f'=== {title} [{handle}] ===')
        for r in rows:
            opt1 = r.get('Option1 Value', '')
            img = r.get('Image Src', '')
            var_img = r.get('Variant Image', '')
            print(f'  Var: {opt1} | MainImg: {img[:100]} | VarImg: {var_img[:100]}')
        print()
