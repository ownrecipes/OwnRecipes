<a name="readme-top"></a>

# Running the App: Tricks

Below some tips and tricks for running the app for some edge-cases.

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#host-api-and-web-on-different-devices">Host api and web on different devices</a></li>
    <li><a href="#web-developer-run-the-api-via-docker-and-the-web-via-npm">Web-Developer? Run the api via docker, and the web via npm</a></li>
    <li><a href="#single-board-computer">Single-board computer</a></li>
    <li><a href="#just-build-the-web-via-docker">Just build the web via docker</a></li>
    <li><a href="#switching-to-a-different-db-engine">Switching to a different DB engine (NOT SUPPORTED)</a></li>
  </ol>
</details>

## Host api and web on different devices

You can split the app up on different devices, or even [connect to a remote DB](Running_the_App.md#connecting-to-a-remote-db).
You will have to make some changes to the used env files (based on your set up),
and be careful about CORS errors and such.

Usually, this isn't necessary and the preferred way is to host everything on one server/device.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Web-Developer? Run the api via docker, and the web via npm

If you just want to run ownrecipes-web in development without docker, and actually don't mind to set up ownrecipes-api via docker, then that may be actually way easier then setting up everything without docker (because getting the api up to running is quite involved).

To only set up the api + MariaDB via docker, follow the guide [Running the App in development](Running_the_App_in_dev.md).

You can only run the api + MariaDB like this:

_Note: This will require docker-compose version 1.28+, as it makes use of the profiles-feature._

```bash
cd OwnRecipes
sudo docker compose build
sudo docker compose up
```

Then, [set up the web without docker for development](Running_the_App_Without_Docker_in_dev.md/#ownrecipes-web). If you didn't change the environment-files for ownrecipes-api, then you probably don't need to for ownrecipes-web, too! \o/

Just start the web in development and you should be ready to rumble:
```bash
cd ownrecipes-web
npm start
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Single-board computer

I am running OwnRecipes on my Raspberry Pi 3, and it is performing quite well.

Key is to [run it without docker](Running_the_App_Without_Docker.md), as docker is too resource-hungry for my Raspberry Pi 3.

You can even host OwnRecipes under a sub-path, like https://my-raspberry-pi.com/ownrecipes.
First, make sure that your [web-server](Running_the_App_Without_Docker.md/#web-server-nginx-option-2) is really listening for / serving the right sub-path accordingly. I use nginx over apache, as I found it to perform better.

Then, change the file `ownrecipes-web/package.json`,
that the config `homepage` is pointing to your domain and sub-path, for example:
```json
{
  "...": "...",
  "homepage": "https://my-raspberry-pi.com/ownrecipes",
  "...": "...",
}
```

Build that:
```bash
cd ownrecipes-web
npm run build
```

And copy the result to the directory that your web-server is serving.

**Tip:** As building the web takes pretty long on my Raspberry Pi, I rather do that on my desktop computer, and copy the result via scp to my Raspberry Pi. You don't need NodeJS on your Raspberry Pi to run the web,
as the app is compiled to a static website. Make sure that the `.env.production.local` is fed with correct values, or create a separate file `.env.raspi`. Build the app with `REACT_APP_ENV=raspi npm run build:prod`. Alternatively, [just build the web via docker](#just-build-the-web-via-docker) on your powerful machine and copy the result.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Just build the web via docker

You can host ownrecipes-web without docker, but use docker to build it. This can be useful to build it on a different machine, e. g. for [hosting it on a Raspberry Pi](#single-board-computer).

Build web:
```bash
cd ownrecipes-web
sudo ./docs/scripts/docker_build.sh
```

Note that the result will be the build as tar-archive.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Switching to a different DB engine

⚠ WARNING: Switching to a different DB engine is not supported! ⚠

By default the DB engine MariaDB is being used. When [running the api without docker](Running_the_App_Without_Docker.md), the DB engine can be replaced. The required steps include:

* Edit `<ownrecipes-api\>/base/requirements.txt`: Substitute the mysqlclient-package, e. g. by `psycopg2` to utilize PostgreSQL.
* Edit the [env-file](Setting_up_env_file.md#generalized-database-variables): Include `DATABASE_ENGINE`. Replace the MYSQL-variables with either the [PostgreSQL variables](Setting_up_env_file.md#postgresql) or the [generalized variables](Setting_up_env_file.md#generalized-database-variables).
* If running with docker, then you will need to build or use the api locally, and edit the `docker-prod.yml` or `docker-compose.yml` accordingly.
