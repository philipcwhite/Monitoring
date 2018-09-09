import time
import agent_settings, agent_sql
import asyncio

class EventAgentThresholds():
    def __init__(self, monitor, severity, threshold, compare, duration):
        self.monitor = monitor
        self.severity = severity
        self.threshold = threshold
        self.compare = compare
        self.duration = duration

class EventAgentData():
    def __init__(self, time, host, name, value):
        self.time = time
        self.host = host
        self.name = name
        self.value = value

class AgentEvents():
    def get_thresholds():
        pass

    async def process_data():
        agent_time = int(round(time.time()))
        agent_thresholds = await agent_sql.AgentSQL.select_thresholds()
        a_val = 0
        b_val = 0
        for i in agent_thresholds:
            monitor = i[0]
            severity = i[1]
            threshold = int(i[2])
            compare = i[3]
            duration = i[4]
            time_window = agent_time - duration
            print(monitor, severity, threshold, compare, duration, time_window)
            agent_data = await agent_sql.AgentSQL.select_agent_data_events(time_window, monitor)
            a_val = 0
            b_val = 0
            for i in agent_data:
                print(i[0])
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
            else:
                print(monitor + " Threshold False")






def create_loop():
        loop = asyncio.new_event_loop() 
        loop.run_until_complete(AgentEvents.process_data())
        loop.close 
create_loop()





