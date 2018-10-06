import cherrypy
from web_controller import WebController

cherrypy.tree.mount(WebController(), '/', config="C:\\Progra~1\\monitoring\\website\\config.txt")
cherrypy.engine.start()
cherrypy.engine.block()