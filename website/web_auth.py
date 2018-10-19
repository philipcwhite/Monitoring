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
            raise cherrypy.HTTPRedirect("/")
        raise cherrypy.HTTPRedirect("/")

    def change_password(username, pass1, pass2):
        encrypt_password1 = hashlib.sha224(pass1.encode()).hexdigest()
        encrypt_password2 = hashlib.sha224(pass2.encode()).hexdigest()
        authuser = WebData.web_auth(username, encrypt_password1)
        if not authuser is None:
            WebData.web_change_password(username, encrypt_password2)
            raise cherrypy.HTTPRedirect("/settings")
        raise cherrypy.HTTPRedirect("/error")
