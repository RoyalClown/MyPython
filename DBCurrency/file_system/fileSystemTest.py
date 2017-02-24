"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/24
"""
import requests

from DBCurrency.file_system.FileSystemConstant import File_Server_Url
with open("I:\PythonPrj\MyPython\DBCurrency\\file_system\download_files\logo-holt.png", "rb") as f:
    res = requests.post(File_Server_Url, files={'file': f})
    res_j = res.json()
path = res_j["path"]
print(path)