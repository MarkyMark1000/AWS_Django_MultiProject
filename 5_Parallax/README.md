# OVERVIEW

Previously, I worked on a project that used parallax scrolling using "background-attachment: fixed".   Unfortunately I found that I had to turn the effect off when viewing the page on an iPhone because it didn't work properly.

Initially, I did not have time to investigate this furthur, but I have noticed that some websites do manage to get this to work and I wanted a template should I need to use it in the future.

The first page demonstrates the use of "background-attachment: fixed" and it probably won't work on an iPhone.

The second page is taken from Keith Clark's page (see Relevant Links at the bottom).   I suggest taking a look at this website.   It is very interesting, especially the debug section where you can see the different layers of the site.

The third page demonstrates how I have used this technique to move multiple images and a foreground with a parallax effect that work's on an iPhone.   Some work could be done to blend the pictures in more and add a footer, but the basic concept is present.

I have tested this with an iPhone, Safari, Chrome, Opera and Edge on my local computer and it appears to work effectively.   Unfortunately I do not have access to extensive browser
testing software, but I suspect that this is unlikely to work on older browsers.   I have
used Bootstrap 4 here!

### Make File

---

The settings.py file has been adjusted to display the ip/port on on the local network and
the make file has been adjusted to use 0.0.0.0:8080.   This should make the site accessible
on the local network so that it can be viewed on an iPhone.   It is extremely unlikely that
this feature will work properly if it is run using Docker.

This has not been tested on a live site.

### Relevant Links

---

https://stackoverflow.com/questions/24057655/parallax-scrolling-in-safari-on-ios

https://keithclark.co.uk/articles/pure-css-parallax-websites/

This is excellent, try the debug button:  
https://keithclark.co.uk/articles/pure-css-parallax-websites/demo3/
