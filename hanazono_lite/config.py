import os
import json


class Config:
    _instance = None

    @staticmethod
    def getInstance():
        if Config._instance == None:
            Config()
        return Config._instance

    def __init__(self):
        if Config._instance != None:
            raise Exception("This class is a singleton!")
        else:
            with open(os.environ["CONFIG"]) as f:
                Config._instance = json.load(f)
            f.close()
