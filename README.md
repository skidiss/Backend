## DermaSkin App Backend
This repository is backend of DermaSkin APP. 

## Technologies
Project is created with:
* Python version: 3.7
* Flask
* Flask-Alchemy
* SQlite3
* Google Compute Engine (VM Instances)
* Google Cloud Bucket

## Setup for Local
To run this project locally setup Vagrant on local machine that has been installed vagrant using ssh:
```powershell
> mkdir backend
> cd backend
> vagrant init debian/bullseye64
> vagrant up
> vagrant ssh
```

## Setup for deployment on GCP
Login to Instance SSH
```bash
~$ sudo apt update && sudo apt -y upgrade
~$ sudo apt install python3-venv
~$ sudo apt install git
~$ git clone git@github.com:skidiss/Backend.git
~$ cd Backend
~$ pip install -r requirements.txt
~$ python 
   >> from app import db
   >> db.create_all()
~$ gunicorn -w 4 0.0.0.0:5000 app:app
```
## API Documentation
https://documenter.getpostman.com/view/21367624/Uz5NkDUZ

