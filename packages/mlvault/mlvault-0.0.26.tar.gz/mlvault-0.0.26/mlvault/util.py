import os
from datasets import load_dataset, DatasetDict, IterableDatasetDict, Dataset

from mlvault.config import get_r_token
def is_image(filename:str):
    img_extensions = ["jpg", "jpeg", "png", "webp"]
    extension = filename.split(".")[-1]
    return extension in img_extensions

def find_args(args:list[str], *targets:str):
    for target in targets:
        if target in args:
            index = args.index(target)
            return args[index + 1] 
    return None

def has_args(args:list[str], *targets:str):
    for target in targets:
        if target in args:
            return True
    return False

def load_dataset_for_dpack(repo_id:str):
    ds = load_dataset(repo_id, split="train", token=get_r_token())
    if isinstance(ds, Dataset):
        return ds
    else :
        raise Exception("Invalid dataset")


def parse_str_to_list(str_input:str | None) -> list[str]:
    if not str_input:
        return []
    else:
        splitted = map(lambda token: token.strip(), str_input.split(","))
        filtered = filter(lambda token: token, splitted)
        return list(filtered)

def resolve_relative_path(path:str):
    if path.startswith("/"):
        return path
    else:
        return os.path.join(os.getcwd(), path)
