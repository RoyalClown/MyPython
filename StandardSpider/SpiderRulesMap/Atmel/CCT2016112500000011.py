"""
    @description:   来源:atmel官网
                    商城品牌:爱特梅尔
                    目标类目:Serial EEPROM – I2C（爬取订购码）
                    商城类目:电可擦可编程只读存储器-EEPROM
                    来源网址:http://www.atmel.com/products/memories/serial/i2c.aspx
    @author:        RoyalClown
    @date:          2016/11/25
"""
from DataAnalyse.dbDataGet.Util_data import DataProcessing
from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection

from Spider.Atmel.Serial_EEPROM_I2C.saveAndGo import all_go


class CCT2016112500000011:
    def __init__(self):
        self.url = "http://www.atmel.com/products/memories/serial/i2c.aspx"
        self.task_code = "CCT2016112500000011"
        self.task_id = self.get_task_id()
        print(self.task_id)

    def get_task_id(self):
        orcl_conn = OracleConnection()
        cursor = orcl_conn.conn.cursor()
        cursor.execute(
            "select cct_id from product$component_crawl_task where cct_taskid='{}'".format(self.task_code))
        task_id = cursor.fetchone()[0]
        cursor.close()
        return task_id

    def go(self):
        step = [3]
        if 1 in step:
            print("开始进行爬取")
            all_go(task_code=self.task_code, task_id=self.task_id)
            print("成功完成爬取数据到爬虫数据表\n------------------现在开始下载pdf、img文件-----------------")
        if 2 in step:
            pdf_download = PdfDownload()
            pdf_download.go()
            img_download = ImgDownload()
            img_download.go()
            print("pdf、img下载完成，开始对数据进行分析并存入数据库")
        if 3 in step:
            # 以下为数据分析，基本全部需要改
            data_processing = DataProcessing()
            data_processing.go(self.task_id)


if __name__ == "__main__":
    taskn = CCT2016112500000011()
    taskn.go()