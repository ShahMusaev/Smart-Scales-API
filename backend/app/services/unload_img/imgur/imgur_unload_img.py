import requests
import base64
import os
import json
import sys

from app.services.unload_img.base_unload_service import BaseUnloadService


class Imgur(BaseUnloadService):
    '''
    Anonymous image upload on imgur.com with client_id
    '''
    def __init__(self, img_path):
        self.client_id = os.environ.get('IMGUR_CLIENT_ID') or '2b8986ab0193370'

    def unload_img(self, img_base64: str = None, img_url: str = None):
        if img_url:
            img_path = ''
            try:
                with open(img_path, 'rb') as img:
                        img_base64 = base64.b64encode(img.read())
            except Exception as file_exception:
                print(file_exception)
                return

        headers = {'Authorization':'Client-ID '+ self.client_id}
        data = {'image': img_base64}
        url = 'https://api.imgur.com/3/image'
        try:
            return json.loads(requests.post(url,headers=headers,data=data).text)
        except Exception as net_exception:
            return {'success':False,'error':'SocketException'}