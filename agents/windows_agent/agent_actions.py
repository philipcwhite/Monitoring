import asyncio
import socket
import agent_collect, agent_settings, agent_sql
import ssl

class agent_process():
    async def data_cleanup():
        await agent_sql.AgentSQL.delete_agent_data()
        return None

    async def get_data():
        message = await agent_collect.AgentCollect.get_data()
        return message

    async def send_data():
        message = await agent_process.get_data()
        host = agent_settings.server
        port = agent_settings.port
        agent_ssl = int(agent_settings.secure)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            if agent_ssl == 1:
                #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='localhost.crt')
                context = ssl.create_default_context()
                context.options |= ssl.PROTOCOL_TLSv1_2
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                conn = context.wrap_socket(sock, server_hostname=host)
                conn.connect((host,port))
                byte=str(message).encode()
                conn.send(byte)
                data = conn.recv(1024).decode()
                # Mark data as sent 
                if data == 'Received':
                    await agent_sql.AgentSQL.update_agent_data()
                conn.close()
            else:
                sock.connect((host,port))
                byte=str(message).encode()
                sock.send(byte)
                data = sock.recv(1024)
                if data == 'Received':
                    await agent_sql.AgentSQL.update_agent_data() 
                sock.close()
        except:
            pass

    async def run_process():
        await agent_process.send_data()
        await agent_process.data_cleanup()

    def create_loop():
        loop = asyncio.new_event_loop() 
        loop.run_until_complete(agent_process.run_process())
        loop.close 

