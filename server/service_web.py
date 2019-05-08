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
import socket
# User classes
import web_site, web_server

class MonWebsite(win32serviceutil.ServiceFramework):
    _svc_name_ = "monitoringweb"
    _svc_display_name_ = "Monitoring Website"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        web_server.app_vars.stop_loop = True
        con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        con.connect((web_server.app_vars.stop_ip, web_server.app_vars.server_port))
        byte=str('Close').encode()
        con.send(byte)
        con.close()

    def SvcDoRun(self):
        web_server.app_vars.app_path = 'C:\\PROGRA~1\\monitoring\\server\\'
        web_server.app_vars.cert_path = 'C:\\PROGRA~1\\monitoring\\server\\certificates\\'
        web_site.start_server()
                
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonWebsite)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonWebsite)
