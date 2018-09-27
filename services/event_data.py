import pymysql.cursors
import event_settings

def agent_events_processed():
    connection = pymysql.connect(host = event_settings.dbhost,
                                 user = event_settings.dbuser,
                                 password = event_settings.dbpassword,
                                 db = event_settings.database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE mon_app_agentevent SET processed=1"
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

def agent_filter_select():

    connection = pymysql.connect(host = event_settings.dbhost,
                                 user = event_settings.dbuser,
                                 password = event_settings.dbpassword,
                                 db = event_settings.database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = """select t1.notify_email, t1.notify_name, t2.id, t2.name, t2.monitor, t2.message, t2.severity, t2.status FROM mon_app_notifyrule as t1 
                  INNER JOIN mon_app_agentevent as t2 on 
                  t2.name LIKE t1.agent_name AND t2.monitor LIKE t1.agent_monitor AND t2.message LIKE t1.agent_message
                  AND t2.status LIKE t1.agent_status AND t2.severity LIKE t1.agent_severity AND t2.processed=0"""
            cursor.execute(sql)
            result = cursor.fetchall()
            agent_events_processed()
            return result
    finally:
        connection.close()

#print(str(agent_filter_select()))