import asyncio, configparser, json, os, ssl, time, pymysql.cursors

class CollectSettings:
    app_path = './'
    server = "0.0.0.0"
    port = 8888
    secure = False
    running = 1
    dbhost = 'localhost'
    dbuser = 'monitoring'
    dbpassword = 'monitoring'
    database = 'monitoring'
    cert_name = 'localhost.crt'
    cert_key = 'localhost.pem'
    passphrase = 'secure_monitoring'

class CollectLoad:
    def load_config():
        try:
            CollectSettings.running = 1 
            parser = configparser.ConfigParser()
            parser.read(CollectSettings.app_path + 'settings.ini')
            certificates = dict(parser.items('certificates'))
            database = dict(parser.items('database'))
            server = dict(parser.items('server'))
            CollectSettings.port = int(server['port_collect'])
            CollectSettings.secure = server['secure']
            CollectSettings.passphrase = server['passphrase']
            CollectSettings.cert_key = certificates['key']
            CollectSettings.cert_name = certificates['name']
            CollectSettings.dbhost = database['host']
            CollectSettings.database = database['name']
            CollectSettings.dbuser = database['user']
            CollectSettings.dbpassword = database['password']
        except: pass
      
class CollectData:
    def mon_con():
        connection = pymysql.connect(host = CollectSettings.dbhost,
                                     user = CollectSettings.dbuser,
                                     password = CollectSettings.dbpassword,
                                     db = CollectSettings.database,
                                     charset = 'utf8mb4',
                                     cursorclass = pymysql.cursors.DictCursor)
        return connection

    def agent_system(timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory):
        connection = CollectData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT name FROM agentsystem where name=%s"
                cursor.execute(sql, (name))
                result = cursor.fetchone()
                qname = ""            
                if not result is None:
                    qname = result['name']
                if name == qname:
                    sql = "UPDATE agentsystem SET timestamp=%s, domain=%s, ipaddress=%s, platform=%s, build=%s, architecture=%s, processors=%s, memory=%s WHERE name=%s"
                    cursor.execute(sql, (timestamp, domain, ipaddress, platform, build, architecture, processors, memory, name))
                    connection.commit()
                else:
                    sql = "INSERT INTO agentsystem (timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory))
                    connection.commit()
        finally: connection.close()

    def agent_data(timestamp, name, monitor, value):
        connection = CollectData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO agentdata (timestamp, name, monitor, value) VALUES(%s,%s,%s,%s)"
                cursor.execute(sql, (timestamp, name, monitor, value))
                connection.commit() 
        finally: connection.close()

    def agent_events_open(timestamp, name, monitor, message, status, severity):
        connection = CollectData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO agentevents (timestamp, name, monitor, message, status, severity, processed) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (timestamp, name, monitor, message, status, severity, 0))
                connection.commit()
        finally: connection.close()

    def agent_events_close(name, monitor, severity):
        connection = CollectData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE agentevents SET status=0 AND processed=0 WHERE name=%s AND monitor=%s AND severity=%s AND status=1"
                cursor.execute(sql, (name, monitor, severity))
                connection.commit()
        finally: connection.close()

    def parse_data(message):
        try:
            message = json.loads(message)
            #print(message)
            passphrase = message["passphrase"]
            if CollectSettings.passphrase == passphrase:
                timestamp = message["time"]
                name = message["name"]
                domain = message["domain"]
                ipaddress = message["ip"]
                platform = message["platform"]
                build = message["build"] 
                architecture = message["arch"] 
                processors = message["procs"]
                memory = message["memory"] 
                CollectData.agent_system(timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory)
                for i in message["data"]:
                    CollectData.agent_data(i["time"], name, i["monitor"], i["value"])
                for i in message["events"]:
                    timestamp = i["time"]
                    name = name
                    monitor = i["monitor"]
                    message = i["message"]
                    status = i["status"]
                    severity = i["severity"]
                    if int(status) == 1:
                        CollectData.agent_events_open(timestamp, name, monitor, message, status, severity)
                    elif int(status) == 0:
                        CollectData.agent_events_close(name, monitor, severity)
        except:pass

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if CollectSettings.running == 0:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(loop.stop)
        message = data.decode()
        CollectData.parse_data(message)
        self.transport.write(b'Received')
        self.transport.close()

class CollectServer():
    async def connection_loop():
        loop = asyncio.get_running_loop()
        if CollectSettings.secure == True:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.options |= ssl.PROTOCOL_TLSv1_2
            ssl_context.load_cert_chain(certfile = CollectSettings.app_path + 'certificates\\' + CollectSettings.cert_name, keyfile = CollectSettings.app_path + 'certificates\\' + CollectSettings.cert_key)
            server = await loop.create_server(lambda: EchoServerClientProtocol(), CollectSettings.server, CollectSettings.port, ssl=ssl_context)
        else: server = await loop.create_server(lambda: EchoServerClientProtocol(), CollectSettings.server, CollectSettings.port)
        async with server: await server.serve_forever()

def start_server():
    CollectLoad.load_config()
    try: asyncio.run(CollectServer.connection_loop())
    except: pass
