# Monitoring ver. 0.01b
Monitoring Server and Agents written in Python

## About
The goal of this project is to make a tool that provides good functionality and is relatively easy to deploy and use.  I come from a Windows background so the initial focus of the tool is for Windows based monitoring.  Also, I know how bleak the options are for Windows based monitoring tools so it fills a nice void.  That being said, I do plan to add Linux support as well.

This repository contains the code for the monitoring web server, collect and event engines, and a Windows agent.  It is a early beta at this point however most of the functionality is working.  

### The Monitoring Server
The monitoring server is composed of three services: the website, the collect engine, and the event engine.  These services all connect to a MySQL (MariaDB) backend.  The website coded in pure Python and runs on CherryPy as a Windows service.  It's main purpose is for viewing the event data although it provides user, notification policy, and event administration.  The collect engine mainly acts as a gateway to translate TCP/SSL data from agents into SQL records.  It does some event management as well when it is processing incoming events.  The event engine takes care of agent down events and processes notifications.  Notifications are by default logged and can be sent to a SMTP server.  

### The Windows Agent
The Windows agent collects data via WMIC and processes events locally.  It stores its data in a SQLite database which allows the agent to maintain state even after reboots and system crashes.  Data is transferred via TCP (or TCP/SSL) to the Collect Engine on the Monitoring Server.  All data transmissions require a response from the Collect Server to assure data has been transferred.  If the Agent does not receive a response it will keep trying to send the data until it succeeds.  Data is transferred via TCP over port 8888 (SSL by default).  Agent configuration and thresholds are maintained locally on the agent.  The agent receives no configuration or commands from above.  This is designed by default to allow agents to function in a secured environment.

## Screenshots

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/home.png)
Home View

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/device.png)
Device View

## Updates

10/11/2018 - Updated Notification Rules web pages.  SQL code, some app code, and some templates are done.  I still need to make the add/edit pages.

10/9/2018 - Added some code for managing notifications.  I still need to create templates and add some code for processing.  I've been experimenting with writing my own python webserver as well.  This probably won't be used for this project or revision though.    

10/5/2018 - Added the ability to view closed events and re-open them if needed.  No functionality is currently role locked.  This will be added in a future update.  Updated the About section.

10/5/2018 - Devices, graphing, and the event view are back.  I hope to have the first Windows beta release out in a week or so.  

10/4/2018 - I started a massive rewrite of the webserver using CherryPy.  A lot of the existing functionality is currently missing.  I am working to add this back as soon as possible.  I was going to hold off on updating the code repository but this is the direction I am moving in so I am keeping the project up to date.  I've also cleaned up a lot of the template code and fixed a lot of bugs in the website and collector.  As this gets closer to an official release I will post more detailed documentation on how things work.  I am planning on using InnoSetup for windows to build an installable package for both the agent and server.  I am not a Linux expert so and Linux development will come in a later release.

So what has been done/ported?  The main framework for the site has been moved over.  Pages are there but many are blank.  The event engine and collector are both working.  On the website, I have built a simple cookie/session authentication system.  There is room for improvement here but it is working.  The website runs as a Windows service.  Currently off the default 8080 port.  SSL will be configured later.  No need for Apache, IIS, etc. :)

Time for sleep.  So much more coding left to do...

10/01/2018 - One of the main points of building this app was to make it user friendly.  I think I sadly failed when I incorporated Django.  It's a wonderful framework but I'm not sure I can make a simple deployable package using it.  I know how to make it work but I can see someone who is not a Python coder banging their head on the wall trying to get it to work.  For this reason I'm backpeddling.  I have been working with CherryPy all day and I may go this route if I can get authentication and authorization working.  It is a huge and painful rewrite but it makes the app so much easier for end users (maybe a little harder for me).  

10/01/2018 - Linked to notifications page.  Minor changes.

09/29/2018 - I added forms for modifying notification policies and a password change form.  Not everything is currently linked or stylized at this point.  For the Notification policies I added drop down forms for agent selection and monitor selection.   

09/28/2018 - Updated the Agent and Server services.  The EventService now creates events for agent down.  The first beta should be out in a few weeks.  I still have some work left to do on the website and some code cleanup.  The first release will be more or less a milestone rather than a fully useable product.  There are still a lot of things I need to do.  Django can sometimes be tricky to deploy so I would like to find a better way to release the web server.  Perhaps wrapping Django in CherryPy.  Ease of use is a big priority.  I'll probably use inno setup for the Windows build to do some of the deployment.  

09/27/2018 - Set the event engine to log and email events.  Email can be turned on via the settings.cfg file.  This will all be documented before the first beta release.

09/26/2018 - Repackaged the collector and event engine in the same directory "services".  No real changes to the collector however the event engine is now working.  As of now it just outputs a file to the service directory.  It will eventually send emails.  As of now filters can only be added via the django admin.  It will accept "%_%" for wildcards.  I will be adding a page in the web GUI for adding notification policies.  I am hoping to have a beta release ready in the next few weeks.   

09/25/2018 - Added processed field to agentevents and notifyrule table for event processing.  The processed field is what the event engine will queue off of to process notifications.  The event engine will serve two tasks.  It will generate events when agents have not responded, and it will process event rules.  In this iteration of the application rules will be based off matching event text.  

09/24/2018 - Added paginatation to the index view.  Removed Subscriptions.  Soon to be replaced with Notifications.

09/22/2018 - Updated device page and CSS.

09/21/2018 - I fixed the collector's config file issue.  I still need to encrypt the db password however it's coming along nicely.  I also added back graphs.  They can be accessed currently via the individual device page as links from performance metrics.  I plan to do more with these as time permits.

