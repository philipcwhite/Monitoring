import time, socket
import agent_settings, agent_sql
import asyncio

class AgentEvent():

    def event_create(time, monitor, severity, threshold, compare, duration, status):
        #if status == "open":
        name = agent_settings.name
        message = monitor.replace("perf.", "").replace(".", " ").capitalize()
        message = message + " " + compare + " " + str(threshold) + " for " + str(round(duration/60)) + " minutes"
            
        #check open messages
        check_message = agent_sql.AgentSQL.select_agent_events(message, severity)

        if check_message is None and status == 1:
            agent_sql.AgentSQL.insert_agent_events(time, name, message, severity)
            #message is created and queued
        elif check_message == message and status == 0:
            agent_sql.AgentSQL.close_agent_events(message, severity)
            #message is updated and queued
        else:
            pass
        print(message)
        
    def event_process():
        agent_time = int(round(time.time()))
        agent_thresholds = agent_sql.AgentSQL.select_thresholds()
        a_val = 0
        b_val = 0
        for i in agent_thresholds:
            monitor = i[0]
            severity = i[1]
            threshold = int(i[2])
            compare = i[3]
            duration = i[4]
            time_window = agent_time - duration
            #print(monitor, severity, threshold, compare, duration, time_window)
            agent_data = agent_sql.AgentSQL.select_agent_data_events(time_window, monitor)
            a_val = 0
            b_val = 0
            for i in agent_data:
                #print(i[0])
                value = i[0]
                if compare == ">":
                    if value > threshold:
                        a_val += 1
                        b_val += 1
                    else:
                        b_val += 1
                elif compare == "<":
                    if value < threshold:
                        a_val += 1
                        b_val += 1
                    else:
                        b_val += 1
                elif compare == "=":
                    if value == threshold:
                        a_val += 1
                        b_val += 1
                    else:
                        b_val += 1
            print(a_val, b_val)    
            if a_val == b_val and b_val != 0 :
                print(monitor + " Threshold True")
                AgentEvent.event_create(agent_time, monitor, severity, threshold, compare, duration, 1)
            else:
                print(monitor + " Threshold False")
                AgentEvent.event_create(agent_time, monitor, severity, threshold, compare, duration, 0)

        # Return events
        output = ""
        return output




#AgentEvents.event_process()

"""def create_loop():
        loop = asyncio.new_event_loop() 
        loop.run_until_complete(AgentEvents.event_process())
        loop.close 
create_loop()"""





