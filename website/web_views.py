class WebViews:
    def load_base(user, breadcrumbs, body):
        html = """<!DOCTYPE html><html>        
        <head>
        <title>Monitoring</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
        <link rel="stylesheet" href="/static/mon_app.css" type="text/css" />
        </head>
        <body>
        <div><div class="nav-sidebar">
        <a href="/" class="nav-button1"><svg viewBox="0 0 576 512"><path fill="currentColor" d="M488 312.7V456c0 13.3-10.7 24-24 24H348c-6.6 0-12-5.4-12-12V356c0-6.6-5.4-12-12-12h-72c-6.6 0-12 5.4-12 12v112c0 6.6-5.4 12-12 12H112c-13.3 0-24-10.7-24-24V312.7c0-3.6 1.6-7 4.4-9.3l188-154.8c4.4-3.6 10.8-3.6 15.3 0l188 154.8c2.7 2.3 4.3 5.7 4.3 9.3zm83.6-60.9L488 182.9V44.4c0-6.6-5.4-12-12-12h-56c-6.6 0-12 5.4-12 12V117l-89.5-73.7c-17.7-14.6-43.3-14.6-61 0L4.4 251.8c-5.1 4.2-5.8 11.8-1.6 16.9l25.5 31c4.2 5.1 11.8 5.8 16.9 1.6l235.2-193.7c4.4-3.6 10.8-3.6 15.3 0l235.2 193.7c5.1 4.2 12.7 3.5 16.9-1.6l25.5-31c4.2-5.2 3.4-12.7-1.7-16.9z"></path></svg></a>  
        <a href="/events" class="nav-button2"><svg viewBox="0 0 576 512"><path fill="currentColor" d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"></path></svg></a>
        <a href="/devices" class="nav-button3"><svg viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg></a> 
        <a href="/reports" class="nav-button4"><svg viewBox="0 0 512 512"><path fill="currentColor" d="M500 384c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H12c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v308h436zM372.7 159.5L288 216l-85.3-113.7c-5.1-6.8-15.5-6.3-19.9 1L96 248v104h384l-89.9-187.8c-3.2-6.5-11.4-8.7-17.4-4.7z"></path></svg></a>
        <a href="/settings" class="nav-button5"><svg viewBox="0 0 512 512"><path fill="currentColor" d="M444.788 291.1l42.616 24.599c4.867 2.809 7.126 8.618 5.459 13.985-11.07 35.642-29.97 67.842-54.689 94.586a12.016 12.016 0 0 1-14.832 2.254l-42.584-24.595a191.577 191.577 0 0 1-60.759 35.13v49.182a12.01 12.01 0 0 1-9.377 11.718c-34.956 7.85-72.499 8.256-109.219.007-5.49-1.233-9.403-6.096-9.403-11.723v-49.184a191.555 191.555 0 0 1-60.759-35.13l-42.584 24.595a12.016 12.016 0 0 1-14.832-2.254c-24.718-26.744-43.619-58.944-54.689-94.586-1.667-5.366.592-11.175 5.459-13.985L67.212 291.1a193.48 193.48 0 0 1 0-70.199l-42.616-24.599c-4.867-2.809-7.126-8.618-5.459-13.985 11.07-35.642 29.97-67.842 54.689-94.586a12.016 12.016 0 0 1 14.832-2.254l42.584 24.595a191.577 191.577 0 0 1 60.759-35.13V25.759a12.01 12.01 0 0 1 9.377-11.718c34.956-7.85 72.499-8.256 109.219-.007 5.49 1.233 9.403 6.096 9.403 11.723v49.184a191.555 191.555 0 0 1 60.759 35.13l42.584-24.595a12.016 12.016 0 0 1 14.832 2.254c24.718 26.744 43.619 58.944 54.689 94.586 1.667 5.366-.592 11.175-5.459 13.985L444.788 220.9a193.485 193.485 0 0 1 0 70.2zM336 256c0-44.112-35.888-80-80-80s-80 35.888-80 80 35.888 80 80 80 80-35.888 80-80z"></path></svg></a> 
        </div>
        <div class="search-div">
        <form id="searchform" action="search" method="GET">
        <svg viewBox="0 0 512 512" class="search-font"><path fill="currentColor" d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"></path></svg>
        <input type="text" name="device" class="text-input" style="width:120px" />
        <input type="button" class="search-button" value="Search" onclick="searchform.submit()" /></form>
        </div>
        <div class="mon-container">
        <div class="user-div">"""
        html += breadcrumbs + """| &nbsp;
        <svg class="user-font" viewBox="0 0 448 512"><path fill="currentColor" d="M224 256c70.7 0 128-57.3 128-128S294.7 0 224 0 96 57.3 96 128s57.3 128 128 128zm89.6 32h-16.7c-22.2 10.2-46.9 16-72.9 16s-50.6-5.8-72.9-16h-16.7C60.2 288 0 348.2 0 422.4V464c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48v-41.6c0-74.2-60.2-134.4-134.4-134.4z"></path></svg>
        &nbsp; <a href="/password">""" + user + """</a>&nbsp; (<a href="/logoff">Log Out</a>)</div>"""
        html += body + """</div></div><!--<script src="{% static 'mon_app/js/jquery.min.js' %}"></script>--></body></html>"""
        return html

    def load_refresh(url):
        html = """<div id="refresh"></div>
        <script>function refresh() {$.ajax({url: '""" + url + """', success: function(data) {$('#refresh').html(data);}});setTimeout(refresh, 60000);}    
        $(function(){refresh();});</script>"""
        return html

    def load_bc_home():
        html = """<svg class="bread-font" viewBox="0 0 576 512"><path fill="currentColor" d="M488 312.7V456c0 13.3-10.7 24-24 24H348c-6.6 0-12-5.4-12-12V356c0-6.6-5.4-12-12-12h-72c-6.6 0-12 5.4-12 12v112c0 6.6-5.4 12-12 12H112c-13.3 0-24-10.7-24-24V312.7c0-3.6 1.6-7 4.4-9.3l188-154.8c4.4-3.6 10.8-3.6 15.3 0l188 154.8c2.7 2.3 4.3 5.7 4.3 9.3zm83.6-60.9L488 182.9V44.4c0-6.6-5.4-12-12-12h-56c-6.6 0-12 5.4-12 12V117l-89.5-73.7c-17.7-14.6-43.3-14.6-61 0L4.4 251.8c-5.1 4.2-5.8 11.8-1.6 16.9l25.5 31c4.2 5.1 11.8 5.8 16.9 1.6l235.2-193.7c4.4-3.6 10.8-3.6 15.3 0l235.2 193.7c5.1 4.2 12.7 3.5 16.9-1.6l25.5-31c4.2-5.2 3.4-12.7-1.7-16.9z"></path></svg>
        &nbsp;&nbsp;Home&nbsp;"""  
        return html

    def load_bc_devices():
        html = """<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>
        &nbsp;&nbsp;Devices&nbsp;&nbsp;"""   
        return html

    def load_bc_device(name):
        html = """<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>
        &nbsp;&nbsp;<a href="/devices">Devices</a>&nbsp;>&nbsp;""" + name + """&nbsp;"""  
        return html

    def load_bc_device_graph(name, monitor):
        html = """<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>
        &nbsp;&nbsp;<a href="/devices">Devices</a>&nbsp;>&nbsp;<a href="/devices/""" + name + """">""" + name + "</a>&nbsp;>&nbsp;" + monitor + """&nbsp;"""
        return html

    def load_bc_events():
        html = """<svg class="bread-font" viewBox="0 0 576 512"><path fill="currentColor" d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"></path></svg>    
        &nbsp;&nbsp;Events&nbsp;"""  
        return html

    def load_bc_reports():
        html = """<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M500 384c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H12c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v308h436zM372.7 159.5L288 216l-85.3-113.7c-5.1-6.8-15.5-6.3-19.9 1L96 248v104h384l-89.9-187.8c-3.2-6.5-11.4-8.7-17.4-4.7z"></path></svg>
        &nbsp;&nbsp;Reports&nbsp;"""  
        return html

    def load_bc_settings():
        html = """<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M444.788 291.1l42.616 24.599c4.867 2.809 7.126 8.618 5.459 13.985-11.07 35.642-29.97 67.842-54.689 94.586a12.016 12.016 0 0 1-14.832 2.254l-42.584-24.595a191.577 191.577 0 0 1-60.759 35.13v49.182a12.01 12.01 0 0 1-9.377 11.718c-34.956 7.85-72.499 8.256-109.219.007-5.49-1.233-9.403-6.096-9.403-11.723v-49.184a191.555 191.555 0 0 1-60.759-35.13l-42.584 24.595a12.016 12.016 0 0 1-14.832-2.254c-24.718-26.744-43.619-58.944-54.689-94.586-1.667-5.366.592-11.175 5.459-13.985L67.212 291.1a193.48 193.48 0 0 1 0-70.199l-42.616-24.599c-4.867-2.809-7.126-8.618-5.459-13.985 11.07-35.642 29.97-67.842 54.689-94.586a12.016 12.016 0 0 1 14.832-2.254l42.584 24.595a191.577 191.577 0 0 1 60.759-35.13V25.759a12.01 12.01 0 0 1 9.377-11.718c34.956-7.85 72.499-8.256 109.219-.007 5.49 1.233 9.403 6.096 9.403 11.723v49.184a191.555 191.555 0 0 1 60.759 35.13l42.584-24.595a12.016 12.016 0 0 1 14.832 2.254c24.718 26.744 43.619 58.944 54.689 94.586 1.667 5.366-.592 11.175-5.459 13.985L444.788 220.9a193.485 193.485 0 0 1 0 70.2zM336 256c0-44.112-35.888-80-80-80s-80 35.888-80 80 35.888 80 80 80 80-35.888 80-80z"></path></svg>
        &nbsp;&nbsp;Settings&nbsp;"""  
        return html

    def load_login():
        html = """<!DOCTYPE html>
        <html>
        <head><title>Monitoring</title>
        <link rel="stylesheet" href="/static/mon_app.css" />
        </head>
        <body style="background-color:#325D88">
        <br />
        <br />
        <div style="display:flex;justify-content:center">
        <table style="width:300px"><tr><td>
        <div class="card-div">
        <div class="card-header">Monitoring Login</div>
        <table style="width:100%;">
        <tr>
        <td style="padding-left:10px">
        <form action="verify" method="POST">
        <table>
        <tr><td style="width:150px">Username</td><td style="width:150px"><input type="text" class="text-input" name="username" /></td></tr>
        <tr><td>Password</td><td><input type="password" class="text-input" name="password" /></td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Login" /></td></tr>
        </table>
        </form>
        </td></tr></table> 
        </div></td></tr></table>
        </div>
        </body>
        </html>"""
        return html

    def load_basic_page(title, content):
        html = """<table style="width:100%;"><tr><td>
        <div class="card-div">
        <div class="card-header">""" + title + """</div>
        <table style="width:100%;">
        <tr>
        <td style="padding-left:10px">
        """ + content + """
        </td></tr></table> 
        </div></td></tr></table>"""
        return html

    def load_device_content(system, data):
        html = """<table style="width:100%;">
        <tr><td colspan="4" style="padding-bottom:4px;text-align:left">
        <div class="card-div" style="height:45px">
        <div class="card-header">System Information</div>
        <div style="padding-left: 10px">
        """ + system + """
        </div></div></td></tr>
        """ + data + """
        </table>"""
        return html

    def load_events_content(summary, events):
        html = """<table style="width:100%;">
        <tr><td><div class="card-div">
        <div class="card-header">Event Summary</div>
        """ + summary + """ 
        </div></td></tr>
        <tr><td style="text-align: left;padding-top:8px">
        <div class="card-div">
        <div class="card-header">Events</div>
        """ + events + """    
        </div></td></tr></table>"""
        return html

    def load_change_password():
        html = """
        <form action="" method="POST">
        <table>
        <tr><td style="width:150px">Old Password</td><td style="width:150px"><input type="password" class="text-input" name="pass1" /></td></tr>
        <tr><td>New Password</td><td><input type="password" class="text-input" name="pass2" /></td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Submit" /></td></tr>
        </table>
        </form>"""
        return html

    def load_user_add():
        html = """
        <form action="" method="POST">
        <table>
        <tr><td style="width:150px">Username</td><td style="width:150px"><input type="text" class="text-input" name="username" /></td></tr>
        <tr><td>New Password</td><td><input type="password" class="text-input" name="password" /></td></tr>
        <tr><td>Role</td><td><input type='radio' name='role' value='0' /> User <input type='radio' name='role' value='1' /> Admin</td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Submit" /></td></tr>
        </table>
        </form>"""
        return html
    
    def load_user_edit_password():
        html = """
        <form action="" method="POST">
        <table>
        <tr><td style="width:150px">Old Password</td><td style="width:150px"><input type="password" class="text-input" name="pass1" /></td></tr>
        <tr><td>New Password</td><td><input type="password" class="text-input" name="pass2" /></td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Submit" /></td></tr>
        </table>
        </form>"""
        return html
    
    def load_user_edit_role(role):
        html = """
        <form action="" method="POST">
        <table>
        <tr><td>Role</td>
        <td>"""
        if role == 0: html += "<input type='radio' name='role' value='0' checked='checked' /> User<input type='radio' name='role' value='1' /> Admin" 
        else: html += "<input type='radio' name='role' value='0' /> User<input type='radio' name='role' value='1' checked='checked' /> Admin"
        html += """</td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Submit" /></td></tr>
        </table>
        </form>"""
        return html

    def load_confirm_delete(id):
        html = """
        <table>
        <tr><td>Are you sure you want to delete this user? &nbsp;
        <input type="button" onclick="window.location.href='/user_delete_confirm/""" + str(id) + """'" class="action-button" value="Yes" /> 
        <input type="button" onclick="window.location.href='/users/'" class="action-button" value="No" />
        </td></tr>
        </table>"""
        return html

    def load_reports():
        html = """
        <table style='width:100%'>
        <tr><td><b>Device Report:</b> An overview of all device configuration data.</td>
        <td style='text-align:right'>
        <input type="button" onclick="window.location.href='/report/devices.html'" class="action-button" value="html" />&nbsp;
        <input type="button" onclick="window.location.href='/report/devices.csv'" class="action-button" value="csv" />
        </td></tr>
        <tr><td><b>Event Report:</b> An export of all open events.</td>
        <td style='text-align:right'>
        <input type="button" onclick="window.location.href='/report/events.html'" class="action-button" value="html" />&nbsp;
        <input type="button" onclick="window.location.href='/report/events.csv'" class="action-button" value="csv" />
        </td></tr>
        </table>
        """
        return html

    def load_help():
        html = r"""
        <h2 id='top'>Table of Contents</h2>
        <b><a href='#intro'>Introduction</a></b><br />
        <b><a href='#agent'>Agent</a></b><br />
        &nbsp;-<a href='#agent_settings'>Settings</a><br />
        <b><a href='#collector'>Collector</a></b><br />
        &nbsp;-<a href='#collect_settings'>Settings</a><br />
        <b><a href='#event'>Event Engine</a></b><br />
        &nbsp;-<a href='#event_settings'>Settings</a><br />
        <b><a href='#website'>Website</a></b><br />
        &nbsp;-<a href='#website_main'>Main</a><br />
        &nbsp;-<a href='#website_devices'>Devices</a><br />
        &nbsp;-<a href='#website_events'>Events</a><br />
        &nbsp;-<a href='#website_reports'>Reports</a><br />
        &nbsp;-<a href='#website_settings'>Settings</a><br />
        &nbsp;-<a href='#website_server'>Web Server</a><br />
        <br />
        <h2 id='intro'>Introduction</h2>
        The monitoring application consist of four major components (Agent, Collector, Event Engine, and Website).  These components 
        work together to perform basic monitoring. This guide is to help you better understand how the components function.
        <br /><br /><b><a href='#top'>top</a></b></br />
        <h2 id='agent'>Agent</h2>
        The Agent is one of the most complex components.  It collects data and creates events based on configuration settings and it 
        syncs the data to the collector.  Every Minute the agent polls for new performance data.  It then logs this data in a SQLite 
        database.  It reviews the rules provided by the configuration settings, and then it connects to the collector to send data. 
        If the data is delivered successfully, the collector will send a response and the agent will mark data as sent.  If the agent 
        can't communicate, it will continue to log the data locally.  
        <br />
        <h3 id='agent_settings'>Settings</h3>
        The agent settings file (monitoring\agent\settings.cfg) is the most complex settings file.  <br />
        <h4>Server Communications</h4>
        In settings.cfg the following three line control server communications.  These line work in conjunction with the collector 
        and must be configured correctly on both in order to work. <br />
        server: 10.211.55.17 - This is where the agent sends data (ie the collector's IP). <br />  
        port: 8888 - This is the connection port that the agent and collector share.<br />
        secure: 0 - Setting this to 1 Enables SSL/TLS 1.2.  This setting must be identical on the collector.<br />
        <h4>Monitoring Services</h4>
        The services variable designates what services to be monitored.  To monitor services list whatever services you would like 
        monitored in a comma seperated list. Ex.<br />
        services: Spooler,LanmanServer<br />
        <h4>Event Management</h4>
        Agents control what events get sent forward and the configuration is defined here.  The agent ships with a predefined 
        list to help you out.  In settings.cfg you will see several lines that look like this: <br />
        thresh: perf.filesystem.c.percent.free,4,15,<,900.<br /><br />
        What this means is monitor,severity,threshold,operator,duration.  The monitor is predefined and only set monitors can be used.  
        The severity can be 1 - Critcal, 2 - Major, 3 - Warning, 4 - Informational.  The threshold depends on the monitor although many 
        are percentages 0-100.  The operator defines if you want to trigger for greater than or less than the threshold.  For services 
        only equals is allowed.  And lastly is the duration (in seconds) to check for when creating an event.  
        <br /><br /><b><a href='#top'>top</a></b></br />  
        <h2 id='collector'>Collector</h2>
        The collector works hand in had with the agent and it's configuration reflects this.  Like all of the other components, 
        the collector also runs as a Windows service and can be controlled via services.msc or net start/stop.
        <br />
        <h3 id='collect_settings'>Settings</h3>
        The collector has serveral settings.  THese mainly configure the socket and create the connection to the database.  <br />
        database:monitoring - This is the database that the application is connecting to.<br />
        dbhost:localhost -  This is the host of the database.<br />
        dbpassword:test - This is the password of the DBO.<br />
        dbuser:test - This is the username of the DBO.<br />
        mon_port:8888 -This is the port that the agents connect to.<br />
        secure:0 - This is the security level that the collector and the agent communicate on (1=SSL, 0=non-SSL)<br />
        mon_server:10.211.55.17 - This is the host IP of the collector.
        <br /><br /><b><a href='#top'>top</a></b></br />
        <h2 id='event'>Event Engine</h2>
        The Event engine does a little less than what it's name implies.  It does however still do some event processing.  It's main 
        job is to process notifications, and create and delete availability events.  So if a agent stops responding, it will create 
        an event based on the time that the agent has stopped communicating.  
        <h3 id='event_settings'>Settings</h3>
        Like the other modules, all configurations are maintained in the settings.cfg file.<br /><br />
        availability_check:300 - This is the duration in seconds that the server will wait before opening an agent down event<br />
        availability_severity:1 - This is the severity that the server will assign to an agent down event (1 - Critcal, 2 - Major, 3 - Warning, 4 - Informational).<br />
        database:monitoring - This is the database that the application is connecting to.<br />
        dbhost:localhost -  This is the host of the database.<br />
        dbpassword:test - This is the password of the DBO.<br />
        dbuser:test - This is the username of the DBO.<br />
        mailactive:0 - If mail is being sent then this needs to be set to 1.<br />
        mailadmin:admin@monitoring - This is the address that the mail will come from.<br />
        mailserver:localhost - This is the mail relay server's address
        <br /><br /><b><a href='#top'>top</a></b></br />
        <h2 id='website'>Website</h2>
        The website is the most user interactive component of the monitoring application and consists of several sections.  This guide will 
        briefly cover each section.<br />
        <h3 id='website_main'>Main</h3>
        This section includes the main page when you log in.  On the main page there is an overview of of the agents, events, and the 
        monitoring server.<br />
        <h3 id='website_devices'>Devices</h3>
        The device pages include a device list and individual pages for each device reporting.  On these pages you can drill down 
        an additional level to see performance graphs. <br />
        <h3 id='website_events'>Events</h3>
        The events page displays all open and closed events.  Events on these pages can be opened or closed as well.<br />
        <h3 id='website_reports'>Reports</h3>
        The reporting page includes all available reports (currently None)<br />
        <h3 id='website_settings'>Settings</h3>
        The settings page contains the user guide along with user and notification management.<br />
        <h4>User Management</h4>
        Users can be added, changed, and removed from the user management tool <a href='/users'>here</a>.  To add a user select 
        Add User.  You are required to fully fill out the form including the username, password, and role.  You also have the options 
        to change a user's password or roles in this section.  And lastly you can delete a user.  There is a confirmation screen 
        when deleting a user.  If the admin user is deleted, the application will create a new one with the default username admin 
        and password, password.  If you are locked out of the system, you can delete the admin user in MySQL from the user's table 
        and it will recreate the user when the server is restarted.<br />
        <h4>Notification Management</h4>
        You can control who receives notifications <a href='/notify'>here</a>.  While internal events are created on the agent or 
        through the event engine, this section defines who notifications are sent to.  The hostname and monitor textboxes can take 
        wildcards.  To use a wildcard simple type %_%.  Email notifications have to also be enabled on the event engine to send. <br />
        <br />
        To send out all critical events on all systems, you can create a rule with your email address, '%_%' for hostname and monitor, 
        select status open, severity Critical, and set enabled to True.<br />
        <h3 id='website_server'>Web Server</h3>
        The website utilizes <a href='https://github.com/philipcwhite/webserver'>wserver</a> for handling requests.  In the Windows 
        environment the website runs as a Windows service called 'Monitoring Website'.  It can be started or stopped using services.msc 
        or by running net commands: net start (or stop) monitoringweb.  The website can be configured through the settings.cfg file included 
        in the application website directory (\monitoring\website\).<br />
        <h4>SSL</h4>
        Secure Sockets Layer (SSL) can be controlled through four settings.  <br />
        ssl_enabled: True/False - Determines if the server should use SSL.  SSL is run as TLS 1.2.<br />
        server_port: 80 - If enabling SSL, change this to 443 or any port not in use<br />
        cert_key: localhost.pem - Here you can specify the certificate key.  By default it uses the provided localhost key stored in \monitoring\certificates\ <br />
        cert_name: localhost.crt - Here you can specify the certificate.  By default it uses the provided localhost certificate stored in \monitoring\certificates\ <br />
        <h4>Database</h4>
        The next four settings are for configuring the MariaDB(MySQL)<br />
        db_host: localhost<br /> 
        db_name: monitoring<br />
        db_user: test<br />
        db_password test<br />
        <h4>Session</h4>
        The last setting controls the application session timeout in seconds.  This determines how long a user's session is live. 
        User sessions are also controlled via cookies.  The cookie duration is the same as the session.<br />
        session_expire: 7200
        <br /><br /><b><a href='#top'>top</a></b></br />"""

        return html
