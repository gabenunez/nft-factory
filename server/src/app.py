from flask import Flask,request, send_file, jsonify
from module import image_factory as imgfactory

app = Flask(__name__)

@app.route("/health",methods=['GET'])
def health():
    return "Healthy"

@app.route("/preview",methods=['POST'])
def create_preview():
    if request.method == 'POST':
        if not request.json:
            return "Invalid JSON"
        return imgfactory.preview_image(request)

@app.route("/create_collectible",methods=['POST'])
def create_collectible():
    if request.method == 'POST':
        if not request.json:
            return "Invalid JSON"
        
        data = request.args


        if 'n' in data:
            amount = request.args.get('n',type=int)          
            zipped_bytes = imgfactory.create_images(request,amount)
            return send_file(zipped_bytes,attachment_filename='generated.zip',as_attachment=True)
        else:
            return "Invalid(Missing Params)"
        

    return "Invalid"

