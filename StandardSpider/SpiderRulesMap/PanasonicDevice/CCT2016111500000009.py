"""
    @description:   此单号与松下电器
    @author:        RoyalClown
"""
from DataAnalyse.dbDataGet.Util_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection
from Spider.PanasonicDevice.PhotoMOS.saveAndGo import all_go
from Spider.PanasonicGlobal.schottkyBarrierDiodes.csvToDb import CsvToDb


class CCT2016111500000009:
    def __init__(self):
        self.url = "http://device.panasonic.cn/ac/c/control/list_search_spec/photomos/index.jsp"
        self.task_code = "CCT2016111500000009"
        self.task_id = self.get_task_id()

    def get_task_id(self):
        orcl_conn = OracleConnection()
        cursor = orcl_conn.conn.cursor()
        cursor.execute(
            "select cct_id from product$component_crawl_task where cct_taskid='{}'".format(self.task_code))
        task_id = cursor.fetchone()[0]
        cursor.close()
        return task_id

    def go(self):
        print("开始进行爬取")
        all_go(self.task_code, self.task_id)
        print("成功完成爬取数据到爬虫数据表\n------------------现在开始下载pdf、img文件-----------------")
        pdf_download = PdfDownload()
        pdf_download.go()
        # 此类目无图片
        print("pdf、img下载完成，开始对数据进行分析并存入数据库")

        # 以下为数据分析，基本全部需要改
        main = DataProcessing()
        main.go(self.task_id)


if __name__ == "__main__":
    taskn = CCT2016111500000009()
    taskn.go()
