# Create VM Flow

WIP

## Install 

### Create virtualenv with python3.6
```
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar -zxf Python-3.6.4.tgz
cd Python-3.6.4
mkdir pythonroot
configure --prefix `pwd`/pythonroot
make
make install
cd ~
virtualenv py36 -p ~/Python-3.6.4/pythonroot/bin/python3
```

### Use py36 env
Activate py36 env

`source py36/bin/activate`

Exit py46 env

`deactive`

### Install Requirement
`pip install -r requirement`

### migrate db and import data
```
./manage.py migrate
./manage.py loaddata fixture/auth.yaml
```

## Run Server
`./manage.py runserver 0:9000`

## Login Workflow Page
http://yourip:9000/workflow

## Admin site

http://yourip:9000/admin

### Accounts
- manager : manager/manager

- admin : admin/admin

- user : user/user

