import uuid

import aioboto3
import base64
import aiofiles
import os
from backend.config.config import config

from backend.app.services.unload_img.base_unload_service import BaseUnloadService

service_name = 's3'
aws_access_key_id = config.AWS_ACCESS_KEY_ID
aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
endpoint_url = 'https://storage.yandexcloud.net'
bucket = 'itmo-smart-scales'
session = aioboto3.Session()


class StorageUnloadService(BaseUnloadService):
    async def unload_img(self, img_base64: str, img_name: str):
        image_data = base64.b64decode(img_base64)

        temp_file = str(uuid.uuid4())
        async with aiofiles.open(temp_file, 'wb') as f:
            await f.write(image_data)

        try:
            async with session.client(
                    service_name=service_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    endpoint_url=endpoint_url,
            ) as s3_client:
                try:
                    await s3_client.upload_file(temp_file, bucket, img_name)
                except Exception as e:
                    raise (f'Unload fail: {e}')
        finally:
            os.remove(temp_file)

        img_url = f'{endpoint_url}/{bucket}/{img_name}'

        return img_url
