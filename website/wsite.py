from wserver import app
from web_auth import WebAuth
from web_views import WebViews
from web_data import WebData
from web_code import WebIndex, WebDevice, WebDevices, WebEvents, WebNotify, WebSettings, WebSearch, WebUsers


class controller(object):
  
    def verify(self,username=None,password=None):
        user = WebAuth.verify_auth(username, password)
        if not user is None:
            self.login(username)
            self.redirect('/')
        else:
            self.redirect('/login')

    def login(self):
        html = WebViews.load_login()
        return html

    def logoff(self):
        self.logout(self.get_user())
        self.redirect('/login')

    def index(self, page=1):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_home(), WebViews.load_refresh('/index_content/' + str(page)))
        return html
    
    def index_content(self, page=1):
        user = self.get_auth()
        html = WebIndex.index_content(str(page))
        return html

    def events(self, status=1):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_events(), WebViews.load_refresh('/events_content/' + str(status)))
        return html

    def events_content(self, status=1):
        user = self.get_auth()
        html = WebEvents.events_content(status)
        return html

    def event_change(self, id, status):
        user = self.get_auth()
        WebData.web_code_change_event_status(id, status)
        self.redirect('/events')

    def devices(self, name=None, monitor=None):
        user = self.get_auth()
        if name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_devices(), WebViews.load_basic_page('Devices', WebDevices.device_index()))
        elif not name is None and monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_device(name), WebViews.load_refresh('/device_content/' + name))
        elif not name is None and not monitor is None:
            html = WebViews.load_base(user, WebViews.load_bc_device_graph(name, monitor), WebViews.load_refresh('/device_graph_content/' + name + '/' + monitor))
        return html
    
    def device_content(self, name):
        user = self.get_auth()
        html = WebDevice.device_content(name)
        return html

    def device_graph_content(self, name, monitor):
        user = self.get_auth()
        html = WebDevice.device_graph_content(name, monitor)
        return html
    
    def reports(self):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_reports(), 'reports')
        return html

    def settings(self):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(),  WebViews.load_basic_page('Settings', WebSettings.settings()))
        return html
    
    def notify(self):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Notification Rules', WebNotify.notify_rules()))
        return html
    
    def notify_add(self, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user = self.get_auth()
        html=''
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Add Notification Rule', WebNotify.notify_add()))
            return html
        else:
            WebData.web_code_insert_notifyrules(notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            self.redirect('/notify')

    def notify_edit(self, id, notify_name = None, notify_email = None, agent_name = None, agent_monitor = None, agent_status = None, agent_severity = None, notify_enabled = None):
        user = self.get_auth()
        html=''
        if notify_name is None and notify_email is None and agent_name is None and agent_monitor is None and agent_status is None and agent_severity is None and notify_enabled is None:
            html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Edit Notification Rule', WebNotify.notify_edit(id)))
            return html
        else:
            WebData.web_code_update_notifyrules(id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled)
            self.redirect('/notify')

    def notify_delete(self, id):
        user=WebAuth.check_auth()
        WebData.web_code_delete_notify_rule(id)
        self.redirect('/notify')

    def users(self):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Users', WebUsers.users_list()))
        return html

    def user_add(self, username=None, password=None, role=None):
        user = self.get_auth()
        if not username is None and not password is None and not role is None:
            WebUsers.user_add(username, password, role)
            self.redirect('/users')
        else:
            html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Users', WebViews.load_user_add()))
            return html

    def user_edit_pass(self, id, pass1=None, pass2=None):
        user = self.get_auth()
        if pass1 is None and pass2 is None:
            html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Users', WebViews.load_user_edit_password()))
            return html
        else:
            user_data = WebData.web_code_select_user(id)
            print(id, user_data['username'], pass1, pass2)
            changepw = WebAuth.change_password(user_data['username'], pass1, pass2)
            if changepw is True:
                self.redirect('/users')
            else:
                self.redirect('/error')

    def user_edit_role(self, id, role=None):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Users', 'Users'))
        return html

    def user_delete(self, id):
        user = self.get_auth()
        #Add confirmation Page
        self.redirect('/users')
          
    def search(self, device=None):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Search Results', WebSearch.search_devices(device)))
        return html

    def password(self, pass1=None, pass2=None):
        user = self.get_auth()
        if pass1 is None and pass2 is None:
            html = WebViews.load_base(user, WebViews.load_bc_settings(), WebViews.load_basic_page('Change Password', WebViews.load_change_password()))
            return html
        else:
            changepw = WebAuth.change_password(user, pass1, pass2)
            if changepw is True:
                self.redirect('/settings')
            else:
                self.redirect('/error')

    def error(self):
        user = self.get_auth()
        html = WebViews.load_base(user, WebViews.load_bc_settings(),  WebViews.load_basic_page('Error', 'Error'))
        return html

def start_server():
    app.start(controller)


    
