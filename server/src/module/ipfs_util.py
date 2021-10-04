import requests
import uuid
import io
import base64
import json
import os
from dotenv import load_dotenv
pinata_url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'



load_dotenv('../')

pinata_api_key =  os.environ.get('pinata_api_key')
pinata_secret = os.environ.get('pinata_secret')


def encode_image(img_bytes):
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode('ascii')}"

def upload_folder_to_pinata(image_data):
    folder_name = str(uuid.uuid4())
    i = 0
    form_data = []
    for byte_img, metadata in image_data:
        form_data.append(('file',(f'{folder_name}/{i}.png',byte_img)))
        i+= 1


    response = requests.post(url=pinata_url,files=form_data,headers= {
        'pinata_api_key': pinata_api_key,
        'pinata_secret_api_key': pinata_secret
    })  

    if response.status_code == 200:
        form_data.clear()
        pin_data = json.loads(response.text)
        i = 0
        for byte_img, metadata in image_data:
            ipfs_image_url = f"https://ipfs.io/ipfs/{pin_data['IpfsHash']}/{i}.png"
            metadata["image"] = ipfs_image_url
            form_data.append(('file',(f'{folder_name}_data/{i}',json.dumps(metadata))))
            i+=1
        
        response = requests.post(url=pinata_url,files=form_data,headers= {
            'pinata_api_key': pinata_api_key,
            'pinata_secret_api_key': pinata_secret
        })  

        if response.status_code == 200:
            pin_data = json.loads(response.text)
            ipfs_url = f"https://ipfs.io/ipfs/{pin_data['IpfsHash']}"
            return ipfs_url
        else:
            return False
    else:
        return False
   


 