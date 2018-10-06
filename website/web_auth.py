import cherrypy
import hashlib
from web_data import WebData

class WebAuth:
    
    def check_auth():
        auth = cherrypy.session.get('authenticated', None)
        if auth == None: 
            try:
                auth = cherrypy.request.cookie['authenticated']
            except:
                raise cherrypy.HTTPRedirect("/logon")
        return auth

    def verify_auth(username, password):
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        authuser = WebData.web_auth(username, encrypt_password)
        if not authuser is None:
            cherrypy.session['authenticated']=authuser
            cherrypy.session['timeout']=10080
            raise cherrypy.HTTPRedirect("/")
        raise cherrypy.HTTPRedirect("/")

