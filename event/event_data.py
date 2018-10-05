import pymysql.cursors
import event_settings

def mon_con():
    connection = pymysql.connect(host = event_settings.dbhost,
                                 user = event_settings.dbuser,
                                 password = event_settings.dbpassword,
                                 db = event_settings.database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    return connection

def agent_select_id():
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id from agentevent ORDER BY id DESC LIMIT 1" 
            cursor.execute(sql)
            result = cursor.fetchone()
            result = str(result["id"])
            return result
    finally:
        connection.close()

def agent_events_processed(id):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE agentevent SET processed=1 WHERE id<=" + str(id)
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

def agent_filter_select(id):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = """select t1.notify_email, t1.notify_name, t2.id, t2.timestamp, t2.name, t2.monitor, t2.message, t2.severity, t2.status FROM notifyrule as t1 
                  INNER JOIN agentevent as t2 on 
                  t2.name LIKE t1.agent_name AND t2.monitor LIKE t1.agent_monitor 
                  AND t2.status LIKE t1.agent_status AND t2.severity LIKE t1.agent_severity AND t2.processed=0 AND T2.id<=""" + str(id) + " AND t1.notify_enabled=1"
            cursor.execute(sql)
            result = cursor.fetchall()
            agent_events_processed(id)
            return result
    finally:
        connection.close()

def agent_avail_select(timestamp):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM agentsystem WHERE timestamp<" + timestamp
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def agent_avail_event_open(timestamp, name, message, severity):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = r"""INSERT INTO agentevent 
            (timestamp, name, monitor, message, status, severity, processed) 
            SELECT """ + str(timestamp) + """, '""" + name + """', 'perf.system.availability.seconds', '""" + message + """', 1, """ + str(severity) + """, 0 FROM DUAL
            WHERE NOT EXISTS (SELECT name FROM agentevent WHERE name='""" + name + """' AND monitor='perf.system.availability.seconds' AND status=1)"""
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()        

def agent_avail_select_event_open(timestamp):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = r"""SELECT DISTINCT t1.name FROM agentevent as t1 
            INNER JOIN agentdata as t2 on t1.name = t2.name
            WHERE t1.monitor='perf.system.availability.seconds' AND t1.status=1 AND t2.timestamp >=""" + str(timestamp)
            cursor.execute(sql)
            result = cursor.fetchall()
            if not result is None:
                for i in result:
                    name = i['name']
                    print(name)
                    sql = r"UPDATE agentevent SET status=0 WHERE name='" + name + "'"
                    cursor.execute(sql)
                    connection.commit()
    finally:
        connection.close()

