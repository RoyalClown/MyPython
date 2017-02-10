"""
    @description:   来源:kionix
                    商城品牌:Kionix
                    目标类目:加速度计
                    商城类目:加速计/加速度传感器
                    来源网址:http://zh-cn.kionix.com/parametric/Accelerometers
    @author:        RoyalClown
    @date:          2016/11/17
"""
from DataAnalyse.dbDataGet.CCT2016111700000001_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection
from Spider.Kionix.Accelerometer.saveAndGo import all_go


class CCT2016111700000001:
    def __init__(self):
        self.url = "http://www.rohm.com.cn/web/china/search/parametric/-/search/Serial%20EEPROM"
        self.task_code = "CCT2016111700000001"
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
        print("第一步开始进行爬取")
        all_go(task_code=self.task_code, task_id=self.task_id)
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
    taskn = CCT2016111700000001()
    taskn.go()