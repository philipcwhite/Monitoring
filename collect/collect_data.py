import pymysql.cursors
import collect_settings

def mon_con():
    connection = pymysql.connect(host = collect_settings.dbhost,
                                 user = collect_settings.dbuser,
                                 password = collect_settings.dbpassword,
                                 db = collect_settings.database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    return connection

def parse_data(message):
    timestamp = 0
    name = '' 
    domain = '' 
    ipaddress = '' 
    platform = '' 
    buildnumber = '' 
    architecture = '' 
    processors = 0 
    memory = 0

    for i in message.splitlines():
        if 'conf.ipaddress' in i:
            line = i.split(';')
            timestamp = line[0]
            name = line[1]
            ipaddress = line[3]
        if 'conf.os.name' in i:
            line = i.split(';')
            platform = line[3]
        if 'conf.os.build' in i:
            line = i.split(';')
            buildnumber = line[3]
        if 'conf.os.architecture' in i:
            line = i.split(';')
            architecture = line[3]
        if 'conf.domain' in i:
            line = i.split(';')
            domain = line[3]
        if 'conf.processors' in i:
            line = i.split(';')
            processors = line[3]
        if 'conf.memory.total' in i:
            line = i.split(';')
            memory = line[3]

    agent_system(timestamp, name, domain, ipaddress, platform, buildnumber, architecture, processors, memory)

    for i in message.splitlines():
        if ';perf' in i and i.count(";") == 3:
            line = i.split(';')
            timestamp = line[0]
            name = line[1]
            monitor = line[2]
            value = float(line[3])
            agent_data(timestamp, name, monitor, value)

    for i in message.splitlines():
        if ';event;' in i:
            line = i.split(';')
            timestamp = line[0]
            name = line[1]
            monitor = line[3]
            message = line[4]
            status = line[5]
            severity = line[6]
            if int(status) == 1:
                agent_events_open(timestamp, name, monitor, message, status, severity)
            elif int(status) == 0:
                agent_events_close(name, monitor, severity)

        

def agent_system(timestamp, name, domain, ipaddress, platform, buildnumber, architecture, processors, memory):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM agentsystem where name=%s"
            cursor.execute(sql, (name))
            result = cursor.fetchone()
            qname = ""
            
            if not result is None:
                qname = result['name']
            if name == qname:
                sql = "UPDATE agentsystem SET timestamp=%s, domain=%s, ipaddress=%s, platform=%s, buildnumber=%s, architecture=%s, processors=%s, memory=%s WHERE name=%s"
                cursor.execute(sql, (timestamp, domain, ipaddress, platform, buildnumber, architecture, processors, memory, name))
                connection.commit()
            else:
                sql = "INSERT INTO agentsystem (timestamp, name, domain, ipaddress, platform, buildnumber, architecture, processors, memory) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (timestamp, name, domain, ipaddress, platform, buildnumber, architecture, processors, memory))
                connection.commit()
 
    finally:
        connection.close()

def agent_data(timestamp, name, monitor, value):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO agentdata (timestamp, name, monitor, value) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (timestamp, name, monitor, value))
            connection.commit()
 
    finally:
        connection.close()

def agent_events_open(timestamp, name, monitor, message, status, severity):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO agentevent (timestamp, name, monitor, message, status, severity, processed) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (timestamp, name, monitor, message, status, severity, 0))
            connection.commit()
    finally:
        connection.close()

def agent_events_close(name, monitor, severity):
    connection = mon_con()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE agentevent SET status=0 AND processed=0 WHERE name=%s AND monitor=%s AND severity=%s AND status=1"
            cursor.execute(sql, (name, monitor, severity))
            connection.commit()
    finally:
        connection.close()