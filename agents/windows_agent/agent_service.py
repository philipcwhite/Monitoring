# Copyright (C) 2018-2019 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit:  https://github.com/philipcwhite/monitoring

import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import datetime
# User classes
import agent_actions

class AgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MonitoringAgent"
    _svc_display_name_ = "Monitoring Agent"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        agent_actions.AgentProcess.initialize_agent()
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            a = datetime.datetime.now().second
            if a == 0:
                agent_actions.AgentProcess.run_process()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AgentService)
