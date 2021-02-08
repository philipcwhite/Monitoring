# Monitoring ver. 0.04b
Monitoring Server and Agents written in Python

## About
The goal of this project is to make a monitoring tool that provides good functionality and is relatively easy to deploy and use.  It has evolved from a Windows based VB.Net project to a its current itteration written in Python to support mulitiple platforms.  This repository contains the code for the monitoring web server, collect and event engines, and agents.  It is a early beta at this point however most of the functionality is working.  

### The Monitoring Server
The monitoring server is composed of three services: the website, the collect engine, and the event engine.  These services all connect to a MySQL (MariaDB) backend.  The website coded in pure Python and runs on a custom server.  It's main purpose is for viewing the event data although it provides user, notification policy, and event administration.  The collect engine mainly acts as a gateway to translate TCP/SSL data from agents into SQL records.  It does some event management as well when it is processing incoming events.  The event engine takes care of agent down events and processes notifications.  Notifications are by default logged and can be sent to a SMTP server.  

### The Windows Agent
The Windows agent collects data via WMIC and processes events locally.  It stores its data in a SQLite database which allows the agent to maintain state even after reboots and system crashes.  Data is transferred via TCP (or TCP/SSL) to the Collect Engine on the Monitoring Server.  All data transmissions require a response from the Collect Server to assure data has been transferred.  If the Agent does not receive a response it will keep trying to send the data until it succeeds.  Data is transferred via TCP over port 8888 (non-SSL by default).  Agent configuration and thresholds are maintained locally on the agent.  The agent receives no configuration or commands from above.  This is designed by default to allow agents to function in a secured environment.

### The Linux Agent
The Linux agent works very similarly to the Windows version.  Instead of WMIC, it uses basic system calls like free, top, df, etc.  I have done basic testing for this agent on both elementary OS (Ubuntu) and Centos.  There are a couple of differences in the actual monitors but overall it provides about the same level of funtionality.
 
## Screenshots

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring/master/images/home.png)
Home View

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring/master/images/device.png)
Device View

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring/master/images/graph.png)
Graph View

## Updates
2/8/2021 - I updated the Linux code handling events.  I am still testing this as it may break thresholds that use equals.  

2/4/2021 - I updated a large part of the Linux agent code.  Functionality should be identical but I changed how parameters are stored and cleaned up the network monitoring logic.

2/3/2021 - The app is now working with Python 3.9.1.  

1/25/2021 -  I started reimplementing roles in Flask.  The only change at this point is a new session entry and a rule block on the users page for non-admin roles.  

1/4/2021 - I cleaned up some of the agent, collector, and event engine code today.  

12/31/2020 - I finished my table cleanup on the website.  I plan on updating some of the documentation today and calling it a year.  Next week I'll start on refreshing the agent and backend code.  Have a great new year.

12/30/2020 - I cleaned up the work log and finished removing all of the HTML I needed to remove from the model.  I still have a handful of pages to clean up tables but it should be done soon.  I'm looking forward to updating the agents and backend code.  

12/30/2020 - Still updating templates.  Corrected  issues with user and notification add pages.  I should be done with the UI updates soon.  I'll probably put out a release after I finish the majority of the template work.  I also plan on doing some cleanup in the agent and collection code.  I know this can be improved.

12/24/2020 - Happy Holidays.  I updated the events template today to divs and moved the HTML code from the backend to the template.  Cleanup is going well.  About 1/3 of the way through removing tables and moving code into templates.  

12/15/2020 - I removed all tables from the index display page.  Now it is running with divs/css.  I also changed the host list display to iterate through a dict in jinja2.  I still have quite a bit of clean up to do but it's coming along.

12/7/2020 - I'm updating how I'm displaying the SVG icons as part of the CSS refresh.   

12/2/2020 - I deployed the monitoring server to a hosted VPS today.  I did a full deploy with an agent, collector, event engine, DB, and two websites.  Worked like a charm on a 1 CPU, 1 GB Ram server.  This was a good test because now I see some mobile browser issues that need some TLC.  The Flask UI is also missing role based permissions.  These are coming.  

12/1/2020 - I started updating the appearance of the site.  I think it looks a bit more professional.  I'll update screenshots when done as they are very dated.  I still need to do a lot of cleanup especially with the html templates.  I tend to be old school and overuse tables.  

11/28/2020 - I updated the mserver install file for flask/gunicorn.  I'll update directions soon.  Thanks.

11/27/2020 - I finished converting the website to Flask.  There is still a little clean up left to do.  I did make one minor change to the database changing the username field in users to user.  After I do a little cleanup I'm rewrite the mserver install script and post a download. I know this is more of a stability release rather than a feature set but I think it was worth it.  Also I'm debating jumping on the open telemetry project.  Not sure if I'll integrate it in or build a seperate app for it.  Probably too much work for one dev.  :)

11/25/2020 - I'm about 80% converted to Flask on my test site.  I'm going to start uploading changes.  These will break alot of things so do not try to run from source.  I'm testing the site in a subdirectory call monitoring and lot of the links will be broken.  All of this should be fixed in a few days.  The install code will have to be updated as well however it shouldn't be too bad to fix.  This conversion has been a ton of work but overall this has given me a chance to fix a lot of bad code.  There is still quite a bit in there but I'm slowly improving things.  Current db structure remains the same.

11/24/2020 - I am in the process of switching the web server over to using Flask.  While the current web server works fine, I feel this will improve the security and stability of the platform.      

10/1/2020 -  I made some changes to the structure of the app in Github and corrected a few errors.  I am no longer going to code/support the Windows server install.  The Linux files for the server component should work in Windows with a few minor changes.  I'm making this decision so I have more time to work on the app and less time on porting changes between platforms.  

8/21/2020 - Lots of code updates today.  I'm mostly doing code cleanup.  I removed about 40 lines of code and changed some of my string concatenations.  If all goes well, release 0.4b should be ready in the next month.  I have a few more bug fixes, and then I have to test/fix for Windows.  

7/31/2020 - I templated the index page and added rounded corners to the rectangle status block.  

7/17/2020 - Updated the Linux install script.  Some changes break running the server on Windows.  When I finish updating the code, I'll fix these changes for Windows.    

7/17/2020 - I'm continuing to clean up code.  Currently a few things are broken due to this.  I've managed to remove several hundred lines of code and have transistioned even more to templates.  I changed the order of how the app starts up to using a preload file (start.py).  This allows the variables to be populated prior to the database being instantiated. It's not perfect but it's getting better. I'll probably enhance the template engine at some point so even more HTML can be moved out of the backend code.

7/15/2020 - I'm currently doing a huge overhaul of the code.  The current source code works for the most part, but will not install with the installer. If you want a working release please download one of the release packages.  Trying to package some of my modules and clean up code.  I also started work on a template engine so I plan on removing a lot of the HTML from code.  So far I've been able to remove about 200 lines of code, mostly on the database side.  

7/13/2020 - Updated the Linux agent.  Removed over 50 lines of code.  Changed how SQL queries flow.  AgentSQL class now takes care of opening and closing connections (__init__/__del__).  I'll try to migrate these to the Windows agent next and then update the server which will be a bit different going to MySQL.    

5/12/2020 - Still continuing to update code.  Made minor changes today.  

1/23/2020 - Sorry for the lack of updates.  I took a new job and moved across the country.  I noticed I need to make some updates for Python 3.8 and probably put in a setting to allow the version to be a variable in the installs.  I should have updates soon.  Thanks
