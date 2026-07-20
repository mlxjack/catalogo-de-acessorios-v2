import csv

csv_path = 'D:/Dowloads HD 1T/products_export_acessorios_completo.csv'
with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    chicotes = {}
    for r in reader:
        h = r.get('Handle')
        title = r.get('Title')
        if h and 'chicote' in h:
            if h not in chicotes:
                chicotes[h] = []
            chicotes[h].append(r)
            
    for h, rows in chicotes.items():
        print(f"=== Handle: {h} | Title: {rows[0].get('Title')} ===")
        print(f"Number of rows: {len(rows)}")
        print(f"Option1 Name: {rows[0].get('Option1 Name')} | Option2 Name: {rows[0].get('Option2 Name')}")
        print("Option values:", list(set(r.get('Option1 Value') for r in rows if r.get('Option1 Value'))))
        print("Images:", list(set(r.get('Image Src') for r in rows if r.get('Image Src'))))
        print("Variant Images:", list(set(r.get('Variant Image') for r in rows if r.get('Variant Image'))))
        print()
