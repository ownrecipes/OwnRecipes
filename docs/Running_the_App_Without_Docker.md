# Running the App Without Docker in production

Running the App Without Docker in production requires some more steps:
1. You will need to [set up the project like for development](Running_the_App_Without_Docker_in_dev.md).
2. You will need to set up the [api](Running_the_App_Without_Docker_in_dev.md#setup-the-files) and [web](#setup-the-ownrecipes-environment-files) environment-variables for production.
3. You need to build the api.
4. To serve the web and api, you probably want and need to [configure a web server](#web-server-apache-2-option-1).

<details>
  <summary>⚠ Note for Windows users</summary>
  <p>
    This documentation is written for Linux-based systems.
    This documentation will not work with Windows, and you will have a hard time to get the set up done on Windows.
  </p>
  <p>
    Your best bet is to use Linux, or docker.
  </p>
</details>

### Setup the ownrecipes environment files

**Create environment file in /opt/ownrecipes-web/**

`cp /opt/ownrecipes/ownrecipes-web/.env.production /opt/ownrecipes/ownrecipes-web/.env.production.local`

Edit the created file `/opt/ownrecipes/ownrecipes-web/.env.production.local` and change the [variables](Setting_up_env_file.md) to your needs.

### Run ownrecipes-web

```bash
cd /opt/ownrecipes/ownrecipes-web
npm start
```

### Create production build of ownrecipes-web

```bash
cd /opt/ownrecipes/ownrecipes-web
npm run build
```

This will create the build directory as `/opt/ownrecipes/ownrecipes-web/build`.
The content of that directory can be deployed to and served by a [web server](#web-server-apache-2-option-1).

<hr />


## Web-Server: Apache 2 (Option 1)

**Info: If you prefer nginx, stick to the second option below and skip this step.**

`sudo apt-get install apache2`

### Create symbolic links for Apache2

```bash
mkdir /opt/ownrecipes/ownrecipes-apache2/
cd /opt/ownrecipes/ownrecipes-apache2/
ln -s /opt/ownrecipes/ownrecipes-web/build /opt/ownrecipes/ownrecipes-apache2/public-ui
ln -s /opt/ownrecipes/ownrecipes-api/static-files /opt/ownrecipes/ownrecipes-apache2/static-files
ln -s /opt/ownrecipes/ownrecipes-api/site-media /opt/ownrecipes/ownrecipes-apache2/site-media
```

*OwnRecipes will create the* **site-media** *directory when you upload the first image.*

### Edit /etc/apache2/sites-available/default.conf


```
   <VirtualHost *:80>
       ServerName ownrecipes.domain.com
       ServerAdmin postmaster@domain.com
       Header always set Strict-Transport-Security "max-age=15768000"
       DocumentRoot "/opt/ownrecipes/ownrecipes-apache2/public-ui"
       <Directory "/opt/ownrecipes/ownrecipes-apache2/public-ui">
           # HANDLE 404 ERROR ON REFRESH
           RewriteEngine On
           RewriteBase /
           RewriteRulesystemctl ^index\.html$ - [L]
           RewriteCond %{REQUEST_FILENAME} !-f
           RewriteCond %{REQUEST_FILENAME} !-d
           RewriteRule . /index.html [L]
           # HANDLE 404 ERROR ON REFRESH END
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
           Order allow,deny
           allow from all
           Require all granted
       </Directory>

       Alias /static /opt/ownrecipes/ownrecipes-apache2/public-ui/static
       <Location "/static/">
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
           Order allow,deny
           allow from all
           Require all granted
           AddOutputFilterByType DEFLATE text/plain
           AddOutputFilterByType DEFLATE text/javascript
           AddOutputFilterByType DEFLATE application/javascript
           AddOutputFilterByType DEFLATE application/xml
           AddOutputFilterByType DEFLATE application/xhtml+xml
       </Location>

       <Location "/api/">
           ProxyPass http://127.0.0.1:5210/api/
           ProxyPassReverse http://127.0.0.1:5210/api/
       </Location>

       <Location "/admin/">
           ProxyPass http://127.0.0.1:5210/admin/
           ProxyPassReverse http://127.0.0.1:5210/admin/
       </Location>

       Alias /static-files /opt/ownrecipes/ownrecipes-apache2/static-files
       <Directory "/opt/ownrecipes/ownrecipes-apache2/static-files">
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
           Order allow,deny
           allow from all
           Require all granted
       </Directory>
       Alias /site-media /opt/ownrecipes/ownrecipes-apache2/site-media
       <Directory "/opt/ownrecipes/ownrecipes-apache2/site-media">
           Options Indexes FollowSymLinks MultiViews
           AllowOverride All
           Order allow,deny
           allow from all
           Require all granted
       </Directory>
   </VirtualHost>
```

### Reload Apache configuration

`sudo service apache2 restart`

Your OwnRecipes installation should run on your http://ownrecipes.domain.com.

It is HIGHLY recommended you eventually switch over to an HTTPS setup. Let's Encrypt is great for getting that set up.

## Web-Server: nginx (Option 2)

**Info: If you prefer Apache, stick to the first option above and skip this step.**

`sudo apt-get install nginx`

### Create symbolic links for nginx

```bash
mkdir /opt/ownrecipes/ownrecipes-nginx/
cd /opt/ownrecipes/ownrecipes-nginx/
ln -s /opt/ownrecipes/ownrecipes-web/build /opt/ownrecipes/ownrecipes-nginx/public-ui
ln -s /opt/ownrecipes/ownrecipes-api/static-files /opt/ownrecipes/ownrecipes-nginx/static-files
ln -s /opt/ownrecipes/ownrecipes-api/site-media /opt/ownrecipes/ownrecipes-nginx/site-media
```

*OwnRecipes will create the* **site-media** *directory when you upload the first image.*

### Edit /etc/nginx/sites-available/default

```
server {
    listen 80;
    server_name ownrecipes.com;
    disable_symlinks off;

    location / {
        root /opt/ownrecipes/ownrecipes-nginx/public-ui;
        if ($uri = '/index.html') {
            add_header Cache-Control no-store always;
        }
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass       http://127.0.0.1:5210;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Allow the upload of any image size.
        client_max_body_size 0;
    }

    location /static-files/ {
        autoindex on;
        root /opt/ownrecipes/ownrecipes-nginx;
    }

    location /site-media/ {
        autoindex on;
        root /opt/ownrecipes/ownrecipes-nginx;
    }

    location /admin/ {
        proxy_pass       http://127.0.0.1:5210/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
}
```

### Reload Nginx configuration

`sudo service nginx restart`

Your OwnRecipes installation should run on your http://ownrecipes.domain.com.

It is HIGHLY recommended you eventually switch over to an HTTPS setup. Let's Encrypt is great for getting that set up.

<hr />

## Finish up

The set up is complete and everything should be up and running.

You can visit the [Admin Site](Admin_site.md), to create some more users, customize the news, or manage some lists.

Or you can straight away log in to the OwnRecipes web app. By default, the url will be `http://localhost:8080`, or `http://<ownrecipes.domain.com>:8080`.

If you encounter any issue, please read the [Troubleshooting guide](Troubleshooting.md).

## Updating/Upgrading

See [Updating the App](Updating_the_App.md#updating-the-app-without-docker)
