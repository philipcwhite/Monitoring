# Copyright (C) 2018-2019 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit: https://github.com/philipcwhite/webserver

import asyncio
import ssl
import uuid
import datetime
import urllib.parse

class app_vars:
    # Server paths
    app_path = './'
    app_login = '/login'

    # Server configuration
    server_name = 'wServer 0.01b'
    server_ip = '0.0.0.0'
    server_port = 9999
    session_expire = 3600

    # SSL settings
    ssl_enabled = False
    cert_key = 'localhost.pem'
    cert_name = 'localhost.crt'
    cert_path = './certificates/'

    # Service shutdown settings
    stop_ip = '127.0.0.1'
    stop_loop = False

    # Content settings
    content_type = {'css': 'text/css',
                    'csv': 'text/csv',
                    'gif': 'image/gif',
                    'htm': 'text/html',
                    'html': 'text/html',
                    'ico': 'image/x-icon',
                    'jpeg': 'image/jpeg',
                    'jpg': 'image/jpg',
                    'js': 'text/javascript',
                    'png': 'image/png',
                    'text': 'text/plain',
                    'txt': 'text/plain'}
    http_codes = {200: 'HTTP/1.1 200 OK',
                  302: 'HTTP/1.1 302 Found',
                  404: 'HTTP/1.1 404 Not Found'}

class session:
    session_list = []
    def __init__(self, session_id, session_user, session_expire):
        self.session_id = session_id
        self.session_user = session_user
        self.session_expire = session_expire