09/20/2018 - I fixed the collector service so that it now can stop via windows services.  I still need to fix the config file for this and clean up some code.  I removed asyncio from the agent as it wasn't improving performance dramtically and it just made for having more requirements.  I will add it back if it improves performance.

09/17/2018 - Lots of updates today.  I updated the collector.  It now will run as a Windows service with configuration files.  

09/17/2018 - Added search functionality.  Search now returns matching hostnames.  Also added in login_required.  

09/17/2018 - Cleaned up some code.  Finished web templates for Events and Devices.

09/17/2018 - Massive update.  I probably added a few bugs during this.  Some old features may temporarily be missing but will be added back (graphing).  I updated much of the design/theme of the site.  Many of these upgrades are to improve performance and improve useability.  

09/13/2018 - Fixed minor agent bug removing old events.

09/12/2018 - I enabled user authentication.  Still very early with no authorization.  

09/12/2018 - I rewrote much of the agent event code over the past two days.  The Agent now generates and sends events to the collector.  Events also update severity rather than generating new events for each level hit.  The WMI code is now finally gone.  I missed some code on the last clean up.  I also removed a ton of the server side thresholding code.  Some of this will be added back for agent alerts, however most of it is gone for good.  I made a ton of progress on the agent so I'll probably be focusing more time on the server in the coming days.

09/10/2018 - I removed all of the WMI codefrom the agent.  The agent is now using WMIC.  I still have a few monitors to recreate in WMIC and a lot of testing to do.  This removes all dependencies outside the standard Python library.  While the WMI module was great to use, it made deploying the agent a bit harder.  I also moved the OS specific code to a seperate Python file so that much of the existing code can be reuseable if/when I decide to make a Linux agent.  On the server side I have some work to do on correctly processing events.  IE closing based on severity.  

09/10/2018 - Agent has now been updated to create/send events to the server.  I still have a few bugs to track down and timestamp conversions to take care of but it is looking promising.  There will still be some server side event handling.  this will mostly be for agent up/down and cleaning old events.  There is still lots of code that needs to be cleaned up from the overhaul that I recently did.  

09/08/2018 - We have a huge update with lots of broken code everywhere.  I decided to move the bulk of the event engine to the agents to save on processing power on the server.  This is about halfway there.  I also decided to move from an in-memory list to using sqlite.  If an agent goes down, it will maintain some level of state depending on how long it is down for.  Also the amount of data that can be stored before sending has now increased.  The agent itself should work at this point however the event module hasn't been tied in.  Monitoring thresholds are now configurable in the thresholds.cfg file.  I also started to migrate some of the code away from the WMI module.  I may use a more OS independent module in the future or figure how to write all of the performance code natively to avoid importing packages that are not part of the base python install.  I've spend far too many hours playing with pyinstaller, cx_freeze, etc, trying to make a nice deployable package.  

09/04/2018 - I started coding the event engine today.  I also changed the version from beta to alpha.  I still have quite a way to go before this is fully working.  Hopefully cx_freeze is updated for Python 3.7 by the time we have a release.  :)

09/04/2018 - I updated the Agent level thresholds today.  This gives me enough info on the web side to begin coding the event engine.  

09/03/2018 - I continued to work on the threshold settings pages.  Global thresholds are now linked off the settings page.  The website is probably 25% complete at this point.  Most of the design elements are defined and quite a few content pages have been written.  I have yet to tackle authentication and authorization.  

08/30/2018 - I modified the threshold models to include selectors for comparisons.  I also built forms for adding both agent and global thresholds.  These are still a bit rough but they are progressing.  I have not started the event engine yet.  

08/29/2018 - Cleaned up some CSS/HTML.

08/27/2018 - Events can now be closed manually.

08/27/2018 - I added a simple event view today.  Buttons do not work at this point.  I also cleaned up a lot of code and made some changes to the display.

08/25/2018 - Lots of boring updates today.  I fixed some style elements, did some house cleaning on testing files, and I put placeholder pages in for events, reports, and configuration.  

08/24/2018 - I made quite a few changes to the device page.  I now have graph tooltips working for IE, Edge, and Chrome.  I also added in some basic system information.  I haven't decided how I want to display filesystems, Network, and additional parameters yet.  

08/23/2018 - I continued to work on device graphing today.  I also seperated out some code on the website (utils.py was split into two files).  I'm finding chart.js too limiting for what I'd like to do so I'm planning on going the custom route on the graphs.  Chart.js is amazing but I'm having a tough time getting it to match stylistically with my site.  Today I wrote the basic code to display the axis and polylines.  It's not perfect and needs some cleanup but it does match current time to recorded time so graphs are fairly accurately represented.  I'm going to try to add in tooltips to the SVG graph that I'm writing as well.  

08/21/2018 - Worked on the device graphing.  Created a basic graph with chart.js.  Very eary progress.  

08/20/2018 - Cleaned up some code and added links to devices.  Device pages have not yet been written.  

08/18/2018 - Today I uploaded my working project code.  The project is very early going and not especially useful at this point.  I just wanted to publish some of my progress so you can see how far this has come and where it's heading.

08/17/2018 - This is currently a placeholder for a project that I've been working on for about 6 months.  I have been rewriting my .Net Monitoring Server in Python.  I will probably be adding some source code here in the coming weeks.  So far I have written a Windows Agent, a simple collector, and the base framework for the web server.  

The project is currently written in Python 3.6.5 and Django 2.1.  While it is being written on/for Windows, it should be extendable to Linux, etc.  If there is enough interest, I will work on a Linux agent.  It may be a bit more basic as I'm not as familiar with Linux.  

The project is not a direct port.  There will be some differences between what I had previously done on the .Net apps but overall it should feel similar.  
