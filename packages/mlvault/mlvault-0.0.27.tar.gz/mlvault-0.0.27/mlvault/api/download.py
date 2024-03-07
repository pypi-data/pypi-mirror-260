from huggingface_hub import snapshot_download, hf_hub_download
def download_from_hf(repo_id:str, local_dir:str, r_token:str):
    snapshot_download(repo_id=repo_id, local_dir=local_dir, token=r_token, local_dir_use_symlinks=False)

def download_file_from_hf(repo_id:str, file_name:str, local_dir:str, r_token:str):
    hf_hub_download(repo_id=repo_id, filename=file_name, local_dir=local_dir, token=r_token, local_dir_use_symlinks=False)
