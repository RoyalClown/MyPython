"""
    @description:   此单号与松下导电性聚合物钽固体电解电容器 (POSCAP)对应
    @author:        RoyalClown
"""
from DataAnalyse.dbDataGet.Util_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection
from Spider.Panasonic.forth_type1.forthGo import forth_go


class CCT2016110400000005:
    def __init__(self):
        self.url = "https://industrial.panasonic.cn/ea/products/capacitors/polymer-capacitors/poscap#quicktabs-line_up_page_tab=1"
        self.task_code = "CCT2016110400000005"
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
        forth_go(self.url, task_code=self.task_code, task_id=self.task_id)
        print("成功完成爬取数据到爬虫数据表\n------------------现在开始下载pdf、img文件-----------------")
        pdf_download = PdfDownload(self.task_id)
        pdf_download.go()
        img_download = ImgDownload()
        img_download.go()
        print("pdf、img下载完成，开始对数据进行分析并存入数据库")

        # 以下为数据分析，基本全部需要改
        data_processing = DataProcessing()
        data_processing.go(self.task_id)


if __name__ == "__main__":
    taskn = CCT2016110400000005()
    taskn.go()
