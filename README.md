# NSE
Project to download NSE data for last 30 days


Note:


Set FILES_PATH to the path to download the files from NSE in settings.py


Run management command getNSEData as the scheduler or cron tab script at 12:00 AM everyday so that it collects the data for 30 days.


Run python manage.py runserver and access the url 127.0.0.1:8000/getdata
