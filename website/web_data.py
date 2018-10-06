import cherrypy
import pymysql.cursors

class WebData:
    def web_con():
        connection = pymysql.connect(host = cherrypy.request.app.config['database']['host'],
                                     user = cherrypy.request.app.config['database']['user'],
                                     password = cherrypy.request.app.config['database']['passwd'],
                                     db = cherrypy.request.app.config['database']['db'],
                                     charset = 'utf8mb4',
                                     cursorclass = pymysql.cursors.DictCursor)
        return connection

    def web_auth(username, encrypt_password):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT username, password from users where username=%s AND password=%s"
                cursor.execute(sql, (username,encrypt_password))
                result = cursor.fetchone()
                qname = ""
                if not result is None:
                    qname = result['username']
                    return qname
        finally:
            connection.close()

    def web_code_index_device_avail():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT timestamp from agentsystem"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_event_totals(status):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT severity, count(severity) as total from agentevents WHERE status=" + str(status) + r" group by severity"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_system(name):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, ipaddress, platform, buildnumber, architecture, domain, processors, memory FROM agentsystem WHERE name='" + name +"' LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_device_system_search(name):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT name FROM agentsystem WHERE name LIKE '%" + name + r"%'"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_data_latest(name):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and timestamp = (SELECT timestamp from agentdata where name='" + name + "' order by id desc LIMIT 1)"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_filesystem(name, monitor):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and monitor='" + monitor + "' order by id desc LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_device_graph(name, monitor):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and monitor='" + monitor + "' order by id desc LIMIT 61"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_all():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, ipaddress, platform, buildnumber, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_index_devices(page_start, page_end):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, ipaddress, platform, buildnumber, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT " + str(page_start) + "," + str(page_end)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    
    def web_code_index_device_count():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT COUNT(id) as total FROM agentsystem"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_events(status):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, message, severity from agentevents where status=" + str(status) + r" order by id desc"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_change_event_status(id, status):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE agentevents SET status=" + str(status) + r" where id=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()