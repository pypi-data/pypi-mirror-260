# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import distro
import os
import shutil
import signal
import subprocess
import sys
from glob import glob
from pathlib import Path

from promptflow.runtime.utils import logger


def signal_handler(signum, frame):
    signame = signal.Signals(signum).name
    logger.info("Receiving signal %s (%s).", signame, signum)
    try:
        logger.info("Stopping all services.")
        for s in glob("/service/runit/*"):
            logger.info("Stopping service %s.", s)
            subprocess.run(["sv", "stop", s])
    finally:
        sys.exit(1)


# register signal handler to gracefully shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def copy_package_data():
    package_data_folder = Path(__file__).resolve().parent.parent / "package_data"
    if not package_data_folder.exists():
        raise RuntimeError("Prompt flow sdk package data folder not found")
    logger.info(f"Find prompt flow runtime package data: {package_data_folder}")

    target_folder = Path("/service")
    shutil.copytree(package_data_folder, target_folder, dirs_exist_ok=True)
    # chmod to executable
    for root, dirs, files in os.walk(target_folder):
        for d in [os.path.join(root, d) for d in dirs]:
            os.chmod(d, 0o755)
        for f in [os.path.join(root, f) for f in files]:
            os.chmod(f, 0o755)
    logger.info(f"Copy prompt flow runtime package data to: {target_folder}")


def ensure_runit_installed():
    """Install runit if not exists."""
    if shutil.which("runsvdir") is not None:
        return

    logger.info("Installing runit...")
    try:
        if distro.id() in ["ubuntu", "debian"]:
            subprocess.run(
                ["apt-get", "update"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["apt-get", "install", "runit", "-y"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if shutil.which("runsvdir") is None:
                raise RuntimeError("There is installation failure and can not found 'runsvdir'.")

            logger.info("Successfully installed runit.")
        else:
            raise RuntimeError(f"Unsupported Linux distribution: {distro.id()}")
    except Exception as e:
        logger.error("Failed to install runit: %s", e)
        raise


def ensure_azcopy_installed():
    """Install azcopy if not exists."""
    if shutil.which("azcopy") is not None:
        return

    logger.info("Installing azcopy...")
    try:
        # install wget if not exists
        if shutil.which("wget") is None:
            subprocess.run(
                ["apt-get", "install", "wget", "-y"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        subprocess.run(
            ["wget", "https://aka.ms/downloadazcopy-v10-linux", "-O", "azcopy.tar.gz"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(["tar", "-xf", "azcopy.tar.gz", "--strip-components=1"], check=True)
        shutil.move("./azcopy", "/usr/bin/azcopy")
        os.chmod("/usr/bin/azcopy", 0o755)

        logger.info("Successfully installed azcopy.")
    except Exception as e:
        logger.error("Failed to install azcopy: %s", e)
        raise


def ensure_linux_distribution_supported():
    if sys.platform != "linux":
        raise RuntimeError("Only Linux distribution is supported.")

    logger.info("Linux distribution info: %s", distro.info())

    if distro.id() not in ["ubuntu", "debian"]:
        raise RuntimeError("Only Ubuntu, Debian Linux distributions are supported.")


def main():
    try:
        # add argparse when needed
        logger.info("Starting prompt flow runtime...")

        ensure_linux_distribution_supported()
        ensure_runit_installed()
        ensure_azcopy_installed()
        copy_package_data()

        entry_process = subprocess.Popen(["runsvdir", "/service/runit"], shell=False)
        logger.info("Started prompt flow runtime successfully.")
        entry_process.wait()
    except Exception as e:
        logger.error("Failed to start prompt flow runtime: %s", e)
        raise


if __name__ == "__main__":
    main()
