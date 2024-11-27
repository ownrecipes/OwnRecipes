# Creating a Release

## Preparation

### Make sure everything is finished

1. Update the locales for ownrecipes-web. You might need a release-branch to do so.
    ```bash
    cd OwnRecipes/ownrecipes-web
    npm run locales
    ```
2. Update the env-files for docker-production:
    ```bash
    cd OwnRecipes
    cp ownrecipes-web/.env.production .env.docker.production.web
    cp ownrecipes-api/docs/samples/docker/.env.production .env.docker.production.api
    ```

### Start releases

<details>
  <summary>Web</summary>

```bash
cd ownrecipes-web
git checkout -b release/<version>

>> manual step: update package.json version && package-lock.json version

git add .
git commit -m "Release <version>"

git push -u origin release/<version>

>> manual step: merge via GitHub

git checkout master
git pull

git checkout development
git merge --no-ff master

>> manual step: bump package.json version && package-lock.json version

git add .
git commit -m "Prepare next version"

git push
```

</details>
<details>
  <summary>Demo</summary>

```bash
>> manual step: get release commit-id of ownrecipes-web

git checkout gh-pages-deploy
git rebase commit-id
npm install
npm run deploy
git push --force
```

</details>
<details>
  <summary>Api</summary>

```bash
git checkout development
git pull

git checkout -b release/<version>

>> manual step: update base/urls.py version

git add .
git commit -m "Release <version>"

git push -u origin release/<version>

>> manual step: merge via GitHub

git checkout master
git pull

git checkout development
git merge --no-ff master

git push
```

</details>
<details>
  <summary>Nginx</summary>

```bash
Nothing to do.
```

</details>
<details>
  <summary>OwnRecipes</summary>

```bash
git checkout -b release/<version>

>> manual step: Copy README.MD to docs/index.md, fixup links to docs

>> manual step: update quick-start.py, variable app_version

>> manual step: create releases/<version>.json

git add .
git commit -m "Release <version>"
git push -u origin release/<version>

>> manual step: merge via GitHub

git checkout master
git pull

git checkout development
git merge --no-ff master

git push
```

</details>

## GitHub

1. Get an Auth token from GitHub. See [GitHub Help](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) for details on how to do this.
2. Create a file named `secrets.py` with the following content:
    ```python
    #!/usr/bin/env python
    # encoding: utf-8

    username = 'username'
    password = 'token'
    ```
3. Create a release doc and place in the releases folder. See the release folder for examples.
4. Once you have a release file created, you can run the release script. This script takes the release file you just created as its only argument.
  - `./release releases/x.x.x.json`

## Docker

### ownrecipes-nginx

Checkout the source, build the image, tag it and upload it to docker-hub:

```bash
# Checkout the source
git clone https://github.com/ownrecipes/ownrecipes-nginx --branch <tag>
cd ownrecipes-nginx

# Build the image, tag it
docker build . -t ownrecipes/ownrecipes-nginx:<tag>
docker build . -t ownrecipes/ownrecipes-nginx:latest

# Upload it to docker-hub
docker login
docker push ownrecipes/ownrecipes-nginx:<tag>
docker push ownrecipes/ownrecipes-nginx:latest
```

### ownrecipes-api

Checkout the source, build the image, tag it and upload it to docker-hub:

```bash
# Checkout the source
git clone https://github.com/ownrecipes/ownrecipes-api --branch <tag>
cd ownrecipes-api

# Build the image, tag it
docker build . -t ownrecipes/ownrecipes-api:<tag>
docker build . -t ownrecipes/ownrecipes-api:latest

# Upload it to docker-hub
docker login
docker push ownrecipes/ownrecipes-api:<tag>
docker push ownrecipes/ownrecipes-api:latest
```

### ownrecipes-web

Checkout the source, build the app, build the image, tag it and upload it to docker-hub:

```bash
# Checkout the source
git clone https://github.com/ownrecipes/ownrecipes-web --branch <tag>
cd ownrecipes-web

# Build the app
npm install
npm run build

# Build the image, tag it
docker build . -f Dockerfile-release -t ownrecipes/ownrecipes-web:<tag>
docker build . -f Dockerfile-release -t ownrecipes/ownrecipes-web:latest

# Upload it to docker-hub
docker login
docker push ownrecipes/ownrecipes-web:<tag>
docker push ownrecipes/ownrecipes-web:latest
```
