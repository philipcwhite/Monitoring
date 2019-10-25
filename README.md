# Monitoring ver. 0.03b
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

10/25/2019 - I updated the linux server installer to install pymysql and rewrite the static path for the certificates.  Unfortunately the demo site will be on hold for now due to Azure only allowing me to keep it live for 120 hours.  I have a Visual Studio subscription so my account is limited.  I may have to script somthing to run it for periods of less than 24 hours per day or consider other hosting.  

10/18/2019 - I uploaded a new shell script to install the server components.  It still needs some work but it at least takes care of copying the files, creating the services, and enabling them.  I'm still working through a few systemd issues but I believe it's coming together.  Probably a few more days on this and then back to bug hunting.  Hopefully I get to a new release by the end of the year.  

10/11-2019 - I'll hopefully have a public demo site up and running in the next few weeks.  I did some preliminary testing in Azure today and everything seems to be working as intended.  I'm going to finish with the systemd install scripts before I move any farther forward.  I did notice a couple of bugs when I deployed to Azure that I'll try to sort out too.  The systemd scripts probably need a little cleanup too.  If you're wondering I'm testing on Ubuntu in Azure.  It's so weird when you code in Python using Visual Studio Code on a Elementary Linux VM running on a macbook via Parallels, then deploy to Ubuntu on Azure.  That's a lot of Microsoft in Linux land.

10/9/2019 - I added a shell script to automate installing the Linux agent.  I still need to build the systemd files and install script for the Linux server.  

9/23/2019 - I added in a systemd service file so the Linux agent can be run on startup using systemctl.  I will add scripts for the server as time permits.  

6/7/2019 - I added in configurable data retention options in settings.ini on the server.  This will now by default remove events, data, and agents older than 30 days.  

5/20/2019 - I think I fixed part of the issue with packets not fully sending.  I will probably add some additional flow control to the SQL query for preventing all queued data from being sent at once.

5/11/2019 - 0.03b is out today.  This is the first release supporting both Windows and Linux.  

5/11/2019 - I finally got my conversion from CSV to JSON working with SSL.  Now the agents send data as JSON packets instead of CSV.  I think I still need to put some flow control in to prevent huge packets but things are working for the most part.  Packet sizes should now be significantly smaller.  The upside (or downside) of using JSON is that the packets have to be correct.  CSV would work even if the datastream was partially interupted, inserting part of the data (with data loss) instead of no data.  I think if I build in some flow restrictions this should be able to be mitigated.  Also the smaller packet size should help as well.

5/11/2019 - I had a setback today.  I tried updating the agent to use JSON and SSL no longer works.  Still investigating but I may have to roll back some updates.  

5/10/2019 -  The agent and collector now use a shared security key.  I also fixed an issue with the event engine not loading its configuration for Windows.  I still have a few more things to work on, on the Linux side (systemd startup).

5/9/2019 - I've been busy updating all of the boring stuff today like user guides.  I still have a long way to go.  Hopefully next week I'll be able to prepare a new beta release for both Windows and Linux.  0.03b is coming!  :) 

5/8/2019 - I finished the directory re-org today.  The Windows specific paths for services are now loaded via the service scripts.  I also tested SSL and it is working.  The next beta should be out soon with Linux support for at least elementary OS (Ubuntu).  

5/8/2019 - I am working on rearranging some code to better share resources like certificates and configuration files.  I added a new directory called server where I am moving the website, event engine, and collector.  I've also switched from text files to ini files for configuration.  The three server components will now share the same ini file.  I rewrote the three Windows services as well.  I will make similar startup scripts for systemd on linux.  I also updated the agents to use ini files.  I have not tested all of the code as of yet.   

5/7/2019 - It looks like we have a fully working app on elementary OS.  I still have a few things to test, lots of bugs to squash, and a ton of docs to update but things are looking good.  I just tested the event engine today and it's working fine.  I also updated the Windows agent to use subprocess.  

5/6/2019 - I updated the Event engine so it should now work on Linux.  I still need to test.  My changes to the device page for filesystem seem to have broken the Windows agent's display.  Another thing to add to the to-do list.  Also I still need to switch the Windows agent to use subprocess.  Hopefully I will get this done this week.  

