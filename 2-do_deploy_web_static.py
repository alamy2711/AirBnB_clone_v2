#!/usr/bin/python3
"""
Web server distribution script using Fabric for deployment.
"""

from fabric.api import *
import os.path

# Set default environment variables for Fabric
env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"


def do_deploy(archive_path):
    """
    Distributes a web server archive to specified web servers.

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
        arch = archive_path.split("/")
        base_striped = arch[1].strip('.tgz')

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create necessary directories and extract the archive
        sudo('mkdir -p /data/web_static/releases/{}'.format(base_striped))
        main = "/data/web_static/releases/{}".format(base_striped)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arch[1], main))

        # Clean up by removing the temporary archive
        # and moving web_static content
        sudo('rm /tmp/{}'.format(arch[1]))
        sudo('mv {}/web_static/* {}/'.format(main, main))

        # Update the symbolic link to point to the new release
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))

        return True
    except Exception as ex:
        # Handle exceptions and return False if deployment fails
        print(f"Deployment failed: {ex}")
        return False
