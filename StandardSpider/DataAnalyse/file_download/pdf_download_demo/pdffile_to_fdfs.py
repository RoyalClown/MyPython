# coding=utf-8
'''
下载pdf文件，存储到fdfs文件系统
@author: yingp
'''

from pymongo.mongo_client import MongoClient

from util_common import html_downloader, Constant
import threading
import random
import os
import urllib
import urllib.request
import requests
from PyPDF2.pdf import PdfFileReader, PdfFileWriter


class FileMain():
    def __init__(self, userName='someone', maxThread=100, tempDir="/tmp/"):
        cli = MongoClient(Constant.MONGODB_URL)
        self.db = cli.spider
        self.user = self._get_user(userName)
        self.activeThread = 0
        self.maxThread = maxThread
        self.tempDir = tempDir
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        self.successed = 0
        self.failured = 0
        self.total = 0
        # last one
        self.isLast = False

    def _get_user(self, userName):
        rs_user = self.db.user.find_one({"name": userName})
        if rs_user is None:
            # 初次接入
            print(userName, "：is new for this task, Welcome!")
            rs_user = self.db.user.insert({"name": userName, "starttime": 0})
        return rs_user

    # 获得N个任务
    def _get_task(self, size=1):
        try:
            if self.isLast:
                return self.db.component_original.find({"attachTask": Constant.TODO}, {"_id": True, "attachUrl": True})
            rand = random.random()
            result = self.db.component_original.find({"attachTask": Constant.TODO, "random": {"$gt": rand}}).sort(
                "random", 1).limit(size)
            if result is None:
                result = self.db.component_original.find({"attachTask": Constant.TODO, "random": {"$lt": rand}}).sort(
                    "random", -1).limit(size)
            return result
        except:
            return []

    def hasNext(self):
        try:
            count = self.db.component_original.find({"attachTask": Constant.TODO}).count()
            self.isLast = count <= self.maxThread - self.activeThread
            return count > 0
        except:
            return True

    def _save_one_result(self, _id, cont_file):
        # 保存并生成
        try:
            with open(cont_file, 'rb') as file:
                res = requests.post(Constant.FS_API_UPLOAD, files={'file': file})
                res_j = res.json()
                self.db.component_original.update_one({'_id': _id}, {
                    '$set': {'attachTask': Constant.DONE, 'attachUrl_uu': res_j['path'],
                             'attach_download_user': self.user["name"]}})
        except Exception as e:
            print('failed on save', e)

    def _on_download_success(self, _id, cont_file):
        self.activeThread -= 1
        self._save_one_result(_id, cont_file)
        self.successed += 1

    def _save_with_url(self, _id, attachUrl_uu):
        self.activeThread -= 1
        self.db.component_original.update_one({'_id': _id}, {
            '$set': {'attachTask': Constant.DONE, 'attachUrl_uu': attachUrl_uu,
                     'attach_download_user': self.user["name"]}})
        self.successed += 1

    def _on_download_error(self, e, url):
        self.activeThread -= 1
        self.failured += 1
        print("failed! url: ", url, e)

    '''不同器件的attachUrl可能一样，按attachUrl先查是否有已经下载了的
    '''

    def _find_by_mouser_url(self, url):
        result = self.db.component_original.find_one(
            {"attachTask": Constant.DONE, "attachUrl": url, "attachUrl_uu": {"$exists": True}})
        if result is not None:
            return result['attachUrl_uu']
        return None

    def _before_download(self, _id, url):
        exist_url = self._find_by_mouser_url(url)
        if exist_url is not None:
            self._save_with_url(_id, exist_url)
            return True
        return False

    def craw(self):
        if self.maxThread > self.activeThread:
            currentTasks = self._get_task(self.maxThread - self.activeThread)
            for task in currentTasks:
                # 只考虑.pdf文件
                if str(task["attachUrl"]).find(".pdf") > -1:
                    crawer = CrawerThread(task["_id"], task["attachUrl"], self.tempDir, self._before_download,
                                          self._on_download_success, self._on_download_error)
                    crawer.start()
                    self.activeThread += 1
                    self.total += 1

    def statistic(self):
        return self.successed, self.failured, self.activeThread, self.total

    def close(self):
        self.db.close()


class CrawerThread(threading.Thread):
    def __init__(self, _id, attachUrl, tempDir, beforeHandler, success, error):
        threading.Thread.__init__(self)
        self.downloader = html_downloader.HtmlDownloader()
        self._id = _id
        self.attachUrl = attachUrl
        self.tempDir = tempDir
        self.beforeHandler = beforeHandler
        self.success = success
        self.error = error

    def run(self):
        if self.beforeHandler(self._id, self.attachUrl):
            return
        filename = self.tempDir + str(random.random())
        filename1 = self.tempDir + str(random.random()) + '.pdf'
        try:
            urllib.request.urlretrieve(self.attachUrl, filename)
            input_stream = open(filename, 'rb')
            pdf_input = PdfFileReader(input_stream)
            pdf_output = PdfFileWriter()

            page = 0
            pages = pdf_input.getNumPages() - 1
            # remove last page
            while page < pages:
                pdf_output.addPage(pdf_input.getPage(page))
                page += 1

            output_stream = open(filename1, 'wb')
            pdf_output.write(output_stream)
            output_stream.close()
            input_stream.close()
            if self.success is not None:
                self.success(self._id, filename1)
        except Exception as e:
            if self.error is not None:
                self.error(e, self.attachUrl)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(filename1):
                os.remove(filename1)
