import os
import re
from mlvault.datapack.main import DataTray, export_datataset_by_filters
from mlvault.util import find_args, has_args, is_image, parse_str_to_list, resolve_relative_path
from PIL import Image


def search(base_dir:str, token_filter:list[str]):
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
    for class_dir in class_dirs:
        class_name = re.sub(r'\[.*\]', '', class_dir).replace("_", " ").strip()
        class_dir_images_dict[class_name] = []
        class_images = list(filter(lambda name: is_image(name), os.listdir(os.path.join(cucrrent, class_dir))))
        class_dir_images_dict[class_name] = class_images
        for image_name in class_images:
            if image_name not in image_info_dict:
                print(f"Image {image_name} from {class_name} not found in base directory")
            else :
                image_record = image_info_dict[image_name]
                def remove_and_reinsert():
                    image_record['captions'].remove(class_name)
                if class_name in image_record['captions']:
                    remove_and_reinsert()
                image_record['captions'].insert(0, class_name)
    data_tray = DataTray()
    for image_name in image_info_dict:
        image_record = image_info_dict[image_name]
        image = Image.open(image_record['path'])
        filter_len = len(token_filter)
        if filter_len:
            filter_matched = 0
            for toekn_filter in token_filter:
                if toekn_filter in image_record['captions']:
                    filter_matched += 1
            if filter_matched != filter_len:
                continue
        captions = ", ".join(image_record['captions'])
        data_tray.add("generated/generated", image_name, image, captions, ".txt")
    dataset = data_tray.to_dataset()
    return dataset



def print_help():
    print("Usage: mlvcli pack <options>")
    print("Options:")
    print("  -b <base directory>")
    print("  -f <class filter> : quotes are required, comma separated")
    print("  -e <to exclude class filter> : quotes are required, comma separated")

def run_search(args:list[str]):
    base_dir = find_args(args, "-b")
    if base_dir:
        base_dir = resolve_relative_path(base_dir)
    print(base_dir)
    dest_dir = find_args(args, "-d")
    if dest_dir:
        dest_dir = resolve_relative_path(dest_dir)
    count = has_args(args, "-c", "--count")
    token_filter = parse_str_to_list(find_args(args, "-f"))
    exclude_filter = parse_str_to_list(find_args(args, "-e"))
    if not token_filter or not exclude_filter:
        print("Please provide a filter")
        print_help()
        exit(1)
    if not base_dir:
        print("Please provide a base directory")
        print_help()
        exit(1)
    elif not os.path.exists(base_dir):
        print("Base directory does not exist")
        print_help()
        exit(1)
    elif not dest_dir and count:
        dset = search(base_dir, token_filter)
        export_datataset_by_filters(dset, target_dir=None, filters=token_filter, exclude_filters=exclude_filter)
    else:
        dset = search(base_dir, token_filter)
        export_datataset_by_filters(dset, dest_dir, filters=token_filter, exclude_filters=exclude_filter)
