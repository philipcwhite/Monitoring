import os
import agent_sql

class AgentWindows():
    def data_windows(agent_time, name):
        # Memory Total
        try:
            process = os.popen('wmic path Win32_ComputerSystem get TotalPhysicalMemory /value')
            result = process.read()
            process.close()
            result = result.replace("\n","").replace("TotalPhysicalMemory=","")
            result = round(int(result)  / 1024 / 1024, 0)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.memory.total', str(result))
        except:
            pass

        # CPU Util
        try:
            process = os.popen('wmic path Win32_PerfFormattedData_PerfOS_Processor where name="_Total" get PercentProcessorTime /value')
            result = process.read()
            process.close()
            result = result.replace("\n","").replace("PercentProcessorTime=","")
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.processor.percent.used', str(result))
        except:
            pass

        # Filesystem
        try:
            process = os.popen('''wmic path Win32_PerfFormattedData_PerfDisk_LogicalDisk WHERE "Name LIKE '%:'" get Name,PercentFreeSpace,PercentIdleTime /format:csv''')
            result = process.read()
            process.close()
            result = result.replace("\n\n","\n")
            result_list = list(filter(None, result.split("\n")))
            for i in result_list:
                if not 'PercentFreeSpace' in i:
                    ld_list = i.split(",")
                    ld_name = ld_list[1].replace(":","").lower()
                    ld_free = float(ld_list[2])
                    ld_at = 100 - float(ld_list[3])
                    agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.filesystem.' + ld_name + '.percent.free', str(ld_free))
                    agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.filesystem.' + ld_name + '.percent.active', str(ld_at))
        except:
            pass
        
        # Memory
        try:
            process = os.popen('wmic path Win32_OperatingSystem get FreePhysicalMemory,TotalVisibleMemorySize /value')
            result = process.read()
            process.close()
            result = result.replace("\n\n\n\n","")
            result = result.replace("\n\n",";")
            result_list = result.split(";")     
            FreeMem = int(result_list[0].replace("FreePhysicalMemory=",""))
            TotalMem = int(result_list[1].replace("TotalVisibleMemorySize=",""))
            PercentMem = ((TotalMem-FreeMem)/TotalMem)*100
            PercentMem = round(PercentMem,2)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.memory.percent.used', str(PercentMem))
        except:
            pass




"""        # Network
        try:    
            BytesReceivedPersec = 0
            BytesSentPersec = 0
            for i in c.Win32_PerfFormattedData_Tcpip_NetworkInterface():
                BytesReceivedPersec = BytesReceivedPersec + int(i.BytesReceivedPersec)
                BytesSentPersec = BytesSentPersec + int(i.BytesSentPersec)
                BytesReceivedPersec = BytesReceivedPersec
                BytesSentPersec = BytesSentPersec
                agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.network.bytes.received', str(BytesReceivedPersec))
                agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.network.bytes.sent', str(BytesSentPersec))
        except:
            pass

        # Pagefile
        try:
            for i in c.Win32_PerfFormattedData_PerfOS_PagingFile(Name = '_Total'):
                agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.pagefile.percent.used', str(i.PercentUsage))
        except:
            pass

        # Uptime
        try:
            for i in c.Win32_PerfFormattedData_PerfOS_System():
                agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.system.uptime.seconds', str(i.SystemUptime))
        except:
            pass
       
        # Service Monitoring
        try:
            if agent_settings.services:
                for service in agent_settings.services:
                    for i in c.Win32_Service(Name = service):
                        sname = 'perf.service.' + service.replace(' ','').lower() + '.state'
                        state = i.State
                        if state == 'Running':
                            state = 1
                        else:
                            state = 0
                        agent_sql.AgentSQL.insert_agentdata(agent_time, name, sname, str(state))
        except:
            pass
        
        output = agent_sql.AgentSQL.select_agent_data()
        return output"""
