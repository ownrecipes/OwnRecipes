# Migrating from OpenEats

Hello and welcome to OwnRecipes!

OwnRecipes is a fork from OpenEats. Migrating to OwnRecipes is very easy. The important bit to know is, that you can not just copy the OpenEats database into the current release of OwnRecipes. Instead, migrate to the first release 3.0.0 of OwnRecipes, and then [Updating the App](Updating_the_App.md) to the newest release.

Another way is explained further below in [Migrating using the current release of OwnRecipes](#migrating-using-the-current-release-of-ownrecipes). This may be preferred, if launching an outdated setup is not desired due to security compliances or other reasons.

## Steps

1. Setup OwnRecipes v3.0.0 following the [Docker Guide](Running_the_App.md) or [Without Docker Guide](Running_the_App_Without_Docker.md). Make sure after cloning the git repo(s) to checkout the git tag 3.0.0: `git checkout 3.0.0`. Be aware that there have been some changes to the structure of the environment-files, and the way the Web-App is being build. You will have to migrate your env-file(s), see below for a mapping of the old env-values.
2. Take a backup of OpenEats, following the [official guide of OpenEats](https://github.com/open-eats/OpenEats/docs/Taking_and_Restoring_Backups.md).
3. [Restore the backup into OwnRecipes](Taking_and_Restoring_Backups.md).
4. Follow the guide [Updating the App](Updating_the_App.md) to migrate to the newest release of OwnRecipes.

## Mapping of the OpenEats env values

You will have to change the following variable names.

Please be aware that there are also some new env-variables. Those are not listed here. All available env-variables are listed in the doc [Setting_up_env_file](Setting_up_env_file.md).

| OpenEats     | OwnRecipes |
| ------------ | ---------- |
| NODE_ENV     | (removed)  |
| NODE_URL     | (still there, but part of the api env) |
| NODE_API_URL | REACT_APP_API_URL |
| NODE_LOCALE  | REACT_APP_LOCALE  |

## Migrating using the current release of OwnRecipes (EXPERIMENTAL)

Another way to migrate the OpenEats database is to run the current release of OwnRecipes WITH DOCKER IN DEVELOPMENT MODE, run the django migrations to the point of the OpenEats database, restore the database backup, and then run the remaining django migrations.

**Steps:**

1. Setup OwnRecipes following the [Docker Guide](Running_the_App.md). Be aware that there have been some changes to the structure of the environment-files, and the way the Web-App is being build. You will have to migrate your env-file(s), see above for a mapping of the old env-values.
2. Run the django migrations for OpenEats: Get the api container-id from `sudo docker ps`. Then run `sudo docker exec -i <container-id> /bin/sh < ownrecipes-api/docs/migrate-openeats.sh`. This will run the django migration-scripts for OwnRecipes release 3.0.0, that are compatible with OpenEats 1.5.1. Consider the `migrate-openeats.sh` script as experimental.
3. Take a backup of OpenEats, following the [official guide of OpenEats](https://github.com/open-eats/OpenEats/docs/Taking_and_Restoring_Backups.md).
4. [Restore the backup into OwnRecipes](Taking_and_Restoring_Backups.md).
5. Finally, run the remaining django migrations for OwnRecipes, following the guide [Updating the App](Updating_the_App.md).

**Without docker:**
The steps should be fairly similar, but it is not tested. Please be aware that you will have to edit the `migrate-openeats.sh` script to use the proper paths. As you have read the docs up to this point, you will most certainly get it done. ;-)