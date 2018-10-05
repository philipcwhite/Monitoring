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
    def events(self):
        user=WebAuth.check_auth()
        html = WebViews.load_base(user, WebViews.load_bc_events(), WebViews.load_refresh("/events_content/"))
        return html

    @cherrypy.expose
    def events_content(self):
        user = WebAuth.check_auth()
        html = WebEvents.events_content()
        return html

    @cherrypy.expose
    def event_close(self, id):
        user = WebAuth.check_auth()
        WebData.web_code_close_event(id)
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

