import os, json

def createConfig(folderpath: str, configpath: str):
    if not os.path.exists(configpath):
        if not os.path.isdir(folderpath):
            os.mkdir(folderpath)
            
        with open(configpath, 'w') as f:
            f.write('{ "server": "your.own.server.here", "port": "6667", "creds": { "nick": "put", "username": "your", "realname": "creds", "pass": "here" }}')
    else:
        return None

def loadConfig(configpath: str) -> dict:
    with open(configpath, 'r') as f:
        data = json.load(f)

    return data