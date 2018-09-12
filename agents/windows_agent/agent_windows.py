import os
import agent_settings, agent_sql

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

        # Network
        try:
            nw_br = 0
            nw_bs = 0
            process = os.popen('wmic path Win32_PerfFormattedData_Tcpip_NetworkInterface get BytesReceivedPersec,BytesSentPersec /format:csv')
            result = process.read()
            process.close()
            result = result.replace("\n\n","\n")
            result_list = list(filter(None, result.split("\n")))
            for i in result_list:
                if not 'BytesReceivedPersec' in i:
                    nw_list = i.split(",")
                    nw_br = nw_br + int(nw_list[1])
                    nw_bs = nw_bs + int(nw_list[2])
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.network.bytes.received', str(nw_br))
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.network.bytes.sent', str(nw_bs))
        except:
            pass

        # Pagefile
        try:
            process = os.popen('wmic path Win32_PerfFormattedData_PerfOS_PagingFile where name="_Total" get PercentUsage /value')
            result = process.read()
            process.close()
            result = result.replace("\n","").replace("PercentUsage=","")
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.pagefile.percent.used', str(result))
        except:
            pass

        # Processor Util
        try:
            process = os.popen('wmic path Win32_PerfFormattedData_PerfOS_Processor where name="_Total" get PercentProcessorTime /value')
            result = process.read()
            process.close()
            result = result.replace("\n","").replace("PercentProcessorTime=","")
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.processor.percent.used', str(result))
        except:
            pass

        # Uptime
        try:
            process = os.popen('wmic path Win32_PerfFormattedData_PerfOS_System get SystemUptime /value')
            result = process.read()
            process.close()
            result = result.replace("\n","").replace("SystemUpTime=","")
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'perf.system.uptime.seconds', str(result))
        except:
            pass

        # Service Monitoring
        try:
            if agent_settings.services:
                for service in agent_settings.services:
                    process = os.popen('wmic path Win32_Service where name="' + service + '" get State /value')
                    result = process.read()
                    process.close()
                    result = result.replace("\n","").replace("State=","")
                    sname = 'perf.service.' + service.replace(' ','').lower() + '.state'
                    if result == 'Running':
                        result = 1
                    else:
                        result = 0
                    agent_sql.AgentSQL.insert_agentdata(agent_time, name, sname, str(result))
        except:
            pass
