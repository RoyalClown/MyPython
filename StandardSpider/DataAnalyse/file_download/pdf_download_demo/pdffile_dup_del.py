# coding=utf-8
'''
duplication deletion
'''

from pymongo.mongo_client import MongoClient

from util_common import Constant
import requests

cli = MongoClient(Constant.MONGODB_URL)
db = cli.spider
attachs = db.component_original.find({"attachTask": Constant.DONE},
                                     {"_id": True, "attachUrl": True, "attachUrl_uu": True})

fs_api_delete = "http://10.10.100.200:9999/file/delete?path=%s"
attach_ids = set()

for attach in attachs:
    if attach["_id"] not in attach_ids:
        try:
            oth_attachs = db.component_original.find(
                {"attachTask": Constant.DONE, "_id": {"$ne": attach["_id"]}, "attachUrl": attach["attachUrl"],
                 "attachUrl_uu": {"$ne": attach["attachUrl_uu"]}}, {"_id": True, "attachUrl_uu": True})
            for oth_attach in oth_attachs:
                requests.get(fs_api_delete % oth_attach['attachUrl_uu'])
                db.component_original.update_one({'_id': oth_attach["_id"]}, {
                    '$set': {'attachUrl_uu': attach['attachUrl_uu'], 'attach_download_user': 'duplication'}})
                attach_ids.add(oth_attach["_id"])
                print('delete', attach['attachUrl'], oth_attach['attachUrl_uu'])
        except Exception as e:
            print(attach['attachUrl_uu'], e)
            continue
cli.close()
