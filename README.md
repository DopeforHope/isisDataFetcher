# isisDataFetcher

Hello and welcome to the ISIS Data Fetcher Project.

[ISIS](https://isis.tu-berlin.de/) stands for Information System for Instructors and Student from the **TU Berlin**.  
As far as I know ISIS bases on **Moodle** and has a **Shibboleth** Login in front.

So the project is dedicated to all TU Students but everyone is invited to help. I can't provide a test account for you so if you want to use/test any code you have to have an ISIS account or the credentials from someone else.


## Idea
I want a programm which downloads all **PDFs**, **ZIPs** and so on from all your courses from the ISIS website.


##Programm Sections
###Login
The login from ISIS is done with **Shibboleth**.  
The following image shows how it works.

![Shibboleth Login](http://i.stack.imgur.com/LcVqI.png)
[More informations...](http://stackoverflow.com/questions/16512965/logging-into-saml-shibboleth-authenticated-server-using-python)  
So a simple curl request won't make it and you have to access the login page from the ISIS main site to get the initial cookie.

My approach is very simply with **Selenium** which just follows the redirections.

If everything went well you should be on your ISIS page(https://isis.tu-berlin.de/my/) and have several cookies which you can use from now on to access all your pages.


###Finding Courses, Weeks and Data
Now we want to extract at first the courses which should be done with **XPaths** in my opinion.
The XPaths for the most important are/will be on another wiki page.

The first step should be to collect all your courses, the second to collect the weeks from your courses and the last to get all file links from a week.


So in the end we will get a tree structure with the user, the courses as first level, weeks as second and files as third.

That means for example:

user  
|-course1  
||-week1  
|||-pdffile1.pdf(link)  
|||-zip2.zip(link)  
||-week2  
|||-video.mp4(link)  
||-week3  
|-course2  
.  
.  
.  



###Fetching Data
Last but not least everything needs to be downloaded and copied in the right folder structure of your PC.




##Approach
Right now everything is made with Selenium but the latest idea has been to make the login with Selenium and give the cookies to spyder so he can crawl for all files.

