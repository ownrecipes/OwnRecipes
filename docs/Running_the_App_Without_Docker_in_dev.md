# Running the App Without Docker in development

Following this guide, you will set up the database MariaDB, the ownrecipes-api and ownrecipes-web.

<details>
  <summary>⚠ Note for Windows users</summary>
  <p>
    This documentation is written for Linux-based systems.
    This documentation will not work with Windows, and you will have a hard time to get the set up done on Windows.
  </p>
  <p>
    Your best bet is to use Linux, or docker.
  </p>
</details>

## Install Prerequisites

`sudo apt install git build-essential libjpeg-dev zlib1g-dev`

## Create Base Directory

*It is recommended to stick to the path "/opt/ownrecipes/ownrecipes-api" to minimize the required changes in the configuration files.*

```bash
mkdir /opt/ownrecipes/
```

## Database

We will use MariaDB. The minimum required version is 10.4, and the recommended and tested version is 10.11 LTS.

### Install

```bash
sudo apt install mariadb-server
```
Don't forget to run `sudo mysql_secure_installation`!

Install Additional Dependencies:

`sudo apt install default-libmysqlclient-dev libssl-dev`

### Setup Database

Log Into Your MySQL Database:

`sudo mysql`

Create Database and Db-User:

`CREATE DATABASE ownrecipes;`

*Change username and password. You will have to change that in the configuration files, too.*

*It is recommended to stick to the username "ownrecipes" to minimize the required changes in the configuration files.*

`GRANT ALL PRIVILEGES ON ownrecipes.* TO 'username'@'localhost' IDENTIFIED BY 'password';`

Example:

`GRANT ALL PRIVILEGES ON ownrecipes.* TO 'ownrecipes'@'localhost' IDENTIFIED BY 'db-trustNo1';`

Commit Changes:

`FLUSH PRIVILEGES;`

Exit From MySQL:

`EXIT;`

## ownrecipes-api

### Install dependencies

`sudo apt-get install python3 python3-pip python-venv git build-essential`

### Setup the files

**Get the Source of ownrecipes-api from GitHub:**

`cd /opt/ownrecipes`

```bash
git clone https://github.com/ownrecipes/ownrecipes-api.git
cd /opt/ownrecipes/ownrecipes-api
```

**Create .env Environment file:**

First, copy one of the following files for your setup (locahost, server or proxy).
Then, open the file `/opt/ownrecipes/ownrecipes-api/.env.service.local` and change the [variables](Setting_up_env_file.md) to your needs. You will have to change at least all variables with "\<placeholder-values\>".

*localhost:*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/localhost/.env /opt/ownrecipes/ownrecipes-api/.env.service.local`

*server:*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/server/.env /opt/ownrecipes/ownrecipes-api/.env.service.local`

*proxy:*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/proxy/.env /opt/ownrecipes/ownrecipes-api/.env.service.local`

**Copy the /opt/ownrecipes/ownrecipes-api/base/prod-entrypoint.sh file:**

*If you are using a different directory than "/opt/ownrecipes", then you have to adjust the file to your needs.*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/prod-entrypoint.sh /opt/ownrecipes/ownrecipes-api/base/`

**Copy the /opt/ownrecipes/ownrecipes-api/base/gunicorn_start.sh file:**

*If you are using a different directory than "/opt/ownrecipes", or can't use the os user "ownrecipes", then you have to adjust the file to your needs.*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/gunicorn_start.sh /opt/ownrecipes/ownrecipes-api/base/`

**Copy the /opt/ownrecipes/ownrecipes-api/base/gc.sh file:**

