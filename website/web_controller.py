import cherrypy
import web_views
from web_auth import WebAuth
from web_views import WebViews
from web_code import WebIndex, WebSearch

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
        html = WebViews.load_base(user, WebViews.load_bc_events(), "events")
        return html

    @cherrypy.expose
    def devices(self, name=None, monitor=None):
        user=WebAuth.check_auth()
        if name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_devices(), "devices")
        elif not name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_device(name), "devices")
        elif not name is None and not monitor is None:
            return "Test"
        
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
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page(WebSearch.search_devices(device)))
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

