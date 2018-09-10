import asyncio
import socket
import agent_settings, agent_sql, agent_data, agent_event
import ssl

class AgentProcess():
    async def send_data(message):
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
                    agent_sql.AgentSQL.update_agent_data()
                    agent_sql.AgentSQL.update_agent_events()
                conn.close()
            else:
                sock.connect((host,port))
                byte=str(message).encode()
                sock.send(byte)
                data = sock.recv(1024)
                if data == 'Received':
                    agent_sql.AgentSQL.update_agent_data() 
                    agent_sql.AgentSQL.update_agent_events()
                sock.close()
        except:
            pass

    async def run_process():
        send_message = agent_data.AgentData.data_process()
        event_message = agent_event.AgentEvent.event_process()
        message = send_message + event_message
        await AgentProcess.send_data(message)
        agent_sql.AgentSQL.delete_agent_data()
        agent_sql.AgentSQL.delete_agent_events()

    def create_loop():
        loop = asyncio.new_event_loop() 
        loop.run_until_complete(AgentProcess.run_process())
        loop.close 






