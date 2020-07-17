from web.server import app_vars
import data
import configparser

def load_config():
    # Add Try block
    parser = configparser.ConfigParser()
    parser.read('settings.ini')
    #parser.read(app_vars.app_path + 'settings.ini')
    certificates = dict(parser.items('certificates'))
    database = dict(parser.items('database'))
    server = dict(parser.items('server'))
    app_vars.server_port = int(server['port_web'])
    app_vars.session_expire = int(server['session_expire'])
    app_vars.ssl_enabled = eval(server['secure'])
    app_vars.cert_key = certificates['key']
    app_vars.cert_name = certificates['name']
    data.host = database['host']
    data.instance = database['name']
    data.user = database['user']
    data.password = database['password']

load_config()

import views
views.start_server()