5/5/2019 - Linux agent is now working for all monitors except disk activity.  

5/4/2019 - I added network monitoring to the Linux agent.  Total bytes sent and received per second.  It's more or less an average of 60 seconds but it is what it is.  Linux agent is almost complete.  I still have pagefile and disk activity to add.  Pagefile will be easy but I'm not sure I will be able to do disk activity though.  After this I have to update the event engine and the Windows agent.  When all of this is done, I'll do some cleanup and publish the 0.03b.

5/3/2019 - The Linux development effort is progressing well.  I switched Linux agent to use subprocess today.  Most basic monitors are done on this agent as well.  I will have to update the Windows agent to bring the changes inline with the Linux agent.  I changed filesystem.free to used.  I also made some minor changes to the website to correct issues with Chromium on Linux and other display issues for Linux systems.  

5/2/2019 - Lots of updates to the Linux Agent today.  I added uptime, improved memory and CPU functions, and set the build to the distrobution name and version.

5/1/2019 - We have a partially working linux agent.  It collects some basic system settings and CPU and Memory.  I still have some testing to do on other Linux platforms for the CPU/Memory stats but it should work on most newer systems.  I'll probably test on Centos and Elementary OS (basically Ubuntu).  I still have to rewrite the event engine and I believe the collector isn't picking up the settings.cfg file so I'll have to look into that.  I think I'll probably write some better code for parsing config files when I have time as well.  Thanks to Jaren for the Linux help this week.  

4/28/2019 - I fixed the website code for loading the database connection.  I believe the collector will work fine under Linux with a few tweaks as well.  The Event engine may need to be rewritten since its loop is currently maintained by the Windows service.  Most of these are easy fixes.  I'm going to tackle all of these before moving on to the Linux agent.  Right now for Linux I am just running the Python scripts directly.  If someone knows of a better way to do this please let me know.  

I finally have a decent testing environment on Linux.  I set up Elementary OS with MySQL, Python 3.7.3, and Visual Studio Code.  It may not be a hardcore Linux environment but the interface is nice and simple which works for me.  The desktop performance is pretty good under Parallels but Parallels seems to waste a ton of CPU for Linux VMs which kind of sucks.  I had the same issues in Virtualbox so it could just be that my Mac is too old.

4/28/2019 - I had some issues with my Mac being able to process POST commands between Safari and Python. Everything worked when processing from Chrome.  Safari actually worked when the server was on my Windows VM so I'm a bit lost to where the error was.  Safari was basically sending packets without the body so arguments were not present but it only occured when Python was running on my Mac.  

I've since switched testing to an Ubuntu based Linux VM where the webserver is working fine so far. There are a few things that need to be fixed in the existing code (website doesn't fully load the configuration, etc.).  I hope to get a few of these issues fixed this week.  After I finish testing the server components, I plan on starting on the Agent.    

4/15/2019 - I installed MySQL and Python on my Mac and caught a few errors in the code today.  I have a lot of code to review/fix in order to make this platform independent but I think I can do it.  

4/15/2019 - Release 0.02b.  This is a minor update with all changes since the last release.  Also I installed Python 3 on my Mac so I plan on doing some testing to see if the apps will run on MacOS.  

1/8/2019 - I added some basic reports for device config and open events.  Both can be displayed as HTML or CSV.

1/7/2019 - I created the Help page for the website.  It details what all of the configuration files do and then some.  It could probably use some clean up but it's a step in the right direction.  And yes I still need to build reports... 

1/5/2019  - Some minor changes today.  Added an about page and styled the reports page.  I still need to actually build some reports.  So much to do...  I've been contemplating how to best package the app.  I'll probably use pyinstaller and pack the app with inno setup.  This should make it so that the only outside step needed will be setting up MariaDB/MySQL.  I would prefer to not use freezing tools but they do make things easier for distrobution.  

1/4/2019 - I added a settings.cfg file for the website.  Now all 4 applications have settings files for overrides.  

1/4/2019 - I removed the DB, re-ran the creation script and noticed some odd behavior with pages that must have been cached.  I changed the paging variable to an int and now everything appears to be working fine.  

