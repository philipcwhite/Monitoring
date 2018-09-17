# Monitoring2 ver. 0.01a
Monitoring Server and Agents written in Python

## About

This repository currently contains the code for the monitoring server, collector, and Windows agent.  It is a early beta at this point however some of the functionality is working.  The agent and collector currently work.  The agent collects WMI data and sends it via SSL to the collector which translates the data to the MySQL database.  The webserver is partially working.  The home page displays some agent data and graphs and refreshes content via AJAX.    

## Screenshots

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/home.png)
Home View

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/device.png)
Device View

## Updates

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
