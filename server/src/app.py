from flask import Flask,request, send_file, jsonify
import json
import tempfile
import os
from PIL import Image
from collections import OrderedDict
from random import randint
import io
import base64
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello,World!</p>"

def create_pool(files,request_data):
    pool = OrderedDict()
    layers = request_data['layers']
    for layer in layers:
        pool[layer] = {}
    for file in files:
        file_name = file.filename
        img_attr = request_data['data'][file_name]
        layer = img_attr['layer']
        name = img_attr['name']
        rarity = img_attr['percent']
        if not rarity in pool[layer]:
            pool[layer].update({
                rarity: []
            })
        pool[layer][rarity].append({name:file})
    return pool

def calculate_rarity(rarity_pool):
    selected_rarity = 1000
    chance = randint(0,100)
    for rarity in rarity_pool:
        t1 = 0 + rarity
        t2 = 100 - rarity
        if chance <= t1 or chance >= t2:
            if rarity < selected_rarity:
                selected_rarity = rarity
    if selected_rarity == 1000:
        selected_rarity = rarity_pool[randint(0,len(rarity_pool)-1)]
    
    return selected_rarity

def pool_random_image(pool):
    in_img = None
    buf = io.BytesIO()

    for layer in pool:
        rarity_pool = list(pool[layer])
        selected_rarity = calculate_rarity(rarity_pool)  
        item_pool = pool[layer][selected_rarity]
        item = item_pool[randint(0,len(item_pool)-1)]
        file = item[list(item)[0]]
        if not in_img:
            in_img = Image.open(file).convert('RGBA')
        else:
            image = Image.open(file).convert('RGBA')
            in_img.paste(image,(0,0),image)
    
    in_img.save(buf,'PNG')
    buf.seek(0)
    return buf.read()

def generate_image(files,request_data):
    return pool_random_image(create_pool(files,request_data))


def encode_image(img_bytes):
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode('ascii')}"

@app.route("/generate",methods=['POST'])
def generate_bulk_data():
    pass

@app.route("/preview",methods=['GET','POST'])
def generate_preview():
    if request.method == 'POST':
        upload_files = request.files.getlist("files")
        request_data = json.loads(request.form.get('filedata'))
        image_bytes = generate_image(upload_files,request_data)
        encoded = encode_image(image_bytes)
        res_data = {
            "image":encoded
        }
        return jsonify(res_data)
    
    #For testing through local browser
    return '''
    <form method="POST" enctype="multipart/form-data" action="/upload">
        <input type="file" name="files" multiple="">
        <input type="text" name="filedata">
        <input type="submit" value="upload">
    </form>
    '''

