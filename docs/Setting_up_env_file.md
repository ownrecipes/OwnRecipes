## Configuring your Environment

This file will provide some context on the env settings.

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#database-config">Database config</a></li>
    <li><a href="#api--django-config">API / Django config</a></li>
    <li><a href="#web-config">Web config</a></li>
  </ol>
</details>

## Database config

The following environment variables can be applied to the ownrecipes-api/.env files.

Docker configurations come with MariaDB. We only need to set the following options, the rest are not required.
For a full list of settings see: https://hub.docker.com/_/mariadb/

#### MYSQL_HOST
The address or hostname of the DB.

Do not include this in your env file if you are using docker to house the DB.

EX: `MYSQL_HOST=my.db.com`

#### MYSQL_PORT
The port the database is exposed on.

Do not include this in your env file if you are using docker to house the DB.

EX: `MYSQL_PORT=3306`

#### MYSQL_DATABASE
The database name.

EX: `MYSQL_DATABASE=ownrecipes`

#### MYSQL_USER
The user for the database.

Do not include this in your env file if you are using docker to house the DB.

EX: `MYSQL_USER=ownrecipes`

#### MYSQL_PASSWORD
The password for the user given above.

Do not include this in your env file if you are using docker to house the DB.

EX: `MYSQL_PASSWORD=root`

#### MYSQL_ROOT_PASSWORD
The password for the mysql root user.

Only required if running the database via docker.

EX: `MYSQL_ROOT_PASSWORD=db-trustNo1`

### Generalized database variables
⚠ WARNING: Switching to a different DB engine is not supported! ⚠

You can use generalized variable names to utilize a different DB engine.
Do not use them if you are using the official docker builds.

<details>
  <summary>Generalized database variables</summary>

#### DATABASE_ENGINE
The django database engine package name.

EX: `DATABASE_ENGINE=django.db.backends.mysql`

#### DATABASE_HOST
The address or hostname of the DB.

EX: `DATABASE_HOST=my.db.com`

#### DATABASE_PORT
The port the database is exposed on.

EX: `DATABASE_PORT=3306`

#### DATABASE_NAME
The database name.

EX: `DATABASE_NAME=ownrecipes`

#### DATABASE_USER
The user for the database.

EX: `DATABASE_USER=ownrecipes`

#### DATABASE_PASSWORD
The password for the user given above.

EX: `DATABASE_PASSWORD=root`

</details>

### PostgreSQL
⚠ WARNING: The PostgreSQL DB engine is not supported! ⚠

