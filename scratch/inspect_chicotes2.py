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

# Get full picture of all active products
active_handles = set()
for handle, rows in rows_by_handle.items():
    status = rows[0].get('Status', 'active').strip().lower()
    if status == 'active':
        active_handles.add(handle)

# Print all info about chicote and porta-pernadas-e-chicotes
targets = ['porta-pernadas-e-chicotes', 'chicote-pesca', 'chicote-finesse', 'chicote-montado']
for handle, rows in rows_by_handle.items():
    if handle not in active_handles:
        continue
    if any(t in handle for t in targets):
        title = rows[0].get('Title', '')
        ptype = rows[0].get('Type', '')
        body = rows[0].get('Body (HTML)', '')[:300]
        print(f"HANDLE: {handle}")
        print(f"TITLE: {title}")
        print(f"TYPE: {ptype}")
        print(f"BODY: {body}")
        print()
        for r in rows:
            opt1 = r.get('Option1 Name', '')
            opt1v = r.get('Option1 Value', '')
            img = r.get('Image Src', '')
            var_img = r.get('Variant Image', '')
            print(f"  OPT: [{opt1}]=[{opt1v}] | IMG: {img} | VAR_IMG: {var_img}")
        print("---")
        print()
