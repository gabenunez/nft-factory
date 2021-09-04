from flask import Flask,request, send_file
import json
import tempfile
import os
from PIL import Image
from collections import OrderedDict
from random import randint
import io
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello,World!</p>"

@app.route("/upload",methods=['GET','POST'])
def upload_files():
    if request.method == 'POST':
        upload_files = request.files.getlist("files")
        request_data = json.loads(request.form.get('filedata'))
        layers = request_data['layers']

        pool = OrderedDict()

        for layer in layers:
            pool[layer] = {}

        for file in upload_files:
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
            
        chance = randint(0,100)
        base_pool = pool[list(pool)[0]]
        rarity_pool = list(base_pool)
        in_img = None
        for layer in pool:
            chance = randint(0,100)
            rarity_pool = list(pool[layer])
            print(rarity_pool)
            selected_rarity = 1000
            for rarity in rarity_pool:
                t1 = 0 + rarity
                t2 = 100 - rarity
                if chance <= t1 or chance >= t2:
                    if rarity < selected_rarity:
                        selected_rarity = rarity
                
            item_pool = pool[layer][selected_rarity]
            item = item_pool[randint(0,len(item_pool)-1)]
            file = item[list(item)[0]]
            if not in_img:
                in_img = Image.open(file).convert('RGBA')
            else:
                image = Image.open(file).convert('RGBA')
                in_img.paste(image,(0,0),image)   
        buf = io.BytesIO()
        #in_img = in_img.resize((512,512),Image.NEAREST)
        in_img.save(buf,'PNG')
        buf.seek(0)
        byteImg = buf.read()
        
        return send_file(io.BytesIO(byteImg),mimetype='image/png',attachment_filename='generated.png')
    return '''
    <form method="POST" enctype="multipart/form-data" action="/upload">
        <input type="file" name="files" multiple="">
        <input type="text" name="filedata">
        <input type="submit" value="upload">
    </form>
    '''

def get_rarity(chance,selected_rarity,rarity_pool):
    rarity = rarity_pool.pop()
    if rarity > selected_rarity:
        selected_rarity = rarity
