# Setting up HTTPS (experimental)

:warning: THIS FEATURE IS EXPERIMENTAL AND MAY NOT WORK AS EXPECTED. :warning:

It is highly recommended that you serve your content over https. [Let's Encrypt](https://letsencrypt.org/getting-started/) provides a super easy, automated, and free process for serving your content over https. If you are using nginx, they will also automatically update your plain http vhost files.

OwnRecipes has basic https support. It should be sufficient for most use cases. For more advanced needs, you may want to [set up your own proxy server](Creating_a_proxy_server_for_docker.md).

First, open the file `/opt/ownrecipes/docker-prod.yml`. For the nginx service, uncomment the ssl volume:
``` yml
services:
  # [...]
  nginx:
    # [...]
    volumes:
      # [...]
      - /opt/ownrecipes/ssl:/ssl/:ro
```

Make sure the directory `/opt/ownrecipes/ssl` exists, or create it. Move your ssl-certificate-files to `/opt/ownrecipes/ssl/cert.pem` (public key) and `/opt/ownrecipes/ssl/cert.key` (private key). It is crucial to name them exactly as stated, or nginx won't find them.

Second, in your file `/opt/ownrecipes/.env.docker.production.api` enable the [env-variable HTTP_X_FORWARDED_PROTO](Setting_up_env_file.md#http_x_forwarded_proto):
```
HTTP_X_FORWARDED_PROTO=true
```

Restart your docker containers.

  - `sudo docker compose -f docker-prod.yml -f docker-prod.override.yml -f docker-prod.version.yml restart`
  - OR
  - Just run the [`quick-start.py`](Running_the_App.md#start-docker-containers) script again

Open your OwnRecipes instance via https to confirm it worked.
