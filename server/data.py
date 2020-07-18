import pymysql.cursors

# Database settings
host = 'localhost'
instance = 'monitoring'
user = 'monitoring'
password = 'monitoring'

class Data:
    '''def __init__(self):
        print(settings.db_user, 3)
        self.con = pymysql.connect(host = 'localhost', user = 'monitoring', password = 'monitoring', db = 'monitoring', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()'''

    def __init__(self):
        from web.server import app_vars
        self.con = pymysql.connect(host = host, user = user, password = password, db = instance, charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def web_auth(self, username, encrypt_password):
        sql = r"SELECT username, password from users where username=%s AND password=%s"
        self.cursor.execute(sql, (username, encrypt_password))
        result = self.cursor.fetchone()
        qname = ""
        if not result is None:
            qname = result['username']
            return qname
        
    def web_change_password(self, username, password):
        sql = r"UPDATE users SET password='" + str(password) + "' WHERE username='" + str(username) + "'"
        self.cursor.execute(sql)
        self.con.commit()

    def web_code_index_device_avail(self):
        sql = r"SELECT timestamp from agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_event_totals(self, status):
        sql = r"SELECT severity, count(severity) as total from agentevents WHERE status=" + str(status) + r" group by severity"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_device_system(self, name):
        sql = r"SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name='" + name +"' LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def web_code_device_system_names(self):
        sql = r"SELECT name FROM agentsystem ORDER by name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_device_system_search(self, name):
        sql = r"SELECT name FROM agentsystem WHERE name LIKE '%" + name + r"%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_device_data_latest(self, name):
        sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and timestamp = (SELECT timestamp from agentdata where name='" + name + "' order by id desc LIMIT 1)"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_device_filesystem(self, name, monitor):
        sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and monitor='" + monitor + "' order by id desc LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def web_code_device_graph(self, name, monitor):
        sql = r"SELECT id, timestamp, name, monitor, value from agentdata where name='" + name + r"' and monitor='" + monitor + "' order by id desc LIMIT 61"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_device_all(self):
        sql = r"SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_index_devices(self, page_start, page_end):
        sql = r"SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT " + str(page_start) + "," + str(page_end)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def web_code_index_device_count(self):
        sql = r"SELECT COUNT(id) as total FROM agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def web_code_events(self, status):
        sql = r"SELECT id, timestamp, name, monitor, message, severity from agentevents where status=" + str(status) + r" order by id desc"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_change_event_status(self, id, status):
        sql = r"UPDATE agentevents SET status=" + str(status) + r" where id=" + str(id)
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_select_notifyrules(self):
        sql = r"SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule order by notify_name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def web_code_select_notifyrule(self, id):
        sql = r"SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule WHERE id=" + str(id) + " order by notify_name"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def web_code_insert_notifyrules(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = r"INSERT INTO notifyrule (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled) VALUES ('" + notify_name + "','" + notify_email + "','" + agent_name + "','" + agent_monitor + "'," + str(agent_status) + "," + str(agent_severity) + "," + str(notify_enabled) + ")"
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_update_notifyrules(self, id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = r"UPDATE notifyrule SET notify_name='" + notify_name + "',notify_email='" + notify_email + "',agent_name='" + agent_name + "',agent_monitor='" + agent_monitor + "',agent_status=" + str(agent_status) + ",agent_severity=" + str(agent_severity) + ",notify_enabled=" + str(notify_enabled)
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_delete_notify_rule(self, id):
        sql = r"DELETE FROM notifyrule where id=" + str(id)
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_select_users(self):
        sql = r"SELECT id, username FROM users order by username" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def web_code_select_user(self, id):
        sql = r"SELECT id, username, role FROM users WHERE id=" + str(id) 
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def web_code_create_user(self, username, encrypt_pass, role):
        sql = r"INSERT INTO users (username, password, role) SELECT '" + username + "', '" + encrypt_pass + "', " + str(role)  + " FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE username='" + username + "') LIMIT 1"
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_edit_user_role(self, id, role):
        sql = r"UPDATE users set role=" + str(role) + " where id=" + str(id)
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_edit_user_password(self, id, encrypt_pass):
        sql = r"UPDATE users set password=" + str(encrypt_pass) + " where id=" + str(id)
        self.cursor.execute(sql)
        self.con.commit()
        
    def web_code_delete_user(self, id):
        sql = r"DELETE FROM users where id=" + str(id)
        self.cursor.execute(sql)
        self.con.commit()