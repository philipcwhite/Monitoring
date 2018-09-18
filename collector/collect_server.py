import asyncio
import ssl
import collect_data, collect_settings

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        #print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        #print('Data Received: ' + '\n' + str(message))
        collect_data.parse_data(message)

        #print('Send: {!r}'.format('Received'))
        self.transport.write(b'Received')

        #print('Close the client socket')
        self.transport.close()

class CollectServer():
    def connection_loop():
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.options |= ssl.PROTOCOL_TLSv1_2
        ssl_context.load_cert_chain(certfile = collect_settings.application_path + "localhost.crt", keyfile = collect_settings.application_path + "localhost.pem")
        loop = asyncio.new_event_loop()
        coro = loop.create_server(EchoServerClientProtocol, collect_settings.server, collect_settings.port, ssl=ssl_context)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        #print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

#CollectServer.connection_loop()