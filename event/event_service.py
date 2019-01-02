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
import event

class EventService(win32serviceutil.ServiceFramework):
    _svc_name_ = "EventService"
    _svc_display_name_ = "Event Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        event_collect.CollectServer.send_close()

    def SvcDoRun(self):
        event_load.load_config()
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            a = datetime.datetime.now().second
            if a == 0:
                event.EventAvailable.check_available()
                event.EventAvailable.check_open()
                event.ServerEvent.process_events()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
                
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(EventService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(EventService)


