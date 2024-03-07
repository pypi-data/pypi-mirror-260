import os
from os.path import join as join_path
from os.path import isfile
from datasets import Dataset
from PIL import Image
import numpy as np
from huggingface_hub import upload_file
import toml
import yaml
from huggingface_hub.file_download import hf_hub_download
from tqdm import tqdm
from typing import Any
from mlvault.api import download_file_from_hf
from mlvault.config import get_r_token
from mlvault.util import load_dataset_for_dpack, parse_str_to_list

def to_optional_dict(d:Any, keys:list[str]):
    output = {}
    for key in keys:
        val = d.__dict__[key] if hasattr(d, key) else None
        if(val):
            output[key] = val
    return output

def get_ext(file_name: str):
    return os.path.splitext(file_name)[1].lower()

imgs = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']

def list_dir_in_img(path:str):
    files = os.listdir(path)
    filtered = filter(lambda file: get_ext(file) in imgs, files)
    return list(filtered)   

def check_has_filters(captions:str, filters:list[str], exclude_filters:list[str]=[]):
    caption_list = list(map(lambda token: token.strip(), captions.split(",")))
    filter_cnt = 0
    for e_filter in exclude_filters:
        if e_filter in caption_list:
            return False
    for filter in filters:
        if filter in caption_list:
            filter_cnt += 1
    if filter_cnt == len(filters):
        return True
    else:
        return False

def export_dataset_rows(dataset:Dataset, target_dir:str, filters:list[str]=[]):
    data_len = len(dataset)
    print(f"exporting {data_len} files")
    for i in tqdm(range(data_len)):
        data = dataset[i]
        os.makedirs(target_dir, exist_ok=True)
        file_name = data['file_name']
        base_name = os.path.splitext(file_name)[0]
        extension = data['caption_extension']
        caption = data['caption']
        image = data['image']
        to_save_img_path = f"{target_dir}/{file_name}"
        to_save_caption_path = f"{target_dir}/{base_name}{extension}"
        caption = (data['caption'] or "").strip()
        if caption:
            captions = list(map(lambda token: token.strip(), caption.split(",")))
            filtered_captions = list(filter(lambda token: token not in filters, captions))
            primary_captions = ", ".join([*filters, *filtered_captions])
            open(to_save_caption_path, 'w').write(primary_captions)
        nparr = np.array(image)
        Image.fromarray(nparr).save(to_save_img_path)
    

def export_datataset_by_filters(dataset:Dataset, target_dir:str|None, filters:list[str]=[], exclude_filters:list[str]=[]):
    print(f"exporting by filters {filters}")
    filtered = dataset.filter(lambda data: check_has_filters(data['caption'], filters, exclude_filters))
    data_len = len(filtered)
    if target_dir:
        print(f"exporting {data_len} files")
        export_dataset_rows(filtered, target_dir, filters)
        print("Datasets exported!")
    else:
        print(f"Dataset has {data_len} files")
        return filtered

def export_dataset_by_divider(dataset:Dataset, target_dir:str, divider:str):
    print(f"exporting by divider {divider}")
    print(dataset[2])
    filtered = dataset.filter(lambda data: data['div'] == divider)
    data_len = len(filtered)
    print(f"exporting {data_len} files")
    export_dataset_rows(filtered, target_dir)
    print("Datasets exported!")

class DataTray:
    imgs: list = []
    caption: list[str] = []
    div: list[str] = []
    file_name: list[str] = []
    caption_extension:list[str] = []

    def add(self, div: str, img_file_name: str, image: Image.Image, caption: str, caption_extension:str):
        self.div.append(div)
        self.file_name.append(img_file_name)
        self.imgs.append(image)
        self.caption.append(caption)
        self.caption_extension.append(caption_extension)

    def to_dataset(self):
        ds = Dataset.from_dict(
            {
                "div": self.div,
                "image": self.imgs,
                "caption": self.caption,
                "file_name": self.file_name,
                "caption_extension": self.caption_extension
            }
        )
        return ds
    
    def push_to_hub(self, repo_id:str, w_token:str):
        dset = self.to_dataset()
        if(len(dset)):
            dset.push_to_hub(repo_id, token=w_token, private=True)

