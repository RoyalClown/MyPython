"""
    @description:   此单号与松下半导体肖特基二极管对应
    @author:        RoyalClown
"""
from DataAnalyse.dbDataGet.Util_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection
from Spider.PanasonicGlobal.schottkyBarrierDiodes.csvToDb import CsvToDb


class CCT2016110400000007:
    def __init__(self):
        self.url = "https://industrial.panasonic.cn/ea/products/capacitors/polymer-capacitors/sp-cap#quicktabs-line_up_page_tab=1"
        self.task_code = "CCT2016110400000007"
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
        csv_to_db = CsvToDb(task_code=self.task_code, task_id=self.task_id)
        csv_to_db.csv_download()
        csv_to_db.get_csv_data()
        print("成功完成爬取数据到爬虫数据表\n------------------现在开始下载pdf、img文件-----------------")
        pdf_download = PdfDownload(self.task_id)
        pdf_download.go()
        # 此类目无图片
        print("pdf、img下载完成，开始对数据进行分析并存入数据库")

        # 以下为数据分析，基本全部需要改
        main = DataProcessing()
        main.go(self.task_id)


if __name__ == "__main__":
    taskn = CCT2016110400000007()
    taskn.go()
