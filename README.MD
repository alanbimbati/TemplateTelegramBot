# Installation

## Create a virtual environment
```
python3 -m venv venv
```

## Activate the environment

```
source venv/bin/activate
```
## install the dependencies
```
pip3 install requirements.txt
```
## Configuration

modfy the ```settings.py``` file

# Set Backup Database

## Settings Backup
These flags automatically backup the database into the a Telegram channel. This option is helpful only if database is low and if you have a good server connection. The Telegram Cloud storage is free, so it's really good for low budget projects. The ```backup.py``` file, sends backup into a Telegram channel and has the limit of the Telegram channel (2GB per file). The Bot needs privileges to write on the channel so it has to be set as admin in the CHANNEL_LOG.

```
BACKUP_DAILY = True
BACKUP_HOURLY = False

BOT_TOKEN = '<BOT_TOKEN>'
CHANNEL_LOG = '<ID_CHANNEL>'
DB_NAME = 'database'
PROJECT_NAME = '<PROJECT_NAME>'
```

## Starting the backup job
```python3 backup.py &```

## Restore the database
This function is as simple as dummy: it writes a file into the storage to overwrite the database. Use this function carefully and only if the database is little. In the ```settings.py``` file set the flag to true ```ALLOW_ADMIN_RESTORE = True```

# Creating database
Modify the ```model.py ``` file. I use SQLAlchemy to create the database so I forward you into the [SQLAlchemy documentation](https://www.sqlalchemy.org/)

# Starting the bot
```python3 main.py```

## Host the bot into Android Device
If you want to test your bot but you haven't budget to buy a server, you can easily host into an Android Smartphone thanks to [Termux app](https://github.com/termux/termux-app#f-droid) avaiable on [F-droid](https://f-droid.org/). 
This is a temprary way to run it, a server is always a better way to host it: your Android device can turn off for low battery or do not have the internet connection. By the way, I love this solution for personal uses in combo to a cloud backup into a Telegram channel, so I post it here.

* Install Termux on your Android device
* Open it and clone the repository: ```git clone https://github.com/alanbimbati/TemplateTelegramBot```
* Simply starting the bot here

# Usage
## Start the bot
Write ```/start``` to start the bot. You will be stored on the database
## Add Administrator
Write ```/addAdmin @username``` to add other administrator
### Is admin
You can check if a user is admin with the right function. First get the chatid of the user
```chatid = getChaid(message)```
then get the user profile from the chatid
```
from Utilities import Utilities
utility = Utilities()
user = utility.getUser(chatid)
```
then check if is the user is admin
```
if utility.isAdmin(user):
```

## Delete account
Write ```/deleteMe``` to delete your account (respect GDPR)
