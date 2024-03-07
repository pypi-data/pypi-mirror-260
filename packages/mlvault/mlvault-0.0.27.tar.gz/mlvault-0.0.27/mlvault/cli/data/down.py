import os
from ...datapack import DataPackLoader
from ...config import get_r_token

def download_dataset(args:list[str]):
    repo_id = args[0]
    DataPackLoader.load_datapack_from_hf(repo_id, os.getcwd()).export_files()
