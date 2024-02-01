#!/usr/bin/python3
"""
Web server distribution script using Fabric for deployment.
"""

from fabric.api import *
import tarfile
import os.path
import re
from datetime import datetime

# Set default environment variables for Fabric
env.user = 'ubuntu'
env.hosts = ["52.91.147.15", "52.91.147.53"]
env.key_filename = "~/id_rsa"


def do_pack():
    """
    Create a compressed archive of the web_static directory.

    Returns:
        str: The path to the created archive
        or None if the archive creation fails.
    """
    # Ensure the 'versions' directory exists
    target = local("mkdir -p ./versions")

    # Generate a unique name for the archive based on the current timestamp
    name = str(datetime.now()).replace(" ", '')
    opt = re.sub(r'[^\w\s]', '', name)

    # Create the tar archive with the web_static directory
    tar = local('tar -cvzf versions/web_static_{}.tgz web_static'.format(opt))

    # Check if the archive was successfully created
    if os.path.exists("./versions/web_static_{}.tgz".format(opt)):
        return os.path.normpath("./versions/web_static_{}.tgz".format(opt))
    else:
        return None


def do_deploy(archive_path):
    """
    Deploy a web server archive to specified web servers.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Check if the provided archive_path exists
    if os.path.exists(archive_path) is False:
        return False

    try:
        # Extract information from the archive_path
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create necessary directories and extract the archive
        sudo('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))

        # Clean up by removing the temporary archive
        # -and moving web_static content
        sudo('rm /tmp/{}'.format(arc[1]))
        sudo('mv {}/web_static/* {}/'.format(main, main))

        # Update the symbolic link to point to the new release
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))

        return True
    except Exception as ex:
        # Handle exceptions and return False if deployment fails
        print(f"Deployment failed: {ex}")
        return False


def deploy():
    """
    Perform the deployment of the web server archive to specified web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    path = do_pack()
    if path is None:
        return False
    success = do_deploy(path)
    return success