class web_handle(asyncio.Protocol):
    session_id = None
    get_cookie = None
    set_cookie = None
    controller = None
    arguments = None
    extension = None
    method = None
    path = None
    response_code = None
    response_location = None
    response_length = None

    def cookie(self, key = None, value = None, expires = None):
        # Set session cookie
        session_id = str(uuid.uuid1())
        if self.get_cookie is None:
            self.session_id = session_id
            if not self.set_cookie is None:
                self.set_cookie += 'Set-Cookie: session_id=' + self.session_id + '; max-age=' + str(app_vars.session_expire) + '; path=/ \r\n'
            else:
                self.set_cookie = 'Set-Cookie: session_id=' + self.session_id + '; max-age=' + str(app_vars.session_expire) + '; path=/ \r\n'
        else:
            if not 'session_id' in self.get_cookie:
                if not self.set_cookie is None:
                    self.set_cookie += 'Set-Cookie: session_id=' + self.session_id + '; max-age=' + str(app_vars.session_expire) + '; path=/ \r\n'   
        # Set other cookies
        if not key is None:
            if value is None: value = ''
            if expires is None: expires = ''
            self.set_cookie += 'Set-Cookie: ' + str(key) + '=' + str(value) + '; max-age=' + str(expires) + '; path=/ \r\n'

    def login(self, user):
        if not user is None:
            expires = datetime.datetime.now() + datetime.timedelta(seconds = app_vars.session_expire)
            user=session(self.session_id, user, expires)
            session.session_list.append(user)

    def logout(self, user):
        for i, o in enumerate(session.session_list):
            if o.session_user == user:
                del session.session_list[i]
                break
        self.set_cookie = 'Set-Cookie: session_id=' + self.session_id + '; max-age=0; path=/ \r\n'

    def get_user(self):
        user = None
        expires = None
        for i in session.session_list:
            if i.session_id == self.session_id:
                user = i.session_user
                expires = i.session_expire
        if not expires is None:
            if expires < datetime.datetime.now():
                for i, o in enumerate(session.session_list):
                    if o.session_user == user:
                        del session.session_list[i]
                        break
        if not user is None and expires > datetime.datetime.now():
            return user
        else: return None

    def get_auth(self):
        authorized = False
        user = self.get_user()
        if not user is None: authorized = True
        if authorized == False:
            self.redirect(app_vars.app_login)
            return 'Not Authorized'
        else: return user

    def error_404(self):
        self.response_code = 404
        html = '<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>'
        return html

    def redirect(self, location):
        self.response_code = 302
        self.response_location = 'Location: ' + location + '\r\n'

    def get_headers(self, request):
        # Process all incoming header requests
        request_list = []
        request_list = request.split('\n')
        self.method = request_list[0].split(' ')[0]
        self.path = request_list[0].split(' ')[1]
        if '.' in self.path:
            ext = self.path.split('.')[-1]
            if ext in app_vars.content_type: self.extension = ext
            else: self.extension = 'html'
        else: self.extension = 'html'
        self.arguments = urllib.parse.unquote(request_list[-1])
        for i in request_list:
            if 'Cookie:' in i: 
                self.get_cookie = i.replace('Cookie: ','')
                session_id = self.get_cookie.split(';')[0].replace('session_id=','')
                if not session_id == '': self.session_id = session_id
        print('METHOD:' + self.method)
        print('PATH:' + self.path)
        print('EXT:' + self.extension)
        print('ARGUMENTS:' + self.arguments)
        if not self.get_cookie is None:
            print('COOKIE:' + self.get_cookie)
            print('SESSION_ID:' + self.session_id)
        print('')

    def set_headers(self):
        # Set default header for OK responses
        response_code = 200
        response_location = ''
        if not self.response_code is None: response_code = self.response_code
        if not self.response_location is None: response_location = self.response_location
        http_status = app_vars.http_codes[response_code] + '\r\n'  
        content_type = 'Content-Type: ' + app_vars.content_type[self.extension] + ' \r\n'
        server_date = 'Date: ' + str(datetime.datetime.now()) + '\r\n'
        server_name = 'Server: ' + app_vars.server_name + '\r\n'
        content_length = 'Content-Length: ' + self.response_length + '\r\n'
        accept_range = ''
        # Process images or text files 
        if 'image' in app_vars.content_type[self.extension]: 
            accept_range = 'Accept-Ranges: bytes\r\n'
            head = http_status + content_type + accept_range + '\r\n'
            return head.encode()
        else:
            self.cookie()
            cookie_text = ''
            if not self.set_cookie is None: cookie_text = self.set_cookie
            head = http_status + content_type + server_date + server_name + content_length + cookie_text + response_location + '\r\n'
            return head.encode()  
  
    def call_controller(self):        
        args = []
        parsed_url = self.path.split('?')
        path_string = parsed_url[0]
        path_func = path_string.split('/')[1]
        if path_func == '':path_func='index'
        for i in dir(self.controller):
            if not '__' in i:
                if i == path_func:
                    for x in path_string.split('/'):
                        if not x == '': args.append(x)
                    if args: del args[0]
                    if '?' in self.path:
                        parsed_args = parsed_url[1].split('&')
                        for x in parsed_args:
                            args.append(x.split('=')[1])
                    # Handle POST
                    if self.method == 'POST':
                        parsed_args = self.arguments.split('&')
                        for x in parsed_args: args.append(x.split('=')[1])
                    self.arguments = args
                    func = getattr(self.controller, i)
                    proc = None
                    '''try:
                        if args: proc = func(self, *args)
                        else: proc = func(self)
                    except: proc = self.error_404()'''
                    if args: proc = func(self, *args)
                    else: proc = func(self)

                    if proc is None: proc = ''
                    self.response_length=str(len(proc))
                    head = self.set_headers()
                    resp_msg = head + proc.encode()
                    return resp_msg

    def call_static(self):
        if '/favicon.ico' in self.path or '/static/' in self.path:
            url=self.path[1:]
            if 'favicon.ico' in url: url = 'static/favicon.ico'
            f = open(app_vars.app_path + url, 'rb')
            obj = f.read()
            self.response_length=str(len(obj))
            head = self.set_headers()
            resp = head + obj
            return resp

    def connection_made(self, transport):
        #peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        # Check to see if loop should end
        if app_vars.stop_loop == True:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(loop.stop)
        # Parse headers, route request, return data
        message = data.decode('utf-8', 'ignore')
        self.get_headers(message)
        reply = None
        reply = self.call_static()
        if reply is None: reply = self.call_controller()
        self.transport.write(reply)               
        self.transport.close()

class web_server():
    async def connection_loop():
        loop = asyncio.get_running_loop()
        if app_vars.ssl_enabled == True:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.options |= ssl.PROTOCOL_TLSv1_2
            ssl_context.load_cert_chain(certfile = app_vars.cert_path + app_vars.cert_name, keyfile = app_vars.cert_path + app_vars.cert_key)
            server = await loop.create_server(lambda: web_handle(), app_vars.server_ip, app_vars.server_port, ssl=ssl_context)
        else: server = await loop.create_server(lambda: web_handle(), app_vars.server_ip, app_vars.server_port)
        async with server: await server.serve_forever()
        
class app:
    def start(controller):
        web_handle.controller = controller
        try: asyncio.run(web_server.connection_loop())
        except: pass
