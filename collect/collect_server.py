import asyncio
import ssl, time
import collect_load, collect_data, collect_settings

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        #peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        if collect_settings.running == 0:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(loop.stop)
        message = data.decode()
        print(message)
        collect_data.parse_data(message)
        self.transport.write(b'Received')
        self.transport.close()

class CollectServer():
    async def connection_loop():
        loop = asyncio.get_running_loop()
        if collect_settings.secure == 1:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.options |= ssl.PROTOCOL_TLSv1_2
            ssl_context.load_cert_chain(certfile = collect_settings.application_path + "localhost.crt", keyfile = collect_settings.application_path + "localhost.pem")
            server = await loop.create_server(lambda: EchoServerClientProtocol(), collect_settings.server, collect_settings.port, ssl=ssl_context)
        else:
            server = await loop.create_server(lambda: EchoServerClientProtocol(), collect_settings.server, collect_settings.port)
        async with server: await server.serve_forever()

    def server_start():
        collect_load.load_config()
        try:
            asyncio.run(CollectServer.connection_loop())
        except:
            pass


#CollectServer.server_start()