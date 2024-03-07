import huggingface_hub

def upload_file(repo_id:str, local_file:str, repo_path:str, w_token:str):
    repo_exists = huggingface_hub.repo_exists(repo_id=repo_id, token=w_token)
    if not repo_exists:
        huggingface_hub.create_repo(repo_id=repo_id, token=w_token, private=True)
    huggingface_hub.upload_file(repo_id=repo_id, path_in_repo=repo_path, path_or_fileobj=local_file, token=w_token)
