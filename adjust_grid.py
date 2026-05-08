import os, struct, re

def get_image_info(data):
    size = len(data)
    pos = 0
    if size >= 2 and data[pos] == 0xFF and data[pos+1] == 0xD8:
        pos += 2
        while pos < size:
            if data[pos] != 0xFF: return None
            marker = data[pos+1]
            pos += 2
            if marker in (0xC0, 0xC1, 0xC2):
                h = struct.unpack('>H', data[pos+3:pos+5])[0]
                w = struct.unpack('>H', data[pos+5:pos+7])[0]
                return w, h
            length = struct.unpack('>H', data[pos:pos+2])[0]
            pos += length
    return None

path = r'c:\Mothers day\main.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'(<div class="dump-item\s+t-(?:tall|med|short)">)\s*(<img src="New folder/([^"]+)")', re.MULTILINE)

def replacer(match):
    div_tag = match.group(1)
    img_tag = match.group(2)
    filename = match.group(3)
    
    img_path = os.path.join(r'c:\Mothers day\New folder', filename)
    try:
        with open(img_path, 'rb') as fp:
            dim = get_image_info(fp.read())
            if dim:
                w, h = dim
                ratio = w / h
                if ratio < 0.75:
                    new_div = '<div class="dump-item t-tall">'
                elif ratio > 1.05:
                    new_div = '<div class="dump-item t-short">'
                else:
                    new_div = '<div class="dump-item t-med">'
                return f'{new_div}\n                {img_tag}'
    except:
        pass
    return match.group(0)

new_html = pattern.sub(replacer, html)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Done modifying HTML based on aspect ratios.')
