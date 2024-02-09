#!/usr/bin/env python
# encoding: utf-8

from time import sleep
from os import getcwd, name as os_name
from subprocess import call, Popen, DEVNULL, PIPE, STDOUT


def update_image_tags(version=None):
    """
    A simple function to configure the OwnRecipes version.

    :param version: The version of OwnRecipes the users wants to run.
                    This is a git Tag.
    :return: A file called `docker-prod.version.yml`.
             With the version of each image to pull.
    """
    version = version if version is not None else 'latest'
    version = '''version: '3.1'
services:
  api:
    image: ownrecipes/ownrecipes-api:%s
  web:
    image: ownrecipes/ownrecipes-web:%s
  nginx:
    image: ownrecipes/ownrecipes-nginx:%s
''' % (version, version, version)
    with open('docker-prod.version.yml', 'w') as f:
        f.write(version)


def download_images(version=None):
    """ Download the required images """
    version = version if version is not None else 'latest'
    print("==================")
    print("Downloading Images")
    print("==================")
    call(['docker', 'pull', 'ownrecipes/ownrecipes-api:' + version])
    call(['docker', 'pull', 'ownrecipes/ownrecipes-web:' + version])
    call(['docker', 'pull', 'ownrecipes/ownrecipes-nginx:' + version])


def getDockerCompose():
    """ Check if docker-compose V1 or V2 is available """
    try:
        Popen(['docker-compose', '--version'], stdin=DEVNULL, stdout=DEVNULL, stderr=STDOUT)
        return 'docker-compose'
    except OSError:
        return 'docker compose'


def start_containers():
    """
    Takes a back up of the Recipe images and DB.
    Restarts OwnRecipes with a new (or the same) version.
    """
    print("==================")
    print("Starting OwnRecipes")
    print("==================")

    dockerCompose = getDockerCompose()
    if dockerCompose is None:
        raise RuntimeError("docker-compose not found. Please install the requirements and try again.")
    dockerComposeArr = dockerCompose.split(' ')

    # Check if the DB is up and running locally.
    # If it is then take a backup.
    # If the user is using a remote DB, do nothing.
    # If no DB is found, Start the docker DB and wait 45s to start.
    p = Popen(
        ['docker', 'ps', '-q', '-f', 'name=ownrecipes_db_1'],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if output and not err:
        print("Taking a database backup (saving as ownrecipes.sql)...")
        if os_name == 'nt':
            call(
                'docker exec ownrecipes_db_1 sh -c ' +
                '"exec mysqldump ownrecipes -u root -p"$MYSQL_ROOT_PASSWORD""' +
                ' > ownrecipes.sql',
                shell=True
            )
        else:
            call(
                'docker exec ownrecipes_db_1 sh -c ' +
                '\'exec mysqldump ownrecipes -u root -p"$MYSQL_ROOT_PASSWORD"\'' +
                ' > ownrecipes.sql',
                shell=True
            )
    elif 'MYSQL_HOST' in open('.env.docker.production.api').read():
        # TODO: add process to backup remote DB
        print("Using remote DB...")
    else:
        print("Creating the DB. This may take a minute...")
        call([*dockerComposeArr, '-f', 'docker-prod.yml', 'up', '-d', 'db'])
        sleep(45)

    # Check if the API is up.
    # If it is then take a backup of the Recipe images folder.
    # The backup folder is called `site-media`.
    p = Popen(
        ['docker', 'ps', '-q', '-f', 'name=ownrecipes_api_1'],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if output and not err:
        print("Taking a image backup save to 'site-media'...")
        call(
            'docker cp ownrecipes_api_1:/code/site-media/ ' + getcwd(),
            shell=True
        )

    # Stop each container that needs to be updated.
    # Don't stop the DB! There is no reason to.
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'nginx'
    ])
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'web'
    ])
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'api'
    ])

    # Start all the containers
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'up', '-d'
    ])

    print("App started. Please wait ~30 seconds for the containers to come online.")


def stop_containers():
    print("==================")
    print("Stopping OwnRecipes")
    print("==================")

    dockerCompose = getDockerCompose()
    if dockerCompose is None:
        raise RuntimeError("docker-compose not found. Please install the requirements and try again.")
    dockerComposeArr = dockerCompose.split(' ')

    # Stop each container.
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'nginx'
    ])
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'web'
    ])
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'api'
    ])
    call([
        *dockerComposeArr,
        '-f', 'docker-prod.yml',
        '-f', 'docker-prod.version.yml',
        '-f', 'docker-prod.override.yml',
        'stop', 'db'
    ])


    print("App stopped.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='OwnRecipes quick setup script. '
                    'This script will restart your OwnRecipes server and '
                    'take a database and recipe image backup.'
    )
    parser.add_argument(
        '-t',
        '--tag',
        type=str,
        help='The git tag of OwnRecipes you want to run. '
             'If not included, then the master branch will be used.'
    )
    parser.add_argument(
        'stop',
        nargs='?',
        help='Stops all OwnRecipes containers for the specified tag (or master).'
    )
    args = parser.parse_args()

    update_image_tags(args.tag)
    if args.stop:
        stop_containers()
    else:
        download_images(args.tag)
        start_containers()
