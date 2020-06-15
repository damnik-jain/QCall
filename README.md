
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
