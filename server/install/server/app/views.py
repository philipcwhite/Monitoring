from flask import Flask, render_template, request, redirect, session, url_for
from monitoring import app
from monitoring.model import Auth, Code, Data

# Decorators
def authenticate(func):
    def wrapper(*args, **kwargs):
        if session.get('auth') is None:
            return redirect('login')
        else: return func(*args, **kwargs)     
    wrapper.__name__ = func.__name__     
    return wrapper     

class Web:
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            A = Auth()
            auth = A.verify(user,password)
            if auth == 'admin':
                session['user'] = user
                session['auth'] = True
                return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session['auth'] = None
        session['user'] = None
        return redirect(url_for('login'))
        
    @app.route('/')
    #@authenticate
    def index():
        user = session.get('user')
        if 'page' in request.args:
            page = request.args.get('page')
            content = f'index_content?page={page}'
        else:
            content = 'index_content'
        return render_template('index.html', user = user, index_content = content)

    @app.route('/index_content')
    #@authenticate
    def index_content():
        page = 1 
        if 'page' in request.args:
            page = request.args.get('page')
        C = Code()
        content = C.index(page)
        return render_template('index_content.html', **content)

    @app.route('/password', methods=['GET', 'POST'])
    #@authenticate
    def password():
        user = session.get('user')
        if request.method == 'GET':
            return render_template('password.html')
        if request.method == 'POST':
            password_old = request.form['pass1']
            password_new = request.form['pass2']
            A = Auth()
            A.user_password_change(user, pass1, pass2)
            return redirect(url_for('index'))
            
    @app.route('/search')
    #@app.authenticate
    def search():
        user = session.get('user')
        device = None
        if 'device' in request.args:
            device = request.args.get('device')
        D = Data()
        devices = D.search_devices(device)
        return render_template('search.html', user = user, device = device, devices = devices)

    @app.route('/events')
    #@authenticate
    def events():
        user = session.get('user')
        if 'status' in request.args:
            status = request.args.get('status')
            content = f'events_content?status={status}'
        else:
            content = 'events_content'
        return render_template('events.html', user = user, events_content = content)

    @app.route('/events_content')
    #@authenticate
    def events_content():
        status = '1'
        if 'status' in request.args:
            status = request.args.get('status')
        C = Code()
        content = C.events(status)
        return render_template('events_content.html', **content)

    @app.route('/event_change/<id>/<status>')
    #@authenticate
    def event_change(id, status):
        D = Data()
        D.event_change_status(id,status)
        return redirect(url_for('events'))
    
    @app.route('/devices')
    #@authenticate
    def devices():
        user = session.get('user')
        return render_template('devices.html', user=user)

    @app.route('/devices_content')
    #@authenticate
    def devices_content():
        C = Code()
        device_list = C.devices()
        return render_template('devices_content.html', device_list=device_list)

    @app.route('/device/<name>')
    #@authenticate
    def device(name):
        user = session.get('user')
        return render_template('device.html', user = user, device_content='../device_content/' + name)

    @app.route('/device_content/<name>')
    #@authenticate
    def device_content(name):
        C = Code()
        device, filesystem = C.device(name)
        return render_template('device_content.html', name = name, **device, filesystem = filesystem)
    
    @app.route('/graph/<name>/<monitor>')
    #@authenticate
    def graph(name, monitor):
        user = session.get('user')
        return render_template('graph.html', user = user, name = name, monitor = monitor, graph_content = '/monitoring/graph_content/' + name + '/' + monitor)

    @app.route('/graph_content/<name>/<monitor>')
    #@authenticate
    def graph_content(name, monitor):
        C = Code()
        graph = C.device_graph(name, monitor)
        return render_template('graph_content.html', graph = graph)