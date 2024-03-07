# coding: utf-8
import configparser
import mlvault

class ConfigManaer:
    package_path:str = mlvault.__path__[0] # type: ignore
    config_ini_path = f"{package_path}/config.ini"
    ini:configparser.ConfigParser

    def __init__(self) -> None:
        self.ini = configparser.ConfigParser()
        self.ini.read(self.config_ini_path, encoding='utf-8')
        if not self.ini.has_section("AUTH"):
            self.ini.add_section("AUTH")
        pass

    def reset(self):
        self.ini.remove_section('AUTH')
        self.ini.add_section('AUTH')
        self.ask_r_token()
        self.ask_w_token()
        self.save()
    
    def set_auth(self, r_token="", w_token=""):
        if(r_token):
            self.set_r_token(r_token)
        if(w_token):
            self.set_w_token(w_token)

    def set_r_token(self, r_token:str):
        if not self.ini.has_section("AUTH"):
            self.ini.add_section("AUTH")
        self.ini.set('AUTH', 'r_token', r_token)
        self.save()

    def set_w_token(self, w_token:str):
        if not self.ini.has_section("AUTH"):
            self.ini.add_section("AUTH")
        self.ini.set('AUTH', 'w_token', w_token)
        self.save()
    
    def ask_r_token(self):
        r_token = input("Please enter your Hugging face read token.\n")
        self.ini.set('AUTH', 'r_token', r_token)
        self.save()
    
    def ask_w_token(self):
        w_token = input("Please enter your Hugging face write token.\n")
        self.ini.set('AUTH', 'w_token', w_token)
        self.save()
    
    def save(self):
        with open(self.config_ini_path, 'w') as f:
            self.ini.write(f)

def config():
    ConfigManaer().reset()

def get_r_token():
    config = ConfigManaer()
    return config.ini.get('AUTH', 'r_token')

def get_w_token():
    config = ConfigManaer()
    return config.ini.get('AUTH', 'w_token')

def set_auth_config(r_token="", w_token=""):
    config = ConfigManaer()
    config.set_auth(r_token, w_token)