*If you are using a different directory than "/opt/ownrecipes", then you have to adjust the file to your needs.*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/gc.sh /opt/ownrecipes/ownrecipes-api/base/`

**Create systemd service to run the api:**

*If you are using a different directory than "/opt/ownrecipes", or can't use the os user "ownrecipes", then you have to adjust the file to your needs.*

`cp /opt/ownrecipes/ownrecipes-api/docs/samples/no_docker/ownrecipes.service /lib/systemd/system/`

### Create the OS user

```bash
sudo useradd -m -d /opt/ownrecipes username
sudo chown -R username:groupname /opt/ownrecipes
```

Example:

```bash
sudo useradd -m -d /opt/ownrecipes ownrecipes
sudo chown -R ownrecipes:ownrecipes /opt/ownrecipes
```

Tip: Change default shell to bash for more convenient terminal usage:

`sudo chsh -s /bin/bash ownrecipes`

### Install the Python Requirements

First, change user to the OS user for ownrecipes:

```bash
sudo su ownrecipes
cd /opt/ownrecipes/ownrecipes-api
```

Then, create the python virtual environment:

```bash
python3 -m venv /opt/ownrecipes/ownrecipes-api
. bin/activate
python3 -m pip install wheel
```

```bash
pip3 install -U -r base/requirements.txt
```

On some systems, it may be neccessary to add the newly installed tools to the PATH.
Check that the python tools are working by executing:

```bash
gunicorn --version
```

If you see an error, add the python tools permanently to the path. To permanently add shell path:

```bash
echo "export PATH=\$PATH:~/.local/bin" >> ~/.bashrc
echo "export PATH=$PATH:~/.local/bin" >> /opt/ownrecipes/ownrecipes-api/.env.service.local
```

Restart the terminal session and re-validate that gunicorn is found.

### Populate the database

First, change user to the OS user for ownrecipes

```bash
sudo su ownrecipes
```

```bash
cd /opt/ownrecipes/ownrecipes-api
/bin/bash -ac '. .env.service.local; exec python3 manage.py migrate'
/bin/bash -ac '. .env.service.local; exec python3 manage.py createsuperuser'
```

Optional: Seed the database with example data.
```bash
/bin/bash -ac '. .env.service.local; exec python3 manage.py loaddata course_data.json'
/bin/bash -ac '. .env.service.local; exec python3 manage.py loaddata cuisine_data.json'
/bin/bash -ac '. .env.service.local; exec python3 manage.py loaddata news_data.json'
/bin/bash -ac '. .env.service.local; exec python3 manage.py loaddata recipe_data.json'
/bin/bash -ac '. .env.service.local; exec python3 manage.py loaddata ing_data.json'
```

### Start the api

Open a new terminal.

`sudo service ownrecipes start`

**Check if the api is running correctly:**

`sudo service ownrecipes status`

If all is running correctly, you should see the line
```diff
+ Active: active (running)
```

... and probably as last lines `[INFO] Booting worker with pid: ...`.

### Optional: Cron job for householding

*Note: Linux only.*

Add a cron job to run garbage collection daily.

```bash
sudo crontab -e

0 6 * * * su ownrecipes -c "/opt/ownrecipes/ownrecipes-api/base/gc.sh"

sudo service cron restart
```

### Troubleshooting

#### Run the api in a terminal

In case your api just won't work as expected, you could run your api in a terminal to hopefully get some more detailed error information.

Log in as ownrecipes user:

```bash
sudo su ownrecipes
cd ~/ownrecipes-api
```

Make the entrypoint-script executable:

```bash
chmod +x base/prod-entrypoint.sh
```

Run the api:

*The following command will source the environment file and make the variables available to all subsequent called scripts.*

```bash
/bin/bash -ac '. .env.service.local; exec ./base/prod-entrypoint.sh'
```

<hr />


## ownrecipes-web

### Install dependencies

Install [NodeJS](Install_Prerequisites.md/#nodejs).

### Setup the files

**Get the source of ownrecipes-web from git:**

`cd /opt/ownrecipes/`

```bash
git clone https://github.com/ownrecipes/ownrecipes-web.git
cd /opt/ownrecipes/ownrecipes-web/
```

### Install the dependencies

```bash
npm install
```

### Run ownrecipes-web

```bash
npm start
```

## Finish up

The set up is complete and everything should be up and running.

You can visit the [Admin Site](Admin_site.md), to create some more users, customize the news, or manage some lists.

Or you can straight away log in to the OwnRecipes web app. By default, the url will be `http://localhost:8080`.

OwnRecipes will shut down with your system. You can simply launch OwnRecipes by running:
```bash
cd /opt/ownrecipes/ownrecipes-web/
sudo service ownrecipes start
npm start
```

If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).
