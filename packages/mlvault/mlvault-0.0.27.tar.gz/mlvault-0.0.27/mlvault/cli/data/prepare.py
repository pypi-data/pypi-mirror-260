import os
import re
import shutil
from mlvault.datapack.main import DataTray, export_datataset_by_filters
from mlvault.util import find_args, has_args, is_image, parse_str_to_list, resolve_relative_path
from PIL import Image


def prepare(base_dir:str, target_dir:str):
    cucrrent = os.getcwd()
    image_info_dict = {}
    class_dir_images_dict = {}
    base_dir = base_dir if base_dir.startswith("/") else os.path.join(cucrrent, base_dir)
    images = filter(lambda name: is_image(name),  os.listdir(os.path.join(base_dir)))
    for image_name in images:
        image_info_dict[image_name] = {}
        name, _ = os.path.splitext(image_name)
        caption_file_name = name + ".txt"
        caption_file_path = os.path.join(base_dir, caption_file_name)
        image_info_dict[image_name]["path"] = os.path.join(base_dir, image_name)
        image_info_dict[image_name]["captions"] = []
        is_file_exist = os.path.exists(caption_file_path)
        if is_file_exist:
            with open(caption_file_path, "r") as f:
                image_info_dict[image_name]["captions"] = list(map(lambda token: token.strip() ,f.readline().replace("_", " ").replace('1girl', 'girl').replace('1boy', 'boy').split(", ")))

    current_list = os.listdir(cucrrent)
    class_dirs = filter(lambda name: re.match(r'\[.*\].*',name) , current_list )
    task_list = dict = {}
    for class_dir in class_dirs:
        class_name = re.sub(r'\[.*\]', '', class_dir).replace("_", " ").strip()
        class_dir_images_dict[class_name] = []
        class_images = list(filter(lambda name: is_image(name), os.listdir(os.path.join(cucrrent, class_dir))))
        class_dir_images_dict[class_name] = class_images
        for image_name in class_images:
            if image_name not in image_info_dict:
                img_path = os.path.join(cucrrent, class_dir, image_name)
                target_path = os.path.join(target_dir, image_name)
                task_list[target_path] = img_path
                print(f"Image {image_name} from [{class_name}] not found in base directory")
            else :
                image_record = image_info_dict[image_name]
                def remove_and_reinsert():
                    image_record['captions'].remove(class_name)
                if class_name in image_record['captions']:
                    remove_and_reinsert()
                image_record['captions'].insert(0, class_name)
    print(f"Found {len(task_list)} images to prepare")
    for target_path in task_list:
        img_path = task_list[target_path]
        shutil.copyfile(img_path, target_path)
        print(f"Copied {img_path}\n -> {target_path}")


def print_help():
    print("Usage: mlvcli pack <options>")
    print("Options:")
    print("  -b <base directory>")
    print("  -f <class filter> : quotes are required, comma separated")
    print("  -e <to exclude class filter> : quotes are required, comma separated")

def run_prepare(args:list[str]):
    base_dir = find_args(args, "-b")
    if base_dir:
        base_dir = resolve_relative_path(base_dir)
    dest_dir = find_args(args, "-d") or "__need_caption_and_image_in_base_dir"
    if dest_dir:
        dest_dir = resolve_relative_path(dest_dir)

    if not base_dir:
        print("Please provide a base directory")
        print_help()
        exit(1)
    elif not os.path.exists(base_dir):
        print("Base directory does not exist")
        print_help()
        exit(1)
    if not dest_dir:
        print("Please provide a base directory")
        print_help()
        exit(1)
    else:
        os.makedirs(dest_dir, exist_ok=True)
        prepare(base_dir, dest_dir)
