import os
import sys

from mlvault.api.download import download_file_from_hf
from mlvault.util import resolve_relative_path,has_args
from .data import main as data
from mlvault.config import config, get_r_token, set_auth_config

NAMESPACES = ["data", "config", "get", 'file']

def exit_with_help(msg=""):
    if msg:
        print()
        print("  Error:")
        print(f"    {msg}")
        print()
    print("Usage: mlvcli <namespace> <args>")
    print("Namespaces: data, config")
    print("For help on a namespace, run: mlvault <namespace> --help")
    exit(1)

def main():
    input_args = sys.argv[1:]
    if len(sys.argv) < 2:
        exit_with_help("Invalid args")
    namespace_name, *args = input_args
    if namespace_name not in NAMESPACES:
        print(f"Namespace {namespace_name} not found")
        exit(1)
    if namespace_name == "data":
        data(args)
    elif namespace_name == "config-env":
        if len(args) == 0:
            config()
        else:
            r_token = os.getenv("HUGGING_FACE_READ_TOKEN")
            w_token = os.getenv("HUUGING_FACE_WRITE_TOKEN")
            if r_token:
                set_auth_config(r_token=r_token)
            if w_token:
                set_auth_config(w_token=w_token)
        pass
    elif namespace_name == "config":
        read_from_env = has_args(args,"-e")
        if read_from_env:
            rtoken = os.environ.get("HUGGING_FACE_READ_TOKEN")
            wtoken = os.environ.get("HUGGING_FACE_WRITE_TOKEN")
            if not rtoken or not wtoken:
                print("No tokens found in environment")
                exit(1)
            else:
                set_auth_config(r_token=rtoken, w_token=wtoken)
                print("set tokens from environment variables")
        elif len(args) == 0:
            config()
        else:
            r_token = args.index("-r")
            r_value = args[r_token+1]
            w_token = args.index("-w")
            w_value = args[w_token+1]
            if r_value:
                set_auth_config(r_token=r_value)
            if w_value:
                set_auth_config(w_token=w_value)
        pass
    elif namespace_name == "file":
        repo_id, filename = args[0].split(":")
        target = args[1] if len(args) > 1 else os.getcwd()
        download_file_from_hf(repo_id=repo_id, file_name=filename, local_dir=resolve_relative_path(target), r_token=get_r_token())
