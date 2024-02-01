#!/usr/bin/python3
"""
Model for Web server distribution script using Fabric
"""

from fabric.api import local
import tarfile
import os.path
import re
from datetime import datetime


def do_pack():
    """
    Distributes an archive containing the web_static directory to web servers.

    Returns:
        str: The path to the created archive
        or None if the archive creation fails.
    """
    # Ensure the 'versions' directory exists
    target = local("mkdir -p versions")

    # Generate a unique name for the archive based on the current timestamp
    string_name = str(datetime.now()).replace(" ", '')
    opt_sub = re.sub(r'[^\w\s]', '', string_name)

    # Create the tar archive with the web_static directory
    tar = local('tar -cvzf versions/web_static_{}.tgz web_static'.format(opt_sub))

    # Check if the archive was successfully created
    if os.path.exists("./versions/web_static_{}.tgz".format(opt_sub)):
        return os.path.normpath("/versions/web_static_{}.tgz".format(opt_sub))
    else:
        return None
