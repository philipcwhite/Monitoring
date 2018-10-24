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

    def web_change_password(username, password):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE users SET password='" + str(password) + "' WHERE username='" + str(username) + "'"
                cursor.execute(sql)
                connection.commit()
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

    def web_code_device_system_names():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT name FROM agentsystem ORDER by name"
                cursor.execute(sql)
                result = cursor.fetchall()
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

    def web_code_select_notifyrules():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule order by notify_name"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    
    def web_code_select_notifyrule(id):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule WHERE id=" + str(id) + " order by notify_name"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_insert_notifyrules(notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"INSERT INTO notifyrule (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled) VALUES ('" + notify_name + "','" + notify_email + "','" + agent_name + "','" + agent_monitor + "'," + str(agent_status) + "," + str(agent_severity) + "," + str(notify_enabled) + ")"
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_update_notifyrules(id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE notifyrule SET notify_name='" + notify_name + "',notify_email='" + notify_email + "',agent_name='" + agent_name + "',agent_monitor='" + agent_monitor + "',agent_status=" + str(agent_status) + ",agent_severity=" + str(agent_severity) + ",notify_enabled=" + str(notify_enabled)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_delete_notify_rule(id):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"DELETE FROM notifyrule where id=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_select_users():
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, username FROM users order by username" 
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def web_code_select_user(id):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"SELECT id, username, role FROM users WHERE id=" + str(id) 
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def web_code_create_user(username, encrypt_pass, role):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"INSERT INTO users (username, password, role) SELECT '" + username + "', '" + encrypt_pass + "', " + str(role)  + " FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE username='" + username + "') LIMIT 1"
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_edit_user_role(id, role):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE users set role=" + str(role) + " where id=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_edit_user_password(id, encrypt_pass):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"UPDATE users set password=" + str(encrypt_pass) + " where id=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()

    def web_code_delete_user(id):
        connection = WebData.web_con()
        try:
            with connection.cursor() as cursor:
                sql = r"DELETE FROM users where id=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally:
            connection.close()    