1/4/2019 - Fixed a lot of issues with user creation and deletion.  Now a default admin user with the password password is created by default when the website is started.  Also users can now be deleted.  There is a confirmation screen as well.  I will add some role permissions soon to differentiate between users and admins.  

1/2/2019 - Fixed an issue with the agent not recording data being sent in non-ssl mode.  Reorganized code for the collector and event engine.  Changed ssl paths in the collector and website to use the certificates directory.

12/31/2018 - If you missed it I did publish a very beta release this morning (0.01b).  It is essentially just a snapshot of the library code at the point of (pre) release.  While that may seem boring, I think it helps keep things on track as it forced me to look into code freezing, updating installation notes, and addressing a few open issues.  I've been working on the project for nearly a year here and have had it live on Github since August.  I hope to have a real release sometime in 2019 but in the mean time I will try to release a few pre-release betas to keep things in check.  

Since 0.01b has been released, all code changes going forward will fall under 0.02b.  And yes there are already a few new updates.  I updated the agent to include the timer in the agent.py script (formerly agent_actions.py) and removed it from the agent_service.py file.  It can now be run independently from agent_service.py if necessary.  

And lastly thanks to everyone who has stopped by to see the project.  If you find it useful please make sure to star or share a link to the page.  I do appreciate it.  

12/31/2018 - I made some minor changes to configurations in preperation for a beta release.  The application was changed to non-SSL by default however it is quite easy to enable SSL.  Install instructions have been improved.  Much of this will eventually be simpilfied and scripted.

12/27/2018 - Minor code changes to the Webserver, collector, event engine, and website.  I'm going to start building a few basic reports and then I plan on packaging an initial beta release.  

12/26/2018 - I changed some of the code to use regex instead of string replace.  It's probably a bit of overkill on some of the queries but it removes some of the double string replaces as well.  I also combined another of the SQL queries reducing some additional overhead.

12/26/2018 - I continued to clean up the agent.  I combined a few function calls and removed a lot of unnecessary code.  I also renamed and reordered (alphabetical for the most part) a lot of the functions to give them a better description.  I'm almost done with the code cleanup on the agent.  There are still a few things with WMIC that I'd like to tweak if possible since the output and parsing are kind of ugly.  I'll probably clean the collector and event engine next before enhancing the website.  I think these two have far less code to clean up.  

12/24/2018 - I reworked a lot of the agent today.  I reduced the number of files that it requires from 10 down to 3 and cleaned up a lot of code.  It still has room for improvement but I think this is a good change.  

12/21/2018 - Updated the Wiki to include some installation and configuration notes.  While it seems like there are a lot of steps at this point it will be greatly simplified after it has been compiled and packaged.  

12/19/2018 - Fixed the issue with the collector not stopping.  

12/18/2018 - Lots of updates today and some new broken code.  It looks like Python 3.7 did actually break a few things.  I am working on fixing these.  The Collector now starts fine and receives data but it will not end via a Windows service Stop.  After revisiting some of my old code there is a lot of room for improvement so I'll try to do some cleanup while I'm working on the 3.7 issues.  Also I replaced CherryPy with my own custom web server.  Initial tests are good.  You should see updates more frequently now that things have settled a bit with my web server project.

11/19/2018 - The code in question does work with Python 3.7 but it can be improved and will be.  I have been working on building a new async webserver which has pulled some of my time from this project.  If the webserver becomes a viable replacement for CherryPy then I will replace CherryPy with it in a future release.  

11/7/2018 - I believe some of my async code is not compliant with Python 3.7.  I will update the project to 3.7.1 when I have time and correct this.  

10/25/2018 - User management is almost complete.  I am still looking at possibly removing CherryPy and writing a custom webserver.  This would essentially remove all dependencies except pymysql.  It may not be the best idea however I do like the idea of knowing how all of the code is processed and this keeps me one step closer tho that.  Plus it's more exciting to write your own webserver than to use someone elses.  

10/19/2018 - Created password reset page, updated login page, and updated some styling.  Also configured the site to use SSL however this is turned off by default.  Uncomment sections in server.conf to enable.

10/17/2018 - Finished coding the Notification Rules page.  Also replaced the default CherryPy favicon with a generic M.  I'll probably update this to something custom later on.  I have a little work left to do with user and session management that I'll be tackling next.

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
