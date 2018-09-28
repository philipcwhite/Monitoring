import event_settings, event_data
import time

class EventAvailable():
    def check_available():
        try:
            check_time = str(time.time() - event_settings.availability_check).split('.')[0]
            cur_time = str(time.time()).split('.')[0]
            hosts = event_data.agent_avail_select(check_time)
            for i in hosts:
                name = i["name"]
                message = "Agent not responding for " + str(int(round(event_settings.availability_check / 60,0)))  + " minutes"
                event_data.agent_avail_event_open(cur_time, name, message, str(event_settings.availability_severity))
        except:
            pass

    def check_open():
        try:
            check_time = str(time.time() - event_settings.availability_check).split('.')[0]
            event_data.agent_avail_select_event_open(check_time)
        except:
            pass





