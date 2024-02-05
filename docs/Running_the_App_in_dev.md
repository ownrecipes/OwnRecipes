# Running the app with docker for development

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

Install [docker and docker-compose](Install_Prerequisites.md/#docker).
Install [git](Install_Prerequisites.md/#git).

## Setup OwnRecipes

First clone the repos:
```bash
git clone https://github.com/ownrecipes/OwnRecipes.git
cd OwnRecipes

git clone https://github.com/ownrecipes/ownrecipes-api.git
git clone https://github.com/ownrecipes/ownrecipes-web.git
```

Then run it:
```bash
sudo docker compose --profile all build
sudo docker compose --profile all up
```

_[Click here if docker compose throws an error](Troubleshooting.md#docker-compose-throws-an-error)._

All container, db, api and web, should start successfully. Check the terminal output for any error. If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).

## First Time Setup

To create a super user:
```bash
sudo docker compose run --rm --entrypoint 'python manage.py createsuperuser' api
```
Follow the prompts given to create your user. You can do this as many times as you like.

If you want to add some test data you can load a few recipes and some news data. This data isn't really needed unless you just wanna see how the app looks and if its working.
```bash
sudo docker compose run --rm --entrypoint 'sh' api
./manage.py loaddata course_data.json
./manage.py loaddata cuisine_data.json
./manage.py loaddata news_data.json
./manage.py loaddata recipe_data.json
./manage.py loaddata ing_data.json
```

## Finish up

The set up is complete and everything should be up and running.

You can visit the [Admin Site](Admin_site.md), to create some more users, customize the news, or manage some lists.

Or you can straight away log in to the OwnRecipes web app. By default, the url will be `http://localhost:8080`.

OwnRecipes will shut down with your system. You can simply launch OwnRecipes by running:
```bash
cd OwnRecipes
sudo docker compose --profile all up
```

If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).

## Updating/Upgrading

See [Updating the App](Updating_the_App.md#running-the-app-with-docker-development)