You can either use the [generalized database variables](#generalized-database-variables), or even use specialized ones.
The specialized ones will also work with docker.

<details>
  <summary>PostgreSQL database variables</summary>

#### DATABASE_ENGINE
The django database engine package name.

EX: `DATABASE_ENGINE=django.db.backends.postgresql`

#### POSTGRES_HOST
The address or hostname of the DB.

EX: `POSTGRES_HOST=my.db.com`

#### POSTGRES_PORT
The port the database is exposed on.

EX: `POSTGRES_PORT=5432`

#### POSTGRES_DB
The database name.

EX: `POSTGRES_DB=ownrecipes`

#### POSTGRES_USER
The user for the database.

EX: `POSTGRES_USER=ownrecipes`

#### POSTGRES_PASSWORD
The password for the user given above.

EX: `POSTGRES_PASSWORD=root`

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## API / Django config

The following environment variables can be applied to the ownrecipes-api/.env files.

#### API_URL
This URL and port combination is used by gunicorn to serve the API.
For docker instances we need to serve via `0.0.0.0`.
`0.0.0.0` means "all IPv4 addresses on the local machine".
If a host has two IP addresses, 192.168.1.1 and 10.1.2.1,
and a server running on the host listens on 0.0.0.0,
it will be reachable at both of those IPs.

EX: `API_URL=0.0.0.0:5210`

#### API_PORT
The port the API is served from.

EX: `API_PORT=5210`

#### DJANGO_SECRET_KEY
A secret key for a particular Django installation.
This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
You can create one yourself or use a generator to do so.

For more information, see: https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY

EX: `DJANGO_SECRET_KEY=sdfsadfas32e98zsdvhhsnz6udvbksjdhfi4galshjfg`

#### DJANGO_SETTINGS_MODULE
The settings file that django will use.

EX: `DJANGO_SETTINGS_MODULE=base.settings`

#### DJANGO_DEBUG
Set the debug environment of the Django app.
This should be set to `False` in production and `True` to debug any issues.

EX: `DJANGO_DEBUG=False`

#### LOGGING
Set the logging behaviour (log level). Logs are written to file to `/path/to/ownrecipes-api/logs` and are named `\<logging>.log`.
Make sure that ownrecipes has write access to the parent directory.

Values (descriptions partially copied from https://docs.djangoproject.com/en/3.2/topics/logging/):

| Value    | Description                     |
| -------- | ------------------------------- |
| OFF      | Turns logging off.              |
| DEBUG    | Low level system information for debugging purposes. Should not be used for production to reduce disk usage etc. |
| INFO     | General system information. Should not be used for production to reduce disk usage etc. |
| WARNING  | Information describing a minor problem that has occurred. Can be helpful to fight issues in production. |
| ERROR    | (Default) Information describing a major problem that has occurred. Can be helpful to fight issues in production. |
| CRITICAL | Information describing a critical problem that has occurred. Can be helpful to fight issues in production. |

EX: `LOGGING=DEBUG` , will write debug information to `/opt/ownrecipes/ownrecipes-api/logs/debug.log`.

The logging configuration is provided by Django. Logging is a fairly complex and opinionated topic, therefore we won't cover it in detail here.
For example, one can send errors straight via e-mail.
If needed, please find more information in the [documentation of Django about logging](https://docs.djangoproject.com/en/3.2/topics/logging/).

#### ALLOWED_HOST
The hostname that the API is being served from.

For more information, see: https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts

EX: `ALLOWED_HOST=ryannoelk.com`

#### NODE_URL
The URL and port the web-app is served from.
The API will use this to prevent CORS issues.

EX: `NODE_URL=localhost:8080`

#### HTTP_X_FORWARDED_PROTO
If you are serving content behind an HTTPS proxy,
set this to `True`, otherwise `False`.

For more information, see: https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header

If you are using the OwnRecipes' nginx,
this setting will [activate the ssl encryption](Setting_up_https.md).

EX: `HTTP_X_FORWARDED_PROTO=True`

#### ADMIN_URL
The url the Django Admin Pages should be served from.
Default: `admin`.

EX: `ADMIN_URL=ownrecipes-admin`

#### DELETE_ORPHAN_FILES

Automatically deletes unused photos and thumbnails. Set to `False` if you want to keep
unused photos, or if you encounter any errors with deletion.
Default: `True`

EX: `DELETE_ORPHAN_FILES=False`

#### MENU_PLAN_GLOBAL

If all instance users share the same menu plan. Useful if the instance is running privately for a family.
Set to `True` if you want all users to view and edit each others menu.
Default: `False`

EX: `MENU_PLAN_GLOBAL=True`

#### SITE_MEDIA_URL
The url the media filse should be served from.
Default: `site-media`.

Is not supported for the docker production build.

EX: `SITE_MEDIA_URL=ownrecipes-site-media`

#### STATIC_FILES_URL
The url the static files, like css files, should be served from.
Default: `static-files`.

Is not supported for the docker production build.

EX: `STATIC_FILES_URL=ownrecipes-static-files`

#### RECIPE_IMAGE_QUALITY

Automatically reduces the size and quality of large images to save disk storage space. Default: `MEDIUM`.

| Value  | File size (estimate) | Size (width x height) | Quality  |
| ------ | -------------------- | --------------------- | -------- |
| OFF    | Original             | Original              | Original |
| HIGH   | 1200 kB              | 1920px x 1440px       | 97       |
| MEDIUM | 600 kB               | 1440px x 1080px       | 94       |
| LOW    | 350 kB               | 1024px x 768px        | 90       |

EX: `RECIPE_IMAGE_QUALITY=OFF`

## Web config

The following environment variables can be applied to the ownrecipes-web/.env files.

#### REACT_APP_API_URL
The hostname/port (my.example.com:5210) the frontend will call the API from.
If unset, the UI will call the API from the same hostname/port. If you are not using the default Nginx server that OwnRecipes comes with, you will either need to set this or configure your own proxy server to redirect all traffic that starts with `/api/` and `/admin/`.

EX: `REACT_APP_API_URL=http://localhost:5210`, `REACT_APP_API_URL=https://api.example.com`

#### REACT_APP_ADMIN_URL
If you have set up a different url for the DJANGO admin page, then you will have to set this variable accordingly.

EX: `REACT_APP_ADMIN_URL=http://localhost:5210/some-admin-path`, `REACT_APP_ADMIN=https://admin.api.example.com`

#### REACT_APP_REQUIRE_LOGIN
If you are storing recipes that would otherwise cause Copyright infringement, or you generally don't want strangers to view your recipes, then you can make OwnRecipes require a login to use any content. If set to `true`, users that are not logged in will be redirected to the login page.

EX: `REACT_APP_REQUIRE_LOGIN=true`

#### REACT_APP_LOCALE
The default (fallback) language the UI will be in.

Options:
- English: en
- German: de

EX: `REACT_APP_LOCALE=de`

#### REACT_APP_LEGAL_URL
If provided, a link to this url will be displayed in the footer.

If your instance of OwnRecipes is reachable from the internet, it may be regulated by law that you have to provide a legal page.

EX: `https://my-ownrecipes-instance.com/legal

#### REACT_APP_PRIVACY_URL
If provided, a link to this url will be displayed in the footer.

If your instance of OwnRecipes is reachable from the internet, it may be regulated by law that you have to provide a privacy page.

EX: `https://my-ownrecipes-instance.com/privacy

#### REACT_APP_DEMO
If set to 'true', then the app will run in demo mode.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
