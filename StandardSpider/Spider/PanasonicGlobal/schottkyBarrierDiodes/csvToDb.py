"""
    @description:   根据下载好的csv文件对数据进行获取
    @author:        RoyalClown
    @date:          2016/11/4
"""
import os

from DBSave.oracleSave import OracleSave
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class CsvToDb:
    def __init__(self, task_code, task_id):
        self.task_code = task_code
        self.task_id = task_id
        self.url = "http://www.semicon.panasonic.co.jp/downloader/csv_prod/?cat=CDF7000&lang=CN"
        self.path = "I:\PythonPrj\StandardSpider\\Spider\\schottkyBarrierDiodes\\"

    def csv_download(self):
        html_analyse = HtmlAnalyse(self.url)
        filename = self.path + 'schottkyBarrierDiodes.csv'
        if os.path.exists(filename):
            return filename
        html_analyse.download(filename)
        return filename

    def get_csv_data(self):
        csv_file = self.csv_download()
        import csv

        with open(csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                component = ['http://www.semicon.panasonic.co.jp/cn/products/discrete/diodes/shottkybarrierdiodes/#products-document', row['锘縋arts'], row['series'], '-', row['Datasheet']]
                try:
                    orcl_conn = OracleSave(self.task_code, self.task_id)
                    orcl_conn.component_insert(component)

                    for k in row:
                        if k not in ('锘縋arts', 'series', 'Datasheet'):
                            single_property = k, row[k]
                            orcl_conn.properties_insert(single_property)
                            print(single_property)
                    orcl_conn.commit()
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    csvtodb = CsvToDb('CCT2016110400000007', 42)
    csvtodb.get_csv_data()
