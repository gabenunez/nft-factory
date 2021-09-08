from flask import Flask,request, send_file, jsonify
from module import image_factory as imgfactory

app = Flask(__name__)

@app.route("/preview",methods=['POST'])
def generate_preview():
    if request.method == 'POST':
        return imgfactory.preview_image(request)

