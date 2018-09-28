import asyncio
import ssl, time
import collect_data, collect_settings

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        collect_data.parse_data(message)
        self.transport.write(b'Received')
        self.transport.close()

class CollectServer():
    def send_close():
        try:
            collect_settings.running = 0
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            context = ssl.create_default_context()
            context.options |= ssl.PROTOCOL_TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            con = context.wrap_socket(sock, server_hostname=collect_settings.server)
            con.connect((collect_settings.server,collect_settings.port))
            byte=str("Close").encode()
            con.send(byte)
            con.close()
        except:
            pass

    def connection_loop():
        try:
            if collect_settings.secure == 1:
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.options |= ssl.PROTOCOL_TLSv1_2
                ssl_context.load_cert_chain(certfile = collect_settings.application_path + "localhost.crt", keyfile = collect_settings.application_path + "localhost.pem")
                loop = asyncio.new_event_loop()
                coro = loop.create_server(EchoServerClientProtocol, collect_settings.server, collect_settings.port, ssl=ssl_context)
                while True:
                    if collect_settings.running == 0:break
                    server = loop.run_until_complete(coro)
                    time.sleep(1)
            else:
                loop = asyncio.new_event_loop()
                coro = loop.create_server(EchoServerClientProtocol, collect_settings.server, collect_settings.port)
                while True:
                    if collect_settings.running == 0:break
                    server = loop.run_until_complete(coro)
                    time.sleep(1)
        except:
            pass

