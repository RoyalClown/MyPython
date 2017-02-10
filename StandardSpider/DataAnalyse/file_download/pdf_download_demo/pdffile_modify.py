# coding=utf-8
'''
remove last page
'''

import os
import random
import urllib.request

import requests
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from pymongo.mongo_client import MongoClient

from util_common import Constant

cli = MongoClient(Constant.MONGODB_URL)
db = cli.spider
attachs = db.component_original.find({"attachTask": Constant.DONE, "attach_download_user": {'$ne': 'admin'}},
                                     {"_id": True, "attachUrl_uu": True})

fs_api_delete = "http://10.10.100.200:9999/file/delete?path=%s"

for attach in attachs:
    old_filename = str(random.random()) + ".pdf"
    new_filename = str(random.random()) + ".pdf"

    try:
        #         urllib.request.urlretrieve(attach['attachUrl_uu'], old_filename)
        # can not connect to dfs.ubtoc.com
        try:
            urllib.request.urlretrieve(
                attach['attachUrl_uu'].replace('dfs.ubtoc.com/', '10.10.100.200:9999/file/download?path='),
                old_filename)
        except:
            # error attach_url
            db.component_original.update_one({'_id': attach["_id"]}, {
                '$set': {'attachTask': Constant.TODO, 'attachUrl_uu': None, 'attach_download_user': None}})
            continue
        input_stream = open(old_filename, 'rb')
        pdf_input = PdfFileReader(input_stream)
        pdf_output = PdfFileWriter()
        page = 0
        pages = pdf_input.getNumPages() - 1
        # remove last page
        while page < pages:
            pdf_output.addPage(pdf_input.getPage(page))
            page += 1
        output_stream = open(new_filename, 'wb')
        pdf_output.write(output_stream)
        output_stream.close()
        # replace file
        with open(new_filename, 'rb') as file:
            requests.get(fs_api_delete % attach['attachUrl_uu'])
            res = requests.post(Constant.FS_API_UPLOAD, files={'file': file})
            res_j = res.json()
            db.component_original.update_one({'_id': attach["_id"]},
                                             {'$set': {'attachUrl_uu': res_j['path'], 'attach_download_user': 'admin'}})
        input_stream.close()
    except Exception as e:
        print(attach['attachUrl_uu'], e)
        continue
    finally:
        if os.path.exists(old_filename):
            os.remove(old_filename)
        if os.path.exists(new_filename):
            os.remove(new_filename)
cli.close()
