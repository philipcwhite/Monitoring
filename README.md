# Monitoring2 ver. 0.01b
Monitoring Server and Agents written in Python

## About

This repository currently contains the code for the monitoring server, collector, and Windows agent.  It is a early beta at this point however some of the functionality is working.  The agent and collector currently work.  The agent collects WMI data and sends it via SSL to the collector which translates the data to the MySQL database.  The webserver is partially working.  The home page displays some agent data and graphs and refreshes content via AJAX.    

## Screenshots

![WebSite](https://raw.githubusercontent.com/philipcwhite/Monitoring2/master/images/home.png)

## Updates

08/21/2018 - Worked on the device graphing.  Created a basic graph with chart.js.  Very eary progress.  

08/20/2018 - Cleaned up some code and added links to devices.  Device pages have not yet been written.  

08/18/2018 - Today I uploaded my working project code.  The project is very early going and not especially useful at this point.  I just wanted to publish some of my progress so you can see how far this has come and where it's heading.

08/17/2018 - This is currently a placeholder for a project that I've been working on for about 6 months.  I have been rewriting my .Net Monitoring Server in Python.  I will probably be adding some source code here in the coming weeks.  So far I have written a Windows Agent, a simple collector, and the base framework for the web server.  

The project is currently written in Python 3.6.5 and Django 2.1.  While it is being written on/for Windows, it should be extendable to Linux, etc.  If there is enough interest, I will work on a Linux agent.  It may be a bit more basic as I'm not as familiar with Linux.  

The project is not a direct port.  There will be some differences between what I had previously done on the .Net apps but overall it should feel similar.  
