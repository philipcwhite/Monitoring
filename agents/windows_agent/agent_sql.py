import sqlite3, time
import agent_settings

class AgentSQL():
    def sql_con():
        try:
            database = agent_settings.application_path + "agent_sqlite.db"
            con = sqlite3.connect(database, isolation_level=None)
            return con
        except:
            pass

    def create_tables():
        try:
            sql_create_agent_data = r"CREATE TABLE IF NOT EXISTS AgentData (time integer,name text,monitor text,value integer,sent integer);" 
            sql_create_agent_events = r"CREATE TABLE IF NOT EXISTS AgentEvents (time integer,name text,monitor text,message text,status integer,severity integer, sent integer);"
            sql_create_agent_thresholds = r"CREATE TABLE IF NOT EXISTS AgentThresholds (monitor text,severity text,threshold integer, compare text,duration integer);"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_create_agent_data)
                c.execute(sql_create_agent_events)
                c.execute(sql_create_agent_thresholds)
            con.commit()
            con.close()
        except:
            pass

    def delete_thresholds():
        try:
            sql_query = r"DELETE FROM AgentThresholds"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def insert_thresholds(monitor, severity, threshold, compare, duration):
        try:
            sql_query = r"INSERT INTO AgentThresholds(monitor, severity, threshold, compare, duration) VALUES('" + monitor + "'," + severity + "," + threshold + ",'" + compare +  "'," + duration + ")"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def select_thresholds():
        try:
            output = ""
            sql_query = r"SELECT monitor, severity, threshold, compare, duration FROM AgentThresholds"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
                rows = c.fetchall()
            con.commit()
            con.close()
            return rows
        except:
            pass

    def insert_agentdata(time, name, monitor, value):
        try:
            sql_query = r"INSERT INTO AgentData(time, name, monitor, value, sent) VALUES(" + time + ",'" + name + "','" + monitor + "','" + value +  "',0)"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def select_agent_data():
        try:
            output = ""
            sql_query = r"SELECT time, name, monitor, value FROM AgentData WHERE sent=0 AND monitor NOT LIKE '%perf.service%'"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
                rows = c.fetchall()
                for time, name, monitor, value in rows:
                    output = output + str(time) + ";" + name + ";" + monitor + ";" + str(value) + "\n"
            con.commit()
            con.close()
            return output
        except:
            pass
    
    def select_agent_data_events(time, monitor):
        try:
            sql_query = r"SELECT value FROM AgentData WHERE monitor='" + monitor + "' AND time > " + str(time) 
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
                rows = c.fetchall()
            con.commit()
            con.close()
            return rows
        except:
            pass

    def update_agent_data():
        try:
            sql_query = r"UPDATE AgentData SET sent=1 WHERE sent=0"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def delete_agent_data():
        try:
            agent_time = str(time.time()-604800).split('.')[0]
            sql_query = r"DELETE FROM AgentData WHERE time<" + agent_time
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def insert_agent_event(time, name, monitor, message, severity):
        try:
            sql_query = r"""UPDATE AgentEvents SET time=""" + str(time) + """, message='""" + message + """', severity=""" + str(severity) + """, sent=0 WHERE monitor='""" + monitor + """' AND """ + str(severity) + """ > 
            (SELECT MAX(severity) FROM AgentEvents WHERE monitor='""" + monitor + """' AND status=1)"""
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()

            sql_query = r"""INSERT INTO AgentEvents(time, name, monitor, message, status, severity, sent) SELECT """ + str(time) + ",'" + name + "','" + monitor + "','" + message + "',1," + str(severity) + """,0
            WHERE NOT EXISTS(SELECT 1 FROM AgentEvents WHERE monitor='""" + monitor + """' AND status=1)"""
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass
    
    def select_agent_event(monitor):
        try:
            sql_query = r"SELECT monitor FROM AgentEvents WHERE monitor='" + monitor + "' AND status = 1" 
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
                monitor = c.fetchone()
            con.commit()
            con.close()
            return monitor
        except:
            pass

    def close_agent_event(monitor, severity):
        try:
            sql_query =  r"UPDATE AgentEvents SET status=0, sent=0 WHERE monitor='" + monitor + "' AND severity = " + severity 
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def select_open_agent_events():
        try:
            output = ""
            sql_query = r"SELECT time, name, monitor, message, status, severity FROM AgentEvents WHERE sent = 0" 
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
                rows = c.fetchall()
                for time, name, monitor, message, status, severity in rows:
                    output = output + str(time) + ";" + name + ";event;" +monitor + ";" + message + ";" + str(status) + ";" + str(severity) + "\n"
            con.commit()
            con.close()
            return output
        except:
            pass

    def update_agent_events():
        try:
            sql_query = r"UPDATE AgentEvents SET sent=1 WHERE sent=0"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass

    def delete_agent_events():
        try:
            sql_query = r"DELETE FROM AgentEvents WHERE status=0 AND sent=1"
            con = AgentSQL.sql_con()
            if con is not None:
                c = con.cursor()
                c.execute(sql_query)
            con.commit()
            con.close()
        except:
            pass
