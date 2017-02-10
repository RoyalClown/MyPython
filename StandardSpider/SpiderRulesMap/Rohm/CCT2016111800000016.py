"""
    @description:   来源:rohm
                    商城品牌:罗姆半导体
                    目标类目:DDR-SDRAM用线性稳压器
                    商城类目:线性稳压器
                    来源网址:http://www.rohm.com.cn/web/china/search/parametric/-/search/Linear%20Regulators%20for%20DDR-SDRAM
    @author:        RoyalClown
    @date:          2016/11/18
"""
from DataAnalyse.dbDataGet.Util_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection
from Spider.Rohm.VoltageRegulator.DDR_SDRAM.saveAndGo import all_go


class CCT2016111800000016:
    def __init__(self):
        self.url = "http://www.rohm.com.cn/web/china/search/parametric/-/search/Linear%20Regulators%20for%20DDR-SDRAM"
        self.task_code = "CCT2016111800000016"
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
        # print("第一步开始进行爬取")
        # all_go(task_code=self.task_code, task_id=self.task_id)
        # print("成功完成爬取数据到爬虫数据表\n------------------现在开始下载pdf、img文件-----------------")

        # pdf_download = PdfDownload(self.task_id)
        # pdf_download.go()
        # img_download = ImgDownload()
        # img_download.go()
        # print("pdf、img下载完成，开始对数据进行分析并存入数据库")

        data_processing = DataProcessing()
        data_processing.go(self.task_id)


if __name__ == "__main__":
    taskn = CCT2016111800000016()
    taskn.go()
