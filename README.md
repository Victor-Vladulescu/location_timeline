# location_timeline

Storing Google Maps location sharing data to keep track of people (with their consent of course). It uses a Python web API and Chromium browser extension to collect and store real time geolocation data.

<br></br>
### Instructions to get users data
In your browser, go to Google Maps, open developer tools, go to network tab, filter by *https://www.google.com/maps/rpc/locationsharing/read*. Copy the response, paste it in Visual Studio Code or other editor, remove first line, format document and you'll have a JSON file. File[0] will be an array of user data, and for each entry you'll need user[0][0] (Google ID). You'll know it's the ID because right under it will be a link to their profile photo which starts with *https://lh3.googleusercontent.com* and underneath that will be their username.
After getting the Google ID for each user, write an SQL query to insert data into the users table (check *api/sql/20240412_1630_Create-database.sql*) after you go through the app first setup and have PostgreSQL:

google_id = the ID that you've extracted

name = whatever name you want

password = random string, it's only important if I ever update this project to have an actual web interface and allow users to download their own data through the internet

last_ping = 0

<br></br>
### Instruction for app first setup
I've only been running this solution on the Ubuntu 22.04.4 LTS distribution of Linux and thus I know for sure that they will work on this environment:

For a first time setup, install PostgreSQL database system, choose a password and through **psql** run the SQL query from *api/sql/20240412_1630_Create-database.sql*. Get the latest version of Python 3, venv (python virtual environment), activate it and install dependencies from *api/requirements.txt* with **pip**. Install Chromium browser, go to Google Maps and connect with the Google account which has location sharing from other people. After this initial setup, you should follow the steps below each time you reboot your host.

<br></br>
### Instructions to set up environment after each system reboot
0. Enter tmux environment (useful if using SSH to connect to host)

1. Enter venv

cd <repository_location/api>

source .venv/bin/activate

2. Export DB_timeline variable

export DB_timeline=postgresql://postgres:<your_password>@localhost:5432/location_timeline

3. Start the API

gunicorn --bind 127.0.0.1:8000 main:app

4. Start Chromium and load up extension from *chrome://extensions/* URL with Developer Mode ticked, Load unpacked *<repository>/browser*

Have one browser window open on Google Maps, that's where the extension will be getting data from.
Optionally you can have the network tab from developer tools on the screen 
and filter by 'locationsharing' to see requests and finish time

5. Open PSQL in a new tmux tab (Ctrl + B,  C) and check that new data is coming in (compare old and new values)

sudo -u postgres psql

\c location_timeline

SELECT COUNT(*) FROM public.history;


<br></br>
### Backup data from PostgreSQL and restore

sudo -u postgres pg_dumpall > filename.sql

sudo -u postgres psql < filename.sql
