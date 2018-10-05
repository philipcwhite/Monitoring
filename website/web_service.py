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
import cherrypy
# User classes
from web_controller import WebController

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
        cherrypy.engine.exit()

    def SvcDoRun(self):
        try:
            cherrypy.tree.mount(WebController(), '/', config="C:\\Progra~1\\monitoring\\website\\config.txt")
            cherrypy.engine.start()
            cherrypy.engine.block()
        except:
            pass
                
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonWebsite)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonWebsite)

