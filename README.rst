I703 Python
==========================

Welcome!
-----------------
.. figure:: http://www.metsvahi.ee/hv/img/welcome.gif



Progression diary:
-----------------

Before labs:
 - First idea was to do user managment system using LARP
 - Turned out to be really hard if you are not new to web but are still new to Python and linux things..
 1) Tried to install Apache server to run web.. turns out its pretty good for html but not for Python... atleast what i found out.
 2) Researched a bit about micro-frameworks and had a pretty good theory on what to do.
 3) Found Flask. Tried to get that to work but it just seemed error upon error upon error.. some virutalisation and things.
 4) Got Flask working!
 5) Just noticed the previous code is using Falcon which seems faster and easyer.. switching to that.
 7) Python is so different from PHP for web. Get kinda stuck with every step. Even sessions need like custom librarys.
 8) Haven't attached any databases or LARP yet.. still trying to get a good foundation to build on.
 9) Why do i tourment myself..

 - Okey.. i know when i am way over my head in something. That was alot of time wasted.
 
 - Gonna do labs to catch up with people and actually learn Python the right way.

Lab 1:
 - Good introduction. 
 - Improved by using Counter object and added all extra functionality except normalize paths because i dont know what that means.
	
Lab 2:
 - Since working from personal Windows computer, downloaded some files from enos to my own folder and using that. 
 - Added gzip reading
 - Added humanizer and gave a few arguments from command line to configure how it does stuff
 - Turned the hole parser into a class so i can use functions within themselves and store data for later processing
	
Lab 3:
 - Replaced my humanizer script with better one provided in Lab 3. 
 - Also did that with the arguments...
 - Added all kinds of data extraction and highscore things based on exercises
	
 - GeoIp under Windows turned out to be tricky... thinking about moving this project over to a linux OS... only i dont have one really since i use Windows...
	
 - EDIT: Installed Linux Mint 17.3 on my main computer for Python and a few other classes in school... its .. interesting..
 - EDIT 2: oh god what have i done... Managed to screw up the video drivers so much that i had to do a clean install again..
 - EDIT 3: skype looks like its from the 90s and i even had to download script to turn on numlock
 - EDIT 4: all the fonts are weird aswell and i kinda need them to look perfect.. Also no programs like Photoshop or Outlook (i know there are alternatives but my job requires them)
 - EDIT 5: NOPE NOPE NOPE, did a clean install on Windows 10 back, i saw how much configuring its required to get Linux to work and i want to see the sun this summer 
 - *note that this linux stuff was over the course of 1-2 weeks, not a day or so*
	
Lab 4:
 - Saw that Lab 4 has lab 3 excerisises.. moving on to that
 - Installed PiP on windows, actually got it to work this time
 - Switching from geoip to pygeoip since the first one doesn't seem to work in windows since it needs some linux librarys.
 - Ipv6 addresses are kinda breaking the code... adding functions to filter them out and added another geoip database for them
 - Added world painting function to the class
 - World painting seems fine
  - blue and lighter colors are minimum
  - red and darker colors are maximum
	
Lab 5:
 - Template generating is pretty small script.
 - Not that i got it working right off the bat but still
 - Opening in browser didnt work like that. 
 - Using os system start to open report.

Lab 6:
 - Oh Falcon my new nemesis..
 - Not entirely sure how to approach this..
 - Have tried 3 different methods but all have failed.. Will move onto Lab 7 until i can figure it out

Lab 7:
 - Image manipulation! Created new project for it, downloaded some wallpapers for testing
 - Since PIL is outdated i use Pillow, same thing kinda
 - Added alot of commands-line arguments to the program like
  - Input and output directory
  - Maximum width and height for the new images
  - Thread count
  - Verbose mode
 - Added .png to the "allowed images" list
 - Added a crop functionality that when enabled, will force the set width and height. Great for making thumbnails!

Lab 8:
 - Due to technical troubles, no sound is on the lecture recording and the wiki doesn't really explain anything..
 - Gonna get more info about it...
 
 
Conclusion:
-----------------
.. figure:: http://www.metsvahi.ee/hv/img/progress_so_far.jpg
