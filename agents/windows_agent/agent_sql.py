import sqlite3, time
import agent_settings


class AgentSQL():
    def sql_con():
        database = agent_settings.application_path + "agent_sqlite.db"
        con = sqlite3.connect(database, isolation_level=None)
        return con

    def create_tables():
        sql_create_agent_data = """CREATE TABLE IF NOT EXISTS AgentData (
        time integer,name text,monitor text,value integer,sent integer);"""
 
        sql_create_agent_events = """CREATE TABLE IF NOT EXISTS AgentEvents (
        time integer,name text,message text,status integer,severity text, sent integer);"""

        sql_create_agent_thresholds = """CREATE TABLE IF NOT EXISTS AgentThresholds (
        monitor text,severity text,threshold text, compare text,duration integer);"""

        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_create_agent_data)
            c.execute(sql_create_agent_events)
            c.execute(sql_create_agent_thresholds)
        con.commit()
        con.close()

    def delete_thresholds():
        sql_query = "DELETE FROM AgentThresholds"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def insert_thresholds(monitor, severity, threshold, compare, duration):
        sql_query = "INSERT INTO AgentThresholds(monitor, severity, threshold, compare, duration) VALUES('" + monitor + "','" + severity + "'," + threshold + ",'" + compare +  "'," + duration + ")"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def select_thresholds():
        output = ""
        sql_query = "SELECT monitor, severity, threshold, compare, duration FROM AgentThresholds"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
            rows = c.fetchall()
        con.commit()
        con.close()
        return rows

    def insert_agentdata(time, name, monitor, value):
        sql_query = "INSERT INTO AgentData(time, name, monitor, value, sent) VALUES(" + time + ",'" + name + "','" + monitor + "','" + value +  "',0)"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def select_agent_data():
        output = ""
        sql_query = "SELECT time, name, monitor, value FROM AgentData WHERE sent=0"
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
    
    def select_agent_data_events(time, monitor):
        sql_query = "SELECT value FROM AgentData WHERE monitor='" + monitor + "' AND time > " + str(time) 
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
            rows = c.fetchall()
        con.commit()
        con.close()
        return rows

    def update_agent_data():
        sql_query = "UPDATE AgentData SET sent=1 WHERE sent=0"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def delete_agent_data():
        agent_time = str(time.time()-604800).split('.')[0]
        sql_query = "DELETE FROM AgentData WHERE time<" + agent_time
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def insert_agent_event(time, name, message, severity):
        sql_query = "INSERT INTO AgentEvents(time, name, message, status, severity, sent) VALUES('" + str(time) + "','" + name + "','" + message + "',1,'" + severity + "',0)"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def select_agent_event(message, severity):
        sql_query = "SELECT message FROM AgentEvents WHERE message='" + message + "' AND severity = '" + severity + "' AND status = 1" 
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
            message = c.fetchone()
        con.commit()
        con.close()
        return message

    def close_agent_event(message, severity):
        sql_query = "UPDATE AgentData SET status=0, sent=0 WHERE message='" + message + "' AND severity = '" + severity 
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
            message = c.fetchone()
        con.commit()
        con.close()

    def select_open_agent_events():
        output = ""
        sql_query = "SELECT time, name, message, status, severity FROM AgentEvents WHERE status = 1 AND sent = 0" 
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
            rows = c.fetchall()
            for time, name, message, status, severity in rows:
                output = output + str(time) + ";" + name + ";" + message + ";" + str(status) + ";" + severity + "\n"
        con.commit()
        con.close()
        return output

    def update_agent_events():
        sql_query = "UPDATE AgentEvents SET sent=1 WHERE sent=0"
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()

    def delete_agent_events():
        agent_time = str(time.time()-604800).split('.')[0]
        sql_query = "DELETE FROM AgentEvents WHERE time<" + agent_time
        con = AgentSQL.sql_con()
        if con is not None:
            c = con.cursor()
            c.execute(sql_query)
        con.commit()
        con.close()
