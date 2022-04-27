# jumpnow CMS Base
139.59.57.121

## Setup and installation

- [ ] Clone the repository <br/>
      `git clone https://github.com/jumpnow-tech/jumpnow.git`

- [ ] Install required libraries and dependencies <br/>
        `sudo apt-get update -y && sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib python3-venv nginx -y`


- [ ] Create Virtual Env <br/>
      `cd jumpnow && python3 -m venv env`

- [ ] Activate Virtual Env <br/>
      `source env/bin/activate`

- [ ] Install dependencies <br/>
      `pip3 install wheel && pip3 install -r requirements.txt`

#### start redis service
```
docker run -p 6379:6379 -d redis:5
```
node-sass -w discovery\static\discovery\scss -o discovery\static\discovery\css --source-map true

node-sass -w dashboard\static\dashboard\scss -o dashboard\static\dashboard\css --source-map true


sudo apt-get install libgtk-3-0\
          libcairo2\
          libegl1\
          libnotify4\
          libgdk-pixbuf2.0-0\
          libvpx6\
          libopus0\
          libpango-1.0-0\
          libwoff1\
          libharfbuzz-icu0\
          libgstreamer-plugins-base1.0-0\
          libgstreamer-gl1.0-0\
          libgstreamer-plugins-bad1.0-0\
          libopenjp2-7\
          libwebpdemux2\
          libenchant1c2a\
          libsecret-1-0\
          libhyphen0\
          libwayland-server0\
          libwayland-egl1\
          libxkbcommon0\
          libepoxy0\
          libgles2\
          gstreamer1.0-libav


send db: 

sudo scp -i /home/ishant/brand.pem /home/ishant/ishant_linux/jumpnow/jumpnow/db.sqlite3 sriraj@52.172.35.186:/home/sriraj/jumpnow

sudo scp -i /home/ishant/brand.pem /home/ishant/ishant_linux/jumpnow/jumpnow/media.zip sriraj@52.172.35.186:/home/sriraj/jumpnow

sudo scp -i /home/ishant/brand.pem sriraj@52.172.35.186:/home/sriraj/jumpnow/db.sqlite3 /home/ishant/ishant_linux/jumpnow/jumpnow

scp /home/ishant/ishant_linux/sriraj/jumpnow/jumpnow/email.json sriraj@128.199.28.207:/home/sriraj/jumpnow/jumpnow


#### Production Branch

Setup gunicorn :

sudo nano /etc/systemd/system/main.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ishant
Group=www-data
WorkingDirectory=/home/ishant/build
ExecStart=/home/ishant/build/main/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ishant/build/main.sock jumpnow.wsgi:application

[Install]
WantedBy=multi-user.target

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
nginx Setup:

sudo nano /etc/nginx/sites-available/main


server {
    listen 80;
    server_name app.jumpnow.agency;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ishant/build/main;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ishant/build/main.sock;
    }

    location /media/ {
        alias /home/ishant/build/main/media/;
    }
}

sudo ln -s /etc/nginx/sites-available/main /etc/nginx/sites-enabled


#### QA Branch

Setup gunicorn :

sudo nano /etc/systemd/system/jumpnow.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ishant
Group=www-data
WorkingDirectory=/home/ishant/jumpnow
ExecStart=/home/ishant/jumpnow/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ishant/jumpnow.sock jumpnow.wsgi:application

[Install]
WantedBy=multi-user.target

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
nginx Setup:

sudo nano /etc/nginx/sites-available/jumpnow


server {
    listen 80;
    server_name devapp.jumpnow.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ishant/jumpnow;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ishant/jumpnow.sock;
    }

    location /media/ {
        alias /home/ishant/jumpnow/media/;
    }
}

sudo ln -s /etc/nginx/sites-available/jumpnow /etc/nginx/sites-enabled

#### DEV Branch

Setup gunicorn :

sudo nano /etc/systemd/system/dev.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ishant
Group=www-data
WorkingDirectory=/home/ishant/builds/dev
ExecStart=/home/ishant/builds/dev/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ishant/builds/dev.sock jumpnow.wsgi:application

[Install]
WantedBy=multi-user.target

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
nginx Setup:

sudo nano /etc/nginx/sites-available/dev


server {
    listen 80;
    server_name devapp.jumpnow.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ishant/builds/dev;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ishant/builds/dev.sock;
    }

    location /media/ {
        alias /home/ishant/builds/dev/media/;
    }
}

sudo ln -s /etc/nginx/sites-available/dev /etc/nginx/sites-enabled



#### To restart server
sudo pkill gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl restart nginx
sudo systemctl restart gunicorn.service


sudo systemctl restart main.service
sudo systemctl restart qa.service
sudo systemctl restart dev.service
sudo systemctl restart nginx

sudo systemctl restart jumpnow.service
sudo systemctl restart nginx

sudo python3 manage.py collectstatic --no-input

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sudo chown -R ishant:ishant /var/lib/jenkins
sudo chown -R ishant:ishant /var/cache/jenkins
sudo chown -R ishant:ishant /var/log/jenkins

CMS PANEL : 



Products - Lexotique , kitchenji, etc - list of products - product x ( with the related fields , buy link )
Blogs  - Lexotique , kitchenji, etc - list of blogs - blogs x ( with the related fields )
settings - Users - Name , Site ownership , username and email/pass ( create general admin , create executive ) 
                          - Lexotique
                          - kitchenji
                          - Madhuram  



Settings - Site owners will have  multiple selection of 


Presentations:

Fresheys:
Web = https://docs.google.com/presentation/d/1lP4BtFX4kIW2gxr7FwuXHpxCKIaDnVkuIizkh-RHpc8/edit#slide=id.g966a22fd74_0_0
Mobile = https://docs.google.com/presentation/d/1jtG1jdyI6lg916VUsZMgMWnFDCgJquBZH0xYZiREY4I/edit


Lexotique:
Web = https://docs.google.com/presentation/d/1FRT00VIZJ7xr8YCDvPrVDcoSHlG9zcKeCezC2vNHHwk/edit?usp=sharing
Mobile = https://docs.google.com/presentation/d/1c0EECcwOZbK2mWitnevRsZa0wpzm1n0RJYg1Omr34cw/edit?usp=sharing


Cron command for emails

* * * * * /home/sriraj/jumpnow/env/bin/python /home/sriraj/jumpnow/manage.py send_queued_mail >> /home/sriraj/jumpnow/send_mail.log 2>&1

11 July

Include delivarables for direct offer

Anshuman
