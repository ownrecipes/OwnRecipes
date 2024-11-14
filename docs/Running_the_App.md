# Running the App

<details>
  <summary>⚠ Note for Windows users</summary>
  <p>
    This documentation is written for Linux-based systems.
    If you are using Windows, please be aware of some subtle changes:
    <ol>
      <li>Do not use the built-in commad-line, but the PowerShell. Some syntax will not work on the command-line.</li>
      <li>There is no sudo. Most of the commands will work without the sudo. If you encounter permission errors, please run your PowerShell as administrator.</li>
    </ol>
  </p>
</details>

## Install Prerequisites

Install [git](Install_Prerequisites.md/#git).
Install [docker and docker-compose](Install_Prerequisites.md/#docker).

## Coming from OpenEats?

See the [Migration Guide](Migrating_from_OpenEats.md).

## Setup docker configuration for production

First clone the repos:
```bash
git clone https://github.com/ownrecipes/OwnRecipes.git
cd OwnRecipes
```

Then, copy the needed environment files:
```bash
cp docs/samples/sample_docker_prod_override.yml docker-prod.override.yml
```

### Note on docker-prod.override.yml

The `docker-prod.override.yml` specifies the port that OwnRecipes is served from as well as any additional configuration that overrides the defaults.
It also allows the containers to reboot themselves when your machine restarts or if the containers fail. You can change this to `never` if you want to manually control when the containers start and stop.
By default the nginx docker container will serve as a reverse proxy for the other services, and serve its content on port 8000 on the host machine (forwarded from port 80 on the container).

### Configure the environment file

Most of the settings in your env-files can stay the same. There are a few config settings that need to be changed for most configurations.
See [Setting_up_env_file.md](Setting_up_env_file.md) for a complete description of the environment variables.

`.env.docker.production.api`:

- [MYSQL_ROOT_PASSWORD](Setting_up_env_file.md#MYSQL_ROOT_PASSWORD)
- [DJANGO_SECRET_KEY](Setting_up_env_file.md#DJANGO_SECRET_KEY)
- [ALLOWED_HOST](Setting_up_env_file.md#ALLOWED_HOST)
- [NODE_URL](Setting_up_env_file.md#NODE_URL)

`.env.docker.production.web`:

- [REACT_APP_API_URL](Setting_up_env_file.md#REACT_APP_API_URL)


#### Note on the ALLOWED_HOST option

The ALLOWED_HOST option must be set equal to the domain or IP address that users will access the site from.
For example, if you are hosting on "mydomain.com", enter:
``ALLOWED_HOST=mydomain.com``

If you are hosting on `192.168.0.12`, enter:
``ALLOWED_HOST=192.168.0.12``

Note that it is not necessary to specify the port.

#### Note on the REACT_APP_API_URL option

The REACT_APP_API_URL specifies the URL that the web-app uses to contact the API.
If you are running OwnRecipes on a port other than 80 or 443, it is necessary to specify this port in the REACT_APP_API_URL option.
E.g. Given that the IP address for the OwnRecipes server is `192.168.0.12` and port is `1234`.

``REACT_APP_API_URL=http://192.168.0.1:1234``

## Start docker containers

Once the files have been created run the command below and replace the version with version of OwnRecipes you want to run. You can also leave this blank (this will pull the latest code)

```bash
sudo ./quick-start.py -t 1.0.3
```
OR
```bash
sudo ./quick-start.py
```
OR
```bash
sudo ./quick-start.py --help
```

<details>
  <summary>What exactly does the quick-start script do?</summary>
  <ol>
    <li>Creates a `docker-prod.version.yml` file with the required image tags.</li>
    <li>Downloads the required images.</li>
    <li>Takes a backup of the database and your images.</li>
    <li>Restarts the OwnRecipes containers.</li>
  </ol>
</details>

After completing the startup, you should see the following line in your terminal:

```
App started. Please wait ~30 seconds for the containers to come online.
```

:warning: THE SETUP IS NOT COMPLETE, YET! Please follow the further instructions! :warning:

If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).

## First Time Setup

To create a super user:
```bash
sudo docker compose -f docker-prod.yml -f docker-prod.override.yml -f docker-prod.version.yml run --rm --entrypoint 'python manage.py createsuperuser' api
```
Follow the prompts given to create your user. You can do this as many times as you like.

_[Click here if docker-compose throws an error](Troubleshooting.md#docker-compose-throws-an-error)._

If you want to add some test data you can load a few recipes and some news data. This data isn't really needed unless you just wanna see how the app looks and if its working.
```bash
sudo docker compose -f docker-prod.yml -f docker-prod.override.yml -f docker-prod.version.yml run --rm --entrypoint 'sh' api
./manage.py loaddata course_data.json
./manage.py loaddata cuisine_data.json
./manage.py loaddata season_data.json
./manage.py loaddata tag_data.json
./manage.py loaddata news_data.json
./manage.py loaddata recipe_data.json
./manage.py loaddata ing_data.json
```

## Finish up

The set up is complete and everything should be up and running.

You can visit the [Admin Site](Admin_site.md), to create some more users, customize the news, or manage some lists.

Or you can straight away log in to the OwnRecipes web app. By default, the url will be `http://localhost:8080`, or `http://<ownrecipes.domain.com>:8080`.

If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).

## Advanced setups

### Setup HTTPS

It is highly recommended that you serve your content over https. See [Setting up HTTPS](Setting_up_https.md) for more information on how to enable ssl.

### Custom Proxy Server

See [Creating a proxy server for docker](Creating_a_proxy_server_for_docker.md) for more information on how to configure a custom nginx server to serve OwnRecipes.

### Connecting to a remote DB
If you are connecting the API to a remote DB (any non-dockerized DB) you need to setup the following configs to your env file.

- [MYSQL_DATABASE](Setting_up_env_file.md#MYSQL_DATABASE)
- [MYSQL_USER](Setting_up_env_file.md#MYSQL_USER)
- [MYSQL_PASSWORD](Setting_up_env_file.md#MYSQL_PASSWORD)
- [MYSQL_HOST](Setting_up_env_file.md#MYSQL_HOST)
- [MYSQL_PORT](Setting_up_env_file.md#MYSQL_PORT)

You will also need to edit your `docker-prod.yml` file to remove the database from the setup process. See [this docker yml](samples/sample_docker_prod_remote_db.yml) for an example.

## Updating/Upgrading

See [Updating the App](Updating_the_App.md#updating-the-app-with-docker-production)
