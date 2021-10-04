from os import stat
from flask import Flask,request, send_file, jsonify, Response, abort
from flask.wrappers import Request
from module import image_factory as imgfactory
from module import payments
from module.error import Error

app = Flask(__name__)

# Health Check
@app.route("/health",methods=['GET'])
def health():
    return Response(status=200)


# Generate Image Preview
@app.route("/preview",methods=['POST'])
def create_preview():
    if request.method == 'POST':
        if not request.json:
            return Error("Invalid JSON")
        
        return imgfactory.preview_image(request)
    
    
    abort(404)

# For Testing Validating
@app.route("/validate",methods=["POST"])
def validate_bear_ownership():
    if(request.method == 'POST'):
        data = request.args
        if 'sign_tx' in data:
            print(str(data.get('sign_tx')))
            validated = payments.process_signed_transaction(str(data.get('sign_tx')))
            if validated:
                return Response(status=200)
            else:
                return Error("Failed to validate ownership")
        
    abort(404)

@app.route("/create_collectible",methods=['POST'])
def create_collectible():
    if request.method == 'POST':
        if not request.json:
            return Error("Invalid JSON")
        
        data = request.args
       
        if 'n' in data and 'sign_tx' in data and 'project_name' in data:
           pass
        else:
            return Error("Invalid Parameters")
            
        sign_tx = str(data.get('sign_tx'))
        processed = payments.process_signed_transaction(sign_tx)

        if processed:
            amount = data.get('n',type=int)
           
            zipped_bytes = imgfactory.create_images(request,amount)
            return send_file(zipped_bytes,attachment_filename='generated.zip',as_attachment=True)
        else:
            return Error('Failed to process signature')
        

    abort(404)

