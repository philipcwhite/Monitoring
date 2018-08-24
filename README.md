# Monitoring2 ver. 0.01b
Monitoring Server and Agents written in Python

## About

This repository currently contains the code for the monitoring server, collector, and Windows agent.  It is a early beta at this point however some of the functionality is working.  The agent and collector currently work.  The agent collects WMI data and sends it via SSL to the collector which translates the data to the MySQL database.  The webserver is partially working.  The home page displays some agent data and graphs and refreshes content via AJAX.    

## Screenshots

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/home.png)

## Updates

08/23/2018 - I continued to work on device graphing today.  I also seperated out some code on the website (utils.py was split into two files).  I'm finding chart.js too limiting for what I'd like to do so I'm planning on going the custom route on the graphs.  Chart.js is amazing but I'm having a tough time getting it to match stylistically with my site.  Today I wrote the basic code to display the axis and polylines.  It's not perfect and needs some cleanup but it does match current time to recorded time so graphs are fairly accurately represented.  I'm going to try to add in tooltips to the SVG graph that I'm writing as well.  

08/21/2018 - Worked on the device graphing.  Created a basic graph with chart.js.  Very eary progress.  

08/20/2018 - Cleaned up some code and added links to devices.  Device pages have not yet been written.  

08/18/2018 - Today I uploaded my working project code.  The project is very early going and not especially useful at this point.  I just wanted to publish some of my progress so you can see how far this has come and where it's heading.

08/17/2018 - This is currently a placeholder for a project that I've been working on for about 6 months.  I have been rewriting my .Net Monitoring Server in Python.  I will probably be adding some source code here in the coming weeks.  So far I have written a Windows Agent, a simple collector, and the base framework for the web server.  

The project is currently written in Python 3.6.5 and Django 2.1.  While it is being written on/for Windows, it should be extendable to Linux, etc.  If there is enough interest, I will work on a Linux agent.  It may be a bit more basic as I'm not as familiar with Linux.  

The project is not a direct port.  There will be some differences between what I had previously done on the .Net apps but overall it should feel similar.  
