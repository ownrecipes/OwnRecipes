# Migrating from OpenEats

Hello and welcome to OwnRecipes!

OwnRecipes is fork from OpenEats. Migrating to OwnRecipes is very easy.

## Steps

1. Setup OwnRecipes following the [Docker Guide](Running_the_App.md) or [Without Docker Guide](Running_the_App_Without_Docker.md). Either way, please be aware that there have been some changes to the structure of the environment-files, and the way the Web-App is being build. You will have to migrate your env-file(s), see below for a mapping of the old env-values.
2. Take a backup of OpenEats, following the official guide of [OpenEats](https://github.com/open-eats/OpenEats/docs/Taking_and_Restoring_Backups.md).
3. [Restore the backup into OwnRecipes](Taking_and_Restoring_Backups.md).
4. Follow the guide [Updating the App](Updating_the_App.md).

## Mapping of the OpenEats env values

You will have to change the following variable names.

Please be aware that there are also some new env-variables. Those are not listed here.

| OpenEats     | OwnRecipes |
| ------------ | ---------- |
| NODE_ENV     | (removed)  |
| NODE_URL     | (still there, but part of the api env) |
| NODE_API_URL | REACT_APP_API_URL |
| NODE_LOCALE  | REACT_APP_LOCALE  |
