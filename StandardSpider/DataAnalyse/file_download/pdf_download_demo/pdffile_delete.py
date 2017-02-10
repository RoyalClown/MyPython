# coding=utf-8
'''
删除attachTask=4的pdf文件，状态为上传错误
db.component_original.find({attachTask:2}).forEach(function(item){if(item['attachUrl']!=null&&item['attachUrl'].indexOf('.pdf')==-1){item['attachTask']=4;db.component_original.save(item);}})
删除无法读取的pdf，并修改状态为未上传
{attachTask:2, attach_download_user:'deprecated'}
'''
from pymongo.mongo_client import MongoClient
from util_common import Constant
import requests

cli = MongoClient(Constant.MONGODB_URL)
db = cli.spider
fs_api_delete = "http://10.10.100.200:9999/file/delete?path=%s"

# deprecated
attachs = db.component_original.find({"attachTask": Constant.DONE, "attach_download_user": 'deprecated'},
                                     {"_id": True, "attachUrl_uu": True})

for attach in attachs:
    try:
        requests.get(fs_api_delete % attach['attachUrl_uu'])
        db.component_original.update_one({'_id': attach["_id"]}, {
            '$set': {'attachUrl_uu': None, 'attach_download_user': None, 'attachTask': Constant.TODO}})
    except Exception as e:
        print(attach['attachUrl_uu'], e)
        continue

# error    
attachs = db.component_original.find({"attachTask": Constant.ERROR}, {"_id": True, "attachUrl_uu": True})

for attach in attachs:
    try:
        requests.get(fs_api_delete % attach['attachUrl_uu'])
        db.component_original.update_one({'_id': attach["_id"]},
                                         {'$set': {'attachUrl_uu': None, 'attach_download_user': None}})
    except Exception as e:
        print(attach['attachUrl_uu'], e)
        continue

cli.close()
