<a name="readme-top"></a>

# Backing up Your Data

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#docker">Docker</a></li>
    <li><a href="#without-docker">Without docker</a></li>
  </ol>
</details>

## Docker

The following commands can be used to take backups of your data and restore those backups. The backup commands are automatically run when you upgrade to a newer version as well.

### Recipes Images

#### Backing up:

Replace `/dir/on/local/system/` with the location where you would like your images.

```sh
docker cp ownrecipes_api_1:/code/site-media/ /dir/on/local/system/
```

#### Restoring:

Replace `/dir/on/local/system/` with the location where you would like your images.

```sh
docker cp /dir/on/local/system/site-media/. ownrecipes_api_1:/code/site-media/
```

### Database

#### Backing up:

Places a sql dump of the database on your current working directory.

```sh
docker exec ownrecipes_db_1 sh -c 'exec mysqldump ownrecipes -u root -p"$MYSQL_ROOT_PASSWORD"' > ownrecipes.sql
```

#### Restoring:

First cd into the dir that contains your sql backup. Once there you need to source your env file so you don't have to type your database password on the command line. Then run the last command to start the restore.
Note: if you changed the database name then you will need to change the last word the statement below to the database name you gave OwnRecipes.

```sh
cd OwnRecipes
source .env.docker.production.api
cat ownrecipes.sql | docker exec -i ownrecipes_db_1 /usr/bin/mysql -u root -p"$MYSQL_ROOT_PASSWORD" ownrecipes
```

### Sources
- [Copying Image Files to and from Docker Containers/Volumes](https://gist.github.com/spalladino/6d981f7b33f6e0afe6bb)
- [DB backups/restores](https://stackoverflow.com/questions/22907231/copying-files-from-host-to-docker-container)


## Without docker

### Recipes Images

#### Backing up:

Replace `/dir/on/local/system/` with the location where you would like your images.

```sh
cp /opt/ownrecipes/ownrecipes-api/site-media /dir/on/local/system/
```

#### Restoring:

Replace `/dir/on/local/system/` with the location where you would like your images.

```sh
cp /dir/on/local/system/site-media/. /opt/ownrecipes/ownrecipes-api/site-media/
```

### Database

#### Backing up:

Places a sql dump of the database on your current working directory.

(Please point to your actual .env, e.g. `.env.service.local`.)

```sh
cd /opt/ownrecipes/ownrecipes-api
. ./.env
mysqldump $MYSQL_DATABASE -u $MYSQL_USER -p"$MYSQL_PASSWORD" > ownrecipes.sql
```

#### Restoring:

```sh
cd /opt/ownrecipes/ownrecipes-api
. ./.env
sudo mysql ownrecipes -u $MYSQL_USER -p"$MYSQL_PASSWORD" < /path/to/your/ownrecipes.sql
```
