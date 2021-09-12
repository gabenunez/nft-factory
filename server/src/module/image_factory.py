from PIL import Image
from random import randint
from random import seed
import io
import base64
import zipfile
import time
from zipfile import ZipFile
import json


def encode_image(img_bytes):
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode('ascii')}"


def create_metadata_attribute(meta_data_attributes, trait_type, value):
    meta_data_attributes['attributes'].append({
        "trait_type": trait_type,
        "value":value
    })

def calculate_total_possibilities(json_data):
    layers = list(json_data)
    total_possibilities = 1
    for layer in layers:
        item_amt = len(json_data[layer])
        total_possibilities *= item_amt

    return total_possibilities

def generate_image_from_pool(metadata_attributes,layer,pool,in_img):

    
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

    create_metadata_attribute(metadata_attributes,layer,item_name)
    
    return in_img


def image_factory(json_data,n=1,is_encoded=True):
    layers = list(json_data)
    images = []
    i = 0
  
    total_possibilties = calculate_total_possibilities(json_data)
    if n > total_possibilties:
        n = total_possibilties

    attribute_data = []


    while i < n:
        metadata_attributes = {
            "name":"",
            "description":"",
            "image":"IPFS Link Goes Here",
            "attributes": []
        }
        metadata_attributes["name"] = f'ProjectName #{i}'

        in_img = None
        for layer in layers:
            items = json_data[layer]
            pool = {}
            for item in items:
                name = item['name']
                image64 = item['image']
                chance = item['chance']
                pool.setdefault(chance,[]).append({name:image64})
            in_img = generate_image_from_pool(metadata_attributes,layer,pool,in_img)  


        duplicate_found = False
        for data in attribute_data:
            if data["attributes"] == metadata_attributes["attributes"]:
                metadata_attributes["attributes"].clear()
                duplicate_found = True
                break
        
        if not duplicate_found:
            attribute_data.append(dict(metadata_attributes))
            
           

            final_img = io.BytesIO()
            in_img.save(final_img,'PNG')
            final_img.seek(0)
            if is_encoded:
                encoded = encode_image(final_img.read())
                images.append((encoded,metadata_attributes))
            else:        
                images.append((final_img.read(),metadata_attributes))
                
            i+=1
        
    return images


def preview_image(request):
    json_data = request.json
    encoded = image_factory(json_data)
    res_data = {
        "image":encoded[0][0]
    }
    return res_data

def create_images(request,n):
    seed(5000 * randint(5,1337))
    json_data =request.json
    encoded = image_factory(json_data,n,is_encoded=False)
    zipped_images = io.BytesIO()
    i = 0

    with ZipFile(zipped_images,'w') as zf:
        for byte_img, metadata in encoded:
            imgdata = zipfile.ZipInfo(f"{i}.png")
            imgdata.date_time = time.localtime(time.time())[:6]
            imgdata.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(imgdata,byte_img)
            
            metadata_buf = io.BytesIO()
            m_bytes = json.dumps(metadata).encode('utf-8')
            metadata_buf.write(m_bytes)
            metadata_buf.seek(0)

            metadata_bytes = zipfile.ZipInfo(f"{i}")
            metadata_bytes.date_time = time.localtime(time.time())[:6]
            metadata_bytes.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(metadata_bytes,metadata_buf.read())


            i += 1

    zipped_images.seek(0)
    return zipped_images

