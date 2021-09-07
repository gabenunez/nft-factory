from flask import Flask,request, send_file, jsonify
from module import image_factory as imgfactory

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello,World!</p>"

@app.route("/preview",methods=['GET','POST'])
def generate_preview():
    if request.method == 'POST':
        return imgfactory.preview_image(request)
    
    #For testing through local browser
    return '''
    <form method="POST" enctype="multipart/form-data" action="/upload">
        <input type="file" name="files" multiple="">
        <input type="text" name="filedata">
        <input type="submit" value="upload">
    </form>
    '''

