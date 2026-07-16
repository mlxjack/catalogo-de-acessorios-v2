import re

data = open('C:/Users/junir/.gemini/antigravity/brain/6fe59c82-297b-4020-8b76-b7f048f17ef9/scratch/generate_data.js', encoding='utf-8').read()

matches = re.finditer(r'name:\s*[\'"](.*?)[\'"]', data, re.IGNORECASE)
for m in matches:
    name = m.group(1).lower()
    if 'rotor' in name or 'snap' in name or 'kit' in name or 'adaptador' in name:
        print(m.group(1))
