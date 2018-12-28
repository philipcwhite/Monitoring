import event_settings, event_data, event_load
import smtplib, datetime, time
from email.message import EmailMessage

class ServerEvent():
    def process_events():
        try:
            id = event_data.agent_select_id()
            output = event_data.agent_filter_select(id)
            for i in output:
                notify_email = i["notify_email"]
                notify_name = i["notify_name"]
                name = i["name"]
                monitor = i["monitor"]
                message = i["message"]
                severity = ""
                if i["severity"] == "1":
                    severity = "critical"
                if i["severity"] == "2":
                    severity = "major"
                if i["severity"] == "3":
                    severity = "warning"
                if i["severity"] == "4":
                    severity = "info"
                status = ""
                if i["status"] == "0":
                    status = "closed"
                else:
                    status = "open"
                timestamp = int(i["timestamp"])
                date = datetime.datetime.fromtimestamp(timestamp)
                email_subject = name + ":" + monitor + ":" + severity + ":" + status 
                email_message = """<div style="font-family:Arial, Helvetica, sans-serif;font-size: 11pt"><b>message:</b> """ + message + "<br /><b>name:</b> " + name + "<br /><b>monitor:</b> " + monitor + "<br /><b>severity:</b> " + severity + "<br /><b>status:</b> " + status + "<br /><b>time opened:</b> " + str(date) + "<br /><b>policy:</b> " + notify_name + "</div>"

                if event_settings.mailactive == 1:
                    msg = EmailMessage()
                    msg["Subject"] = email_subject
                    msg["From"] = event_settings.mailadmin
                    msg["To"] = notify_email
                    msg.set_content(email_message, subtype='html')
                    s = smtplib.SMTP(event_settings.mailserver)
                    s.send_message(msg)
                    s.quit()

                #print(str(time.time()).split('.')[0] + ":" + notify_email + ":" + notify_name + ":" + name + ":" + monitor + ":" + message + ":" + severity + ":" +status + ":" + str(date) + "\n")
                f = open(event_settings.application_path + "output.txt","a")
                f.write(str(time.time()).split('.')[0] + ":" + notify_email + ":" + notify_name + ":" + name + ":" + monitor + ":" + message + ":" + severity + ":" +status + ":" + str(date) + "\n")
                f.close()
        except: pass

#event_load.load_config()
#ServerEvent.process_events()