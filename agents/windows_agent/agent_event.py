import agent_settings, agent_sql

class AgentEvent():
    def event_create(time, monitor, severity, threshold, compare, duration, status):
        try:
            name = agent_settings.name
            message = monitor.replace("perf.", "").replace(".", " ").capitalize()
            message = message + " " + compare + " " + str(threshold) + " for " + str(round(duration/60)) + " minutes"
            # Check open messages
            check_monitor = agent_sql.AgentSQL.select_agent_event(monitor)
            if not check_monitor is None: check_monitor=check_monitor[0]

            # Create, update, and queue events for dispatch
            if check_monitor is None and status == 1:
                agent_sql.AgentSQL.insert_agent_event(time, name, monitor, message, severity)
            elif check_monitor == monitor and status == 0:
                agent_sql.AgentSQL.close_agent_event(monitor, severity)
            else:
                pass
        except:
            pass
        
    def event_process(agent_time):
        try:
            agent_time_int = int(agent_time)
            agent_thresholds = agent_sql.AgentSQL.select_thresholds()
            a_val = 0
            b_val = 0
            for i in agent_thresholds:
                monitor = i[0]
                severity = i[1]
                threshold = int(i[2])
                compare = i[3]
                duration = i[4]
                time_window = agent_time_int - duration
                agent_data = agent_sql.AgentSQL.select_agent_data_events(time_window, monitor)
                a_val = 0
                b_val = 0
                for i in agent_data:
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
                        if value == 0 and threshold == 0:
                            a_val += 1
                            b_val += 1
                        else:
                            b_val += 1
                if a_val == b_val and b_val != 0 :
                    AgentEvent.event_create(agent_time, monitor, severity, threshold, compare, duration, 1)
                else:
                    AgentEvent.event_create(agent_time, monitor, severity, threshold, compare, duration, 0)
            # Return events
            output = agent_sql.AgentSQL.select_open_agent_events()
            return output
        except:
            pass






