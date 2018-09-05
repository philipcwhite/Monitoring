import pymysql.cursors

class agent_thresholds:
    def __init__(self, name, monitor, severity, threshold, compare, timerange):
        self.name = name
        self.monitor = monitor
        self.severity = severity
        self.threshold = threshold
        self.compare = compare
        self.timerange = timerange

class agent_events:
    def __init__(self, eventdate, name, monitor, message, status, severity, threshold, compare, timerange):
        self.eventdate = eventdate
        self.name = name
        self.monitor = monitor
        self.message = message
        self.status = status
        self.severity = severity
        self.threshold = threshold
        self.compare = compare
        self.timerange = timerange

class event_processing:
    agent_list = []
    threshold_list = []
    event_list =[]

    def get_agents():
        connection = pymysql.connect(host='localhost',
        user='django',
        password='django',
        db='monitoring',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT name from mon_app_agentsystem"
                cursor.execute(sql,)
                result = cursor.fetchall()
                if not result is None:
                    print(result)
        finally:
            connection.close()

event_processing.get_agents()






