<a name="readme-top"></a>

# Updating the App

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#updating-the-app-with-docker-production">Updating the App with Docker (production)</a></li>
    <li><a href="#updating-the-app-with-docker-development">Updating the App with Docker (development)</a></li>
    <li><a href="#updating-the-app-without-docker">Updating the App without Docker</a></li>
  </ol>
</details>

## Updating the App with Docker (production)

First, make a backup. Do not skip this step!
If anything goes wrong, make sure you got the backup!

For this, simply (re-)start the app, e. g. by re-running the `quick-start.py`.
This will create the database backup. Copy it to a safe location, where it won't be overriden.

Now pull the latest from the repo:
```bash
cd OwnRecipes
git pull
```

Then check the release notes about any changes to the following files:
- docker-prod.override.yml
- .env.docker.production.api
- .env.docker.production.web

There should only be breaking changes to these files in major releases (IE. 2.0.0, 3.0.0).

Once you know your env and docker-compose files are up to date, run the [`quick-start.py`](Running_the_App.md#start-docker-containers).

Last but not least, if the database (MariaDB) was upgraded, you need to migrate the database:
```bash
# If running a specific tag, substitute ownrecipes_db_1 accordingly.
sudo docker exec ownrecipes_db_1 sh -c 'exec mysql_upgrade -u root -p"$MYSQL_ROOT_PASSWORD"'
```

and then run [`quick-start.py`](Running_the_App.md#start-docker-containers) once again to make sure all bits and pieces are tied error-free.

Enjoy!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Updating the App with Docker (development)

First, make a backup. Do not skip this step!
If anything goes wrong, make sure you got the backup!

For this, run the app as usual. Then enter in a second terminal to create the database backup:
```bash
docker exec ownrecipes_db_1 sh -c \'exec mysqldump ownrecipes -u root -p"$MYSQL_ROOT_PASSWORD"\' > ownrecipes.sql'
```

When updating your local version that is deployed via docker,
you have to keep in mind that the installed dependencies
are being cached to reduce startup times.

Thus, when you update your local version and the new version
requires new dependencies (or new package versions), you will
have to clean up the related local docker stuff.

First, clean up everything:
```bash
cd OwnRecipes
sudo docker compose --profile all down
```

Now update your local repositories:
```bash
cd OwnRecipes
git checkout development
git pull

cd ownrecipes-api
git checkout development
git pull

cd ../ownrecipes-web
git checkout development
git pull
```

Then check the release notes or GitHub issues about any changes to the following files:
- docker-prod.override.yml
- .env.docker.production.api
- .env.docker.production.web

There should only be breaking changes to these files in major releases (IE. 2.0.0, 3.0.0).

Once you know your env and docker-compose files are up to date, [run the app as you usual](Running_the_App_in_dev.md#setup-ownrecipes):
```bash
sudo docker compose --profile all build
sudo docker compose --profile all up
```

Last but not least, if the database (MariaDB) was upgraded, you need to migrate the database:
```bash
sudo docker exec ownrecipes_db_1 sh -c 'exec mysql_upgrade -u root -p"$MYSQL_ROOT_PASSWORD"'
# Restart the app to reconnect the api to the updated database.
sudo docker compose --profile all stop
sudo docker compose --profile all up
```

Enjoy!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Updating the app without docker

You managed to run the App without docker, what is pretty cool.
Updating is a bit more involved, as running the App without docker is anyway.

First, make a backup. Do not skip this step!
If anything goes wrong, make sure you got the backup!

For this, run the app as usual. Then enter in a second terminal to create the database backup:
```bash
cd ownrecipes-api
. ./.env.service.local
mysqldump -u $MYSQL_USER -p"$MYSQL_PASSWORD" $MYSQL_DATABASE > /path/to/backup/folder/ownrecipes_db.sql
```

Second, check if your database (e. g. MariaDB) needs to be updated.
If so, do it now. Make sure to run `mysql_upgrade` afterwards.

Next, pull the latest from the repos:
```bash
sudo su ownrecipes

cd OwnRecipes
git pull

cd ownrecipes-api
git pull

cd ../ownrecipes-web
git pull
```

Then check the release notes about any changes to the following files:
- docker-prod.override.yml
- ownrecipes-api/.env[.service|.development|.production][.local]
- ownrecipes-web/.env[.service|.development|.production][.local]

There should only be breaking changes to these files in major releases (IE. 2.0.0, 3.0.0).

Then, [install the python requirements for ownrecipes-api](Running_the_App_Without_Docker_in_dev/#install-the-python-requirements) and [update all the dependencies for ownrecipes-web](Running_the_App_Without_Docker_in_dev/#install-the-dependencies).

Finally, [rebuild ownrecipes-web](#create-production-build-of-ownrecipes-web), deploy and run the app/service as usual.

Enjoy!

<p align="right">(<a href="#readme-top">back to top</a>)</p>
