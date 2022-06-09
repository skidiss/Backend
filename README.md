![](images/DermaSkin%20logo.png)

# DermaSkin App Backend 
This repository is backend f DermaSkin APP.
# Technologies
The project created with :
* python37 with flask
* Virtual Machine
* Mysql

# Steps to configure and deployment using flask
- Create 2 buckets in cloud storage for GET and POSH processes resulting from the detection process
   * Create a virtual machine on the GCP compute engine with Deep Learning for Linux Tensorflow 2.2 image
   * Install libraries in virtual machines such as a. tensorflow==2.2.0 b. h5py==2.10.0 c. Flask-RESTful==0.3.8 d. Flask-SQLAlchemy==2.4.1 e. filedepot==0.8.0
  * main.py Scripting Process
  * Run main.py with the command sudo python3 main.py& (on linux) 
  * The flash is running and the API has been obtained according to the External IP on the compute engine
