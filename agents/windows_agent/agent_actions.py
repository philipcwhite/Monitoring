import asyncio
import socket
import agent_wmi
import agent_settings
import ssl

class agent_process():

    async def get_data():
        message = await agent_wmi.AgentWMI.get_wmi()
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
                #print(data)
                if data == 'Received':
                    agent_settings.agent_list = []
                #print(agent_settings.agent_list)
                conn.close()
            else:
                sock.connect((host,port))
                byte=str(message).encode()
                sock.send(byte)
                data = sock.recv(1024)
                #print(data.decode())
                sock.close()
        except:
            #print(agent_settings.agent_list)
            pass

        
        #data = s.recv(1024)
        #print(data.decode())


    def create_loop():
        loop = asyncio.new_event_loop() 
        loop.run_until_complete(agent_process.send_data())
        loop.close 

