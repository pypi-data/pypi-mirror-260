import os
from huggingface_hub import snapshot_download, HfFileSystem
from mlvault.cli.data.prepare import run_prepare
from mlvault.cli.data.search  import run_search
from mlvault.cli.data.extract import run_extract
from .down import download_dataset
from .pack import run_pack
from mlvault.datapack import DataPack, DataPackLoader
from mlvault.config import get_r_token, get_w_token

def upload_dataset(args:list[str]):
    try:
        i_file_path, = args
        file_path = i_file_path if i_file_path.startswith("/") else os.path.join(os.getcwd(), i_file_path)
        if not file_path.endswith(".yml"):
            print("File must be a .yml file")
            exit(1)
        if not os.path.exists(file_path):
            print("File does not exist")
            exit(1)
        else:
            DataPack.from_yml(file_path).push_to_hub(get_w_token())
    except Exception as e:
        print(e)
        print("Please provide a file name")
        exit(1)


def snapshot(repo_id:str):
    snapshot_download(repo_id, token=get_r_token(), local_dir=os.getcwd())

def models(repo_id:str):
    hfs = HfFileSystem(token=get_r_token())
    res_list= hfs.glob(f'{repo_id}/**.safetensors')
    print(f"Found {len(res_list)} models")
    if len(res_list) == 0:
        print("No models found")
        exit(1)
    else:
        for res in res_list:
            if res:
                file_name = str(res).split("/")[-1]
                lpath = os.path.join(os.getcwd(), file_name)
                hfs.get_file(res, lpath)
                print(f"Downloaded {res} -> {lpath}")
        print("Download models successfully")

def main(input_args:list[str]):
    action, *args = input_args
    if action == "up":
        upload_dataset(args)
    elif action == "down":
        download_dataset(args)
    elif action == "snapshot":
        snapshot(args[0])
    elif action == "model":
        models(args[0])
    elif action == "pack":
        run_pack(args)
    elif action == "search":
        run_search(args)
    elif action == "prepare":
        run_prepare(args)
    elif action == "extract":
        run_extract(args)
