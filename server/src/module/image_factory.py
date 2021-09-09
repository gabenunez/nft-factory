from PIL import Image
from random import randint
import io
import base64
import zipfile
import time
from zipfile import ZipFile


def encode_image(img_bytes):
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode('ascii')}"

def calculate_total_possibilities(json_data):
    layers = list(json_data)
    total_possibilities = 1
    for layer in layers:
        item_amt = len(json_data[layer])
        total_possibilities *= item_amt

    return total_possibilities

def generate_image_from_pool(pool,in_img):
    chance = randint(0,100)
    rarity_pool = list(pool)
    selected_rarity = 1000
    for rarity in rarity_pool:
        t1 = 0 + rarity
        t2 = 100 - rarity
        if chance <= t1 or chance >= t2:
            if rarity < selected_rarity:
                selected_rarity = rarity
    rp = randint(0,len(pool[selected_rarity])-1)
    item_selected = pool[selected_rarity][rp]
    item_name = list(item_selected)[0]
    image_decoded = base64.b64decode(item_selected[item_name])
    buf = io.BytesIO()
    buf.write(image_decoded)
    if not in_img:
        in_img = Image.open(buf).convert('RGBA')
    else:
        image = Image.open(buf).convert('RGBA')
        in_img.paste(image,(0,0),image)
    return in_img


def image_factory(json_data,n=1,is_encoded=True):
    layers = list(json_data)
    images = []
    i = 0
    retry = 0
    while i < n or retry > 25:
        in_img = None
        for layer in layers:
            items = json_data[layer]
            pool = {}
            for item in items:
                name = item['name']
                image64 = item['image']
                chance = item['chance']
                pool.setdefault(chance,[]).append({name:image64})
            in_img = generate_image_from_pool(pool,in_img)   
        final_img = io.BytesIO()
        in_img.save(final_img,'PNG')
        final_img.seek(0)
        if is_encoded:
            encoded = encode_image(final_img.read())
            if encoded not in images:
                images.append(encoded)
                i+=1
                retry = 0
            else:
                retry += 1
        else:
            if final_img not in images:
                images.append(final_img.read())
                i+=1
                retry = 0
            else:
                retry +=1 
        
    return images


def preview_image(request):
    json_data = request.json
    encoded = image_factory(json_data)
    res_data = {
        "image":encoded[0]
    }
    return res_data

def create_images(request,n):
    json_data =request.json
    encoded = image_factory(json_data,n,is_encoded=False)
    zipped_images = io.BytesIO()
    i = 0

    with ZipFile(zipped_images,'w') as zf:
        for byte_img in encoded:
            data = zipfile.ZipInfo(f"{i}.png")
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data,byte_img)
            i += 1

    zipped_images.seek(0)
    return zipped_images

