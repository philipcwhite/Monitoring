import asyncio, configparser, json, os, ssl, time, sqlite3

class CollectSettings:
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
    cert_path = './certificates/'
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
            CollectSettings.secure = eval(server['secure'])
            CollectSettings.passphrase = server['passphrase']
            CollectSettings.cert_key = certificates['key']
            CollectSettings.cert_name = certificates['name']
        except: pass
      
class CollectData:

    def __init__(self):
        self.con = sqlite3.connect('/opt/monitoring/server/database/flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def agent_system(self, timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory):
        print(timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory)
        sql = "SELECT name FROM agentsystem where name=?;"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        qname = ""
        print("name=", name, "result=", result)
        if result != None:
            qname = result[0]
            if name == qname:
                sql = "UPDATE agentsystem SET timestamp=?, domain=?, ipaddress=?, platform=?, build=?, architecture=?, processors=?, memory=? WHERE name=?"
                self.cursor.execute(sql, (timestamp, domain, ipaddress, platform, build, architecture, processors, memory, name))
                self.con.commit()
        else:
            sql = "INSERT INTO agentsystem (timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory) VALUES(?,?,?,?,?,?,?,?,?)"
            self.cursor.execute(sql, (timestamp, name, domain, ipaddress, platform, build, architecture, processors, memory))
            self.con.commit()

    def agent_data(self, values):
        sql = f"INSERT INTO agentdata (timestamp, name, monitor, value) VALUES {values}"
        self.cursor.execute(sql)
        self.con.commit()  

    def agent_events_open(self, timestamp, name, monitor, message, status, severity):
        sql = "INSERT INTO agentevents (timestamp, name, monitor, message, status, severity, processed) VALUES(?,?,?,?,?,?,?)"
        self.cursor.execute(sql, (timestamp, name, monitor, message, status, severity, 0))
        self.con.commit()

    def agent_events_close(self, name, monitor, severity):
        sql = "UPDATE agentevents SET status=0 AND processed=0 WHERE name=? AND monitor=? AND severity=? AND status=1"
        self.cursor.execute(sql, (name, monitor, severity))
        self.con.commit()

class CollectParse:
    def parse_data(message):
        CD = CollectData()
        message = json.loads(message)
        #print(message)
        passphrase = message["passphrase"]
        agentdata = ''
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
            CD.agent_system(timestamp, name, domain, ipaddress, platform, build, architecture, int(processors), float(memory))
            for i in message["data"]:
                agentdata += f"({str(i[list(i)[0]])},'{name}','{list(i)[1]}',{str(i[list(i)[1]])}),"
            for i in message["events"]:
                timestamp = i["time"]
                name = name
                monitor = i["monitor"]
                message = i["message"]
                status = i["status"]
                severity = i["severity"]
                if int(status) == 1:
                    CD.agent_events_open(timestamp, name, monitor, message, status, severity)
                elif int(status) == 0:
                    CD.agent_events_close(name, monitor, severity)
            CD.agent_data(agentdata[:-1])


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if CollectSettings.running == 0:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(loop.stop)
        message = data.decode()
        CollectParse.parse_data(message)
        self.transport.write(b'Received')
        self.transport.close()

class CollectServer():
    async def connection_loop():
        loop = asyncio.get_running_loop()
        if CollectSettings.secure == True:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.options |= ssl.PROTOCOL_TLSv1_2
            ssl_context.load_cert_chain(certfile = CollectSettings.cert_path + CollectSettings.cert_name, keyfile = CollectSettings.cert_path + CollectSettings.cert_key)
            server = await loop.create_server(lambda: EchoServerProtocol(), CollectSettings.server, CollectSettings.port, ssl=ssl_context)
        else: server = await loop.create_server(lambda: EchoServerProtocol(), CollectSettings.server, CollectSettings.port)
        async with server: await server.serve_forever()

def start_server():
    CollectLoad.load_config()
    try: asyncio.run(CollectServer.connection_loop())
    except: pass

start_server()
