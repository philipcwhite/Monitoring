# Copyright (C) 2018 Phil White - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the Apache 2 license.
#
# You should have received a copy of the Apache 2 license with
# this file. If not, please visit : https://github.com/philipcwhite/monitoring2

import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import datetime
# User classes
import collect_server, collect_settings

class CollectService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CollectService"
    _svc_display_name_ = "Collect Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

        collect_settings.running = 0
        con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        con.connect((collect_settings.server,collect_settings.port))
        byte=str('Close').encode()
        con.send(byte)
        con.close()

    def SvcDoRun(self):
        collect_server.CollectServer.server_start()
                
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CollectService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CollectService)


