# Libraries
import urllib.request
import requests
import zipfile
import io
import os
from loguru import logger

# Script Setup
logger = logger.bind(main=True)


class Downloader:
    """
    How to use it 
    dw = Downloader()
    dw.download_from_url('<zip_file_url>', '<save_path>', is_zip = True)
    """

    def __init__(self):
        pass

    @staticmethod
    def download_from_url(self, url_direction, save_path, is_zip=False):
        # TODO: Add progress bar
        logger.info(f'Downloading File/s to {save_path}')
        if os.path.exists(save_path):
            logger.warning('File already exists!, aborting download')
            return save_path
        if is_zip:
            r = requests.get(url_direction)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(save_path)
            logger.info("Downloaded zip and extracted files")

        else:
            urllib.request.urlretrieve(url_direction, save_path)
            logger.info("Downloaded Dataset")
        logger.info('done')
        return save_path
