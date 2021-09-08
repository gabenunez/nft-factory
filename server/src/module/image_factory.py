from PIL import Image
from random import randint
import io
import base64


def encode_image(img_bytes):
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode('ascii')}"


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


def image_factory(json_data):
    layers = list(json_data)
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
    encoded = encode_image(final_img.read())
    return encoded


def preview_image(request):
    json_data = request.json
    encoded = image_factory(json_data)
    res_data = {
        "image":encoded
    }
    return res_data

