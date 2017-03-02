from Lib.DBConnection.OracleConnection import OracleConnection


class OracleSave(OracleConnection):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    def get_component_id(self):
        cursor = self.conn.cursor()
        crawl_id = cursor.execute("select product$component_crawl_seq.nextval from dual").fetchone()[0]
        return crawl_id

    def component_insert(self, component):
        self.component_id = self.get_component_id()
        cursor = self.conn.cursor()
        sql = "insert into product$component_crawl(cc_id, cc_task, cc_code, cc_brandname, cc_unit, cc_kiname, cc_url, cc_attach) VALUES ({},{},'{}','{}','{}','{}','{}','{}')".format(
            self.component_id, self.task_id, *component)
        insert_data = cursor.execute(sql)
        cursor.close()
        print(component)
        return insert_data

    def properties_insert(self, properties):
        cursor = self.conn.cursor()
        sql = "insert into product$propertyvalue_crawl(pvc_id, pvc_componentid, pvc_propertyname, pvc_value) VALUES (product$pv_crawl_seq.nextval,'{}','{}','{}')".format(
            self.component_id, *properties).encode().decode()
        insert_data = cursor.execute(sql)
        cursor.close()
        print(properties)
        return insert_data

    def commit(self):
        self.conn.commit()
