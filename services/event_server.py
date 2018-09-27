import event_settings, event_data
import os

class ServerEvent():
    def process_events():
        try:
            output = event_data.agent_filter_select()
            f = open(event_settings.application_path + "output.txt","a")
            f.write(str(output))
            f.close()
        except:
            pass

#ServerEvent.process_events()
