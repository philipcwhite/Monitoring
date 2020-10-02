import pymysql.cursors

# Database settings
host = 'localhost'
instance = 'monitoring'
user = 'monitoring'
password = 'monitoring'

class Data:

    def __init__(self):
        from web.server import app_vars
        self.con = pymysql.connect(host = host, user = user, password = password, db = instance, charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def web_auth(self, username, encrypt_password):
        sql = "SELECT username, password from users where username=%s AND password=%s"
        self.cursor.execute(sql, (username, encrypt_password))
        result = self.cursor.fetchone()
        qname = ''
        if not result is None:
            qname = result['username']
            return qname
        
    def change_password(self, username, password):
        sql = "UPDATE users SET password=%s WHERE username=%s"
        self.cursor.execute(sql, (password, username))
        self.con.commit()

    def index_device_avail(self):
        sql = "SELECT timestamp from agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def event_totals(self, status):
        sql = "SELECT severity, count(severity) as total from agentevents WHERE status=%s group by severity"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result
        
    def device_system(self, name):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name=%s LIMIT 1"
        self.cursor.execute(sql, (name))
        result = self.cursor.fetchone()
        return result
        
    def device_system_names(self):
        sql = "SELECT name FROM agentsystem ORDER by name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def device_system_search(self, name):
        sql = f"SELECT name FROM agentsystem WHERE name LIKE '%{name}%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def device_data_latest(self, name):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=%s and timestamp = (SELECT timestamp from agentdata where name=%s order by id desc LIMIT 1)"
        self.cursor.execute(sql, (name, name))
        result = self.cursor.fetchall()
        return result
        
    def device_filesystem(self, name, monitor):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=%s and monitor=%s order by id desc LIMIT 1"
        self.cursor.execute(sql, (name, monitor))
        result = self.cursor.fetchone()
        return result
        
    def device_graph(self, name, monitor):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=%s and monitor=%s order by id desc LIMIT 61"
        self.cursor.execute(sql, (name, monitor))
        result = self.cursor.fetchall()
        return result
        
    def device_all(self):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def index_devices(self, page_start, page_end):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT %s,%s"
        self.cursor.execute(sql, (page_start, page_end))
        result = self.cursor.fetchall()
        return result
            
    def index_device_count(self):
        sql = "SELECT COUNT(id) as total FROM agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    def events(self, status):
        sql = "SELECT id, timestamp, name, monitor, message, severity from agentevents where status=%s order by id desc"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result
        
    def change_event_status(self, id, status):
        sql = "UPDATE agentevents SET status=%s where id=%s"
        self.cursor.execute(sql, (status, id))
        self.con.commit()
        
    def select_notifyrules(self):
        sql = "SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule order by notify_name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def select_notifyrule(self, id):
        sql = "SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule WHERE id=%s order by notify_name"
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def insert_notifyrules(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "INSERT INTO notifyrule (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled))
        self.con.commit()
        
    def update_notifyrules(self, id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "UPDATE notifyrule SET notify_name=%s, notify_email=%s, agent_name=%s, agent_monitor=%s, agent_status=%s, agent_severity=%s, notify_enabled=%s WHERE id=%s"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled, id))
        self.con.commit()
        
    def delete_notify_rule(self, id):
        sql = "DELETE FROM notifyrule where id=%s"
        self.cursor.execute(sql, (id))
        self.con.commit()
        
    def select_users(self):
        sql = "SELECT id, username FROM users order by username" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def select_user(self, id):
        sql = "SELECT id, username, role FROM users WHERE id=%s" 
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def create_user(self, username, encrypt_pass, role):
        sql = "INSERT INTO users (username, password, role) SELECT %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE username=%s) LIMIT 1"
        self.cursor.execute(sql, (username, encrypt_pass, role, username))
        self.con.commit()
        
    def edit_user_role(self, id, role):
        sql = "UPDATE users set role=%s where id=%s"
        self.cursor.execute(sql, (role, id))
        self.con.commit()
        
    def edit_user_password(self, id, encrypt_pass):
        sql = "UPDATE users set password=%s where id=%s"
        self.cursor.execute(sql, (encrypt_pass, id))
        self.con.commit()
        
    def delete_user(self, id):
        sql = "DELETE FROM users where id=%s"
        self.cursor.execute(sql, (id))
        self.con.commit()
