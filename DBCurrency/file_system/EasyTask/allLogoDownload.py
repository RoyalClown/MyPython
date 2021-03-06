"""
    @description:   
    @author:        RoyalClown
    @date:          2017/5/4
"""

import cx_Oracle

from DBCurrency.file_system.fileSystem import FileSystem
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.Constant import B2B_Oracle_Url


class BrandLogo:
    def __init__(self):
        pass

    def get_download_urls(self):
        oracle_conn = cx_Oracle.connect(B2B_Oracle_Url)
        cursor = oracle_conn.cursor()
        sql_sentence = "select distinct br_logourl,br_name_en from product$brand where br_logourl is not null order by br_name_en"
        cursor.execute(sql_sentence)
        brand_logo_urls = cursor.fetchall()
        cursor.close()
        oracle_conn.close()
        return brand_logo_urls

    def update_local_url(self, server_file_url, br_id):
        oracle_conn = cx_Oracle.connect(B2B_Oracle_Url)
        cursor = oracle_conn.cursor()
        sql_sentence = "update product$brand_import set br_logourl_c='{}' where br_id={}".format(server_file_url, br_id)
        cursor.execute(sql_sentence)
        print("Update Success !!")
        cursor.close()
        oracle_conn.commit()
        oracle_conn.close()

    def brand_logo_go(self):
        def thread_go(brand_logo_url):
            logo_url, br_name = brand_logo_url

            # if "https" in logo_url:
            #     return
            server_file_url = file_system.file_download(logo_url, ".png", file_name=br_name.replace("/", ""))

        brand_logo_urls = self.get_download_urls()
        file_system = FileSystem()

        # threadingpool = ThreadingPool(20)
        # threadingpool.multi_thread(thread_go, brand_logo_urls)

        for brand_logo_url in brand_logo_urls:
            thread_go(brand_logo_url)


if __name__ == "__main__":
    brand_logo = BrandLogo()
    brand_logo.brand_logo_go()
