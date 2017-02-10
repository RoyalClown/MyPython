"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/16
"""
from Lib.DBConnection.OracleConnection import OracleConnection

conn = OracleConnection()
cursor = conn.conn.cursor()
cursor.execute(
    "select sess.sid,sess.serial#,lo.oracle_username,lo.os_user_name,ao.object_name,lo.locked_mode from v$locked_object lo, dba_objects ao, v$session sess where ao.object_id = lo.object_id and lo.session_id = sess.sid and os_user_name='RoyalClown'")
sessions = cursor.fetchall()
for session in sessions:
    sid = session[0]
    serial = session[1]
    cursor = conn.conn.cursor()
    sql = "alter system kill session '{},{}'".format(sid, serial)
    cursor.execute(sql)
    cursor.close()

    conn.conn.commit()
    print("kill success")