class SubsetConfig:

    def __init__(self, name:str, config_input:dict, work_dir:str) -> None:
        if(name.startswith(":")):
            repo_name, subset_name = name[1:].split(":")
            self.name = subset_name
            self.dynamic_repo_id = repo_name
            base = work_dir.rsplit(":")[0]
            self.work_dir = f"{base}/{subset_name}"
        else:
            self.name = name
            self.work_dir = work_dir
            self.dynamic_repo_id = None
        if "path" in config_input:
            self.path = config_input["path"]
        if "class_tokens" in config_input:
            self.class_tokens = config_input["class_tokens"]
        if "is_reg" in config_input:
            self.is_reg = config_input["is_reg"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        self.filters = parse_str_to_list(config_input.get("filters"))
        self.exclude_filters = parse_str_to_list(config_input.get("exclude", []))
        pass
    
    def to_toml_dict(self, dataset_dir:str):
        toml_dict = to_optional_dict(self, ["caption_extension", "keep_tokens", "num_repeats", "shuffle_caption", "class_tokens", "is_reg"])
        toml_dict["image_dir"] = join_path(dataset_dir, self.name)
        if self.dynamic_repo_id:
            toml_dict["caption_extension"] = ".txt"
        return toml_dict

    def expost_dset_files(self,  default_dataset: Dataset | None):
        if self.dynamic_repo_id:
            ds = load_dataset_for_dpack(self.dynamic_repo_id)
            export_datataset_by_filters(ds, self.work_dir, self.filters, self.exclude_filters)
        elif default_dataset:
            subset_div = self.work_dir.split("/")[-2:]
            export_dataset_by_divider(default_dataset, self.work_dir, "/".join(subset_div))


class DatasetConfig:
    subsets: dict[str, SubsetConfig] = {}

    def __init__(self, name:str, config_input:dict, work_dir:str) -> None:
        self.work_dir = work_dir
        self.name = name
        if "resolution" in config_input:
            self.resolution = config_input["resolution"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        if "class_tokens" in config_input:
            self.class_tokens = config_input["class_tokens"]
        for dataset_key in config_input['subsets']:
            config = { **config_input, **config_input['subsets'][dataset_key]}
            self.subsets[dataset_key] = SubsetConfig(dataset_key, config, join_path(work_dir, dataset_key))
        pass

    def to_dict(self):
        dict_subsets = {}
        for subset_key in self.subsets:
            dict_subsets[subset_key] = self.subsets[subset_key].__dict__
        return {
            "caption_extension": self.caption_extension,
            "name": self.name,
            "subsets": dict_subsets
        }
    def to_toml_dict(self, dataset_dir:str):
        toml_dict = to_optional_dict(self, ["resolution"])
        toml_dict["subsets"] = []
        for subset_key in self.subsets:
            toml_dict["subsets"].append(self.subsets[subset_key].to_toml_dict(join_path(dataset_dir, self.name)))
        return toml_dict
    
    def export_dset_files(self,  default_dataset: Dataset | None):
        for subset_key in self.subsets:
            self.subsets[subset_key].expost_dset_files(default_dataset)


class InputConfig:
    datasets: dict[str, DatasetConfig] = {}

    def __init__(self, config_input:dict, work_dir:str) -> None:
        self.dataset_repo = config_input.get("dataset_repo")
        self.work_dir = work_dir
        if "resolution" in config_input:
            self.resolution = config_input["resolution"]
        if "caption_extension" in config_input:
            self.caption_extension = config_input["caption_extension"]
        if "keep_tokens" in config_input:
            self.keep_tokens = config_input["keep_tokens"]
        if "num_repeats" in config_input:
            self.num_repeats = config_input["num_repeats"]
        if "shuffle_caption" in config_input:
            self.shuffle_caption = config_input["shuffle_caption"]
        for dataset_key in config_input['datasets']:
            config = { **config_input, **config_input['datasets'][dataset_key]}
            self.datasets[dataset_key] = DatasetConfig(dataset_key, config, join_path(work_dir, dataset_key))
        pass

    def to_dict(self):
        dict_datasets = {}
        for dataset_key in self.datasets:
            dict_datasets[dataset_key] = self.datasets[dataset_key].to_dict()
        return {
            "repo_id": self.dataset_repo,
            "datasets": dict_datasets
        }
    
    def to_toml_dict(self, datasets_dir:str):
        toml_dict = {"general":{"enable_bucket":True}, "datasets":[]}
        for dataset_key in self.datasets:
            toml_dict["datasets"].append(self.datasets[dataset_key].to_toml_dict(datasets_dir))
        return toml_dict
    
    def export_dset_files(self, default_dataset: Dataset | None):
        for dataset_key in self.datasets:
            self.datasets[dataset_key].export_dset_files(default_dataset)


class OutputConfig:

    def __init__(self, config_input:dict) -> None:
        self.model_name = config_input["model_name"]
        self.save_model_as = config_input["save_model_as"]
        pass 

class TrainConfig:
    def __init__(self, config_input:dict) -> None:
        self.base_model = config_input.get("base_model", None)
        self.continue_from = config_input.get("continue_from", None)
        pass

class SampleConfig:
    def __init__(self, config_input) -> None:
        self.prompts = config_input["prompts"]
        self.sampler = config_input["sampler"]
        pass

class DataPack:
    @staticmethod
    def from_yml(config_file_path:str):
        config =  yaml.load(open(config_file_path, 'r'), Loader=yaml.FullLoader)
        os.path.dirname(config_file_path)
        return DataPack(config, os.path.dirname(config_file_path))

    def __init__(self, config:dict, work_dir:str):
        self.work_dir = work_dir
        self.input = InputConfig(config["input"], join_path(work_dir, "datasets"))
        self.output = OutputConfig(config["output"])
        self.train = TrainConfig(config["train"])
        self.sample = SampleConfig(config["sample"])
    
    def to_dict(self):
        return {
            "input": self.input.to_dict()
        }
    
    def to_data_tray(self):
        data_tray = DataTray()
        for dataset_key in self.input.datasets:
            for subset_key in self.input.datasets[dataset_key].subsets:
                if(subset_key.startswith(":")):
                    print("Dataset will resolved at runtime. skipping...")
                    continue
                else:
                    print("Uploading to data tray")
                    subset = self.input.datasets[dataset_key].subsets[subset_key]
                    extension = subset.caption_extension
                    src_dir = subset.path
                    img_names = list_dir_in_img(src_dir)
                    caption = []
                    for img_name in img_names:
                        name, _ = os.path.splitext(img_name)
                        tag_name = f"{name}{extension}"
                        caption = ""
                        img_path = f"{src_dir}/{img_name}"
                        img = Image.open(img_path)
                        if tag_name and  isfile(f"{src_dir}/{tag_name}"):
                            caption = open(f"{src_dir}/{tag_name}", "r").read()
                        data_tray.add(
                            div=f"{dataset_key}/{subset_key}", image=img, caption=caption, img_file_name=img_name, caption_extension=extension
                        )
                    print(f"{len(img_names)} images added to data tray")
        return data_tray
    
    def push_to_hub(self, w_token:str):
        if self.input.dataset_repo:    
            try:
                print("Start pushing to hub!")
                self.to_data_tray().push_to_hub(self.input.dataset_repo, w_token)
                config_file = f"{self.work_dir}/config.yml"
                upload_file(
                    repo_id=self.input.dataset_repo,
                    path_or_fileobj=config_file,
                    path_in_repo="config.yml",
                    token=w_token,
                    repo_type="dataset",
                )
            except:
                print("Can not push to hub!")
                raise
    
    def export_files(self):
        try:
            print("Start exporting files!")
            if self.input.dataset_repo:
                hf_hub_download(repo_id=self.input.dataset_repo, filename="config.yml", repo_type="dataset", local_dir=self.work_dir, token=get_r_token())
            self.export_datasets()
            self.write_sample_prompt(self.work_dir)
            self.write_toml(self.work_dir)
        except:
            print("Can not export files!")
            raise

    def write_sample_prompt(self, base_dir:str):
        sample_prompt:list[str] = self.sample.prompts
        sample_prompt_path = f"{base_dir}/sample.txt"
        open(sample_prompt_path, "w").write("\n".join(sample_prompt))
        print("Sample prompt written!")

    def write_toml(self, base_dir:str):
        toml_dict = self.input.to_toml_dict(join_path(base_dir, "datasets"))
        toml_path = f"{base_dir}/config.toml"
        toml.dump(toml_dict, open(toml_path, "w"))
        self.toml_path = toml_path
        print("toml written!")
    
    def export_datasets(self):
        repo_id = self.input.dataset_repo
        dataset = load_dataset_for_dpack(repo_id) if repo_id else None
        self.input.export_dset_files(dataset)
        print("datasets exported!")

class DataPackLoader:
    @staticmethod
    def load_datapack_from_hf(repo_id:str, base_dir:str) -> DataPack:
        hf_hub_download(repo_id=repo_id, filename="config.yml", repo_type="dataset", local_dir=base_dir, token=get_r_token())
        config_file_path = f"{base_dir}/config.yml"
        return DataPack.from_yml(config_file_path)
