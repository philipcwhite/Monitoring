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

    def web_code_event_totals():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT severity, count(severity) as total from agentevent WHERE status=1 group by severity"
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
                sql = r"SELECT name FROM agentsystem WHERE name LIKE '%" + name +"%'"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_data_latest(name):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + "' and timestamp = (SELECT timestamp from agentdata where name='" + name + "' order by id desc LIMIT 1)"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_device_filesystem(name, monitor):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + "' and monitor='" + monitor + "' order by id desc LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_device_graph(name, monitor):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + "' and monitor='" + monitor + "' order by id desc LIMIT 61"
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

    def web_code_open_events():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, timestamp, name, monitor, message, severity from agentevent where status=1 order by id desc"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_close_event(id):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE agentevent SET status=0 where id=" + id
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()