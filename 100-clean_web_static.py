#!/usr/bin/python3
"""
Web server distribution script for cleaning up out-of-date archives.
"""

from fabric.api import *
from fabric.state import commands, connections
import os.path

# Set default environment variables for Fabric
env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"


def do_clean(number=0):
    """
    Deletes out-of-date archives on both local and remote servers.

    Args:
        number (int): The number of archives to keep.
        Defaults to 0 (keeps at least one).

    Returns:
        None
    """
    # Get the list of archives on the local machine
    local_archives = local('ls -t ~/AirBnB_Clone_V2/versions/').split()

    # Get the list of releases on the remote server
    with cd("/data/web_static/releases"):
        remote_archives = sudo("ls -t .").split()

    # Set the base path for remote releases
    remote_path = "/data/web_static/releases"

    # Convert number to integer
    number = int(number)

    # Determine the number of archives to keep
    num_to_keep = 1 if number == 0 else number

    # Remove excess local archives
    if len(local_archives) > num_to_keep:
        local_to_remove = local_archives[num_to_keep:]
        for archive in local_to_remove:
            local('rm -f ~/AirBnB_Clone_V2/versions/{}'.format(archive))

    # Remove excess remote releases
    if len(remote_archives) > num_to_keep:
        remote_to_remove = remote_archives[num_to_keep:]
        for release in remote_to_remove:
            sudo('rm -rf {}/{}'.format(remote_path, release.strip(".tgz")))
