
# QCalls
Conduct meetings as good as live <br>

## Installation Instructions
There are two folder in the project as mentioned below
qcalls-website : To start the website.
qcalls-video-streamer : To start the video streamer service. The video-streamer server shares the loads for better performance.

### Dependencies Installation
First of all install all the dependencies
```
> cd <Project Directory>
> dir

 Directory of C:\Users\Damnik\Project\QCalls\QCalls

06/16/2020  07:36 AM    <DIR>          .
06/16/2020  07:36 AM    <DIR>          ..
06/16/2020  07:41 AM    <DIR>          .git
05/23/2020  11:15 PM    <DIR>          .github
06/15/2020  10:32 PM               185 .gitignore
05/23/2020  04:44 PM            11,357 LICENSE
06/16/2020  07:47 AM    <DIR>          qcalls-video-streamer
06/16/2020  07:46 AM    <DIR>          qcalls-website
05/27/2020  11:46 PM             1,009 README.md
05/28/2020  12:08 PM               794 requirements.txt
               4 File(s)         13,345 bytes
               6 Dir(s)  183,621,943,296 bytes free

> pip install -r requirements.txt
```

### Video streaming service
Now let's bring up the qcalls-video-streamer service
```
> cd <Project Directory>
> cd qcalls-video-stream
> python webstreaming.py
```
Now your video-streaming service should be up.

### Starting Website 
Now let's bring up the website
```
> cd <Project Directory>
> cd qcalls-website
```

Before starting the website, migrate the database using the following commands

```
> python manage.py makemigrations
> python manage.py migrate
```

To run the website
```
> python manage.py runserver
```
