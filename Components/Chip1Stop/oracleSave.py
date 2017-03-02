from Lib.DBConnection.OracleConnection import OracleConnection


class OracleSave(OracleConnection):
    def __init__(self, taskcode='CHIP1STOP', taskid=1000001):
        super().__init__()
        self.taskcode = taskcode
        self.taskid = taskid

    def get_crawl_id(self):
        cursor = self.conn.cursor()
        crawlid = cursor.execute("select product$component_crawl_seq.nextval from dual").fetchone()[0]
        # pvcid = cursor.execute("").fetchone()[0]
        return crawlid

    def component_insert(self, component):
        taskid = self.taskid
        self.crawl_id = self.get_crawl_id()
        cursor = self.conn.cursor()
        sql = "insert into product$component_crawl(cc_id, cc_task, cc_code, cc_brandname, cc_unit, cc_kiname, cc_url, cc_attach) VALUES ({},{},'{}','{}','{}','{}','{}','{}')".format(
            self.crawl_id, taskid, *component)
        insert_data = cursor.execute(sql)
        cursor.close()
        print(component)
        return insert_data

    def properties_insert(self, properties):
        cursor = self.conn.cursor()
        sql = "insert into product$propertyvalue_crawl(pvc_id, pvc_componentid, pvc_propertyname, pvc_value) VALUES (product$pv_crawl_seq.nextval,'{}','{}','{}')".format(
            self.crawl_id, *properties).encode().decode()
        insert_data = cursor.execute(sql)
        cursor.close()
        print(properties)
        return insert_data

    def commit(self):
        self.conn.commit()
