import subprocess
import requests
from tqdm import tqdm
subprocess.call('wget -P . "https://civitai.com/api/download/models/238308?type=Model&format=SafeTensor&size=pruned&fp=fp16" --content-disposition', shell=True)
# response = requests.get("https://civitai.com/api/download/models/238308?type=Model&format=SafeTensor&size=pruned&fp=fp16", allow_redirects=True, stream=True)
# content_dispotion = response.headers['Content-Disposition']
# file_name = content_dispotion[content_dispotion.find('filename=') + len('filename='):]
# all = tqdm(response.iter_content(), total=int(response.headers.get('content-length', 0)), unit='MB', unit_scale=True)
# for i in all:
#     pass
# print(file_name)

# print(response.headers)
# for chunk in response.iter_content(chunk_size=1024):
#     print(chunk)
# content_type = response.headers['Content-Type']
# ATTRIBUTE = 'filename='

# print(file_name)
# from mlvault.datapack.main import DataPack, DataPackLoader
# with open("config.json", "r") as f:
#     registry = json.load(f)
#     pack = DataPack(registry,os.getcwd())
#     pack.export_files()
