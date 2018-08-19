import wmi
import socket
import pythoncom
import agent_settings
import time

class AgentData():
    def __init__(self, time, host, name, value):
        self.time = time
        self.host = host
        self.name = name
        self.value = value

class AgentWMI():
    async def get_wmi():
        # Set time
        agent_time = str(time.time()).split('.')[0]
        # Initialize WMI
        pythoncom.CoInitialize()
        c = wmi.WMI()
        # Get Hostname
        hostname = socket.gethostname().lower()
        # Set Return string
        output = ""
            
        # Configuration
        try:
            for i in c.Win32_OperatingSystem():
                AData1 = AgentData(time = agent_time, host = hostname, name = 'conf.os.name', value = i.Caption)
                AData2 = AgentData(time = agent_time, host = hostname, name = 'conf.os.build', value = i.BuildNumber)
                AData3 = AgentData(time = agent_time, host = hostname, name = 'conf.os.architecture', value = i.OSArchitecture)
                agent_settings.agent_list.append(AData1)
                agent_settings.agent_list.append(AData2)
                agent_settings.agent_list.append(AData3)
        except:
            pass

        try:
            for i in c.Win32_ComputerSystem():
                TotalMemory = round(int(i.TotalPhysicalMemory) / 1024 / 1024, 0)
                AData1 = AgentData(time = agent_time, host = hostname, name = 'conf.domain', value = i.Domain)
                AData2 = AgentData(time = agent_time, host = hostname, name = 'conf.processors', value = i.NumberOfProcessors)
                AData3 = AgentData(time = agent_time, host = hostname, name = 'conf.memory.total', value = TotalMemory)
                agent_settings.agent_list.append(AData1)
                agent_settings.agent_list.append(AData2)
                agent_settings.agent_list.append(AData3)
        except:
            pass

        try:
            ipaddress = socket.gethostbyname(socket.gethostname())
            AData=AgentData(time = agent_time, host = hostname, name = 'conf.ipaddress', value = ipaddress)
            agent_settings.agent_list.append(AData)
        except:
            pass

        # Filesystem
        try:
            for i in c.Win32_PerfFormattedData_PerfDisk_LogicalDisk():
                Name = i.Name.replace(':','').lower()
                PercentFreeSpace = i.PercentFreeSpace
                ActiveTime=100 - int(i.PercentIdleTime)
                if len(Name) < 3:
                    AData1=AgentData(time = agent_time, host = hostname, name = 'perf.filesystem.' + Name + '.percent.free', value = i.PercentFreeSpace)
                    AData2=AgentData(time = agent_time, host = hostname, name = 'perf.filesystem.' + Name + '.percent.active', value = ActiveTime)
                    agent_settings.agent_list.append(AData1)
                    agent_settings.agent_list.append(AData2)
        except:
            pass

        # Memory
        try:
            for i in c.Win32_OperatingSystem():
                FreeMem = int(i.FreePhysicalMemory)
                TotalMem = int(i.TotalVisibleMemorySize)
                PercentMem = ((TotalMem-FreeMem)/TotalMem)*100
                PercentMem = round(PercentMem,2)
                AData = AgentData(time = agent_time, host = hostname, name = 'perf.memory.percent.used', value = PercentMem)
                agent_settings.agent_list.append(AData)
        except:
            pass

        # Network
        try:    
            BytesReceivedPersec = 0
            BytesSentPersec = 0
            for i in c.Win32_PerfFormattedData_Tcpip_NetworkInterface():
                BytesReceivedPersec = BytesReceivedPersec + int(i.BytesReceivedPersec)
                BytesSentPersec = BytesSentPersec + int(i.BytesSentPersec)
            BytesReceivedPersec = BytesReceivedPersec
            BytesSentPersec = BytesSentPersec
            AData1 = AgentData(time = agent_time, host = hostname, name = 'perf.network.bytes.received', value = BytesReceivedPersec)
            AData2 = AgentData(time = agent_time, host = hostname, name = 'perf.network.bytes.sent', value = BytesSentPersec)
            agent_settings.agent_list.append(AData1)
            agent_settings.agent_list.append(AData2)
        except:
            pass

        # Pagefile
        try:
            for i in c.Win32_PerfFormattedData_PerfOS_PagingFile(Name = '_Total'):
                AData = AgentData(time = agent_time, host = hostname, name = 'perf.pagefile.percent.used', value = i.PercentUsage)
                agent_settings.agent_list.append(AData)
        except:
            pass

        # Processor
        try:
            for i in c.Win32_PerfFormattedData_PerfOS_Processor(Name='_Total'):
                AData = AgentData(time = agent_time, host = hostname, name = 'perf.processor.percent.used', value = i.PercentProcessorTime)
                agent_settings.agent_list.append(AData)
        except:
            pass

        # Uptime
        try:
            for i in c.Win32_PerfFormattedData_PerfOS_System():
                AData = AgentData(time = agent_time, host = hostname, name = 'perf.system.uptime.seconds', value = i.SystemUptime)
                agent_settings.agent_list.append(AData)
        except:
            pass
       
        # Service Monitoring
        try:
            if agent_settings.servicemon:
                for service in agent_settings.servicemon:
                    for i in c.Win32_Service(Name = service):
                        sname = 'perf.service.' + service.replace(' ','').lower() + '.state'
                        state = i.State
                        if state == 'Running':
                            state = 1
                        else:
                            state = 0
                        AData = AgentData(time = agent_time, host = hostname, name = sname, value = state)
                        agent_settings.agent_list.append(AData)
        except:
            pass
        
        # Return list of WMI data 
        for i in agent_settings.agent_list:
            output = output + i.time + ';' + i.host + ';' + i.name + ';'  + str(i.value) + '\n'

        return output




