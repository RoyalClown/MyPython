"""
    @description:   来源:英飞凌官网
                    商城品牌:英飞凌
                    目标类目:600V CoolMOS™ N-Channel Power MOSFET
                    商城类目:金属氧化物半导体场效应管-MOSFET
                    来源网址:http://www.infineon.com/cms/cn/product/power/power-mosfet/500v-900v-n-channel-coolmos-power-mosfet/600v-coolmos-n-channel-power-mosfet/channel.html?channel=ff80808112ab681d0112ab6a628704d8
    @author:        RoyalClown
    @date:          2016/12/9
"""
from Spider.Infineon.CoolMOSN_ChannelPowerMOSFET600V.saveAndGo import all_go
from DataAnalyse.dbDataGet.Infineon_data import DataProcessing

from DataAnalyse.file_download.img_download import ImgDownload
from DataAnalyse.file_download.pdf_download import PdfDownload
from Lib.DBConnection.OracleConnection import OracleConnection


class CCT2016120800000013:
    def __init__(self):
        self.task_code = "CCT2016120800000013"
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
    taskn = CCT2016120800000013()
    taskn.go()
