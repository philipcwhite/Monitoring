import configparser 
from web.server import app, app_vars
from web.templates import render
from data import Data
from code import WebAuth, WebCode

class controller(object):
    
    def verify(self, username=None, password=None):
        user = WebAuth.verify_auth(username, password)
        if not user is None:
            self.login(username)
            self.redirect('/')
        else: self.redirect('/login')

    def login(self):
        return render('login.html')

    def logoff(self):
        self.logout(self.get_user())
        self.redirect('/login')

    def index(self, page=1):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('home'), body = render('refresh.html', url = '/index_content/' + str(page)))

    def index_content(self, page=1):
        user = self.get_auth()
        head1, block1, head2, block2, head3, block3, head4, block4, pager = WebCode.index(page)
        return render('index.html', head1 = head1, block1 = block1, head2 = head2, block2 = block2, head3 = head3, block3 = block3, head4 = head4, block4 = block4, pager = pager)

    def events(self, status=1):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('events'), body = render('refresh.html', url = '/events_content/' + str(status)))
 
    def events_content(self, status=1):
        user = self.get_auth()
        return WebCode.events(status)

    def event_change(self, id, status):
        user = self.get_auth()
        WD = Data() 
        WD.change_event_status(id, status)
        self.redirect('/events')

    def devices(self, name=None, monitor=None):
        user = self.get_auth()
        if name is None and monitor is None:
            html = render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('devices'), body = render('basic.html', title = 'Devices', content = WebCode.device_index()))
        elif not name is None and monitor is None:
            html = render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('device', name), body = render('refresh.html', url = '/device_content/' + name))
        elif not name is None and not monitor is None:
            html = render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('device_graph', name, monitor), body = render('refresh.html', url = '/device_graph_content/' + name + '/' + monitor))
        return html
    
    def device_content(self, name):
        user = self.get_auth()
        return WebCode.device_content(name)

    def device_graph_content(self, name, monitor):
        user = self.get_auth()
        return render('basic.html', title = "System Performance", content = WebCode.device_graph(name, monitor))
    
    def reports(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('reports'), body = render('reports.html'))
    
    def report(self, filename):
        user = self.get_auth()
        html = ''
        ext = filename.split('.')[1]
        if ext == 'csv': self.extension = 'csv'
        else: self.extension = 'html'
        if 'devices.' in filename : html = WebCode.report_devices(ext)
        if 'events.' in filename : html = WebCode.report_events(ext)
        return html

    def settings(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('settings.html'))

    def about(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('about.html'))
        
    def notify(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Notification Rules', content = WebCode.notify_rules()))
    
    def notify_add(self, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user = self.get_auth()
        html=''
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Add Notification Rule', content = WebCode.notify_add()))
        else:
            WD.insert_notifyrules(notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            self.redirect('/notify')

    def notify_edit(self, id, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user = self.get_auth()
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Edit Notification Rule', content = WebCode.notify_edit(id)))
        else:
            WD = Data() 
            WD.update_notifyrules(id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            self.redirect('/notify')

    def notify_delete(self, id):
        user=WebAuth.check_auth()
        WD = Data() 
        WD.delete_notify_rule(id)
        self.redirect('/notify')

    def users(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Users', content = WebCode.user_list()))
        
    def user_add(self, username=None, password=None, role=None):
        user = self.get_auth()
        if not username is None and not password is None and not role is None:
            WebCode.user_add(username, password, role)
            self.redirect('/users')
        else:
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Users', content = render('user_add.html')))
           
    def user_edit_pass(self, id, pass1 = None, pass2 = None):
        user = self.get_auth()
        if pass1 is None and pass2 is None:
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Users', content = render('user_edit_password.html')))
        else:
            encryptpw = WebAuth.set_password(pass1, pass2)
            if not encryptpw is None:
                WD.edit_user_password(str(id), encryptpw)
                self.redirect('/users')
            else: self.redirect('/error')

    def user_edit_role(self, id, role=None):
        user = self.get_auth()
        if role == None: 
            WD = Data() 
            roleid = WD.select_user(id)
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Users', content = WebCode.load_user_edit_role(roleid['role'])))
        else:
            WD = Data() 
            WD.edit_user_role(id, role)
            self.redirect('/users')

    def user_delete(self, id):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('user_delete.html', id = str(id)))

    def user_delete_confirm(self, id):
        WD = Data()
        WD.delete_user(id)
        self.redirect('/users')

    def help(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs =  WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Help', content = render('help.html')))
          
    def search(self, device=None):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Search Results', content = WebCode.search_devices(device)))

    def password(self, pass1=None, pass2=None):
        user = self.get_auth()
        if pass1 is None and pass2 is None:
            return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'), body = render('basic.html', title = 'Change Password', content = render('password_change.html')))
        else:
            changepw = WebAuth.change_password(user, pass1, pass2)
            if changepw is True: self.redirect('/settings')
            else: self.redirect('/error')

    def error(self):
        user = self.get_auth()
        return render('base.html', user = user, breadcrumbs = WebCode.breadcrumbs('settings'),  body = render('basic.html', title = 'Error', content = 'Error'))

def start_server():
    #WebCode.user_initialize() # Comment out to prevent the admin user from being created.
    app.start(controller)

#start_server()
