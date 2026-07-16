import json
import re

data_js_path = 'D:/chumbada-catalogo-v2/assets/js/data.js'
with open(data_js_path, 'r', encoding='utf-8') as f:
    data = f.read()

json_str = data.split('window.PRODUCTS = ')[1].rsplit(';', 1)[0]
products = json.loads(json_str)

urls = set()

for p in products:
    img = p.get('img', '')
    if img and 'shopify.com' in img:
        urls.add(img)
    
    for image in p.get('images', []):
        if 'shopify.com' in image:
            urls.add(image)
            
    video = p.get('video', '')
    if video and 'shopify.com' in video:
        urls.add(video)
        
    desc = p.get('description', '')
    if desc:
        desc_urls = re.findall(r'(https://cdn\.shopify\.com/[^\"\'\>\s]+)', desc)
        urls.update(desc_urls)

images = [u for u in urls if not u.endswith('.mp4') and not u.endswith('.mov')]
videos = [u for u in urls if u.endswith('.mp4') or u.endswith('.mov')]

print(f"Total unique Shopify URLs: {len(urls)}")
print(f"Total Images: {len(images)}")
print(f"Total Videos: {len(videos)}")
