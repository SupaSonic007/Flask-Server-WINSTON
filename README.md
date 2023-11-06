# Flask-Server-WINSTON
The flask server for W.I.N.S.T.O.N.

# How to run the server

**INFO:**
* All dependencies are in the `requirements.txt` file. To install them, run `pip install -r requirements.txt`
* All styles will be supplied in the zip file.
* The server will be run on localhost

**Windows:**
Run `startFlask.bat`

**Linux:**
Run `sudo startFlask.sh`

# Important Information:

* You will be supplied with a user by default and an empty database. The user will have admin powers, but I heavily encourage you to create another user and test out the way that a standard user will interact with the site.
* The site has **mobile support** and has been designed with mobile compatibility in mind. To work with this, you can connect to the server through the same network that the server is on and test it out there.

# How to use the site:
There are buttons on how to do everything and the site is layed out in a way to not leave you asking this question, but here are some of the features:

* Account Creation & Login (Which can be found in the top right of the page when not logged in on desktop and in the dropdown for mobile)
* Forgot password (This can be found on the login page, but the mailing servers will not work without the proper credentials, thus the code is shown as to how it works in email.py)
* `Logout` button (This can be found in the top right of the page when logged in on desktop and in the dropdown for mobile)

* Posting forums (This is found on the `posts` page)
    * Markdown formatting is supported in the post body
    * Images can be used in the post body by using the syntax `![alt text](image url)` as images won't be hosted by the server.
* Editing posts (After creating a post, if you are on the post page that you own, you will see an edit button)
* Deleting posts (On the edit page of a post, there will be a delete button with a confirmation if you'd like to delete a post)
* Saving posts (On a post, if you are logged in, a save button will appear)
* Commenting on posts (On a post, if you are logged in, a comment box will appear down the bottom to add a comment, otherwise comments will be shown for the post normally)

* Profile page (This can be found by clicking on your username in the top right of the page when logged in on desktop and in the dropdown for mobile or by clicking on someone's username from a post)
* Editing profile (On your `profile` page, there will be an edit button)

* Saved posts (On your `profile` page, there will be a button to view your collections which hold saved posts)

* WinstoVision video stream (On the `stream` page, there will be 3 streams, one for each camera, but due to the fact that the cameras are not connected, you will see a blender stream instead if it's running)

* `About us` page (This can be found in the navbar of the page)

* `Admin` page to view all parts of the database and edit them (This can be found in the `admin` tab of the navbar, but you will need to be logged in as an admin to view it)
* Inspecting the database on the `admin` page
* Editing the database through an SQL query on the `admin` page

* `API` Implementation - Accessing tables
    * There is a lot, so you may have to view the code to see all of the endpoints (The function names explain the endpoints).

* `@admin_required` Decorator has been introduced to the site to allow for admin only access to certain pages. This was made to prevent having to create a new check every time that a page is created that requires admin access and replaces `@login_required`.

# Important Notes:
* Admin Credentials:
    * Username: `user1`
    * email (if needed): `admin@example.com`
    * Password: `password`