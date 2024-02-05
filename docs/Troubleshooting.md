<a name="readme-top"></a>

# Troubleshooting

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#docker-compose-throws-an-error">docker-compose throws an error</a></li>
    <li><a href="#can-not-create-a-superuser">Can not create a superuser</a></li>
    <li><a href="#the-docker-container-ownrecipes_web_1-exits">The docker container ownrecipes_web_1 exits</a></li>
    <li><a href="#browser-can-not-reach-the-web-app">Browser can not reach the web-app</a></li>
    <li><a href="#browser-can-not-connect-to-the-api">Browser can not connect to the api</a></li>
  </ol>
</details>

## docker-compose throws an error

If running a `docker compose`-command throws an error like:
```
docker: command not found
```

Then your setup is missing docker, or you are using the older docker-compose V1.
In the latter case, use the older command `docker-compose`.

If running a `docker-compose`-command throws an error like:
```
ERROR: The Compose file './docker-prod.yml' is invalid because:
services.api.depends_on contains an invalid type, it should be an array
```

Then your setup doesn't meet the [minimum requirement for docker-compose](Install_Prerequisites.md#note-on-docker-compose-version). Please follow the instructions to fix the setup.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Can not create a superuser

You have started the db and api, but can not [create the superuser](Running_the_App.md#first-time-setup) for the api.

Then probably your api can not connect to the db. Please double check your env-file (`.env.docker.production.api` when running via docker in production).
The vars `MYSQL_DATABASE` and `MYSQL_ROOT_PASSWORD` are used to connect to the db, make sure they are correct.

You may also want to check the terminal output for any errors during start. If you run the `quick-start.py`-script, then some errors may be hidden. Run the following command instead to get a more comprehensive output: `docker compose -f docker-prod.yml -f docker-prod.override.yml -f docker-prod.version.yml restart`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## The docker container ownrecipes_web_1 exits

In production, the container `ownrecipes_web_1` will exit. This is intended behaviour. The container will initialize the web-app and provide the build as volume, that is mounted into the nginx.
After the initialization, the container is not needed any longer and therefore will exit.

The required containers for OwnRecipes to operate are db, api and nginx. With your browser of choice, you should be able to connect to the web-app via the nginx, that you can reach via the configured url (see `.env.docker.production.api`, var `NODE_URL`).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Browser can not reach the web-app

Double check that you are using the correct url. If you run OwnRecipes via docker in production mode, the url is configured in `.env.docker.production.api` and the port is specified in `docker_prod_override.yml` (see the nginx port mapping).

If you still can't reach the web-app, please double check that OwnRecipes is running. If you run OwnRecipes via docker, run `docker ps` in a terminal and check that the containers db, api and nginx (or web if hosting in development mode) are up. If any of your services is not running, you will have to investigate that. You may want to check any console output whatsoever.

If all your services/containers are up and healthy, then reduce the technical complexity. For instance, temporarily [disable ssl](Setting_up_https.md). You can also by-pass the web-app altogether and try to reach the [admin site](Admin_site.md). The admin site is powered by the api (Django) and is unrelated to the web-app. If you can not reach the admin site, than either your urls are wrong, or your nginx is not functional, or perhaps there is some firewall interfering.

Last, you can check that the api (and db) are functional. For instance, you could repeat the [creation of the superuser](Running_the_App.md#first-time-setup).

If all of those steps couldn't help you to get your OwnRecipes running, feel free to [open an issue](https://github.com/ownrecipes/OwnRecipes/blob/master/CONTRIBUTING.md) and we will get it solved together.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Browser can not connect to the api

When you open the web-app, there pops up an alert "Connection to the server failed. Please try again later.".
This means that you certainly reach the web-app, and (if running in production) therefore that also the nginx is probably functional. But the web-app can not send requests to the api.

First, check that your api is running, for instance that the docker container is up (run `docker ps` in a terminal). If it is, try to reach the [admin site](Admin_site.md). The admin site is powered by the api (Django) and is unrelated to the web-app. If you can not reach the admin site, than either your urls are wrong, or your nginx is not functional, or perhaps there is some firewall interfering.

If you can reach the admin site, then your api and db are up and running, and appearently also your nginx and web-app. This is good news! Now, check why the web-app can not reach the api. First, check that the env-file for the web-app (`.env.docker.production.web` when running with docker in production mode) is correct. The var [`REACT_APP_API_URL`](Setting_up_env_file.md#react_app_api_url) is used to send the requests to the api. Make sure it is correct, and includes the protocol (http, https), host and port. Second, perhaps also reduce the technical complexity, for instance temporarily [disable ssl](Setting_up_https.md).

You can also open the browser developer tools (probably by pressing `[F12]`) and switch to the Network tab. (I recommend Firefox for this, as I find Chrome's Network tab confusing.) There you can gather more information about future requests made to the api (-> open the developer tools, Network tab first, then reload your web-app). You should see some requests handled by nginx directly (like css and js files), that are probably succeeding. And you should see the failing request(s) to the api (probably `/ownrecipes-api/api/v1/news/entry/` and `/ownrecipes-api/api/v1/recipe/mini-browse/` when visiting the home page).

If all of those steps couldn't help you to get your OwnRecipes running, feel free to [open an issue](https://github.com/ownrecipes/OwnRecipes/blob/master/CONTRIBUTING.md) and we will get it solved together.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
