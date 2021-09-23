from os import stat
from flask import Flask,request, send_file, jsonify, Response, abort
from flask.wrappers import Request
from module import image_factory as imgfactory
from module import payments
from module.error import Error

app = Flask(__name__)

@app.route("/health",methods=['GET'])
def health():
    return Response(status=200)

@app.route("/preview",methods=['POST'])
def create_preview():
    if request.method == 'POST':
        if not request.json:
            return Error("Invalid JSON")
        
        return imgfactory.preview_image(request)
    
    
    abort(404)

@app.route("/create_collectible",methods=['POST'])
def create_collectible():
    if request.method == 'POST':
        if not request.json:
            return Error("Invalid JSON")
        
        data = request.args
        sign_tx = False
        if 'n' in data and 'sign_tx' in data:
            sign_tx = str(data.get('sign_tx'))
        else:
            return Error("Invalid Parameters")

        processed = payments.process_signed_transaction('')

        if processed:
            amount = request.args.get('n',type=int)          
            zipped_bytes = imgfactory.create_images(request,amount)
            return send_file(zipped_bytes,attachment_filename='generated.zip',as_attachment=True)
        else:
            return Error('Failed to process payment')
        

    abort(404)

