from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
import os

class CustomBuildCommand(_build_py):
    """Ensure the maps are built"""

    def run(self):
        if not os.path.exists("src/interscript/maps"):
            print("Maps have not been built. Please issue ./build.sh before trying to build a package.")
            exit(1)

        # Call the superclass method to perform the standard build
        super().run()

setup(
    cmdclass={
        'build_py': CustomBuildCommand,
    },
)
