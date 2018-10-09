import cherrypy
import web_views
from web_auth import WebAuth
from web_views import WebViews
from web_data import WebData
from web_code import WebIndex, WebDevice, WebDevices, WebEvents, WebSearch

user=""

class WebController:
    
    @cherrypy.expose
    def index(self, page=1):
        user=WebAuth.check_auth()
        qstring = "?page=" + str(page)
        html = WebViews.load_base(user, WebViews.load_bc_home(), WebViews.load_refresh("/index_content/" + qstring))
        return html
    
    @cherrypy.expose
    def index_content(self, page=1):
        user=WebAuth.check_auth()
        qstring = cherrypy.request.query_string
        html = WebIndex.index_content(qstring)
        return html

    @cherrypy.expose
    def events(self, status=1):
        user=WebAuth.check_auth()
        html = WebViews.load_base(user, WebViews.load_bc_events(), WebViews.load_refresh("/events_content/" + str(status)))
        return html

    @cherrypy.expose
    def events_content(self, status=1):
        user = WebAuth.check_auth()
        html = WebEvents.events_content(status)
        return html

    @cherrypy.expose
    def event_change(self, id, status):
        user = WebAuth.check_auth()
        WebData.web_code_change_event_status(id, status)
        raise cherrypy.HTTPRedirect("/events")


    @cherrypy.expose
    def devices(self, name=None, monitor=None):
        user=WebAuth.check_auth()
        if name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_devices(), WebViews.load_basic_page("Devices", WebDevices.device_index()))
        elif not name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_device(name), WebViews.load_refresh("/device_content/" + name))
        elif not name is None and not monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_device_graph(name, monitor), WebViews.load_refresh("/device_graph_content/" + name + "/" + monitor))
        return html
    
    @cherrypy.expose
    def device_content(self, name):
        user=WebAuth.check_auth()
        html = WebDevice.device_content(name)
        return html

    @cherrypy.expose
    def device_graph_content(self, name, monitor):
        user=WebAuth.check_auth()
        html = WebDevice.device_graph_content(name, monitor)
        return html

    @cherrypy.expose
    def reports(self):
        user=WebAuth.check_auth()
        html = WebViews.load_base(user, WebViews.load_bc_reports(), "reports")
        return html

    @cherrypy.expose
    def settings(self):
        user=WebAuth.check_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), "settings")
        return html

    @cherrypy.expose
    def notify(self):
        user=WebAuth.check_auth()
        html=""
        return html
    
    @cherrypy.expose
    def notify_add(self, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user=WebAuth.check_auth()
        html=""
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            return html
        else:
            # process post
            return html

    @cherrypy.expose
    def notify_edit(self, id, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user=WebAuth.check_auth()
        html=""
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            return html
        else:
            # process post
            return html
 
    @cherrypy.expose
    def notify_delete(self, id):
        user=WebAuth.check_auth()
        html=""
        return html 
    
    @cherrypy.expose
    def search(self, device=None):
        user=WebAuth.check_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page("Search Results", WebSearch.search_devices(device)))
        return html

    @cherrypy.expose
    def verify(self,username=None,password=None):
        WebAuth.verify_auth(username, password)

    @cherrypy.expose
    def logon(self):
        html = WebViews.load_login()
        return html

    @cherrypy.expose
    def logoff(self):
        cherrypy.session.delete()
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect("/logon")

