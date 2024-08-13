from flask import Flask, render_template, request, redirect, session, url_for, make_response
#from app import app
#from app.model import Auth, Code, Data
from app import app
from model import Auth, Code, Data



# Decorators
def authenticate(func):
    def wrapper(*args, **kwargs):
        if session.get('auth') is None:
            return redirect('login')
        else: 
            return func(*args, **kwargs)     
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
            if auth[0] == user:
                session['user'] = user
                session['auth'] = True
                session['role'] = auth[1]
                return redirect(url_for('index'))

    @app.route('/logoff')
    def logoff():
        session['auth'] = None
        session['user'] = None
        session['role'] = None
        return redirect(url_for('login'))
        
    @app.route('/')
    @authenticate
    def index():
        if 'page' in request.args:
            page = request.args.get('page')
            content = f'index_content?page={page}'
        else:
            content = 'index_content'
        return render_template('index.html', index_content = content)

    @app.route('/index_content')
    @authenticate
    def index_content():
        page = 1 
        if 'page' in request.args:
            page = request.args.get('page')
        C = Code()
        content = C.index(page)
        return render_template('index_content.html', **content)

    @app.route('/password', methods=['GET', 'POST'])
    @authenticate
    def password():
        user = session.get('user')
        if request.method == 'GET':
            return render_template('password.html', user=user)
        if request.method == 'POST':
            pass1 = request.form['pass1']
            pass2 = request.form['pass2']
            A = Auth()
            A.user_password_change(user, pass1, pass2)
            return redirect(url_for('index'))
            
    @app.route('/search')
    @authenticate
    def search():
        device = None
        if 'device' in request.args:
            device = request.args.get('device')
        D = Data()
        devices = D.search_devices(device)
        return render_template('search.html', device = device, devices = devices)

    @app.route('/events')
    @authenticate
    def events():
        if 'status' in request.args:
            status = request.args.get('status')
            content = f'events_content?status={status}'
        else:
            content = 'events_content'
        return render_template('events.html', events_content = content)

    @app.route('/events_content')
    @authenticate
    def events_content():
        status = '1'
        if 'status' in request.args:
            status = request.args.get('status')
        C = Code()
        content = C.events(status)
        return render_template('events_content.html', **content)

    @app.route('/event_change/<id>/<status>')
    @authenticate
    def event_change(id, status):
        D = Data()
        D.event_change_status(id,status)
        return redirect(url_for('events'))
    
    @app.route('/devices')
    @authenticate
    def devices():
        return render_template('devices.html')

    @app.route('/devices_content')
    @authenticate
    def devices_content():
        C = Code()
        device_list = C.devices()
        return render_template('devices_content.html', device_list=device_list)

    @app.route('/device/<name>')
    @authenticate
    def device(name):
        return render_template('device.html', name = name, device_content='../device_content/' + name)

    @app.route('/device_content/<name>')
    @authenticate
    def device_content(name):
        C = Code()
        device, filesystem = C.device(name)
        return render_template('device_content.html', name = name, **device, filesystem = filesystem)
    
    @app.route('/graph/<name>/<monitor>')
    @authenticate
    def graph(name, monitor):
        return render_template('graph.html', name = name, monitor = monitor, graph_content = '/graph_content/' + name + '/' + monitor)

    @app.route('/graph_content/<name>/<monitor>')
    @authenticate
    def graph_content(name, monitor):
        C = Code()
        graph = C.device_graph(name, monitor)
        return render_template('graph_content.html', graph = graph)

    @app.route('/reports')
    @authenticate
    def reports():
        return render_template('reports.html')

    @app.route('/reports/<report>')
    @authenticate
    def report(report):
        name = report.split('.')[0]
        ext = report.split('.')[1]
        C = Code()
        output = C.report(name, ext)
        if ext == 'html':
            return render_template('report.html', output = output)
        if ext == 'csv':
            output_csv = make_response(output) #, 'unicode')
            output_csv.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output_csv.headers["Content-type"] = "text/csv"
            return output_csv

    @app.route('/settings')
    @authenticate
    def settings():
        return render_template('settings.html')

    @app.route('/help')
    @authenticate
    def help():
        return render_template('help.html')

    @app.route('/about')
    @authenticate
    def about():
        return render_template('about.html')

    @app.route('/notify')
    @authenticate
    def notify():
        D = Data()
        notify = D.notify_rules()
        return render_template('notify.html', user = user, notify = notify)

    @app.route('/notify_add', methods=['GET', 'POST'])
    @authenticate
    def notify_add():
        if request.method == 'GET':
            D = Data()
            device_names = D.notify_device_names()
            return render_template('notify_add.html', device_names = device_names)
        if request.method == 'POST':
            notify_name = request.form['notify_name']
            notify_email = request.form['notify_email']
            agent_name = request.form['agent_name']
            agent_monitor = request.form['agent_monitor']
            agent_status = request.form['agent_status']
            agent_severity = request.form['agent_severity']
            notify_enabled = request.form['notify_enabled']
            D = Data()
            D.notify_add(notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            return redirect(url_for('notify'))

    @app.route('/notify_edit/<id>', methods=['GET', 'POST'])
    @authenticate
    def notify_edit(id):
        if request.method == 'GET':
            D = Data()
            device_names = D.notify_device_names()
            notify_rule = D.notify_rule(id)
            return render_template('notify_edit.html', device_names = device_names, **notify_rule)
        if request.method == 'POST':
            notify_name = request.form['notify_name']
            notify_email = request.form['notify_email']
            agent_name = request.form['agent_name']
            agent_monitor = request.form['agent_monitor']
            agent_status = request.form['agent_status']
            agent_severity = request.form['agent_severity']
            notify_enabled = request.form['notify_enabled']
            D = Data()
            D.notify_edit(notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            return redirect(url_for('notify'))

    @app.route('/notify_delete/<id>')
    @authenticate
    def notify_delete(id):
        D = Data()
        D.notify_delete(id)
        return redirect(url_for('notify.html'))

    @app.route('/users')
    @authenticate
    def users():
        role = session.get('role')
        if role == 1:
            D = Data()
            users = D.users_select()
            return render_template('users.html', users = users)
        else:
            return redirect(url_for('settings'))

    @app.route('/user_add', methods=['GET', 'POST'])
    @authenticate
    def user_add():
        if request.method == 'GET':
            return render_template('user_add.html')
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            role = request.form['role']
            A = Auth()
            A.user_add(user, password, role)
            return redirect(url_for('users'))

    @app.route('/user_pass/<user>', methods=['GET', 'POST'])
    @authenticate
    def user_pass(user):
        if request.method == 'GET':
            return render_template('user_pass.html')
        if request.method == 'POST':
            user = request.form['user']
            pass1 = request.form['pass1']
            pass2 = request.form['pass2']
            A = Auth()
            A.user_password_change_admin(user, pass1, pass2)
            return redirect(url_for('users'))

    @app.route('/user_role/<id>', methods=['GET', 'POST'])
    @authenticate
    def user_role(id):
        if request.method == 'GET':
            D = Data()
            content = D.user_select(id)
            return render_template('user_role.html', user=content[1], role=content[2])
        if request.method == 'POST':
            id = request.form['id']
            role = request.form['role']
            D = Data()
            D.user_edit_role(id, role)
            return redirect(url_for('users'))

    @app.route('/user_delete/<id>')
    @authenticate
    def user_delete(id):
        D = Data()
        D.user_delete(id)
        return redirect(url_for('users'))